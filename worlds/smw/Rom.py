import Utils
from worlds.AutoWorld import World
from worlds.Files import APDeltaPatch
from .Aesthetics import generate_shuffled_header_data, generate_shuffled_ow_palettes, generate_curated_level_palette_data, generate_curated_map_palette_data, generate_shuffled_sfx
from .Levels import level_info_dict, full_bowser_rooms, standard_bowser_rooms, submap_boss_rooms, ow_boss_rooms
from .Names.TextBox import generate_goal_text, title_text_mapping, generate_text_box

USHASH = 'cdd3c8c37322978ca8669b34bc89c804'
ROM_PLAYER_LIMIT = 65535

import hashlib
import os
from pkgutil import get_data
import bsdiff4


ability_rom_data = {
    0xBC0003: [[0x1F1C, 0x7]], # Run         0x80
    0xBC0004: [[0x1F1C, 0x6]], # Carry       0x40
    0xBC0005: [[0x1F1C, 0x2]], # Swim        0x04
    0xBC0006: [[0x1F1C, 0x3]], # Spin Jump   0x08
    0xBC0007: [[0x1F1C, 0x5]], # Climb       0x20
    0xBC0008: [[0x1F1C, 0x1]], # Yoshi       0x02
    0xBC0009: [[0x1F1C, 0x4]], # P-Switch    0x10
    #0xBC000A: [[]]
    0xBC000B: [[0x1F2D, 0x3]], # P-Balloon   0x08
    0xBC000D: [[0x1F2D, 0x4]]  # Super Star  0x10
}

icon_rom_data = {
    0xBC0002: [0x1B00C], # Yoshi Egg
    0xBC0012: [0x1B00E], # Boss Token

    0xBC0017: [0x1B004], # 1 coin
    0xBC0018: [0x1B006], # 5 coins
    0xBC0019: [0x1B008], # 10 coins
    0xBC001A: [0x1B00A], # 50 coins

    0xBC0001: [0x1B010]  # 1-Up Mushroom
}
    
item_rom_data = {
    0xBC000E: [0x1F28, 0x1,  0x1C], # Yellow Switch Palace
    0xBC000F: [0x1F27, 0x1,  0x1C], # Green Switch Palace
    0xBC0010: [0x1F2A, 0x1,  0x1C], # Red Switch Palace
    0xBC0011: [0x1F29, 0x1,  0x1C], # Blue Switch Palace
    0xBC001B: [0x1F1E, 0x80, 0x39]  # Special Zone Clear
}

trap_rom_data = {
    0xBC0013: [0x0086, 0x1, 0x0E],  # Ice Trap
    0xBC0014: [0x18BD, 0x7F, 0x18], # Stun Trap
    0xBC0016: [0x0F31, 0x1],        # Timer Trap
    0xBC001C: [0x18B4, 0x1, 0x44],  # Reverse controls trap
    0xBC001D: [0x18B7, 0x1],        # Thwimp Trap
}


class SMWDeltaPatch(APDeltaPatch):
    hash = USHASH
    game = "Super Mario World"
    patch_file_ending = ".apsmw"

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


class LocalRom:

    def __init__(self, file, patch=True, vanillaRom=None, name=None, hash=None):
        self.name = name
        self.hash = hash
        self.orig_buffer = None

        with open(file, 'rb') as stream:
            self.buffer = Utils.read_snes_rom(stream)
        
    def read_bit(self, address: int, bit_number: int) -> bool:
        bitflag = (1 << bit_number)
        return ((self.buffer[address] & bitflag) != 0)

    def read_byte(self, address: int) -> int:
        return self.buffer[address]

    def read_bytes(self, startaddress: int, length: int) -> bytearray:
        return self.buffer[startaddress:startaddress + length]

    def write_byte(self, address: int, value: int):
        self.buffer[address] = value

    def write_bytes(self, startaddress: int, values):
        self.buffer[startaddress:startaddress + len(values)] = values

    def write_to_file(self, file):
        with open(file, 'wb') as outfile:
            outfile.write(self.buffer)

    def read_from_file(self, file):
        with open(file, 'rb') as stream:
            self.buffer = bytearray(stream.read())

    def apply_patch(self, patch: bytes):
        self.buffer = bytearray(bsdiff4.patch(bytes(self.buffer), patch))

    def write_crc(self):
        crc = (sum(self.buffer[:0x7FDC] + self.buffer[0x7FE0:]) + 0x01FE) & 0xFFFF
        inv = crc ^ 0xFFFF
        self.write_bytes(0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])


