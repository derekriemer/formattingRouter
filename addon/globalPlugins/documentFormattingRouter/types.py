from collections import namedtuple
from dataclasses import dataclass


@dataclass(frozen=True)
class WorldState:
    categoryIndex: int
    itemIndex: int

FormattingItem = namedtuple('FormattingItem', ['name', 'configKey'])
