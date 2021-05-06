from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  # Unicode codepoint.
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt),  # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True,
    transparent=True,
    dark=(ord("."), (0, 48, 64), (0, 0, 0)),
    light=(ord("."), (0, 191, 255), (26, 26, 26)),
)
vertical_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2551, (0, 48, 64), (0, 0, 0)),
    light=(0x2551, (0, 191, 255), (26, 26, 26)),
)
horizontal_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2550, (0, 48, 64), (0, 0, 0)),
    light=(0x2550, (0, 191, 255), (26, 26, 26)),
)
right_down_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2554, (0, 48, 64), (0, 0, 0)),
    light=(0x2554, (0, 191, 255), (26, 26, 26)),
)
right_up_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x255A, (0, 48, 64), (0, 0, 0)),
    light=(0x255A, (0, 191, 255), (26, 26, 26)),
)
left_up_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x255D, (0, 48, 64), (0, 0, 0)),
    light=(0x255D, (0, 191, 255), (26, 26, 26)),
)
left_down_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2557, (0, 48, 64), (0, 0, 0)),
    light=(0x2557, (0, 191, 255), (26, 26, 26)),
)
t_down_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2566, (0, 48, 64), (0, 0, 0)),
    light=(0x2566, (0, 191, 255), (26, 26, 26)),
)
t_up_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2569, (0, 48, 64), (0, 0, 0)),
    light=(0x2569, (0, 191, 255), (26, 26, 26)),
)
t_left_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2563, (0, 48, 64), (0, 0, 0)),
    light=(0x2563, (0, 191, 255), (26, 26, 26)),
)
t_right_wall = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2560, (0, 48, 64), (0, 0, 0)),
    light=(0x2560, (0, 191, 255), (26, 26, 26)),
)
pillar = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x2588, (0, 48, 64), (0, 0, 0)),
    light=(0x2588, (0, 191, 255), (26, 26, 26)),
)
cross = new_tile(
    walkable=False,
    transparent=False,
    dark=(0x256C, (0, 48, 64), (0, 0, 0)),
    light=(0x256C, (0, 191, 255), (26, 26, 26)),
)
door = new_tile(
    walkable=True,
    transparent=False,
    dark=(0x2229, (0, 48, 64), (0, 0, 0)),
    light=(0x2229, (128, 128, 128), (26, 26, 26)),
)