def handle_level_shuffle(rom, active_level_dict):
    for level_id, level_data in level_info_dict.items():
        if level_id not in active_level_dict.keys():
            continue

        tile_id = active_level_dict[level_id]
        tile_data = level_info_dict[tile_id]

        if level_id > 0x80:
            level_id = level_id - 0x50

        rom.write_byte(tile_data.levelIDAddress, level_id)
        rom.write_byte(0x2D608 + level_id, tile_data.eventIDValue)

    for level_id, tile_id in active_level_dict.items():
        rom.write_byte(0x37F70 + level_id, tile_id)
        rom.write_byte(0x37F00 + tile_id, level_id)

def read_graphics_file(filename):
    return get_data(__name__, f"data/graphics/{filename}")

def handle_uncompressed_player_gfx(rom):
    # Decompresses and moves into a expanded region the player, yoshi and animated graphics
    # This should make swapping the graphics a lot easier.
    # Maybe I should look into making a 32x32 version at some point...
    # It also moves some 8x8 tiles in GFX00, thus making some free space for indicators and other stuff
    # in VRAM during gameplay, will come super handy later.
    # 
    # FOR FUTURE REFERENCE
    # Player graphics are now located at 0xE0000
    # Player auxiliary tiles are now located at 0xE6000
    # Yoshi graphics are now located at 0xE8800
    SMW_COMPRESSED_PLAYER_GFX = 0x40000
    SMW_COMPRESSED_ANIMATED_GFX = 0x43FC0
    SMW_COMPRESSED_GFX_00 = 0x459F9
    SMW_COMPRESSED_GFX_10 = 0x4EF1E
    SMW_COMPRESSED_GFX_28 = 0x5C06C
    compressed_player_gfx = rom.read_bytes(SMW_COMPRESSED_PLAYER_GFX, 0x3FC0)
    compressed_animated_gfx = rom.read_bytes(SMW_COMPRESSED_ANIMATED_GFX, 0x1A39)
    compressed_gfx_00 = rom.read_bytes(SMW_COMPRESSED_GFX_00, 0x0838)
    compressed_gfx_10 = rom.read_bytes(SMW_COMPRESSED_GFX_10, 0x0891)
    compressed_gfx_28 = rom.read_bytes(SMW_COMPRESSED_GFX_28, 0x0637)
    decompressed_player_gfx = decompress_gfx(compressed_player_gfx)
    decompressed_animated_gfx = convert_3bpp(decompress_gfx(compressed_animated_gfx))
    decompressed_gfx_00 = convert_3bpp(decompress_gfx(compressed_gfx_00))
    decompressed_gfx_10 = convert_3bpp(decompress_gfx(compressed_gfx_10))
    decompressed_gfx_28 = decompress_gfx(compressed_gfx_28)

    # Copy berry tiles
    order = [0x26C, 0x26D, 0x26E, 0x26F,
             0x27C, 0x27D, 0x27E, 0x27F,
             0x2E0, 0x2E1, 0x2E2, 0x2E3,
             0x2E4, 0x2E5, 0x2E6, 0x2E7]
    decompressed_animated_gfx += copy_gfx_tiles(decompressed_player_gfx, order, [5, 32])

    # Copy Mario's auxiliary tiles
    order = [0x80, 0x91, 0x81, 0x90, 0x82, 0x83]
    decompressed_gfx_00 += copy_gfx_tiles(decompressed_player_gfx, order, [5, 32])
    order = [0x69, 0x69, 0x0C, 0x69, 0x1A, 0x1B, 0x0D, 0x69, 0x22, 0x23, 0x32, 0x33, 0x0A, 0x0B, 0x20, 0x21,
             0x30, 0x31, 0x7E, 0x69, 0x80, 0x4A, 0x81, 0x5B, 0x82, 0x4B, 0x83, 0x5A, 0x84, 0x69, 0x85, 0x85]
    player_small_tiles = copy_gfx_tiles(decompressed_gfx_00, order, [5, 32])

    # Copy OW mario tiles
    order = [0x06, 0x07, 0x16, 0x17,
             0x08, 0x09, 0x18, 0x19,
             0x0A, 0x0B, 0x1A, 0x1B,
             0x0C, 0x0D, 0x1C, 0x1D,
             0x0E, 0x0F, 0x1E, 0x1F,
             0x20, 0x21, 0x30, 0x31,
             0x24, 0x25, 0x34, 0x35,
             0x46, 0x47, 0x56, 0x57,
             0x64, 0x65, 0x74, 0x75,
             0x66, 0x67, 0x76, 0x77,
             0x2E, 0x2F, 0x3E, 0x3F,
             0x40, 0x41, 0x50, 0x51,
             0x42, 0x43, 0x52, 0x53]
    player_map_tiles = copy_gfx_tiles(decompressed_gfx_10, order, [5, 32])

    # Copy HUD mario tiles
    order = [0x30, 0x31, 0x32, 0x33, 0x34]
    player_name_tiles = copy_gfx_tiles(decompressed_gfx_28, order, [4, 16])

    rom.write_bytes(0xE0000, decompressed_player_gfx)
    rom.write_bytes(0xE8000, decompressed_animated_gfx)
    rom.write_bytes(0xE6000, player_small_tiles)
    rom.write_bytes(0xE6400, player_map_tiles)
    rom.write_bytes(0xE6C00, player_name_tiles)

