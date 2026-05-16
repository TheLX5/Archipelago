import logging
import settings
import threading
import base64
import os

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld
from worlds.LauncherComponents import Component, Type, components, launch
from typing import Dict, Any

from worlds.mmx4.Rules import set_rules

from .Locations import get_location_names, get_total_locations
from .Items import create_item, create_itempool, item_table
from .Options import MMX4Options
from .Regions import create_regions
from .Client import MMX4Client
from .Rom import HASH_US, MMX4ProcedurePatch, patch_rom

class MMX4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Mega Man X4 US ROM"""
        description = "Mega Man X4 US ROM File"
        copy_to = "Mega Man X4 (USA).bin"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class MMX4Web(WebWorld):
    theme = "grass"
    game_info_languages = []
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up MMX4 for Archipelago. ",
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
    options: MMX4Options
    web = MMX4Web()

    def __init__(self, multiworld: "MultiWorld", player: int):
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def generate_early(self):
        if getattr(self.options.character, "value", self.options.character) == self.options.character.option_zero:
            self.options.local_items.value.add("Soul Body")

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
            "TotalLocations": get_total_locations(self), # get_total_locations(self) comes from Locations.py
            "death_link": bool(self.options.death_link.value),
            "damage_link": bool(self.options.damage_link.value),
            "energy_link": bool(self.options.energy_link.value),
            "energy_link_auto_heal": bool(self.options.energy_link_auto_heal.value),
            "energy_link_cost_per_hp": int(self.options.energy_link_cost_per_hp.value),
        }

        return slot_data
    

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)

    def generate_output(self, output_directory: str):
        try:
            rom_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                        f"{MMX4ProcedurePatch.patch_file_ending}")
            patch = MMX4ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch_rom(self, patch)
            self.rom_name = patch.name
            patch.write(rom_path)
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
