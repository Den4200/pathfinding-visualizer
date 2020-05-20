import arcade
from arcade_ui import InteractiveWidget

from astar import Settings as s, Tile
from astar.utils import find_grid_box


class Grid(InteractiveWidget):
    __widget_name__ = 'grid'

    def __init__(self) -> None:
        self.boxes = arcade.ShapeElementList()
        self.filled = arcade.ShapeElementList()

        self.hash_map = dict()

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

        self.active = True
        self.should_place = False
        self.should_break = False

    def draw(self) -> None:
        if len(self.filled) > 0:
            self.filled.draw()

        self.boxes.draw()

    def move(self, delta_x: float, delta_y: float) -> None:
        pass

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
            box = self.hash_map.get((center_x, center_y))

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
                    self.hash_map[(center_x, center_y)] = box

            elif self.should_break:
                if box is not None:
                    self.filled.remove(box)
                    self.hash_map.pop((center_x, center_y))