def decompress_gfx(compressed_graphics):
    # This code decompresses graphics in LC_LZ2 format in order to be able to swap player and yoshi's graphics with ease.
    decompressed_gfx = bytearray([])
    i = 0
    while True:
        cmd = compressed_graphics[i]
        i += 1
        if cmd == 0xFF:
            break
        else:
            if (cmd >> 5) == 0x07:
                size = ((cmd & 0x03) << 8) + compressed_graphics[i] + 1
                cmd = (cmd & 0x1C) >> 2
                i += 1
            else:
                size = (cmd & 0x1F) + 1
                cmd = cmd >> 5
            if cmd == 0x00:
                decompressed_gfx += bytearray([compressed_graphics[i+j] for j in range(size)])
                i += size
            elif cmd == 0x01:
                byte_fill = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([byte_fill for j in range(size)])
            elif cmd == 0x02:
                byte_fill_1 = compressed_graphics[i]
                i += 1
                byte_fill_2 = compressed_graphics[i]
                i += 1
                for j in range(size):
                    if (j & 0x1) == 0x00:
                        decompressed_gfx += bytearray([byte_fill_1])
                    else:
                        decompressed_gfx += bytearray([byte_fill_2])
            elif cmd == 0x03:
                byte_read = compressed_graphics[i]
                i += 1
                decompressed_gfx += bytearray([(byte_read + j) for j in range(size)])
            elif cmd == 0x04:
                position = (compressed_graphics[i] << 8) + compressed_graphics[i+1]
                i += 2
                for j in range(size):
                    copy_byte = decompressed_gfx[position+j]
                    decompressed_gfx += bytearray([copy_byte])
    return decompressed_gfx


def convert_3bpp(decompressed_gfx):
    i = 0
    converted_gfx = bytearray([])
    while i < len(decompressed_gfx):
        converted_gfx += bytearray([decompressed_gfx[i+j] for j in range(16)])
        i += 16
        for j in range(8):
            converted_gfx += bytearray([decompressed_gfx[i]])
            converted_gfx += bytearray([0x00])
            i += 1
    return converted_gfx


def copy_gfx_tiles(original, order, size):
    result = bytearray([])
    for x in range(len(order)):
        z = order[x] << size[0]
        result += bytearray([original[z+y] for y in range(size[1])])
    return result


