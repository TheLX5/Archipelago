import logging

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from typing import Dict

from worlds.mmx4.Rules import set_rules

from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import MMX4Options
from .Regions import create_regions
from .Client import MMX4Client

class MMX4Web(WebWorld):
    theme = "Ice"
    
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up (the game you are randomizing) for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "setup_en.md",
        "setup/en",
        ["KinTheInfinite"]
    )]

class MMX4World(World):
    """
    Mega Man X4 is a 1997 action-platform game developed and published by Capcom. 
    Mega Man X4 allows the player to choose between the two mechanoid "Reploids" protagonists at the beginning of the game
    X, who uses an arm cannon; or Zero, who wields an energy blade.
    Two Maverick Hunters, X and Zero, fight against a Reploid army called the "Repliforce" who are waging war against humanity to earn their independence.
    """

    game = "Mega Man X4"
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = MMX4Options
    options = MMX4Options
    web = MMX4Web()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

    #def generate_early(self):

    def create_regions(self):
        create_regions(self)

    def create_items(self):
        self.multiworld.itempool += create_itempool(self)
        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    # The slot data is what youre sending to the AP server kinda. You dont have to add all your options. Really you want the ones you think a pop tracker would use
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": get_total_locations(self) # get_total_locations(self) comes from Locations.py
        }

        return slot_data
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)