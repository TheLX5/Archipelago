import os
import settings
import threading
import pkgutil
import hashlib

from BaseClasses import MultiWorld, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld, LogicMixin
from rule_builder.rules import Rule

from .options import RHAOptions
from .client import RHAClient
from .regions import create_regions
from .rom import patch_rom, RHAProcedurePatch, HASH_JP
from .enums import Items, Locations, Regions
from .items import RHAItem, all_items, item_groups
from .locations import all_locations, count_locations_active, location_groups
from .constants import *

from typing import Any, ClassVar, TextIO, Optional, Sequence, Tuple

class RHASettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Rhythm Tengoku JP rom"""
        copy_to = "Rhythm Tengoku (Japan).gba"
        description = "Rhythm Tengoku (Japan) ROM File"
        md5s = [HASH_JP]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class RHAWeb(WebWorld):
    theme = "ice"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Mega Man X2 with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )
    tutorials = [setup_en]
    #option_groups = rha_option_groups

class RHAWorld(World):
    """
    beat.
    """
    game = GAME_NAME
    web = RHAWeb()

    settings: ClassVar[RHASettings]
    
    options_dataclass = RHAOptions
    options: RHAOptions

    required_client_version = (0, 6, 7)

    item_name_to_id = {str(name): data.code for name, data in all_items.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    #origin_region_name = Regions.intro_stage.value
    rule_macros: dict[str, Rule.Resolved]

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.rule_macros = {}
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)

    def create_items(self) -> None:
        itempool: list[RHAItem] = []

        self.total_required_locations = count_locations_active(self)

        # Submit stage bundles to item pool
        stage_bundles = sorted(item_groups["Stage Bundle"])
        self.selected_stage = self.random.choice(stage_bundles)
        precollected_items = [item.name for item in self.multiworld.precollected_items[self.player]]
        if set(stage_bundles).isdisjoint(precollected_items):
            self.push_precollected(self.create_item(self.selected_stage))
            stage_bundles.remove(self.selected_stage)
        for stage in stage_bundles:
            if stage in precollected_items:
                continue
            itempool.append(self.create_item(stage))

        itempool += [self.create_item(Items.medal) for _ in range(50)]

        # Setup junk items
        junk_count = self.total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([Items.nothing] * 2)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: Items, force_classification=False) -> RHAItem:
        name = str(name)
        data = all_items[name]
        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        created_item = RHAItem(name, classification, data.code, self.player)
        return created_item


    def set_rules(self):
        from .rules import RHARules
        RHARules(self).set_rules()

        # Debug
        return
        from Utils import visualize_regions
        state = CollectionState(self.multiworld, allow_partial_entrances=True)
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Menu"), "my_world.puml", show_entrance_names=True,
                        regions_to_highlight=state.reachable_regions[self.player])


    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "perfects",
            "superbs",
        )
        return slot_data


    def generate_early(self):
        patch_version = f"{self.world_version.major:02}{self.world_version.minor:02}{self.world_version.build:02}"
        self.auth =  bytearray(f'RHA-{patch_version}-{self.player}-{self.multiworld.seed:11}\0', 'utf8')[:21]
        self.auth.extend([0] * (21 - len(self.auth)))


    def get_filler_item_name(self) -> str:
        return str(Items.nothing)


    def generate_output(self, output_directory: str):
        try:
            patch = RHAProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("rha_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/rha_basepatch.bsdiff4"))
            patch_rom(self, patch)

            self.rom_name = patch.name

            patch.write(os.path.join(output_directory,
                                     f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"))
        except Exception:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected


    def modify_multidata(self, multidata: dict):
        import base64
        # Put the player's unique authentication in connect_names.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