def handle_location_item_info(rom, world: World):
    from .Levels import location_id_to_level_id

    block_info = bytearray([0x00 for _ in range(582)])
    normal_exit_info = bytearray([0x00 for _ in range(96)])
    secret_exit_info = bytearray([0x00 for _ in range(96)])
    bonus_block_info = bytearray([0x00 for _ in range(96)])
    moon_info = bytearray([0x00 for _ in range(96)])
    dragon_coin_info = bytearray([0x00 for _ in range(96)])
    hidden_1up_info = bytearray([0x00 for _ in range(96)])
    locations = world.multiworld.get_filled_locations(world.player)
    for location in locations:
        if "Normal Exit" in location.name:
            normal_exit_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif "Secret Exit" in location.name:
            secret_exit_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif "Dragon Coins" in location.name:
            dragon_coin_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif "3-Up Moon" in location.name:
            moon_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif "Hidden 1-Up" in location.name:
            hidden_1up_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif "1-Up from Bonus Block" in location.name:
            bonus_block_info[location_id_to_level_id[location.name][0]] = (location.item.classification & 0x07) * 2
        elif location.address > 0xBC0600:
            block_info[location.address - 0xBC0600] = (location.item.classification & 0x07) * 2

    rom.write_bytes(0x8850D, normal_exit_info)
    rom.write_bytes(0x8856D, secret_exit_info)
    rom.write_bytes(0x8844D, dragon_coin_info)
    rom.write_bytes(0x884AD, moon_info)
    rom.write_bytes(0x8862D, hidden_1up_info)
    rom.write_bytes(0x885CD, bonus_block_info)
    rom.write_bytes(0x88207, block_info)


def file_to_bytes(filename):  
    return open(os.path.dirname(__file__)+filename, "rb").read()
   

def handle_music_shuffle(rom, world: World):
    from .Aesthetics import generate_shuffled_level_music, generate_shuffled_ow_music, level_music_address_data, ow_music_address_data

    shuffled_level_music = generate_shuffled_level_music(world)
    for i in range(len(shuffled_level_music)):
        rom.write_byte(level_music_address_data[i], shuffled_level_music[i])

    shuffled_ow_music = generate_shuffled_ow_music(world)
    for i in range(len(shuffled_ow_music)):
        for addr in ow_music_address_data[i]:
            rom.write_byte(addr, shuffled_ow_music[i])


def handle_mario_palette(rom, world: World):
    from .Aesthetics import mario_palettes, fire_mario_palettes, ow_mario_palettes

    chosen_palette = world.options.mario_palette.value

    rom.write_bytes(0x32C8, bytes(mario_palettes[chosen_palette]))
    rom.write_bytes(0x32F0, bytes(fire_mario_palettes[chosen_palette]))
    rom.write_bytes(0x359C, bytes(ow_mario_palettes[chosen_palette]))


def handle_swap_donut_gh_exits(rom):
    rom.write_bytes(0x2567C, bytes([0xC0]))
    rom.write_bytes(0x25873, bytes([0xA9]))
    rom.write_bytes(0x25875, bytes([0x85]))
    rom.write_bytes(0x25954, bytes([0x92]))
    rom.write_bytes(0x25956, bytes([0x0A]))
    rom.write_bytes(0x25E31, bytes([0x00, 0x00, 0xD8, 0x04, 0x24, 0x00, 0x98, 0x04, 0x48, 0x00, 0xD8, 0x03, 0x6C, 0x00, 0x56, 0x03,
                                    0x90, 0x00, 0x56, 0x03, 0xB4, 0x00, 0x56, 0x03, 0x10, 0x05, 0x18, 0x05, 0x28, 0x09, 0x24, 0x05,
                                    0x38, 0x0B, 0x14, 0x07, 0xEC, 0x09, 0x12, 0x05, 0xF0, 0x09, 0xD2, 0x04, 0xF4, 0x09, 0x92, 0x04]))
    rom.write_bytes(0x26371, bytes([0x32]))


