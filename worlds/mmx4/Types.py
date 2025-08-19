from typing import NamedTuple, Optional
from BaseClasses import Location, Item, ItemClassification

class MMX4Location(Location):
    game = "Mega Man X4"

class MMX4Item(Item):
    game = "Mega Man X4"

class ItemData(NamedTuple):
    ap_code: Optional[int]
    classification: ItemClassification
    count: Optional[int] = 1

class LocData(NamedTuple):
    ap_code: Optional[int]
    region: Optional[str]
