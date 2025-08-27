import os
import hashlib
import settings
import Utils
import pkgutil
import pkgutil
from tempfile import mktemp

import logging
logger = logging.getLogger()

from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from . import MMX4World

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

HASH_US = "1c425b49bb25c45b3964b2d565dd0ec0"

boss_data = {
    0: (14574100,14574101), # Intro
    1: (14574104,14574105), # Web Spider
    2: (14574109,14574110), # Cyber Peacock
    3: (14574114,14574115), # Storm Owl 
    4: (14574118,14574119), # Magma Dragoon
    5: (14574122,14574123), # Jet Stingray
    6: (14574125,14574126), # Split Mushroom
    7: (14574128,14574129), # Slash Beast
    8: (14574133,14574134), # Frost Walrus
    9: (14574135),          # Memorial Hall Colonel
    10: (14574136),         # Space Port Colonel
    11: (14574137),         # Double / Iris
    12: (14574138),         # General
    13: (14574139),         # Web Spider (Rematch)
    14: (14574140),         # Cyber Peacock (Rematch)
    15: (14574141),         # Storm Owl (Rematch)
    16: (14574142),         # Magma Dragoon (Rematch)
    17: (14574143),         # Jet Stingray (Rematch)
    18: (14574144),         # Split Mushroom (Rematch)
    19: (14574145),         # Slash Beast (Rematch)
    20: (14574146),         # Frost Walrus (Rematch)
    21: (14574300),         # Sigma
}

armor_data = {
    0: 14574108,    # Head
    1: 14574117,    # Body
    2: 14574112,    # Arms 1
    3: 14574113,    # Arms 2
    4: 14574102,    # Legs
}

item_data = {
    # Intro
    0x800F4D30: 14574200,
    0x800F4D40: 14574201,
    0x800F4D38: 14574202,
    # Web Spider
    0x800F52B0: 14574203,
    0x800F52C0: 14574204,
    0x800F52B8: 14574103,
    # Cyber Peacock
    0x800F7438: 14574106,
    0x800F7440: 14574107,
    # Storm Owl
    0x800F7700: 14574205,
    0x800F7978: 14574206,
    0x800F76F8: 14574111,
    # Magma Dragoon
    0x800F6854: 14574116,
    0x800F66B4: 14574207,
    0x800F66BC: 14574208,
    0x800F685C: 14574209,
    # Jet Stingray
    0x800F6C40: 14574120,
    0x800F6E98: 14574121,
    0x800F6EA0: 14574210,
    # Split Mushroom
    0x800F6320: 14574124,
    0x800F6328: 14574211,
    0x800F6330: 14574212,
    # Slash Beast
    0x800F7D3C: 14574127,
    0x800F7D44: 14574213,
    # Frost Walrus
    0x800F56C0: 14574214,
    0x800F56C8: 14574215,
    0x800F56B8: 14574216,
    0x800F56B0: 14574217,
    0x800F5660: 14574218,
    0x800F5680: 14574219,
    0x800F5688: 14574220,
    0x800F5690: 14574221,
    0x800F5698: 14574222,
    0x800F56A0: 14574223,
    0x800F56A8: 14574224,
    0x800F5668: 14574225,
    0x800F5678: 14574226,
    0x800F5868: 14574227,
    0x800F5658: 14574230,
    0x800F5670: 14574231,
    0x800F5860: 14574232,
    # Final Weapon 1
    0x800F86CC: 14574228,
    0x800F8564: 14574229,
    0x800F855C: 14574230,
    # Final Weapon 2
    0x800F87E0: 14574231,
    0x800F87E8: 14574232,
    0x800F87F0: 14574233,
    0x800F87F8: 14574234,
    0x800F8910: 14574235,
    0x800F8918: 14574236,
    0x800F8920: 14574237,
}

unlock_data = {
    "Weapons": {
        14575100: 0x01, # Lightning Web
        14575101: 0x20, # Aiming Laser
        14575102: 0x40, # Double Cyclone
        14575103: 0x08, # Rising Fire
        14575104: 0x10, # Ground Hunter
        14575105: 0x04, # Soul Body
        14575106: 0x80, # Twin Slasher
        14575107: 0x02, # Frost Tower
    },
    "Armor": {
        14575108: 0x01, # Helmet
        14575109: 0x02, # Body
        14575110: 0x04, # Arms
        14575111: 0x04, # Arms
        14575112: 0x08, # Legs
    },
    "Tanks": {
        14575114: [0x10, 0x20], # Sub Tank
        14575115: 0x40, # Weapon Energy Tank
        14575116: 0x80, # Extra Lives Tank
    },
    "Access": {
        14575200: 0x01, # Web Spíder
        14575201: 0x01, # Cyber Peacock
        14575202: 0x01, # Storm Owl
        14575203: 0x01, # Magma Dragoon
        14575204: 0x01, # Jet Stingray
        14575205: 0x01, # Split Mushroom
        14575206: 0x01, # Slash Beast
        14575207: 0x01, # Frost Walrus
    }
}

class MMX4PatchExtension(APPatchExtension):
    game = "Mega Man X4"

    @staticmethod
    def apply_basepatch(_: APProcedurePatch, rom: bytes) -> bytes:
        import pyxdelta
        delta_tempfile = mktemp()
        patch_tempfile = mktemp()
        xdelta_patch = pkgutil.get_data(__name__, os.path.join("data", "MMX4_Archipelago.xdelta"))
        with open(patch_tempfile, "wb") as f:
            f.write(xdelta_patch)
        pyxdelta.decode(get_base_rom_path(), patch_tempfile, delta_tempfile)

        with open(delta_tempfile, "rb") as f:
            rom = f.read()

        return rom

class MMX4ProcedurePatch(APProcedurePatch, APTokenMixin):
    hash = [HASH_US]
    game = "Mega Man X4"
    patch_file_ending = ".apmmx4"
    result_file_ending = ".cue"
    name: bytearray
    procedure = [
        ("apply_basepatch", []),
        #("apply_tokens", ["token_patch.bin"]),     # We should uncomment this the moment we have something to actually patch per game
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_byte(self, offset: int, value: int):
        self.write_token(APTokenTypes.WRITE, offset, bytes([value]))

    def write_bytes(self, offset: int, values: Union[List[int], bytes]):
        self.write_token(APTokenTypes.WRITE, offset, bytes(values))

    def patch(self, target: str) -> None:
        file_name = target[:-4]
        if os.path.exists(file_name + ".bin") and os.path.exists(file_name + ".cue"):
            logger.info("Patched ROM + CUE already exist!")
            return

        super().patch(target)

        os.rename(target, file_name + ".bin")
        rom_name = target[target.rfind('/') + 1:-4]
        print (rom_name)
        cue_file = f'FILE "{rom_name}.bin" BINARY\n'
        cue_file += f'  TRACK 01 MODE2/2352\n'
        cue_file += f'    INDEX 01 00:00:00\n'

        with open(file_name + ".cue", 'wb') as outfile:
            outfile.write(bytes(cue_file, 'utf-8'))


def patch_rom(world: "MMX4World", patch: MMX4ProcedurePatch):
    from Utils import __version__
    patch.name = bytearray(f'MMX4{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:13}\0', 'utf8')[:16]
    patch.name.extend([0] * (16 - len(patch.name)))
    patch.write_bytes(0x20B98578, patch.name)
    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US}:
            raise Exception('Supplied Base Rom does not match known MD5 for US 1.0 release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["mmx4_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

