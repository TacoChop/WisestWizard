from __future__ import annotations

from typing import Iterable, Optional, TYPE_CHECKING

import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity


class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = ()):
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.horizontal_wall, order="F")

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

    def get_blocking_entity_at_location(self, location_x: int, location_y: int) -> Optional[Entity]:
        for entity in self.entities:
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity

        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        Renders the map.
        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )

        for entity in self.entities:
            # Only print entities that are in the FOV.
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    def adjacent_tile_types(self, x1: int, y1: int) -> np.ndarray:
        """
        Determines whether the tiles surrounding a specific tile are floor tiles or wall tiles. Returns a 3x3 array
        where the value at (1, 1) is the given tile and the other values represent the tiles surrounding it. A 0 in the
        array represents a floor tile and a 1 represents a wall tile.
        :param x1: x coordinate of given tile.
        :param y1: y coordinate of given tile.
        :return: 2d array containing the values for the given tile and the tiles touching it.
        """
        tile_values = np.ones((3, 3), dtype=int, order="C")

        for x2 in range(0, 3):
            for y2 in range(0, 3):
                x = x1 + x2 - 1
                y = y1 + y2 - 1

                if 0 <= x < len(self.tiles) and 0 <= y < len(self.tiles[0]):
                    if self.tiles[x, y] == tile_types.floor:
                        tile_values[y2, x2] = 0

        # TODO: Update for other types of tiles.
        return tile_values