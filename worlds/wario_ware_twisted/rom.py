import Utils
import hashlib
import os
from typing import TYPE_CHECKING, Iterable
from BaseClasses import Location, ItemClassification
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

if TYPE_CHECKING:
    from . import WarioTwistedWorld

from .stage_data import microgame_data, microgame_text_data, microgame_crown_data, game_text_data
from .text_dict import supported_characters
from .items import item_groups
from .locations import location_groups
from .constants import *

HASH_US = '89579f4dfe1ed24a7cd16a6a61a72a17'
HASH_US_TILT = 'e2dbd6a74162fae64f9835762242ca1c'


def align(num: int):
    return ((num + 15) // 16) * 16


class WarioTwistedPatchExtension(APPatchExtension):
    game = GAME_NAME
    
    @staticmethod
    def apply_selected_patches(caller: APProcedurePatch, rom: bytes):
        import bsdiff4
        import pkgutil
        
        basemd5 = hashlib.md5()
        basemd5.update(rom)
        if basemd5.hexdigest() == HASH_US:
            patch_file = pkgutil.get_data(__name__, f"data/wario_twisted_tilt.bsdiff4")
        else:
            patch_file = pkgutil.get_data(__name__, f"data/wario_twisted_no_tilt.bsdiff4")
        rom = bsdiff4.patch(rom, patch_file)

        return rom
        

class WarioTwistedProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US]
    game = GAME_NAME
    patch_file_ending = ".apwariotwisted"
    result_file_ending = ".gba"
    name: bytearray
    procedure = [
        ("apply_selected_patches", []),
        ("apply_tokens", ["token_patch.bin"]),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))

    def write_text(self, original_text_ptr: int, text: str):
        text += "⛉©©©©©©©©"
        if not hasattr(self, "text_location"):
            self.text_location = RANDOM_TEXT_LOCATION
        self.write_bytes(original_text_ptr, (self.text_location | 0x08000000).to_bytes(4, "little"))
        for character in text:
            if character not in supported_characters:
                character = "★"
            data = supported_characters[character]
            for current_byte in data:
                self.write_byte(self.text_location, current_byte)
                self.text_location += 1
        self.text_location = align(self.text_location)


def patch_rom(world: "WarioTwistedWorld", patch: WarioTwistedProcedurePatch):
    patch.name = world.auth
    patch.write_bytes(AUTH_NUMBER_START, patch.name)
    patch.write_byte(SETTING_UNLOCKS, world.options.microgame_unlock.value)
    patch.write_byte(SETTING_GOAL, world.required_crowns)
    patch.write_byte(SETTING_CROWNS, world.options.crowns_required.value)

    microgames_list = world.microgames.copy()
    microgames_list.extend([0xFFFF] * (0x200 - len(microgames_list)))
    idx = 0
    microgame: int
    for microgame in microgames_list:
        patch.write_bytes(MICROGAMES_LIST+idx, microgame.to_bytes(2, "little"))
        idx += 2

    write_location_data(world, patch)
    
    patch.write_file("token_patch.bin", patch.get_token_binary())

classification_text = {
    ItemClassification.progression | ItemClassification.useful:
        "☀LOCATION⛉",
    ItemClassification.progression:
        "⛊LOCATION⛉",
}

def get_location_text(text: str, item_name: str, player_name: str, classification: ItemClassification):
    if classification in classification_text:
        text += f"{classification_text[classification].replace("LOCATION", item_name)} "
    else:
        text += f"{item_name} "
    text += f"(⛊{player_name}⛉)"
    return text

def write_location_data(world: "WarioTwistedWorld", patch: WarioTwistedProcedurePatch):
    filled_locations = world.multiworld.get_filled_locations(world.player)
    location_data_by_name = {location.name: location for location in filled_locations}
    
    # Write microgame text
    for microgame_name in microgame_data.keys():
        if f"{microgame_name} - Clear" not in location_data_by_name.keys():
            continue

        item_name, classification, player_name = get_location_info(world, location_data_by_name[f"{microgame_name} - Clear"])

        clear_text = get_location_text("Clear — ", item_name, player_name, classification)
        crown_text = ""
        if world.options.microgame_crowns:
            crown_text = get_location_text(f"Crown: ⛊{microgame_crown_data[microgame_name]}⛉ Pts. — ", item_name, player_name, classification)
            crown_text += " ★"

        hint_text = f"【{microgame_name}】 {crown_text} {clear_text}"

        microgame_id = microgame_text_data[microgame_name]
        patch.write_text(MICROGAME_PTRS + (microgame_id * 4 * 6), hint_text)

    # Write game text
    for game_group in game_text_data:
        points_text = ""
        clear_text = ""
        for location_name in location_groups[game_group]:
            if location_name not in location_data_by_name.keys():
                continue
            item_name, classification, player_name = get_location_info(world, location_data_by_name[location_name])

            if "- Clear" in location_name:
                clear_text = get_location_text("Clear — ", item_name, player_name, classification)
            else:
                points = location_name.split(" - ")[1].split(" Points")[0]
                current_points_text = get_location_text(f"{points} Pts. — ", item_name, player_name, classification)
                points_text += f"★ {current_points_text} " 

        final_text = f"⛊Rewards:⛉ {clear_text} {points_text}"
        patch.write_text(game_text_data[game_group], final_text)

    # Write misc text
    version = world.world_version.as_simple_string()
    patch.write_text(0x093E07C, f"Welcome to the ⛊WarioWare: Twisted! Archipelago v{version}⛉. Your goal is to collect ☀{world.required_crowns} Crowns⛉ — Once that's achieved, head to the credits sequence in Souvenirs and watch them.")
    patch.write_text(0x093774C, f"Archipelago implementation of ⛊WarioWare: Twisted! v{version}⛉ made by ☀lx5⛉. Go play my other implementations ;)")


def get_location_info(world: "WarioTwistedWorld", location: Location):
    return (
        location.item.name[:32],
        location.item.classification & (ItemClassification.progression | ItemClassification.useful),
        world.multiworld.get_player_name(location.item.player)[:16]
    )

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in [HASH_US, HASH_US_TILT]:
            raise Exception(f"Supplied Base ROM does not match known MD5s for {GAME_NAME}."
                            "Get the correct game and version, then dump it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings
        file_name = get_settings()["wario_ware_twisted_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

