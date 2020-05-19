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
