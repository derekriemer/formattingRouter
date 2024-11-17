from dataclasses import dataclass


@dataclass(frozen=True)
class WorldState:
	categoryIndex:int
	itemIndex: int
