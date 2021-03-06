#!/usr/bin/env python3
import copy

import tcod

from engine import Engine
import entity_factories
from procgen import generate_dungeon


def main() -> None:
    screen_width = 100
    screen_height = 75

    map_width = 100
    map_height = 65

    room_max_size = 25
    room_min_size = 7
    max_rooms = 40

    max_enemies_per_room  = 3

    scifi_tileset = tcod.tileset.load_tilesheet(
        'Yayo_tunur_1040x325.png', 16, 16, tcod.tileset.CHARMAP_CP437
    )

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        max_enemies_per_room=max_enemies_per_room,
        engine=engine,
    )

    engine.update_fov()

    with tcod.context.new(
        columns=screen_width,
        rows=screen_height,
        tileset=scifi_tileset,
        title='Wisest Wizard',
        vsync=True,
    ) as context:

        root_console = tcod.Console(screen_width, screen_height, order='F')

        while True:
            engine.render(console=root_console, context=context)

            engine.event_handler.handle_events()


if __name__ == '__main__':
    main()