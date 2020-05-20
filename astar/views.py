import arcade
from arcade_ui import EventMap, TextBox, View

from astar import Settings as s
from astar.grid import Grid


class AStarVisualization(View):

    def __init__(self, event_map: EventMap, grid: Grid) -> None:
        super().__init__(event_map)
        self.grid = grid

        arcade.set_background_color(arcade.color.WHITE)

    def on_show(self) -> None:
        self.event_map.clear()
        self.event_map.add(self.grid)
        super().setup()

    def on_draw(self) -> None:
        arcade.start_render()
        self.grid.draw()


class LoadingView(View):

    def __init__(self, event_map: EventMap) -> None:
        super().__init__(event_map)

        self.title = None
        self.loading_text = None

        self.grid = None
        self.grid_setup = None

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def on_show(self) -> None:
        self.event_map.clear()

        self.title = TextBox(
            text='A* Pathfinding Visualization',
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 + 50,
            width=400,
            height=60,
            font_size=24,
            border_width=3
        )

        self.loading_text = TextBox(
            text='Building grid..',
            center_x=s.WINDOW_SIZE[0] / 2,
            center_y=s.WINDOW_SIZE[1] / 2 - 50,
            width=160,
            height=50,
            font_size=16,
            border_width=3
        )

        self.grid = Grid()
        self.grid.active = False
        self.grid_setup = self.grid.setup()

        super().setup()

    def on_draw(self) -> None:
        arcade.start_render()
        self.title.draw()
        self.loading_text.draw()

    def on_update(self, delta_time: float) -> None:
        if self.grid_setup is not None:
            try:
                next(self.grid_setup)
            except StopIteration:
                self.grid_setup = None
                self.grid.active = True
                self.window.show_view(
                    AStarVisualization(self.event_map, self.grid)
                )

        super().on_update(delta_time)
