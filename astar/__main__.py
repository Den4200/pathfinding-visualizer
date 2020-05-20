import arcade
from arcade_ui import EventMap, View

from astar import Settings as s
from astar.grid import Grid


class AStarVisualizer(View):

    def __init__(self, event_map: EventMap) -> None:
        super().__init__(event_map)
        self.grid = None
        self.grid_setup = None

        arcade.set_background_color(arcade.color.WHITE)

    def on_show(self) -> None:
        self.event_map.clear()
        self.grid = Grid()
        self.grid_setup = self.grid.setup()

        super().setup()

    def on_draw(self) -> None:
        arcade.start_render()
        self.grid.draw()

    def on_update(self, delta_time: float) -> None:
        if self.grid_setup is not None:
            try:
                next(self.grid_setup)
            except StopIteration:
                self.grid_setup = None

        super().on_update(delta_time)


def main() -> None:
    window = arcade.Window(*s.WINDOW_SIZE, 'A* Pathfinding Visualizer')
    window.show_view(AStarVisualizer(EventMap()))
    arcade.run()


if __name__ == "__main__":
    main()
