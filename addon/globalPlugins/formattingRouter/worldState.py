from dataclasses import dataclass


@dataclass(frozen=True)
class WorldState:
	category:int
	item: int
