from typing import Optional,List

from .types import FormattingItem, WorldState


class FuzzyItemSearch:
    """ A fuzzy search tool that offers various fuzzy searches based on a base buffer."""

    def __init__(self, buffer: str, items: list[List[FormattingItem]]):
        self.buffer = buffer
        self.items = items

    def matches(self, itemText: str):
        return self.buffer in itemText.lower()

    def searchForward(self, worldState: WorldState) -> Optional[WorldState]:
        categoryIndex = worldState.categoryIndex
        itemIndex = worldState.itemIndex
        if itemIndex < len(self.items[categoryIndex])-1:
            itemIndex += 1
        else:
            if categoryIndex  >= len(self.items)-1:
                return
            categoryIndex += 1
        while categoryIndex < len(self.items):
            if itemIndex == len(self.items[categoryIndex]):
                categoryIndex += 1
                itemIndex = 0
                continue
            item = self.items[categoryIndex][itemIndex]
            if self.matches(item.name):
                return WorldState(categoryIndex, itemIndex)
            itemIndex += 1

    def searchBackward(self, worldState: WorldState) -> Optional[WorldState]:
        categoryIndex = worldState.categoryIndex
        itemIndex = worldState.itemIndex
        if itemIndex > 0:
            itemIndex -= 1
        else:
            # Let the below algorithm reset categoryIndex.
            itemIndex = -1
        while categoryIndex >= 0:
            if itemIndex < 0:
                categoryIndex -= 1
                if categoryIndex < 0:
                    return
                itemIndex = len(self.items[categoryIndex])-1
                continue
            item = self.items[categoryIndex][itemIndex]
            if self.matches(item.name):
                return WorldState(categoryIndex, itemIndex)
            itemIndex -= 1

    def searchFirst(self):
        """ convenience method to search for the first item in the list."""
        return self.searchFromHere(WorldState(0,0))

    def searchLast(self):
        # We really do not need a search back from here, it's only used in this func.
        state = WorldState(len(self.items)-1, len(self.items[-1])-1)
        if self.state_matches(state):
            return state
        return self.searchBackward(state)

    def searchFromHere(self, state: WorldState):
        if self.state_matches(state):
            return state
        return self.searchForward(state)

    def state_matches(self, state: WorldState) -> bool:
        return self.matches(self.items[state.categoryIndex][state.itemIndex].name)
