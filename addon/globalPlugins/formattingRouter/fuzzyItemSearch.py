from .worldState import WorldState
from typing import Optional

from addon.globalPlugins.formattingRouter import worldState


class WorldOutOfBoundsError(Exception):
    def __init__(self, state: WorldState):
        super().__init__()
        match state:
            case WorldState(categoryindex, ItemIndex) if categoryindex < 0 or ItemIndex < 0:
                self.message = F"negative sized world: {state} not allowed"
            case WorldState(itemIndex, categoryindex) if categoryindex > len(items):
                self.message = F"World with category index {state.categoryIndex} too large. Max size: {len(items)}"
            case _:
                self.message = F"world of item size : {state.itemIndex} too large. max size: {len(items[state.categoryIndex])}"

class FuzzyItemSearch:
    """ A fuzzy search tool that offers various fuzzy searches based on a base buffer."""

    def __init__(self, buffer, items):
        self.buffer = buffer
        self.items = items

    def _validateWorldState(self,   state:WorldState):
        if state.categoryIndex > len(self.items)or state.itemIndex > self.items[state.categoryIndex] or state.categoryIndex < 0 or state.itemIndex < 0:
            raise WorldOutOfBoundsError(state, self.items)
        
    def searchForward(self, worldState: WorldState) -> Optional[WorldState]:
        self._validateWorldState(worldState)
        categoryIndex = worldState.categoryIndex
        itemIndex = worldState.itemIndex
        while categoryIndex < len(self.items):
            if itemIndex == len(self.items[categoryIndex]):
                categoryIndex += 1
                itemIndex = 0
                continue
            item = self.items[categoryIndex][itemIndex]
            if buffer in item.name:
                return WorldState(categoryIndex, itemIndex)
            itemIndex += 1

    def searchBackwardf(self, worldState: WorldState) -> Optional[WorldState]:
        self._validateWorldState(worldState)
        categoryIndex = worldState.categoryIndex
        itemIndex = worldState.itemIndex
        while categoryIndex >= 0:
            if itemIndex < 0:
                categoryIndex -= 1
                if categoryIndex < 0:
                    return
                itemIndex = len(self.items[categoryIndex])
                continue
            item = self.items[categoryIndex][itemIndex]
            if buffer in item.name:
                return WorldState(categoryIndex, itemIndex)
            itemIndex -= 1

    def state_matches(self, state: WorldState) -> bool:
        self._validateWorldState(self, state)
        return self.buffer in self.items[state.categoryIndex][state.itemIndex].name