def handle_bowser_rooms(rom, world: World):
    if world.options.bowser_castle_rooms == "random_two_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 2)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "random_five_room":
        chosen_rooms = world.random.sample(standard_bowser_rooms, 5)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)

    elif world.options.bowser_castle_rooms == "gauntlet":
        chosen_rooms = standard_bowser_rooms.copy()
        world.random.shuffle(chosen_rooms)

        rom.write_byte(0x3A680, chosen_rooms[0].roomID)
        rom.write_byte(0x3A684, chosen_rooms[0].roomID)
        rom.write_byte(0x3A688, chosen_rooms[0].roomID)
        rom.write_byte(0x3A68C, chosen_rooms[0].roomID)

        for i in range(1, len(chosen_rooms)):
            rom.write_byte(chosen_rooms[i-1].exitAddress, chosen_rooms[i].roomID)

        rom.write_byte(chosen_rooms[len(chosen_rooms)-1].exitAddress, 0xBD)
    elif world.options.bowser_castle_rooms == "labyrinth":
        bowser_rooms_copy = full_bowser_rooms.copy()

        entrance_point = bowser_rooms_copy.pop(0)

        world.random.shuffle(bowser_rooms_copy)

        rom.write_byte(entrance_point.exitAddress, bowser_rooms_copy[0].roomID)
        for i in range(0, len(bowser_rooms_copy) - 1):
            rom.write_byte(bowser_rooms_copy[i].exitAddress, bowser_rooms_copy[i+1].roomID)

        rom.write_byte(bowser_rooms_copy[len(bowser_rooms_copy)-1].exitAddress, 0xBD)


def handle_boss_shuffle(rom, world: World):
    if world.options.boss_shuffle == "simple":
        submap_boss_rooms_copy = submap_boss_rooms.copy()
        ow_boss_rooms_copy = ow_boss_rooms.copy()

        world.random.shuffle(submap_boss_rooms_copy)
        world.random.shuffle(ow_boss_rooms_copy)

        for i in range(len(submap_boss_rooms_copy)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, submap_boss_rooms_copy[i].roomID)

        for i in range(len(ow_boss_rooms_copy)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, ow_boss_rooms_copy[i].roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, ow_boss_rooms_copy[i].roomID)

    elif world.options.boss_shuffle == "full":
        for i in range(len(submap_boss_rooms)):
            chosen_boss = world.random.choice(submap_boss_rooms)
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            chosen_boss = world.random.choice(ow_boss_rooms)
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_boss.roomID)

    elif world.options.boss_shuffle == "singularity":
        chosen_submap_boss = world.random.choice(submap_boss_rooms)
        chosen_ow_boss = world.random.choice(ow_boss_rooms)

        for i in range(len(submap_boss_rooms)):
            rom.write_byte(submap_boss_rooms[i].exitAddress, chosen_submap_boss.roomID)

        for i in range(len(ow_boss_rooms)):
            rom.write_byte(ow_boss_rooms[i].exitAddress, chosen_ow_boss.roomID)

            if ow_boss_rooms[i].exitAddressAlt is not None:
                rom.write_byte(ow_boss_rooms[i].exitAddressAlt, chosen_ow_boss.roomID)


