import arcade
from arcade_ui import InteractiveWidget

from astar import Settings as s, Tile
from astar.utils import find_grid_box, tile_to_pixels

from astar.pathfinding import Node, PathFinder


class Grid(InteractiveWidget):
    __widget_name__ = 'grid'

    def __init__(self) -> None:
        self.boxes = arcade.ShapeElementList()
        self.boxes_hash_map = dict()

        self.filled = arcade.ShapeElementList()
        self.filled_hash_map = dict()

        self.active = True
        self.should_place = False
        self.should_break = False

        self.pathfinder = PathFinder()
        self.find = None
        self.found = False

    def setup(self) -> None:
        for y in range(0, s.WINDOW_SIZE[1], Tile.SCALED):
            for x in range(0, s.WINDOW_SIZE[0], Tile.SCALED):
                center_x, center_y = find_grid_box(x, y)

                box = arcade.create_rectangle_outline(
                    center_x=center_x,
                    center_y=center_y,
                    width=Tile.SCALED,
                    height=Tile.SCALED,
                    color=arcade.color.BLACK
                )
                self.boxes.append(box)
                self.boxes_hash_map[(center_x, center_y)] = box

                yield

    def draw(self) -> None:
        if len(self.filled) > 0:
            self.filled.draw()

        self.boxes.draw()

        arcade.draw_rectangle_filled(
            *tile_to_pixels(3, 3),
            width=Tile.SCALED,
            height=Tile.SCALED,
            color=arcade.color.BLACK
        )

        arcade.draw_rectangle_filled(
            *tile_to_pixels(36, 19),
            width=Tile.SCALED,
            height=Tile.SCALED,
            color=arcade.color.BLACK
        )

    def move(self, delta_x: float, delta_y: float) -> None:
        raise NotImplementedError

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        if self.active:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.should_place = not self.should_place
                self.should_break = False

            elif button == arcade.MOUSE_BUTTON_RIGHT:
                self.should_break = not self.should_break
                self.should_place = False

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        if self.active:
            center_x, center_y = find_grid_box(x, y)
            box = self.filled_hash_map.get((center_x, center_y))

            if self.should_place:
                if box is None:
                    box = arcade.create_rectangle_filled(
                        center_x=center_x,
                        center_y=center_y,
                        width=Tile.SCALED,
                        height=Tile.SCALED,
                        color=arcade.color.RED
                    )

                    self.filled.append(box)
                    self.filled_hash_map[(center_x, center_y)] = box

            elif self.should_break:
                if box is not None:
                    self.filled.remove(box)
                    self.filled_hash_map.pop((center_x, center_y))

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ENTER and self.find is None:
            self.active = False
            self.find = self.pathfinder.find(
                (3, 3),
                (36, 19),
                self.filled_hash_map,
                self.boxes_hash_map
            )

        if key == arcade.key.ESCAPE and self.find is None:
            self.filled = arcade.ShapeElementList()
            self.filled_hash_map.clear()
            self.active = True

    def on_update(self, delta_time: float) -> None:
        if self.find is not None:

            try:
                n = next(self.find)

                if isinstance(n, Node):
                    pos = n.pos

                elif n == 0:
                    self.found = True
                    return

                elif self.found:
                    pos = n

            except StopIteration:
                self.find = None
                self.found = False

            else:
                color = arcade.color.YELLOW if not self.found \
                    else arcade.color.GREEN

                center_x, center_y = tile_to_pixels(*pos)

                self.filled.append(
                    arcade.create_rectangle_filled(
                        center_x=center_x,
                        center_y=center_y,
                        width=Tile.SCALED,
                        height=Tile.SCALED,
                        color=color
                    )
                )
