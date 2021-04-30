from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod
import numpy as np

import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def place_entities(
        room: RectangularRoom, dungeon: GameMap, maximum_enemies: int,
) -> None:
    number_of_enemies = random.randint(0, maximum_enemies)

    for i in range(number_of_enemies):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities) and dungeon.tiles[x, y] == tile_types.floor:
            if random.random() < 0.5:
                entity_factories.custodial_bot.spawn(dungeon, x, y)
            else:
                entity_factories.security_bot.spawn(dungeon, x, y)

def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_enemies_per_room: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    dungeon = GameMap(map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        # Finally, append the new room to the list.
        rooms.append(new_room)

    # Create pillars based on room size and place entities.
    for room in rooms:
        x, y = room.center
        if room.width >= int(room_max_size * 0.5) and room.height >= int(room_max_size * 0.5):
            dungeon.tiles[x - int(room.width / 4), y - int(room.height / 4)] = tile_types.pillar
            dungeon.tiles[x + int(room.width / 4), y - int(room.height / 4)] = tile_types.pillar
            dungeon.tiles[x - int(room.width / 4), y + int(room.height / 4)] = tile_types.pillar
            dungeon.tiles[x + int(room.width / 4), y + int(room.height / 4)] = tile_types.pillar
        elif room.width >= int(room_max_size * 0.5) and room.height < int(room_max_size * 0.5):
            dungeon.tiles[x - int(room.width / 3) + 1, y] = tile_types.pillar
            dungeon.tiles[x + int(room.width / 3) - 1, y] = tile_types.pillar
        elif room.width < int(room_max_size * 0.5) and room.height >= int(room_max_size * 0.5):
            dungeon.tiles[x, y - int(room.height / 3) + 1] = tile_types.pillar
            dungeon.tiles[x, y + int(room.height / 3) - 1] = tile_types.pillar

        place_entities(room, dungeon, max_enemies_per_room)

    # Iterates through the array of dungeon tiles to find wall tiles and change them to the appropriate tile type.
    for (x, y), tile in np.ndenumerate(dungeon.tiles):
        if tile != tile_types.floor and tile != tile_types.pillar:
            try:
                if dungeon.tiles[x - 1, y] == tile_types.floor or dungeon.tiles[x + 1, y] == tile_types.floor:
                    if dungeon.tiles[x + 1, y] == tile_types.horizontal_wall and dungeon.tiles[x + 1, y - 1] == tile_types.floor and dungeon.tiles[x + 1, y + 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.horizontal_wall
                    else:
                        dungeon.tiles[x, y] = tile_types.vertical_wall
                if dungeon.tiles[x, y + 1] != tile_types.floor and dungeon.tiles[x + 1, y] != tile_types.floor:
                    if dungeon.tiles[x + 1, y + 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.right_down_wall
                    elif dungeon.tiles[x - 1, y] == tile_types.floor and dungeon.tiles[x, y - 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.right_down_wall
                if dungeon.tiles[x, y - 1] != tile_types.floor and dungeon.tiles[x + 1, y] != tile_types.floor:
                    if dungeon.tiles[x + 1, y - 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.right_up_wall
                    elif dungeon.tiles[x - 1, y] == tile_types.floor and dungeon.tiles[x, y + 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.right_up_wall
                if dungeon.tiles[x, y + 1] != tile_types.floor and dungeon.tiles[x - 1, y] != tile_types.floor:
                    if dungeon.tiles[x - 1, y + 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.left_down_wall
                    elif dungeon.tiles[x + 1, y] == tile_types.floor and dungeon.tiles[x, y - 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.left_down_wall
                if dungeon.tiles[x, y - 1] != tile_types.floor and dungeon.tiles[x - 1, y] != tile_types.floor:
                    if dungeon.tiles[x - 1, y - 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.left_up_wall
                    elif dungeon.tiles[x + 1, y] == tile_types.floor and dungeon.tiles[x, y + 1] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.left_up_wall
                if dungeon.tiles[x - 1, y - 1] == tile_types.floor and dungeon.tiles[x + 1, y - 1] == tile_types.floor and dungeon.tiles[x - 1, y + 1] == tile_types.floor and dungeon.tiles[x + 1, y + 1] == tile_types.floor:
                    if dungeon.tiles[x, y - 1] == tile_types.floor and dungeon.tiles[x + 1, y] == tile_types.floor and dungeon.tiles[x, y + 1] == tile_types.floor and dungeon.tiles[x - 1, y] == tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.pillar
                    elif dungeon.tiles[x, y - 1] != tile_types.floor and dungeon.tiles[x + 1, y] != tile_types.floor and dungeon.tiles[x, y + 1] != tile_types.floor and dungeon.tiles[x - 1, y] != tile_types.floor:
                        dungeon.tiles[x, y] = tile_types.cross
                if dungeon.tiles[x - 1, y] != tile_types.floor and dungeon.tiles[x, y - 1] == tile_types.floor and dungeon.tiles[x, y + 1] == tile_types.floor and dungeon.tiles[x + 1, y]:
                    dungeon.tiles[x, y] = tile_types.horizontal_wall
            except:
                continue
        # TODO: Make more efficient and work out edge cases. Find way to do T tiles. Possibly a function that assigns
            # each tile a value based on the tiles surrounding it. Value is then used to determine the tile type needed.

    return dungeon