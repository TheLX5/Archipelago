import os
import settings
import threading
import pkgutil
import math

from BaseClasses import MultiWorld, Tutorial
from worlds.AutoWorld import World, WebWorld
from rule_builder.rules import Rule

from .options import TengokuOptions, LevelUnlock
from .client import TengokuClient
from .regions import create_regions
from .rom import patch_rom, TengokuProcedurePatch, HASH_JP
from .enums import Items
from .items import TengokuItem, all_items, item_groups
from .locations import all_locations, count_locations_active, location_groups
from .constants import *
from .stage_data import level_data

from typing import ClassVar, TextIO

class TengokuSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Rhythm Tengoku JP rom"""
        copy_to = "Rhythm Tengoku (Japan).gba"
        description = "Rhythm Tengoku (Japan) ROM File"
        md5s = [HASH_JP]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class TengokuWeb(WebWorld):
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

class TengokuWorld(World):
    """
    beat.
    """
    game = GAME_NAME
    web = TengokuWeb()

    settings: ClassVar[TengokuSettings]
    
    options_dataclass = TengokuOptions
    options: TengokuOptions

    required_client_version = (0, 6, 7)

    item_name_to_id = {str(name): data.code for name, data in all_items.items()}
    location_name_to_id = all_locations
    item_name_groups = item_groups
    location_name_groups = location_groups
    #origin_region_name = Regions.intro_stage.value
    rule_macros: dict[str, Rule.Resolved]

    ut_can_gen_without_yaml: ClassVar = True
    glitches_item_name: str = Items.glitched
    is_ut: bool = False

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.rule_macros = {}
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)

    def create_items(self) -> None:
        itempool: list[TengokuItem] = []

        self.total_required_locations = count_locations_active(self)

        # Submit stage bundles to item pool
        if self.options.level_unlock == LevelUnlock.option_bundles:
            all_stages = sorted(item_groups["Stage Bundle"])
        else:
            all_stages = sorted(item_groups["Stages"])

        self.selected_stage = self.random.choice(all_stages)
        precollected_items = [item.name for item in self.multiworld.precollected_items[self.player]]
        if set(all_stages).isdisjoint(precollected_items):
            self.push_precollected(self.create_item(self.selected_stage))
            all_stages.remove(self.selected_stage)
        else:
            self.selected_stage = "None"
        for stage in all_stages:
            if stage in precollected_items:
                continue
            itempool.append(self.create_item(stage))

        itempool += [self.create_item(Items.medal) for _ in range(self.options.medals.value)]

        # Setup junk items
        junk_count = self.total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([Items.beep] * 2)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: Items, force_classification=False) -> TengokuItem:
        name = str(name)
        data = all_items[name]
        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        created_item = TengokuItem(name, classification, data.code, self.player)
        return created_item


    def set_rules(self):
        from .rules import TengokuRules
        TengokuRules(self).set_rules()


    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "perfects",
            "superbs",
        )
        slot_data["required_medals"] = self.required_medals
        return slot_data


    def generate_early(self):
        patch_version = f"{self.world_version.major:02}{self.world_version.minor:02}{self.world_version.build:02}"
        self.auth =  bytearray(f'RT-{patch_version}-{self.player}-{self.multiworld.seed:11}\0', 'utf8')[:21]
        self.auth.extend([0] * (21 - len(self.auth)))
        self.required_medals = max(math.floor(self.options.medals.value * (self.options.medals_required.value / 100.0)), 1)

        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[GAME_NAME]
            self.options.perfects.value = slot_data["perfects"]
            self.options.superbs.value = slot_data["superbs"]
            self.required_medals = slot_data["required_medals"]
            self.is_ut = True


    @staticmethod
    def interpret_slot_data(slot_data):
        return slot_data


    def get_filler_item_name(self) -> str:
        return str(Items.beep)

    
    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nRequired Medals: {self.required_medals}")



    def generate_output(self, output_directory: str):
        try:
            patch = TengokuProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
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

