from dataclasses import dataclass, field
from typing import List

from crafting_system import constants
from crafting_system.service.exceptions import ItemValidationError


@dataclass
class Item:
    item_type: str = constants.ItemTypes.UNKNOWN
    value: int = 0
    materials: float = 1.0
    dustwork_type: str = constants.DustTypes.UNKNOWN
    tags: list[str] = field(default_factory=list)
    sequence: list[str] | List = field(default_factory=list)

    def __post_init__(self):
        if self.materials < 0:
            raise ItemValidationError("Materials cannot be negative", self)

    @property
    def value_per_materials(self) -> float:
        return self.value / self.materials if self.materials else 0

    def short_sequence(self) -> str:
        short_seq = "no sequence"
        if self.sequence:
            short_seq = ""
            for i in range(len(self.sequence)):
                part = ""
                if isinstance(self.sequence[i], list):
                    part = f"{self.sequence[i][-1]} + "
                else:
                    part = f"{self.sequence[i]} <-|"
                short_seq = part + short_seq
            while not short_seq[-1].isalnum():
                short_seq = short_seq[:-1]
        return short_seq

    def __str__(self):
        shorter_seq = "no sequence"
        if self.sequence:
            shorter_seq = self.sequence[-1]
        return (
            f"{self.item_type:16} | Val: {self.value:8} | Mats: {self.materials:4.1f} | "
            f"VPM: {self.value_per_materials:11.2f} | {shorter_seq}"
        )

    def table_full(self) -> str:
        return (
            f"{self.item_type:16} | Val: {self.value:8} | Mats: {self.materials:4.1f} | "
            f"VPM: {self.value_per_materials:11.2f} | {self.short_sequence()}"
        )
