import os
import hashlib
import settings
import Utils
import pkgutil
import pkgutil
import tempfile

import logging
logger = logging.getLogger()

from typing import TYPE_CHECKING, Union, List

if TYPE_CHECKING:
    from . import MMX4World

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension

HASH_US = "1c425b49bb25c45b3964b2d565dd0ec0"

class MMX4PatchExtension(APPatchExtension):
    game = "Mega Man X4"

    @staticmethod
    def apply_basepatch(_: APProcedurePatch, rom: bytes) -> bytes:
        import pyxdelta

        with tempfile.TemporaryDirectory() as temp_dir:
            patch_tempfile = os.path.join(temp_dir, "patch.xdelta")
            delta_tempfile = os.path.join(temp_dir, "patched_rom.bin")
            xdelta_patch = pkgutil.get_data(__name__, os.path.join("data", "MMX4_Archipelago.xdelta"))

            # Copy xdelta contents into temp file
            with open(patch_tempfile, "wb") as f:
                f.write(xdelta_patch)
            
            # Apply xdelta patch
            pyxdelta.decode(get_base_rom_path(), patch_tempfile, delta_tempfile)

            # Read patched rom
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
        ("apply_tokens", ["token_patch.bin"]),
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
        cue_file = f'FILE "{rom_name}.bin" BINARY\n'
        cue_file += f'  TRACK 01 MODE2/2352\n'
        cue_file += f'    INDEX 01 00:00:00\n'

        with open(file_name + ".cue", 'wb') as outfile:
            outfile.write(bytes(cue_file, 'utf-8'))


def patch_rom(world: "MMX4World", patch: MMX4ProcedurePatch):
    # Template stuff from SNES games, might be worth changing it to another thing
    # This is also used as our ctx.auth in bizhawkclient
    from Utils import __version__
    patch.name = bytearray(f'MMX4{__version__.replace(".", "")[0:3]}_{world.player}_{world.multiworld.seed:13}\0', 'utf8')[:16]
    patch.name.extend([0] * (16 - len(patch.name)))
    patch.write_bytes(0x20B98578, patch.name)   # We overwrite the MMX4_ARCHIPELAGO string from the xdelta

    patch.write_file("token_patch.bin", patch.get_token_binary())


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in {HASH_US}:
            raise Exception('Supplied Base Rom does not match known MD5 for US release. '
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