def patch_rom(world: World, rom, player, active_level_dict):
    # Apply base patch
    rom.apply_patch(get_data(__name__, os.path.join("data", "smw_basepatch.bsdiff4")))

    goal_text = generate_goal_text(world)

    rom.write_bytes(0x2A6E2, goal_text)

    intro_text = generate_text_box("Bowser has stolen all of Mario's abilities. Can you help Mario travel across Dinosaur land to get them back and save the Princess from him?")
    rom.write_bytes(0x2A5D9, intro_text)

    handle_bowser_rooms(rom, world)
    handle_boss_shuffle(rom, world)

    # Title Screen Text
    player_name_bytes = bytearray()
    player_name = world.multiworld.get_player_name(player)
    for i in range(16):
        char = " "
        if i < len(player_name):
            char = player_name[i]
        upper_char = char.upper()
        if upper_char not in title_text_mapping:
            for byte in title_text_mapping["."]:
                player_name_bytes.append(byte)
        else:
            for byte in title_text_mapping[upper_char]:
                player_name_bytes.append(byte)

    rom.write_bytes(0x2B7F1, player_name_bytes) # MARIO A
    rom.write_bytes(0x2B726, player_name_bytes) # MARIO A

    # Always bring up save prompt on beating a level
    if world.options.autosave:
        rom.write_bytes(0x20F93, bytearray([0x00]))

    if world.options.overworld_speed == "fast":
        rom.write_bytes(0x21414, bytearray([0x20, 0x10]))
    elif world.options.overworld_speed == "slow":
        rom.write_bytes(0x21414, bytearray([0x05, 0x05]))

    # Starting Life Count
    rom.write_bytes(0x1E25, bytearray([world.options.starting_life_count.value - 1]))

    handle_uncompressed_player_gfx(rom)

    # Handle Level Shuffle
    handle_level_shuffle(rom, active_level_dict)

    # Handle Music Shuffle
    if world.options.music_shuffle != "none":
        handle_music_shuffle(rom, world)

    generate_shuffled_ow_palettes(rom, world)

    generate_shuffled_header_data(rom, world)

    if world.options.level_palette_shuffle == "on_curated":
        generate_curated_level_palette_data(rom, world)

        # Fix bush filler tiles
        BUSH_FILLER_ADDR = 0x68248
        rom.write_byte(BUSH_FILLER_ADDR + 0x01, 0x04)
        rom.write_byte(BUSH_FILLER_ADDR + 0x03, 0x04)
        rom.write_byte(BUSH_FILLER_ADDR + 0x05, 0x04)
        rom.write_byte(BUSH_FILLER_ADDR + 0x07, 0x04)

    if world.options.overworld_palette_shuffle == "on_curated":
        generate_curated_map_palette_data(rom, world)
    
    if world.options.sfx_shuffle != "none":
        generate_shuffled_sfx(rom, world)
    
    if world.options.swap_donut_gh_exits:
        handle_swap_donut_gh_exits(rom)

    handle_mario_palette(rom, world)

    handle_location_item_info(rom, world)

    # Store all relevant option results in ROM
    rom.write_byte(0x01BFA0, world.options.goal.value)
    if world.options.goal.value == 0:
        rom.write_byte(0x01BFA1, world.options.bosses_required.value)
    else:
        rom.write_byte(0x01BFA1, 0x7F)
    required_yoshi_eggs = world.required_egg_count
    rom.write_byte(0x01BFA2, required_yoshi_eggs)
    #rom.write_byte(0x01BFA3, world.options.display_sent_item_popups.value)
    rom.write_byte(0x01BFA4, world.options.display_received_item_popups.value)
    rom.write_byte(0x01BFA5, world.options.death_link.value)
    rom.write_byte(0x01BFA6, world.options.dragon_coin_checks.value)
    rom.write_byte(0x01BFA7, world.options.swap_donut_gh_exits.value)
    rom.write_byte(0x01BFA8, world.options.moon_checks.value)
    rom.write_byte(0x01BFA9, world.options.hidden_1up_checks.value)
    rom.write_byte(0x01BFAA, world.options.bonus_block_checks.value)
    rom.write_byte(0x01BFAB, world.options.blocksanity.value)
    rom.write_byte(0x01BFAC, world.options.level_palette_shuffle.value)
    rom.write_byte(0x01BFAD, world.options.overworld_palette_shuffle.value)
    rom.write_byte(0x01BFB0, world.options.level_shuffle.value)
    rom.write_byte(0x01BFB1, world.options.block_collect_behavior.value)
    setting_value = 0
    location_visual_indicator = world.options.location_visual_indicator.value
    if "Exits" in location_visual_indicator:
        setting_value |= 0x01
    if "Dragon Coins" in location_visual_indicator:
        setting_value |= 0x02
    if "Moons" in location_visual_indicator:
        setting_value |= 0x04
    if "Bonus Blocks" in location_visual_indicator:
        setting_value |= 0x08
    if "Blocksanity" in location_visual_indicator:
        setting_value |= 0x10
    rom.write_byte(0x01BFB2, setting_value)

    from Utils import __version__
    rom.name = bytearray(f'SMW{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', 'utf8')[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x7FC0, rom.name)

    rom.write_crc()

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if USHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options = Utils.get_options()
    if not file_name:
        file_name = options["smw_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
