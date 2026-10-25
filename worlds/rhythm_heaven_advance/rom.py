import Utils
import hashlib
import os
import orjson
from typing import TYPE_CHECKING, Iterable
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

if TYPE_CHECKING:
    from . import RHAWorld

from .constants import *

HASH_JP = 'f81f60fdb2fd774c72a170a1805db52e'

patches = {
    0x00: "vanilla",
    0x01: "tempoup",
    0x02: "plus",
    0x03: "tempoup_plus",
    0x04: "rumble",
    0x05: "tempoup_rumble",
    0x06: "plus_rumble",
    0x07: "tempoup_plus_rumble",
}

class RHAPatchExtension(APPatchExtension):
    game = GAME_NAME
    
    @staticmethod
    def apply_selected_patches(caller: APProcedurePatch, rom: bytes):
        import bsdiff4
        import pkgutil
        
        json_data = orjson.loads(caller.get_file("data.json"))

        setting_byte = 0x00
        patch_file = 0x00
        if json_data["tempo_up"]:
            patch_file |= 0x01
        if json_data["plus"]:
            patch_file |= 0x02
        if json_data["rumble"]:
            patch_file |= 0x04
            setting_byte |= 0x04
        selected_patch = patches[patch_file]
        patch_file = pkgutil.get_data(__name__, f"data/rhythmheavenadvance_{selected_patch}.patch")
        print (f"Using rhythmheavenadvance_{selected_patch}.patch")
        rom = bsdiff4.patch(rom, patch_file)

        setting_byte |= json_data["voices"]
        setting_byte |= json_data["music"]

        rom = bytearray(rom)
        rom[SETTING_GLOBAL] = setting_byte

        return bytes(rom)
        

class RHAProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_JP]
    game = GAME_NAME
    patch_file_ending = ".aprhythmadvance"
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


def patch_rom(world: "RHAWorld", patch: RHAProcedurePatch):
    patch.name = world.auth
    patch.write_bytes(AUTH_NUMBER_START, patch.name)
    patch.write_byte(SETTING_SUPERBS, world.options.superbs.value)
    patch.write_byte(SETTING_PERFECTS, world.options.perfects.value)
    patch.write_byte(SETTING_MEDALS, world.required_medals)
    patch.write_byte(SETTING_UNLOCKS, world.options.level_unlock.value)
    patch.write_file("token_patch.bin", patch.get_token_binary())

    data_dict = {
        "tempo_up": world.options.tempo_up.value,
        "plus": world.options.patch_plus.value,
        "rumble": 0x04,
        "voices": world.options.default_voices.value,
        "music": world.options.default_music.value,
    }
    patch.write_file("data.json", orjson.dumps(data_dict))

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in [HASH_JP]:
            raise Exception("Supplied Base ROM does not match known MD5s for Rhythm Tengoku (JP)."
                            "Get the correct game and version, then dump it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings
        file_name = get_settings()["rhythm_heaven_advance_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

