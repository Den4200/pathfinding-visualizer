import arcade
from arcade_ui import InteractiveWidget

from astar import Settings as s, Tile
from astar.utils import find_grid_box


class Grid(InteractiveWidget):
    __widget_name__ = 'grid'

    def __init__(self) -> None:
        self.boxes = arcade.ShapeElementList()
        self.filled = arcade.ShapeElementList()

        for y in range(0, s.WINDOW_SIZE[1], Tile.SCALED):
            for x in range(0, s.WINDOW_SIZE[0], Tile.SCALED):
                center_x, center_y = find_grid_box(x, y)

                self.boxes.append(
                    arcade.create_rectangle_outline(
                        center_x=center_x,
                        center_y=center_y,
                        width=Tile.SCALED,
                        height=Tile.SCALED,
                        color=arcade.color.BLACK
                    )
                )

        self.is_pressed = False

    def draw(self) -> None:
        self.filled.draw()
        self.boxes.draw()

    def move(self, delta_x: float, delta_y: float) -> None:
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        self.is_pressed = not self.is_pressed

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        if self.is_pressed:
            center_x, center_y = find_grid_box(x, y)
            self.filled.append(
                arcade.create_rectangle_filled(
                    center_x=center_x,
                    center_y=center_y,
                    width=Tile.SCALED,
                    height=Tile.SCALED,
                    color=arcade.color.RED
                )
            )
