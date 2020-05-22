from __future__ import annotations

import math
from typing import Any, Dict, Optional, Tuple, Iterator, Union

from astar import Settings as s, Tile
from astar.utils import check_point_for_collision, tile_to_pixels


class Node:
    __slots__ = ('parent', 'pos', 'f', 'g', 'h')

    def __init__(
        self,
        pos: Tuple[float, float],
        parent: Optional[Node] = None
    ) -> None:

        self.parent = parent
        self.pos = pos

        self.f = 0
        self.g = 0
        self.h = 0

    def __hash__(self) -> int:
        return hash(self.pos)

    def __eq__(self, other: Node) -> bool:
        return self.pos == other.pos

    def __add__(self, other: Node) -> Node:
        return Node(
            (
                self.pos[0] + other.pos[0],
                self.pos[1] + other.pos[1]
            ),
            self
        )

    def __sub__(self, other: Node) -> Node:
        return Node(
            (
                self.pos[0] - other.pos[0],
                self.pos[1] - other.pos[1]
            ),
            self
        )


class PathFinder:

    def __init__(self, max_tries: int = 5000) -> None:
        self.max_tries = max_tries

    def find(
        self,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        collision_list_hash_map: Dict[Tuple[float, float], Any],
        map_list_hash_map: Dict[Tuple[float, float], Any]
    ) -> Iterator[Union[Tuple[int, int], int]]:

        if self._tile_is_blocked(*end_pos, collision_list_hash_map):
            return

        if not self._tile_is_blocked(*end_pos, map_list_hash_map):
            return

        open_nodes = set()
        closed_nodes = set()

        start_node = Node(start_pos)
        end_node = Node(end_pos)

        open_nodes.add(start_node)

        surroundings = (
            Node((0, -1)),
            Node((1, 0)),
            Node((0, 1)),
            Node((-1, 0))
        )

        for _ in range(self.max_tries):
            if not open_nodes:
                return

            current_node = min(open_nodes, key=lambda node: node.f)

            open_nodes.remove(current_node)
            closed_nodes.add(current_node)

            if current_node == end_node:
                yield 0

                path = []
                current = current_node
                while current is not None:
                    path.append(current.pos)
                    current = current.parent

                yield from reversed(path)
                return

            children = (
                current_node + pos_node for pos_node in surroundings
                if not self._tile_is_blocked(*(current_node + pos_node).pos, collision_list_hash_map)
            )

            for child in children:

                if child in closed_nodes:
                    continue

                # http://theory.stanford.edu/~amitp/GameProgramming/AStarComparison.html#the-a-star-algorithm
                child.g = current_node.g + 1

                n = child - end_node
                child.h = math.sqrt(n.pos[0] ** 2 + n.pos[1] ** 2)

                child.f = child.g + child.h

                if child in open_nodes:
                    if any(child.g > open_node.g for open_node in open_nodes):
                        continue

                open_nodes.add(child)
                yield child

    @staticmethod
    def _tile_is_blocked(x: int, y: int, element_list_hash_map: Dict[Tuple[float, float], Any]) -> bool:
        cx, cy = tile_to_pixels(x, y)

        if cx < 0 or cx > s.WINDOW_SIZE[0] or cy < 0 or cy > s.WINDOW_SIZE[1]:
            return True

        half_tile = Tile.SCALED / 2

        for elem in element_list_hash_map:
            if check_point_for_collision(
                (cx, cy),
                elem[0] - half_tile,
                elem[0] + half_tile,
                elem[1] - half_tile,
                elem[1] + half_tile
            ):
                return True

        return False
