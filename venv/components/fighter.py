from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    entity: Actor

    def __init__(
        self, structure: int, temperature: int, coruption: int, defense: int, power: int
    ):
        self.max_struct = structure
        self._struct = structure
        self.max_temp = temperature
        self._temp = temperature
        self.max_coruption = coruption
        self._coruption = coruption
        self.defense = defense
        self.power = power

    @property
    def struct(self) -> int:
        return self._struct

    @struct.setter
    def struct(self, value: int) -> None:
        self._struct = max(0, min(value, self.max_struct))
        if self._struct == 0 and self.entity.ai:
            self.die()

    @property
    def temp(self) -> int:
        return self._temp

    @temp.setter
    def temp(self, value: int) -> None:
        self._temp = max(0, min(value, self.max_temp))

    @property
    def coruption(self) -> int:
        return self._coruption

    @coruption.setter
    def coruption(self, value: int) -> None:
        self._coruption = max(0, min(value, self.max_coruption))

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
        else:
            death_message = f"{self.entity.name} is dead!"

        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"Remains of {self.entity.name}"

        print(death_message)