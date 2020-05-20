import arcade
from arcade_ui import EventMap

from astar import Settings as s
from astar.views import LoadingView


def main() -> None:
    window = arcade.Window(*s.WINDOW_SIZE, 'A* Pathfinding Visualization')
    window.show_view(LoadingView(EventMap()))
    arcade.run()


if __name__ == "__main__":
    main()
