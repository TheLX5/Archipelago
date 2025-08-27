import logging
import settings
import base64
import os
import threading
from typing import Dict, ClassVar

from BaseClasses import MultiWorld, Item, Tutorial
from worlds.AutoWorld import World, CollectionState, WebWorld

from .Locations import all_locations, setup_locations
from .Items import create_item, create_itempool, item_table
from .Options import MMX4Options, mmx4_option_groups
from .Regions import create_regions, connect_regions
from .Client import MMX4Client
from .Rules import MMX4XRules
from .Rom import HASH_US, MMX4ProcedurePatch, patch_rom
from .Names import ItemName

class MMX4Settings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Mega Man X4 US v1.0 ROM"""
        description = "Mega Man X4 US v1.0 ROM File"
        copy_to = "Mega Man X4 (USA).bin"
        md5s = [HASH_US]

    rom_file: RomFile = RomFile(RomFile.copy_to)

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

    option_groups = mmx4_option_groups

class MMX4World(World):
    """
    Mega Man X4 is a 1997 action-platform game developed and published by Capcom. 
    Mega Man X4 allows the player to choose between the two mechanoid "Reploids" protagonists at the beginning of the game
    X, who uses an arm cannon; or Zero, who wields an energy blade.
    Two Maverick Hunters, X and Zero, fight against a Reploid army called the "Repliforce" who are waging war against humanity to earn their independence.
    """

    game = "Mega Man X4"
    web = MMX4Web()

    settings: ClassVar[MMX4Settings]
    options_dataclass = MMX4Options
    options = MMX4Options

    required_client_version = (0, 6, 2)
    item_name_to_id = {name: data.ap_code for name, data in item_table.items()}
    location_name_to_id = {name: loc_data.ap_code for name, loc_data in all_locations.items()}

    def __init__(self, multiworld: "MultiWorld", player: int):
        self.rom_name = None
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    #def generate_early(self):

    def create_regions(self):
        self.location_table = setup_locations(self)
        create_regions(self)
        connect_regions(self)
        
    def create_items(self):
        self.multiworld.itempool += create_itempool(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)
    
    def set_rules(self):
        MMX4XRules(self).set_mmx4_rules()
    
    # The slot data is what youre sending to the AP server kinda. You dont have to add all your options. Really you want the ones you think a pop tracker would use
    # Seed, Slot, and TotalLocations are all super important for AP though, you need those
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {
            "Seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "Slot": self.multiworld.player_name[self.player],  # to connect to server
            "TotalLocations": len(self.location_table.keys()) # get_total_locations(self) comes from Locations.py
        }

        return slot_data
    
    def collect(self, state: "CollectionState", item: "Item") -> bool:
        return super().collect(state, item)
    
    def remove(self, state: "CollectionState", item: "Item") -> bool:
        return super().remove(state, item)

    def get_filler_item_name(self) -> str:
        return ItemName.small_hp

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
