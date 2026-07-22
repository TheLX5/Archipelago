import Utils
import hashlib
import os
from pathlib import Path
import orjson
import base64
from argparse import Namespace
from typing import TYPE_CHECKING, Iterable, Any
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

if TYPE_CHECKING:
    from . import MMX2World

from .constants import *

HASH_US = '67905b989b00046db06df3434ed79f04'
HASH_LEGACY = 'a8aa24df75686a5bb1a08a27d1876f5f'

LC_EXE_HASH = 'f31847891e120d19d74fe2098b273627'
LC_ROM_OFFSET = 0x110DF20
LC_ROM_SIZE = 0x180000

ROM_SETTINGS = 0x17FFE0

class MMX3PatchExtension(APPatchExtension):
    game = GAME_NAME
    
    @staticmethod
    def handle_enemy_hp(caller: APProcedurePatch, rom: bytes):
        import random

        rom = bytearray(rom)

        rolled_enemy_data: dict[str, dict[str, Any]] = orjson.loads(base64.b64decode(caller.get_file("enemy_data.bin")))
        json_data = orjson.loads(caller.get_file("data.json"))
        random.seed(json_data["seed"])

        for enemy_name, enemy_data in rolled_enemy_data.items():
            hp_address: int = enemy_data["hp_address"]
            hp_value: int = enemy_data["hp"]
            if hp_address == 0x0:
                continue
            if enemy_name == "Morph Moth":
                value_2 = random.randint(1, hp_value - 1)
                rom[0x1ABB7] = value_2
                rom[0x1B05E] = value_2
            elif enemy_name == "Gigantic Mechaniloid CF-0":
                rom[0x39F74] = hp_value
            rom[hp_address] = hp_value

        return bytes(rom)


    @staticmethod
    def handle_enemy_weaknesses(caller: APProcedurePatch, rom: bytes):
        from .boss_data import weapons

        rom = bytearray(rom)

        rolled_enemy_data: dict[str, dict[str, Any]] = orjson.loads(base64.b64decode(caller.get_file("enemy_data.bin")))
        strictness = rom[ROM_SETTINGS+0x10]

        weakness_offset = 0x140000

        for enemy_name, enemy_data in rolled_enemy_data.items():
            weakness_data = [0xFF for _ in range(16)]

            if enemy_name == "Gigantic Mechaniloid CF-0":
                weakness_data[0] = 0x00
                rom[weakness_offset:weakness_offset+16] = bytearray(weakness_data)
                weakness_offset += 16
                continue

            offset: int = enemy_data["weakness_addr"]

            if strictness == 0x00:
                damage_table_data = rom[offset:offset+0x26]
            else:
                damage_table_data = [
                    0x80, 0x80, 0x80, 0x80, 0x01, 0x80, 0x80, 0x80,
                    0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x03,
                    0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
                    0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80,
                    0x80, 0x80, 0x80, 0x80, 0x80, 0x80]

            weakness_data_idx = 0

            # Multipliers are used for certain bosses to be easier to handle
            multiplier = 1
            if enemy_name == "Serges Tank":
                multiplier = 2
            
            for weapon_name in enemy_data["weakness"]:
                weapon = weapons[weapon_name]
                damage_table_data[weapon.id] = int(weapon.damage * multiplier) if weapon.damage < 0x80 else weapon.damage
                weakness_data[weakness_data_idx] = weapon.id
                weakness_data_idx += 1

            # Save damage data, add some potential secondary tables for some bosses
            rom[offset:offset+0x26] = damage_table_data
            if enemy_name == "Wheel Gator":
                offset = 0x37669
                rom[offset:offset+0x26] = damage_table_data

            # Write weaknesses to a ROM table that's copied to RAM on boot
            print (f"{weakness_offset:06X} {len(weakness_data)} {weakness_data}")
            rom[weakness_offset:weakness_offset+16] = bytearray(weakness_data)
            weakness_offset += 16


        return bytes(rom)
    
    
    @staticmethod
    def handle_palettes(caller: APProcedurePatch, rom: bytes):
        rom = bytearray(rom)

        if vars(Utils.persistent_load().get("palette_settings", {}).get(GAME_NAME, Namespace())):
            palette_manager = Utils.persistent_load().get("palette_settings", {}).get(GAME_NAME, Namespace())

            from .aesthetics import get_palette_bytes, player_palettes

            player_palette_options = {
                "Default": palette_manager.pal_default,
                "Crystal Hunter": palette_manager.pal_crystal,
                "Bubble Splash": palette_manager.pal_bubble,
                "Silk Shot": palette_manager.pal_silk,
                "Spin Wheel": palette_manager.pal_wheel,
                "Sonic Slicer": palette_manager.pal_slicer,
                "Strike Chain": palette_manager.pal_chain,
                "Magnet Mine": palette_manager.pal_mine,
                "Speed Burner": palette_manager.pal_burner,
            }
            x_palette_set_offsets = {
                "Default": 0x02B100,
                "Crystal Hunter": 0x02CCA0,
                "Bubble Splash": 0x02CC60,
                "Silk Shot": 0x02CCC0,
                "Spin Wheel": 0x02CD00,
                "Sonic Slicer": 0x02CC40,
                "Strike Chain": 0x02CCE0,
                "Magnet Mine": 0x02CC20,
                "Speed Burner": 0x02CC80,
            }
            # TODO: Add custom palette support
            player_custom_palettes = {}
            for palette_set, offset in x_palette_set_offsets.items():
                palette_option = player_palette_options[palette_set]
                palette = player_palettes[palette_option]

                if palette_set in player_custom_palettes.keys():
                    if len(player_custom_palettes[palette_set]) == 0x10:
                        palette = player_custom_palettes[palette_set]
                data = get_palette_bytes(palette)
                rom[offset:offset+len(data)] = bytes(data)

        return bytes(rom)
    
    
    @staticmethod
    def handle_settings(caller: APProcedurePatch, rom: bytes):
        rom = bytearray(rom)

        json_data = orjson.loads(caller.get_file("data.json"))
        rom[ROM_SETTINGS+0x05] = json_data["energy_link"]
        rom[ROM_SETTINGS+0x06] = json_data["death_link"]
        rom[ROM_SETTINGS+0x07] = json_data["damage_link"]

        if vars(Utils.persistent_load().get("global_settings", {}).get(GAME_NAME, Namespace())):
            global_settings = Utils.persistent_load().get("global_settings", {}).get(GAME_NAME, Namespace())

            group_settings = 0x00
            if hasattr(global_settings, "long_jump"):
                if global_settings.long_jump:
                    group_settings |= 0x01
            if hasattr(global_settings, "shoryuken_input"):
                if global_settings.shoryuken_input:
                    group_settings |= 0x80
            
            rom[ROM_SETTINGS+0x11] = group_settings

            if hasattr(global_settings, "serges_qol"):
                if global_settings.serges_qol:
                    # Remove collision from the cup inside Serges' Tank
                    rom[0x1518F] = 0xEA
                    rom[0x15190] = 0xEA
                    rom[0x15191] = 0xEA
                    rom[0x15192] = 0xEA

                    # Make Serges inside tank have bigger collision
                    rom[0x35BFD] = 0x03
                    rom[0x35BFE] = 0xF8
                    rom[0x35BFF] = 0x0D
                    rom[0x35C00] = 0x16

                    # Serges no longer gets stunned
                    rom[0x149C23] = 0xEA
                    rom[0x149C24] = 0xEA
                    rom[0x149C25] = 0xEA

                    # Serges no longer taunts
                    rom[0x149C41] = 0xEA
                    rom[0x149C42] = 0xEA
                    rom[0x149C43] = 0xEA

                    # Serges no longer has a shield
                    rom[0x149F81] = 0x6B

            button_values = {
                "A": 0x20,
                "B": 0x80,
                "X": 0x10,
                "Y": 0x40,
                "L": 0x08,
                "R": 0x04,
                "START": 0x01,
                "SELECT": 0x02,
            }
            if hasattr(global_settings, "button_dash"):
                rom[0x371FB] = button_values[global_settings.button_dash]
            if hasattr(global_settings, "button_jump"):
                rom[0x371FA] = button_values[global_settings.button_jump]
            if hasattr(global_settings, "button_menu"):
                rom[0x371FE] = button_values[global_settings.button_menu]
            if hasattr(global_settings, "button_shot"):
                rom[0x371F9] = button_values[global_settings.button_shot]
            if hasattr(global_settings, "button_select_l"):
                rom[0x371FC] = button_values[global_settings.button_select_l]
            if hasattr(global_settings, "button_select_r"):
                rom[0x371FD] = button_values[global_settings.button_select_r]

        return bytes(rom)


    @staticmethod
    def output_xml(caller: APProcedurePatch, rom: bytes):
        manifest = caller.get_file("mmx2_manifest_for_bsnes.xml")
        manifest_path = f"{Path(caller.path).absolute().with_suffix('')}.xml"
        with open(manifest_path, "wb") as f:
            f.write(manifest)
        return rom


