import arcade
from arcade_ui import EventMap, View

from astar import Settings as s
from astar.grid import Grid


class AStarVisualizer(View):

    def __init__(self, event_map: EventMap) -> None:
        super().__init__(event_map)
        self.grid = None

        arcade.set_background_color(arcade.color.WHITE)

    def on_show(self) -> None:
        self.event_map.clear()
        self.grid = Grid()

        super().setup()

    def on_draw(self) -> None:
        arcade.start_render()
        self.grid.draw()


def main():
    window = arcade.Window(*s.WINDOW_SIZE, 'A* Pathfinding Visualizer')
    window.show_view(AStarVisualizer(EventMap()))
    arcade.run()


if __name__ == "__main__":
    main()
