from typing import Tuple

from astar import Tile


def tile_to_pixels(x: int, y: int) -> Tuple[float, float]:
    return (
        x * Tile.SCALED + Tile.SCALED / 2,
        y * Tile.SCALED + Tile.SCALED / 2
    )


def pixels_to_tile(x: float, y: float) -> Tuple[int, int]:
    return (
        int((x - (x % Tile.SCALED)) / Tile.SCALED),
        int((y - (y % Tile.SCALED)) / Tile.SCALED)
    )


def find_grid_box(x: int, y: int) -> Tuple[float, float]:
    left_x = x - (x % Tile.SCALED)
    bottom_y = y - (y % Tile.SCALED)

    center_x = left_x + Tile.SCALED / 2
    center_y = bottom_y + Tile.SCALED / 2

    return center_x, center_y


def check_point_for_collision(
    point: Tuple[float, float],
    left: float,
    right: float,
    bottom: float,
    top: float
) -> bool:
    if left < point[0] < right and bottom < point[1] < top:
        return True
    return False
