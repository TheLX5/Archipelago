import os
import settings
import threading
import pkgutil
import hashlib

from BaseClasses import MultiWorld, Tutorial, ItemClassification, CollectionState
from worlds.AutoWorld import World, WebWorld, LogicMixin
from worlds.LauncherComponents import launch as launch_component, components, Component, Type
from rule_builder.rules import Rule

from .options import MMX2Options, XHunterBaseOpen, mmx2_option_groups
from .client import MMX2SNIClient
from .regions import create_regions, connect_regions
from .rom import patch_rom, MMX2ProcedurePatch, HASH_US, HASH_LEGACY, LC_EXE_HASH
from .boss_data import Boss, default_boss_data, shuffle_weaknesses, shuffle_hp
from .enums import Items, Locations, Regions
from .items import MMX2Item, all_items, item_groups
from .locations import all_locations, location_groups, count_locations_active
from .constants import *
from . import tracker

from typing import Any, ClassVar, TextIO, Optional, Sequence, Tuple

def launch_manager(*args):
    from .manager import launch
    launch_component(launch, "Mega Man X2 Manager")

components.append(Component(display_name="Mega Man X2 Manager", component_type=Type.ADJUSTER, func=launch_manager))


class MMX2Settings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the Mega Man X2 US ROM"""
        description = "Mega Man X2 (USA) ROM File"
        copy_to = "Mega Man X2 (USA).sfc"
        md5s = [HASH_US, HASH_LEGACY, LC_EXE_HASH]

        # Borrowed from MM2, let's pray it actually works for X LC
        def browse(self: settings.T,
                   filetypes: Optional[Sequence[Tuple[str, Sequence[str]]]] = None,
                   **kwargs: Any) -> Optional[settings.T]:
            if not filetypes:
                file_types = [("SNES", [".sfc"]), ("Program", [".exe"])]  # LC1 is only a windows executable, no linux
                return super().browse(file_types, **kwargs)
            else:
                return super().browse(filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            """Try to open and validate file against hashes"""
            with open(path, "rb", buffering=0) as f:
                try:
                    f.seek(0)
                    cls._validate_stream_hashes(f)
                    base_rom_bytes = f.read()
                    basemd5 = hashlib.md5()
                    basemd5.update(base_rom_bytes)
                    if basemd5.hexdigest() == LC_EXE_HASH:
                        # we need special behavior here
                        cls.copy_to = None
                except ValueError:
                    raise ValueError(f"File hash does not match for {path}")

    rom_file: RomFile = RomFile(RomFile.copy_to)


class MMX2Web(WebWorld):
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
    option_groups = mmx2_option_groups

class MMX2World(tracker.UTMxin, World):
    """
    Mega Man X2, released in 1994 for the SNES, is the second game in Capcom's "Mega Man X" series. 
    Players control Mega Man X, a Maverick Hunter, as he battles a new group of Mavericks and the X-Hunters, 
    who have taken parts of his ally Zero. The game features classic run-and-gun gameplay with challenging levels, 
    boss battles that grant new weapons, and the use of the Cx4 chip for enhanced graphics.
    """
    game = GAME_NAME
    web = MMX2Web()

    settings: ClassVar[MMX2Settings]
    
    options_dataclass = MMX2Options
    options: MMX2Options

    required_client_version = (0, 6, 7)

    item_name_to_id = {str(name): data.code for name, data in all_items.items()}
    location_name_to_id = all_locations
    #item_name_groups = item_groups
    #location_name_groups = location_groups
    origin_region_name = Regions.intro_stage.value
    rule_macros: dict[str, Rule.Resolved]
    boss_data: dict[str, Boss] = {}

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        self.rule_macros = {}
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

    def create_items(self) -> None:
        itempool: list[MMX2Item] = []

        # Set Maverick Medals
        maverick_location_names =[
            Locations.wheel_gator_clear,
            Locations.bubble_crab_clear,
            Locations.flame_stag_clear,
            Locations.morph_moth_clear,
            Locations.magna_centipede_clear,
            Locations.crystal_snail_clear,
            Locations.overdrive_ostrich_clear,
            Locations.wire_sponge_clear
        ]
        for location_name in maverick_location_names:
            self.get_location(location_name.value).place_locked_item(self.create_item(Items.maverick_medal))

        # Set sigma access item
        self.get_location(Locations.x_hunter_stage_4_clear.value).place_locked_item(self.create_item(Items.stage_sigma))

        # Set victory item
        self.get_location(Locations.x_hunter_stage_5_sigma.value).place_locked_item(self.create_item(Items.victory))

        self.total_required_locations = count_locations_active(self)

        valid_stages = sorted(item_groups["Access Codes"])
        valid_stages.remove(Items.stage_x_hunter)

        self.selected_stage = self.random.choice(valid_stages)
        precollected_items = [item.name for item in self.multiworld.precollected_items[self.player]]
        if set(valid_stages).isdisjoint(precollected_items):
            self.get_location(Locations.intro_stage_clear).place_locked_item(self.create_item(self.selected_stage))
            valid_stages.remove(self.selected_stage)
            self.total_required_locations -= 1

        for stage in valid_stages:
            if stage in precollected_items:
                continue
            itempool.append(self.create_item(stage))
            
        
        if self.options.x_hunter_base_open == XHunterBaseOpen.option_item:
            itempool += [self.create_item(Items.stage_x_hunter)]

        itempool += [self.create_item(Items.spin_wheel)]
        itempool += [self.create_item(Items.bubble_splash)]
        itempool += [self.create_item(Items.speed_burner)]
        itempool += [self.create_item(Items.silk_shot)]
        itempool += [self.create_item(Items.magnet_mine)]
        itempool += [self.create_item(Items.crystal_hunter)]
        itempool += [self.create_item(Items.sonic_slicer)]
        itempool += [self.create_item(Items.strike_chain)]
        itempool += [self.create_item(Items.arms)]
        itempool += [self.create_item(Items.arms)]
        itempool += [self.create_item(Items.helmet)]
        itempool += [self.create_item(Items.body)]
        itempool += [self.create_item(Items.legs)]
        itempool += [self.create_item(Items.heart_tank) for _ in range(8)]
        itempool += [self.create_item(Items.sub_tank) for _ in range(4)]

        # Add optional upgrades into the pool
        if self.options.shoryuken_in_pool:
            itempool += [self.create_item(Items.shoryuken)]
            
        if self.options.pickup_locations:
            for chip_name in self.options.chips.value:
                itempool.append(self.create_item(chip_name))
        
        # Setup junk items
        junk_count = self.total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([Items.small_hp] * 40)
        junk_weights += ([Items.large_hp] * 55)

        junk_pool = []
        for _ in range(junk_count):
            junk_item = self.random.choice(junk_weights)
            junk_pool.append(self.create_item(junk_item))

        itempool += junk_pool

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: Items, force_classification=False) -> MMX2Item:
        name = str(name)
        data = all_items[name]
        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        created_item = MMX2Item(name, classification, data.code, self.player)
        return created_item


    def set_rules(self):
        from .rules import MMX2Rules
        MMX2Rules(self).set_rules()


    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        return slot_data


    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "energy_link",
            "starting_hp",
            "heart_tank_effectiveness",
            "boss_weakness_strictness",
            "pickup_locations",
            "jammed_buster",
            "x_hunter_base_boss_rematch_count",
            "x_hunter_base_level_unlock",
            "x_hunter_base_open",
            "x_hunter_base_medal_count",
            "x_hunters_arena_medal_count",
            "chips",
        )
        slot_data["boss_data"] = {name: data.dump_slot_data() for name, data in self.boss_data.items()}
        return slot_data


    def generate_early(self):
        self.hp_per_upgrade = self.options.heart_tank_effectiveness.value

        # Fill default boss data
        self.boss_data = {name: Boss(name=boss.name,
                                    weakness=boss.weakness,
                                    sub_weakness=boss.sub_weakness,
                                    excluded_weaknesses=boss.excluded_weaknesses,
                                    entrances=boss.entrances,
                                    locations=boss.locations,
                                    weakness_addr=boss.weakness_addr,
                                    hp=boss.hp,
                                    hp_address=boss.hp_address,
                                    required_player_hp=boss.required_player_hp)
                        for name, boss in default_boss_data.items()
                        }
        shuffle_weaknesses(self)
        shuffle_hp(self)
        
        super().generate_early()


    def get_filler_item_name(self) -> str:
        return str(Items.large_hp)


    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nEnemy information:\n")
        spoiler_handle.write(f"{"-" * 69}\n")
        spoiler_handle.write(f" {"BOSS NAME":<26s} | HP | {"WEAKNESSES":<32s} |\n")
        spoiler_handle.write(f"{"-" * 69}\n")
        for boss_name, boss_data in self.boss_data.items():
            spoiler_handle.write(f" {boss_name:<26s} | {boss_data.hp:2} |")
            w = 0
            for weapon in boss_data.weakness:
                if w == 0:
                    spoiler_handle.write(f" {weapon:<32s} |\n")
                    w += 1
                else:
                    spoiler_handle.write(f" {" ":<26s} |    | {weapon:<32s} |\n")
            else:
                spoiler_handle.write(f"{"-" * 69}\n")


    def generate_output(self, output_directory: str):
        try:
            patch = MMX2ProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
            patch.write_file("mmx2_basepatch.bsdiff4", pkgutil.get_data(__name__, "data/mmx2_basepatch.bsdiff4"))
            patch.write_file("mmx2_manifest_for_bsnes.xml", pkgutil.get_data(__name__, "data/mmx2_manifest_for_bsnes.xml"))
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
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def collect(self, state: CollectionState, item: MMX2Item) -> bool:
        change = super().collect(state, item)
        if change and item.name == Items.heart_tank.value:
            state.current_hp[self.player] += self.options.heart_tank_effectiveness.value
        return change
    
    def remove(self, state: CollectionState, item: MMX2Item) -> bool: 
        change = super().remove(state, item)
        if change and item.name == Items.heart_tank.value:
            state.current_hp[self.player] -= self.options.heart_tank_effectiveness.value
        return change


class MMXState(LogicMixin):
    hp: dict[int, int]

    def init_mixin(self, multiworld: MultiWorld) -> None:
        self.current_hp = {
            player: multiworld.worlds[player].options.starting_hp.value for player in multiworld.get_game_players(GAME_NAME)
        }

    def copy_mixin(self, new_state: CollectionState) -> CollectionState:
        new_state.current_hp = {player: hp for player, hp in self.current_hp.items()}
        return new_state