class MMX2ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US, HASH_LEGACY]
    game = GAME_NAME
    patch_file_ending = ".apmmx2"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_tokens", ["token_patch.bin"]),
        ("apply_bsdiff4", ["mmx2_basepatch.bsdiff4"]),
        ("handle_enemy_hp", []),
        ("handle_enemy_weaknesses", []),
        ("handle_palettes", []),
        ("handle_settings", []),
        ("output_xml", []),
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, value.to_bytes(1, "little"))

    def write_bytes(self, offset: int, value: Iterable[int]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))


def patch_rom(world: "MMX2World", patch: MMX2ProcedurePatch):
    from Utils import __version__

    # Prepare some ROM locations to receive the basepatch
    patch.write_bytes(0x00610, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x00632, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01113, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01154, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                          0xFF]))
    patch.write_bytes(0x0120A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x01219, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x0123D, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x026A5, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06A79, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x06CD5, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x06EF8, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x06EFB, bytearray([0xFF]))
    patch.write_bytes(0x06F7B, bytearray([0xFF,0xFF]))
    patch.write_bytes(0x0919E, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0CDE2, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x0CE11, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x21D47, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x22CCE, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x3944B, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x398C8, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x3A187, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x459E6, bytearray([0xFF]))
    patch.write_bytes(0x459E8, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x45C11, bytearray([0xFF]))
    patch.write_bytes(0x45C13, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x1488EF, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x149A02, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x154082, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x155CA5, bytearray([0xFF,0xFF,0xFF]))
    patch.write_bytes(0x1569BB, bytearray([0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x17FB5A, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]))
    patch.write_bytes(0x17FB62, bytearray([0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
                                           0xFF]))
    patch.write_bytes(0x07E80, bytearray([0xFF for _ in range(0x120)]))
    patch.write_bytes(0x0FE80, bytearray([0xFF for _ in range(0x180)]))
    patch.write_bytes(0x17FA0, bytearray([0xFF for _ in range(0x60)]))
    patch.write_bytes(0x1FF00, bytearray([0xFF for _ in range(0x100)]))
    patch.write_bytes(0x3FF78, bytearray([0xFF for _ in range(0x88)]))
    patch.write_bytes(0x30DEC, bytearray([0xFF for _ in range(0x55)]))
    
    # Edit the ROM header
    patch_version = f"{world.world_version.major:02}{world.world_version.minor:02}{world.world_version.build:02}"
    patch.name = bytearray(f'LX2-{patch_version}-{world.player}-{world.multiworld.seed:11}\0', 'utf8')[:21]
    patch.name.extend([0] * (21 - len(patch.name)))
    patch.write_bytes(0x7FC0, patch.name)

    # Starting HP
    patch.write_byte(0x01D6A, 0x7F)
    
    # Write options to the ROM
    patch.write_byte(ROM_SETTINGS+0x00, world.options.x_hunter_base_open.value)
    patch.write_byte(ROM_SETTINGS+0x01, world.options.x_hunter_base_medal_count.value)
    patch.write_byte(ROM_SETTINGS+0x02, world.options.pickup_locations.value)
    patch.write_byte(ROM_SETTINGS+0x03, world.options.jammed_buster.value)
    patch.write_byte(ROM_SETTINGS+0x05, world.options.energy_link.value)
    patch.write_byte(ROM_SETTINGS+0x06, world.options.death_link.value)
    patch.write_byte(ROM_SETTINGS+0x07, world.options.damage_link.value)
    patch.write_byte(ROM_SETTINGS+0x0C, world.options.boss_weakness_rando.value)
    patch.write_byte(ROM_SETTINGS+0x0D, world.options.starting_hp.value)
    patch.write_byte(ROM_SETTINGS+0x0E, world.options.heart_tank_effectiveness.value)
    patch.write_byte(ROM_SETTINGS+0x0F, world.options.x_hunter_base_level_unlock.value)
    patch.write_byte(ROM_SETTINGS+0x10, world.options.boss_weakness_strictness.value)
    patch.write_byte(ROM_SETTINGS+0x12, world.options.x_hunters_arena_medal_count.value)
    patch.write_byte(ROM_SETTINGS+0x13, world.options.x_hunter_base_boss_rematch_count.value)

    patch.write_file("token_patch.bin", patch.get_token_binary())

    # Save enemy data to an external file inside the patch
    json_data = {}
    for boss_name, boss_object in world.boss_data.items():
        json_data[boss_name] = boss_object.dump_rom_data()
    patch.write_file("enemy_data.bin", base64.b64encode(orjson.dumps(json_data)))

    # Save random data to an external file
    data_dict = {
        "seed": world.random.getrandbits(64),
        "energy_link": world.options.energy_link.value,
        "death_link": world.options.death_link.value,
        "damage_link": world.options.damage_link.value,
    }
    patch.write_file("data.json", orjson.dumps(data_dict))

    
def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() == LC_EXE_HASH:
            base_rom_bytes = extract_mmx2(base_rom_bytes)
            basemd5 = hashlib.md5()
            basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US, HASH_LEGACY}:
            raise Exception('Supplied Base Rom does not match known MD5 for US or LC release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        from settings import get_settings
        file_name = get_settings()["mmx2_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def extract_mmx2(exe_file: bytes) -> bytes:
    mmx2 = bytearray(exe_file[LC_ROM_OFFSET:LC_ROM_OFFSET + LC_ROM_SIZE])
    return bytes(mmx2)
