from __future__ import annotations

import random
from typing import Iterator, List, Tuple, TYPE_CHECKING

import tcod
import numpy as np

import entity_factories
from game_map import GameMap
import tile_types


if TYPE_CHECKING:
    from engine import Engine


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
            if random.random() < 0.8:
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

def tile_picker(dungeon: GameMap, x: int, y: int) -> np.ndarray:
    """
    Uses the array returned by GameMap.adjacent_tile_types to determine the proper wall tile to represent a given tile.
    :param dungeon: An instance of GameMap.
    :param x: x coordinate for given tile.
    :param y: y coordinate for given tile.
    :return: Tile from tile_types to represent given tile.
    """
    adjacent_tiles = dungeon.adjacent_tile_types(x, y)
    wall_tiles = np.flatnonzero(adjacent_tiles)

    if len(wall_tiles) == 1:
        return tile_types.pillar
    elif len(wall_tiles) == 2:
        if 1 in wall_tiles or 7 in wall_tiles:
            return tile_types.vertical_wall
        else:
            return tile_types.horizontal_wall
    elif len(wall_tiles) == 3:
        if 1 in wall_tiles:
            if 3 in wall_tiles:
                return tile_types.left_up_wall
            elif 5 in wall_tiles:
                return tile_types.right_up_wall
            else:
                return tile_types.vertical_wall
        elif 7 in wall_tiles:
            if 3 in wall_tiles:
                return tile_types.left_down_wall
            elif 5 in wall_tiles:
                return tile_types.right_down_wall
            else:
                return tile_types.horizontal_wall
    elif len(wall_tiles) == 4 or len(wall_tiles) == 5:
        if 1 in wall_tiles:
            if 3 in wall_tiles and 5 in wall_tiles and 7 in wall_tiles:
                return tile_types.cross
            elif 3 in wall_tiles and 5 in wall_tiles:
                return tile_types.t_up_wall
            elif 3 in wall_tiles and 7 in wall_tiles:
                return tile_types.t_left_wall
            elif 5 in wall_tiles and 7 in wall_tiles:
                return tile_types.t_right_wall
            elif 3 in wall_tiles:
                return tile_types.left_up_wall
            elif 5 in wall_tiles:
                return  tile_types.right_up_wall
            else:
                return tile_types.vertical_wall
        elif 7 in wall_tiles:
            if 3 in wall_tiles and 5 in wall_tiles:
                return tile_types.t_down_wall
            elif 3 in wall_tiles:
                return tile_types.left_down_wall
            elif 5 in wall_tiles:
                return  tile_types.right_down_wall
            else:
                return tile_types.vertical_wall
        else:
            return  tile_types.horizontal_wall
    elif len(wall_tiles) == 6:
        if 1 in wall_tiles and 7 in wall_tiles:
            if 3 in wall_tiles and 5 in wall_tiles:
                return tile_types.cross
            elif 3 in wall_tiles and 0 in wall_tiles and 6 in wall_tiles:
                return tile_types.vertical_wall
            elif 3 in wall_tiles and 2 in wall_tiles and 8 in wall_tiles:
                return tile_types.t_left_wall
            elif 3 in wall_tiles and 6 in wall_tiles and 0 not in wall_tiles:
                return tile_types.left_up_wall
            elif 3 in wall_tiles and 0 in wall_tiles and 6 not in wall_tiles:
                return tile_types.left_down_wall
            elif 5 in wall_tiles and 2 in wall_tiles and 8 in wall_tiles:
                return tile_types.vertical_wall
            elif 5 in wall_tiles and 0 in wall_tiles and 6 in wall_tiles:
                return tile_types.t_right_wall
            elif 5 in wall_tiles and 8 in wall_tiles and 2 not in wall_tiles:
                return tile_types.right_up_wall
            elif 5 in wall_tiles and 2 in wall_tiles and 8 not in wall_tiles:
                return tile_types.right_down_wall
            else:
                return tile_types.horizontal_wall
        elif 1 in wall_tiles and 3 in wall_tiles and 5 in wall_tiles:
            if 6 in wall_tiles and 8 in wall_tiles:
                return tile_types.t_up_wall
            elif 2 in wall_tiles and 0 not in wall_tiles:
                return tile_types.left_up_wall
            elif 0 in wall_tiles and 2 not in wall_tiles:
                return tile_types.right_up_wall
            else:
                return tile_types.horizontal_wall
        elif 7 in wall_tiles and 3 in wall_tiles and 5 in wall_tiles:
            if 0 in wall_tiles and 2 in wall_tiles:
                return tile_types.t_down_wall
            elif 2 in wall_tiles and 8 in wall_tiles or 0 in wall_tiles and 6 in wall_tiles:
                return tile_types.t_down_wall
            elif 8 in wall_tiles and 6 not in wall_tiles:
                return tile_types.left_down_wall
            elif 6 in wall_tiles and 8 not in wall_tiles:
                return tile_types.right_down_wall
            else:
                return tile_types.horizontal_wall
        elif 0 not in wall_tiles and 1 not in wall_tiles and 3 not in wall_tiles:
            return tile_types.right_down_wall
        elif 1 not in wall_tiles and 2 not in wall_tiles and 5 not in wall_tiles:
            return tile_types.left_down_wall
        elif 5 not in wall_tiles and 7 not in wall_tiles and 8 not in wall_tiles:
            return tile_types.left_up_wall
        elif 3 not in wall_tiles and 6 not in wall_tiles and 7 not in wall_tiles:
            return tile_types.right_up_wall
        else:
            return tile_types.horizontal_wall
    elif len(wall_tiles) == 7:
        if 1 in wall_tiles and 3 in wall_tiles and 5 in wall_tiles and 7 in wall_tiles:
            if 0 in wall_tiles and 8 in wall_tiles:
                return tile_types.cross
            elif 2 in wall_tiles and 6 in wall_tiles:
                return tile_types.cross
            elif 0 in wall_tiles and 2 in wall_tiles:
                return tile_types.t_down_wall
            elif 2 in wall_tiles and 8 in wall_tiles:
                return tile_types.t_left_wall
            elif 6 in wall_tiles and 8 in wall_tiles:
                return tile_types.t_up_wall
            elif 0 in wall_tiles and 6 in wall_tiles:
                return tile_types.t_right_wall
            else:
                return tile_types.horizontal_wall
        elif 1 in wall_tiles and 3 in wall_tiles and 5 in wall_tiles:
            if 0 not in wall_tiles:
                return tile_types.left_up_wall
            elif 2 not in wall_tiles:
                return tile_types.right_up_wall
            else:
                return tile_types.horizontal_wall
        elif 3 in wall_tiles and 5 in wall_tiles and 7 in wall_tiles:
            if 6 not in wall_tiles:
                return tile_types.left_down_wall
            elif 8 not in wall_tiles:
                return tile_types.right_down_wall
            else:
                return  tile_types.horizontal_wall
        elif 1 in wall_tiles and 3 in wall_tiles and 7 in wall_tiles:
            if 0 not in wall_tiles:
                return tile_types.left_up_wall
            elif 6 not in wall_tiles:
                return tile_types.left_down_wall
            else:
                return tile_types.vertical_wall
        elif 1 in wall_tiles and 5 in wall_tiles and 7 in wall_tiles:
            if 2 not in wall_tiles:
                return tile_types.right_up_wall
            elif 8 not in wall_tiles:
                return tile_types.right_down_wall
            else:
                return tile_types.vertical_wall
        else:
            return tile_types.horizontal_wall
    elif len(wall_tiles) == 8:
        if 3 not in wall_tiles or 5 not in wall_tiles:
            return tile_types.vertical_wall
        elif 0 not in wall_tiles:
            return tile_types.left_up_wall
        elif 2 not in wall_tiles:
            return tile_types.right_up_wall
        elif 6 not in wall_tiles:
            return tile_types.left_down_wall
        elif 8 not in wall_tiles:
            return tile_types.right_down_wall
        else:
            return tile_types.horizontal_wall
    else:
        return tile_types.horizontal_wall

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_enemies_per_room: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

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
            player.place(*new_room.center, dungeon)
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
            if random.random() > 0.5:
                dungeon.tiles[x, y - int(room.height / 3) + 1] = tile_types.pillar
                dungeon.tiles[x, y + int(room.height / 3) - 1] = tile_types.pillar

        place_entities(room, dungeon, max_enemies_per_room)

    # Iterates through the array of dungeon tiles to find wall tiles and change them to the appropriate tile type.
    for (x, y), tile in np.ndenumerate(dungeon.tiles):
        if tile != tile_types.floor and tile != tile_types.pillar:
            try:
                tile_value = tile_picker(dungeon, x, y)
                dungeon.tiles[x, y] = tile_value
            except:
                continue

    # Insert doors where single tile tunnels pass through the walls of rooms.
    for room in rooms:
        for x in range(1, room.width):
            if (
                dungeon.tiles[room.x1 + x, room.y1] == tile_types.floor and
                dungeon.tiles[room.x1 + x + 1, room.y1] != tile_types.floor and
                dungeon.tiles[room.x1 + x - 1, room.y1] != tile_types.floor
            ):
                dungeon.tiles[room.x1 + x, room.y1] = tile_types.door
            if (
                dungeon.tiles[room.x1 + x, room.y2] == tile_types.floor and
                dungeon.tiles[room.x1 + x + 1, room.y2] != tile_types.floor and
                dungeon.tiles[room.x1 + x - 1, room.y2] != tile_types.floor
            ):
                dungeon.tiles[room.x1 + x, room.y2] = tile_types.door
        for y in range(1, room.height):
            if (
                dungeon.tiles[room.x1, room.y1 + y] == tile_types.floor and
                dungeon.tiles[room.x1, room.y1 + y + 1] != tile_types.floor and
                dungeon.tiles[room.x1, room.y1 + y - 1] != tile_types.floor
            ):
                dungeon.tiles[room.x1, room.y1 + y] = tile_types.door
            if (
                dungeon.tiles[room.x2, room.y1 + y] == tile_types.floor and
                dungeon.tiles[room.x2, room.y1 + y + 1] != tile_types.floor and
                dungeon.tiles[room.x2, room.y1 + y - 1] != tile_types.floor
            ):
                dungeon.tiles[room.x2, room.y1 + y] = tile_types.door

    return dungeon