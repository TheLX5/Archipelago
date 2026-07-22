import logging
import asyncio
import time
from enum import Enum

from Utils import get_unique_identifier
from NetUtils import ClientStatus, color, NetworkItem
from worlds.AutoSNIClient import SNIClient, SnesReader, SnesData, Read

from .constants import *

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from SNIClient import SNIContext

logger = logging.getLogger("Client")
snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
SRAM_START = 0xE00000 

MMX2_WRAM = WRAM_START + 0x1F800
MMX2_SRAM = SRAM_START

MMX2_GAME_STATE         = WRAM_START + 0x000D0
MMX2_MENU_STATE         = WRAM_START + 0x000D1
MMX2_GAMEPLAY_STATE     = WRAM_START + 0x000D2
MMX2_PAUSE_STATE        = WRAM_START + 0x01F37
MMX2_SCREEN_BRIGHTNESS  = WRAM_START + 0x000B4
MMX2_LEVEL_INDEX        = WRAM_START + 0x01FAD
MMX2_CURRENT_HP         = WRAM_START + 0x009FF
MMX2_CAN_MOVE           = WRAM_START + 0x01F25
MMX2_ON_RIDE_ARMOR      = WRAM_START + 0x00A54

MMX2_ENABLE_HEART_TANK      = MMX2_SRAM + 0x00009
MMX2_ENABLE_HP_REFILL       = MMX2_SRAM + 0x0000D
MMX2_HP_REFILL_AMOUNT       = MMX2_SRAM + 0x0000E
MMX2_ENABLE_GIVE_1UP        = MMX2_SRAM + 0x00010
MMX2_ENABLE_WEAPON_REFILL   = MMX2_SRAM + 0x00017
MMX2_WEAPON_REFILL_AMOUNT   = MMX2_SRAM + 0x00018
MMX2_RECEIVING_ITEM         = MMX2_SRAM + 0x00008
MMX2_UNLOCKED_CHARGED_SHOT  = MMX2_SRAM + 0x00013
MMX2_UNLOCKED_CHECKPOINTS   = MMX2_SRAM + 0x00016
MMX2_ENERGY_LINK_COUNT      = MMX2_SRAM + 0x0001F
MMX2_GLOBAL_TIMER           = MMX2_SRAM + 0x00025
MMX2_GLOBAL_DEATHS          = MMX2_SRAM + 0x00029
MMX2_GLOBAL_DMG_DEALT       = MMX2_SRAM + 0x0002B
MMX2_GLOBAL_DMG_TAKEN       = MMX2_SRAM + 0x0002D
MMX2_REFILL_REQUEST         = MMX2_SRAM + 0x0002F
MMX2_REFILL_TARGET          = MMX2_SRAM + 0x00030

MMX2_SFX_FLAG   = MMX2_SRAM + 0x00003
MMX2_SFX_NUMBER = MMX2_SRAM + 0x00004

MMX2_VALIDATION_CHECK = WRAM_START + 0x1F800 + 0x00011

MMX2_LEVEL_CLEARED          = MMX2_SRAM + 0x220
MMX2_DEFEATED_BOSSES        = MMX2_SRAM + 0x240

EXCHANGE_RATE = 500000000

MMX2_RECV_INDEX = MMX2_SRAM + 0x00000
MMX2_ENERGY_LINK_PACKET     = MMX2_SRAM + 0x006
MMX2_DAMAGE_PACKET = MMX2_SRAM + 0x0160
MMX2_DAMAGE_TRAP = MMX2_SRAM + 0x0161

VALID_ACTIONS = [0x00, 0x02, 0x04, 0x06, 0x08, 0x0A, 0x10, 0x12, 0x14, 0x20, 0x24, 0x2A, 0x54, 0x56]

class MMX2Memory(Enum):
    settings = Read(ROM_START + 0x17FFE0, 0x20)
    validation = Read(MMX2_SRAM + 0x11, 0x02)
    received_index = Read(MMX2_SRAM + 0x0000, 0x02)
    victory = Read(MMX2_SRAM + 0x0005, 0x01)
    item_queue = Read(MMX2_SRAM + 0x1000, 0x0FFF)
    item_queue_index = Read(MMX2_SRAM + 0x01C0, 0x02)
    item_queue_target_index = Read(MMX2_SRAM + 0x01C2, 0x02)
    ram_mirror = Read(MMX2_SRAM + 0x100, 0x80)
    defeated_bosses = Read(MMX2_SRAM + 0x240, 0x20)
    levels_completed = Read(MMX2_SRAM + 0x220, 0x20)
    pickups = Read(MMX2_SRAM + 0x260, 0x50)
    collected_locations = Read(MMX2_SRAM + 0x040, 0x08)
    receiving_item = Read(MMX2_SRAM + 0x08, 0x01)
    energy_link_packet = Read(MMX2_ENERGY_LINK_PACKET, 0x02)
    refill_request = Read(MMX2_SRAM + 0x2F, 0x01)
    refill_target = Read(MMX2_SRAM + 0x30, 0x01)
    hp_refill = Read(MMX2_SRAM + 0x00D, 0x01)
    weapon_refill = Read(MMX2_SRAM + 0x017, 0x01)
    hp_tank = Read(MMX2_SRAM + 0x009, 0x01)
    current_hp = Read(MMX2_CURRENT_HP, 0x01)
    damage_packet = Read(MMX2_SRAM + 0x0160, 1)
    damage_trap = Read(MMX2_SRAM + 0x0161, 1)

class ConnectMemory(Enum):
    settings = Read(ROM_START + 0x17FFE0, 0x20)
    rom_name = Read(ROM_START + 0x7FC0, 0x15)
    validation = Read(MMX2_SRAM + 0x11, 0x02)

class MMX2SNIClient(SNIClient):
    game = GAME_NAME
    patch_suffix = ".apmmx2"
    slot_data: dict[str, Any]
    snes_reader = SnesReader(MMX2Memory)
    connect_reader = SnesReader(ConnectMemory)

    def __init__(self):
        super().__init__()
        self.game_state = False
        self.last_death_link = 0
        self.heal_request_command = None
        self.weapon_refill_request_command = None
        self.trade_request = None
        self.data_storage_enabled = False
        self.current_level_value = 42
        self.item_queue = []
        self.current_shared_damage = 0
        self.incoming_shared_damage = 0
        self.shared_damage_label = None
        self.shared_damage_message = ""

    async def validate_rom(self, ctx):
        snes_data = await self.connect_reader.read(ctx)
        if snes_data is None:
            return False

        rom_name = snes_data.get(ConnectMemory.rom_name)
        settings = snes_data.get(ConnectMemory.settings)

        #expected_version = str(rom_name[4:10])
        #world_version = f"{MMX2World.world_version.major:02}{MMX2World.world_version.minor:02}{MMX2World.world_version.build:02}"
        if rom_name == bytes([0] * 0x15) or rom_name[:3] != b"LX2": # or expected_version != world_version:
            if "heal" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("heal")
            if "refill" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("refill")
            if "trade" in ctx.command_processor.commands:
                ctx.command_processor.commands.pop("trade")
            return False
        
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.receive_option = 0
        ctx.send_option = 0
        ctx.allow_collect = True

        if bool(settings[0x05] & 0b1) and "EnergyLink" not in ctx.tags:
            ctx.tags.add("EnergyLink")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["heal"] = cmd_heal
            if "refill" not in ctx.command_processor.commands:
                ctx.command_processor.commands["refill"] = cmd_refill

        if settings[0x07] and "SharedDamage" not in ctx.tags:
            ctx.tags.add("SharedDamage")
            await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        if settings[0x06]:
            await ctx.update_death_link(True)

        if "trade" not in ctx.command_processor.commands:
            ctx.command_processor.commands["trade"] = cmd_trade

        ctx.rom = rom_name

        return True
    #Crystal Snail - HP Pickup 2 (After X-Hunter room)

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            ctx.slot_data = args.get("slot_data", None)
            if ctx.slot_data["energy_link"]:
                ctx.set_notify(f"EnergyLink{ctx.team}")
                if ctx.ui:
                    ctx.ui.enable_energy_link()
                    ctx.ui.energy_link_label.text = "Energy: Standby"
                    logger.info(f"Initialized EnergyLink, use /help to get information about the EnergyLink commands.")

        elif cmd == "SetReply" and args["key"].startswith("EnergyLink"):
            if ctx.ui:
                pool = (args["value"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"

        elif cmd == "Retrieved":
            if f"EnergyLink{ctx.team}" in args["keys"] and args["keys"][f"EnergyLink{ctx.team}"] and ctx.ui:
                pool = (args["keys"][f"EnergyLink{ctx.team}"] or 0) / EXCHANGE_RATE
                ctx.ui.energy_link_label.text = f"Energy: {pool:.2f}"

        elif cmd == "Bounced":
            if ctx.slot_data is None and "tags" not in args:
                return 
            
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()

            if "data" not in args:
                return

            if "SharedDamage" in ctx.tags and "SharedDamage" in args["tags"]:
                if "uuid" in args["data"]:
                    uuid = args["data"]["uuid"]
                else:
                    uuid = "lmao"
                source_name = args["data"]["source"]
                if uuid != get_unique_identifier() or source_name != ctx.player_names[ctx.slot]:
                    damage_amount = args["data"]["damage_points"]
                    self.incoming_shared_damage += damage_amount
                    self.shared_damage_message = f"Received {damage_amount} damage points from {source_name}"


    async def game_watcher(self, ctx: "SNIContext"):
        if ctx.server is None:
            return
        
        from SNIClient import snes_buffered_write, snes_flush_writes

        snes_data = await self.snes_reader.read(ctx)
        if snes_data is None:
            self.game_state = False
            self.current_level_value = 42
            self.item_queue = []
            return
        
        settings = snes_data.get(MMX2Memory.settings)
        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)
    
        validation = int.from_bytes(snes_data.get(MMX2Memory.validation), "little")
        if validation != 0xDEAD:
            self.game_state = False
            return
        
        game_state = ram_mirror[0x00]
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]

        if game_state == 0:
            self.game_state = False
            self.current_level_value = 42
            ctx.locations_checked = set()
            self.item_queue = []
        else:
            self.game_state = True
        
        if not self.game_state:
            return

        if self.trade_request is not None:
            await self.handle_hp_trade(ctx, snes_data)

        if "EnergyLink" in ctx.tags:
            await self.handle_energy_link(ctx, snes_data)

        if "SharedDamage" in ctx.tags:
            await self.handle_incoming_shared_damage(ctx, snes_data)
            await self.handle_sent_shared_damage(ctx, snes_data)

        if "DeathLink" in ctx.tags and menu_state == 0x04 and ctx.last_death_link + 1 < time.time():
            currently_dead = gameplay_state == 0x06
            await ctx.handle_deathlink_state(currently_dead)

        await self.handle_item_queue(ctx, snes_data)

        collected_locations = list(snes_data.get(MMX2Memory.collected_locations))
        defeated_bosses = list(snes_data.get(MMX2Memory.defeated_bosses))
        cleared_levels = list(snes_data.get(MMX2Memory.levels_completed))
        collected_heart_tanks_data = collected_locations[0x00]
        collected_upgrades_data = collected_locations[0x01]
        collected_shoryuken_data = collected_locations[0x02]
        collected_pickups_data = list(snes_data.get(MMX2Memory.pickups))
        collected_sigma_access = collected_locations[0x06]
        pickup_locations_enabled = settings[0x02]

        from .locations import all_locations
        for loc_name, loc_id in all_locations.items():
            game_type = loc_id & GAME_MASK
            if loc_id in ctx.locations_checked or game_type != X2:
                continue

            loc_type = loc_id & TYPE_MASK
            data = loc_id & DATA_MASK
            stage = loc_id & STAGE_MASK

            if loc_type == CLEAR:
                if stage == INTRO and game_state == 0x02 and menu_state == 0x00 and gameplay_state == 0x01:
                    ctx.locations_checked.add(loc_id)
                elif stage == BASE4 and collected_sigma_access:
                        ctx.locations_checked.add(loc_id)
                elif cleared_levels[data]:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == ENEMY:
                if defeated_bosses[data]:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == HEART:
                if collected_heart_tanks_data & data:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == UPGRADE:
                if collected_upgrades_data & data:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == SPECIAL:
                if collected_shoryuken_data:
                    ctx.locations_checked.add(loc_id)
            elif loc_type == PICKUP and pickup_locations_enabled:
                if collected_pickups_data[data]:
                    ctx.locations_checked.add(loc_id)

        await ctx.check_locations(ctx.locations_checked)

        # Goal check
        victory = int.from_bytes(snes_data.get(MMX2Memory.victory),"little")
        if not ctx.finished_game and victory == 0x42:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
   
        # Send Current Room for Tracker
        current_level = ram_mirror[0x05]

        if game_state == 0x00 or (game_state == 0x02 and menu_state != 0x04):
            current_level = -1

        if self.current_level_value != (current_level + 1):
            self.current_level_value = current_level + 1

            # Send level id data to tracker
            await ctx.send_msgs([
                    {
                        "cmd": "Set",
                        "key": f"mmx2_level_id_{ctx.team}_{ctx.slot}",
                        "default": 0, "want_reply": False,
                        "operations": [{"operation": "replace","value": self.current_level_value,}],
                    }
                ])

        recv_index = int.from_bytes(snes_data.get(MMX2Memory.received_index), "little")
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            sending_game = ctx.slot_info[item.player].game
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))
            
            snes_buffered_write(ctx, MMX2_RECV_INDEX, bytearray([recv_index]))
        
            if item.item == 0x1C:
                self.add_item_to_queue("hp refill", 0x02)
            elif item.item == 0x1D:
                self.add_item_to_queue("hp refill", 0x08)
            queue_target_index = int.from_bytes(snes_data.get(MMX2Memory.item_queue_target_index), "little")
            snes_buffered_write(ctx, MMX2_SRAM + 0x1000 + queue_target_index, bytearray([item.item]))
            queue_target_index += 1
            snes_buffered_write(ctx, MMX2_SRAM + 0x01C2, queue_target_index.to_bytes(2, "little"))

        # Handle collected locations
        new_boss_clears = False
        new_cleared_level = False
        new_heart_tank = False
        new_upgrade = False
        new_pickup = False
        new_shoryuken = False
        i = 0
        for loc_id in ctx.checked_locations:
            game_type = loc_id & GAME_MASK
            if loc_id in ctx.locations_checked or game_type != X2:
                continue
            ctx.locations_checked.add(loc_id)
            loc_name = ctx.location_names.lookup_in_game(loc_id)

            logging.info(f"Recovered checks ({i:03}): {loc_name}")
            i += 1

            loc_type = loc_id & TYPE_MASK
            data = loc_id & DATA_MASK
            stage = loc_id & STAGE_MASK

            if loc_type == CLEAR:
                if stage == BASE4:
                    snes_buffered_write(ctx, MMX2_SRAM + 0x046, bytearray([collected_sigma_access]))
                else:
                    cleared_levels[data] = 0xFF
                    new_cleared_level = True
            elif loc_type == ENEMY:
                defeated_bosses[data] = 1
                new_boss_clears = True
            elif loc_type == HEART:
                collected_heart_tanks_data |= data
                new_heart_tank = True
            elif loc_type == UPGRADE:
                collected_upgrades_data |= data
                new_upgrade = True
            elif loc_type == SPECIAL:
                collected_shoryuken_data = 0xFF
                new_shoryuken = True
            elif loc_type == PICKUP:
                collected_pickups_data[data] = 0x01
                new_pickup = True

        if new_cleared_level:
            snes_buffered_write(ctx, MMX2_LEVEL_CLEARED, bytearray(cleared_levels))
        if new_boss_clears:
            snes_buffered_write(ctx, MMX2_DEFEATED_BOSSES, bytearray(defeated_bosses))
        if new_pickup:
            snes_buffered_write(ctx, MMX2_SRAM + 0x260, bytearray(collected_pickups_data))
        if new_shoryuken:
            snes_buffered_write(ctx, MMX2_SRAM + 0x042, bytearray([collected_shoryuken_data]))
        if new_upgrade:
            snes_buffered_write(ctx, MMX2_SRAM + 0x041, bytearray([collected_upgrades_data]))
        if new_heart_tank:
            snes_buffered_write(ctx, MMX2_SRAM + 0x040, bytearray([collected_heart_tanks_data]))

        await snes_flush_writes(ctx)


    def add_item_to_queue(self, item_type, item_additional = None):
        if not hasattr(self, "item_queue"):
            self.item_queue = []
        self.item_queue.append([item_type, item_additional])


    async def handle_item_queue(self, ctx, snes_data: SnesData[MMX2Memory]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        if not hasattr(self, "item_queue") or len(self.item_queue) == 0:
            return
        
        # Do not give items if you can't move, are in pause state, not in the correct mode or not in gameplay state
        receiving_item = int.from_bytes(snes_data.get(MMX2Memory.receiving_item), "little")
        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]
        can_move = list(ram_mirror[0x30:0x36])
        hp_refill = int.from_bytes(snes_data.get(MMX2Memory.hp_refill), "little")
        weapon_refill = int.from_bytes(snes_data.get(MMX2Memory.weapon_refill), "little")
        giving_tank = int.from_bytes(snes_data.get(MMX2Memory.hp_tank), "little")
        on_ride_armor = ram_mirror[0x40]
        if menu_state != 0x04 or \
           gameplay_state != 0x04 or \
           hp_refill != 0x00 or \
           weapon_refill != 0x00 or \
           giving_tank != 0x00 or \
           on_ride_armor == 0x0A or \
           receiving_item != 0x00 or \
           any(can_move):
            return
        
        next_item = self.item_queue.pop(0)
    
        if "hp refill" in next_item[0]:
            max_hp = ram_mirror[0x0A]
            current_hp = ram_mirror[0x08]

            if current_hp < max_hp:
                snes_buffered_write(ctx, MMX2_ENABLE_HP_REFILL, bytearray([0x02]))
                snes_buffered_write(ctx, MMX2_HP_REFILL_AMOUNT, bytearray([next_item[1]]))
                snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))
            else:
                self.item_queue.append(next_item)

        elif next_item[0] == "weapon refill":
            snes_buffered_write(ctx, MMX2_ENABLE_WEAPON_REFILL, bytearray([0x02]))
            snes_buffered_write(ctx, MMX2_WEAPON_REFILL_AMOUNT, bytearray([next_item[1]]))
            snes_buffered_write(ctx, MMX2_RECEIVING_ITEM, bytearray([0x01]))

        await snes_flush_writes(ctx)


    async def handle_hp_trade(self, ctx: "SNIContext", snes_data: SnesData[MMX2Memory]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]
        pause_state = ram_mirror[0x03]
        screen_brightness = ram_mirror[0x04]
        can_move = list(ram_mirror[0x30:0x36])
        if menu_state != 0x04 or \
            gameplay_state != 0x04 or \
            pause_state == 0x00 or \
            screen_brightness != 0x0F or \
            any(can_move):
            return
        
        # Can trade HP -> WPN if HP is above 1
        current_hp = ram_mirror[0x08]
        if current_hp > 0x01:
            max_trade = current_hp - 1
            set_trade = self.trade_request if self.trade_request <= max_trade else max_trade
            self.add_item_to_queue("weapon refill", set_trade)
            new_hp = current_hp - set_trade
            snes_buffered_write(ctx, MMX2_CURRENT_HP, bytearray([new_hp]))
            await snes_flush_writes(ctx)
            self.trade_request = None
            logger.info(f"Traded {set_trade} HP for {set_trade} Weapon Energy.")
        else:
            logger.info("Couldn't process trade. HP is too low.")
        

    async def handle_energy_link(self, ctx, snes_data: SnesData[MMX2Memory]):
        from SNIClient import snes_buffered_write, snes_flush_writes

        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)

        # Deposit heals into the pool regardless of energy_link setting
        energy_packet = int.from_bytes(snes_data.get(MMX2Memory.energy_link_packet), "little")
        if energy_packet != 0:
            energy_packet = (energy_packet * EXCHANGE_RATE) >> 4
            await ctx.send_msgs([{
                "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                    [{"operation": "add", "value": energy_packet},
                    {"operation": "max", "value": 0}],
            }])
            snes_buffered_write(ctx, MMX2_ENERGY_LINK_PACKET, bytearray([0x00, 0x00]))
        
        # Expose EnergyLink to the ROM
        pause_state = ram_mirror[0x03]
        screen_brightness = ram_mirror[0x04]
        if pause_state != 0x00 or screen_brightness == 0x0F:
            pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
            total_energy = int(pool / EXCHANGE_RATE)
            if total_energy < 9999:
                snes_buffered_write(ctx, MMX2_ENERGY_LINK_COUNT, bytearray([total_energy & 0xFF, (total_energy >> 8) & 0xFF]))
            else:
                snes_buffered_write(ctx, MMX2_ENERGY_LINK_COUNT, bytearray([0x0F, 0x27]))

        receiving_item = int.from_bytes(snes_data.get(MMX2Memory.receiving_item), "little")
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]
        pause_state = ram_mirror[0x03]
        can_move = list(ram_mirror[0x30:0x36])
        on_ride_armor = ram_mirror[0x40]
        if menu_state != 0x04 or \
            gameplay_state != 0x04 or \
            pause_state == 0x00 or \
            on_ride_armor == 0x0A or \
            receiving_item != 0x00 or \
            any(can_move):
            return
        
        skip_hp = False
        skip_weapon = False

        pool = ctx.stored_data[f'EnergyLink{ctx.team}'] or 0
        if not skip_hp or not skip_weapon:
            # Handle in-game requests
            request = int.from_bytes(snes_data.get(MMX2Memory.refill_request), "little")
            target = int.from_bytes(snes_data.get(MMX2Memory.refill_target), "little")
            if request != 0:
                if target == 0:
                    if self.heal_request_command is None:
                        self.heal_request_command = request
                else: 
                    if self.weapon_refill_request_command is None:
                        self.weapon_refill_request_command = request
                snes_buffered_write(ctx, MMX2_REFILL_REQUEST, bytearray([0x00]))

        if not skip_hp:
            # Handle heal requests
            if self.heal_request_command:
                heal_needed = self.heal_request_command
                heal_needed_rate = heal_needed * EXCHANGE_RATE
                if pool < EXCHANGE_RATE:
                    logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                    self.heal_request_command = None
                    return
                elif pool < heal_needed_rate:
                    heal_needed = int(pool / EXCHANGE_RATE)
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                        [{"operation": "add", "value": -heal_needed_rate},
                        {"operation": "max", "value": 0}],
                }])
                self.add_item_to_queue("hp refill", heal_needed)
                pool = (pool / EXCHANGE_RATE) - heal_needed
                logger.info(f"Healed by {heal_needed}. Energy available: {pool:.2f}")
                self.heal_request_command = None

        if not skip_weapon:
            # Handle weapon refill requests
            if self.weapon_refill_request_command:
                heal_needed = self.weapon_refill_request_command
                heal_needed_rate = heal_needed * EXCHANGE_RATE
                if pool < EXCHANGE_RATE:
                    logger.info(f"There's not enough Energy for your request ({heal_needed}). Energy available: {pool / EXCHANGE_RATE:.2f}")
                    self.weapon_refill_request_command = None
                    return
                elif pool < heal_needed_rate:
                    heal_needed = int(pool / EXCHANGE_RATE)
                    heal_needed_rate = heal_needed * EXCHANGE_RATE
                await ctx.send_msgs([{
                    "cmd": "Set", "key": f"EnergyLink{ctx.team}", "operations":
                        [{"operation": "add", "value": -heal_needed_rate},
                        {"operation": "max", "value": 0}],
                }])
                self.add_item_to_queue("weapon refill", heal_needed)
                pool = (pool / EXCHANGE_RATE) - heal_needed
                logger.info(f"Refilled current weapon by {heal_needed}. Energy available: {pool:.2f}")
                self.weapon_refill_request_command = None

        await snes_flush_writes(ctx)


    async def handle_incoming_shared_damage(self, ctx, snes_data: SnesData[MMX2Memory]):
        from kvui import MDLabel as Label

        if not self.shared_damage_label:
            self.shared_damage_label = Label(text=f"", size_hint_x=None, width=120, halign="center")
            ctx.ui.connect_layout.add_widget(self.shared_damage_label)

        self.shared_damage_label.text = f"DMG: {self.current_shared_damage}"

        # Ignore incoming damage if you can't move, are in pause state, not in the correct mode or not in gameplay state
        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]
        player_action = ram_mirror[0x41]
        if menu_state != 0x04 or gameplay_state != 0x04 or player_action not in VALID_ACTIONS:
            self.incoming_shared_damage = 0
            return
        
        # We cap damage to 120 which is equal to 12 HP, other games could use other values
        if self.incoming_shared_damage:
            snes_logger.info(self.shared_damage_message)
            self.current_shared_damage += min(self.incoming_shared_damage, 120)
            self.incoming_shared_damage = 0
        
        # Delay damage signal in we're paused or something else
        can_move = list(ram_mirror[0x30:0x36])
        hp_refill = int.from_bytes(snes_data.get(MMX2Memory.hp_refill), "little")
        weapon_refill = int.from_bytes(snes_data.get(MMX2Memory.weapon_refill), "little")
        giving_tank = int.from_bytes(snes_data.get(MMX2Memory.hp_tank), "little")
        receiving_item = int.from_bytes(snes_data.get(MMX2Memory.receiving_item), "little")
        pause_state = ram_mirror[0x03]
        on_ride_armor = ram_mirror[0x40]
        if any(can_move) or \
           hp_refill != 0x00 or \
           pause_state != 0x00 or \
           weapon_refill != 0x00 or \
           on_ride_armor == 0x0A or \
           giving_tank != 0x00 or \
           receiving_item != 0x00:
            return
        
        if self.current_shared_damage >= 10:
            from SNIClient import snes_buffered_write, snes_flush_writes
            damage_amount = int(self.current_shared_damage / 10)
            snes_buffered_write(ctx, MMX2_DAMAGE_TRAP, bytearray([damage_amount]))
            await snes_flush_writes(ctx)

            snes_logger.info(f"Triggered DamageLink for {damage_amount} HP!")
            self.current_shared_damage = self.current_shared_damage % 10


    async def handle_sent_shared_damage(self, ctx, snes_data: SnesData[MMX2Memory]):
        damage_amount = int.from_bytes(snes_data.get(MMX2Memory.damage_packet), "little")
        if damage_amount != 0:
            await ctx.send_msgs([{
                "cmd": "Bounce", "tags": ["SharedDamage"],
                "data": {
                    "time": time.time(),
                    "uuid": get_unique_identifier(),
                    "source": ctx.player_names[ctx.slot],
                    "damage_points": damage_amount
                }
            }])
            snes_logger.info(f"Sent {damage_amount} damage points to players")

            from SNIClient import snes_buffered_write, snes_flush_writes
            snes_buffered_write(ctx, MMX2_DAMAGE_PACKET, bytearray([0x00]))
            await snes_flush_writes(ctx)


    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes

        snes_data = await self.snes_reader.read(ctx)
        if snes_data is None:
            return

        validation = int.from_bytes(snes_data.get(MMX2Memory.validation), "little")
        if validation != 0xDEAD:
            return
        
        receiving_item = int.from_bytes(snes_data.get(MMX2Memory.receiving_item), "little")
        ram_mirror = snes_data.get(MMX2Memory.ram_mirror)
        menu_state = ram_mirror[0x01]
        gameplay_state = ram_mirror[0x02]
        can_move = list(ram_mirror[0x30:0x36])
        hp_refill = int.from_bytes(snes_data.get(MMX2Memory.hp_refill), "little")
        weapon_refill = int.from_bytes(snes_data.get(MMX2Memory.weapon_refill), "little")
        giving_tank = int.from_bytes(snes_data.get(MMX2Memory.hp_tank), "little")
        pause_state = ram_mirror[0x03]
        screen_brightness = ram_mirror[0x04]
        on_ride_armor = ram_mirror[0x40]
        player_action = ram_mirror[0x41]
        if menu_state != 0x04 or \
           gameplay_state != 0x04 or \
           player_action not in VALID_ACTIONS or \
           hp_refill != 0x00 or \
           weapon_refill != 0x00 or \
           giving_tank != 0x00 or \
           on_ride_armor == 0x0A or \
           receiving_item != 0x00 or \
           pause_state != 0x00 or \
           any(can_move):
            print ()
            return
        
        snes_buffered_write(ctx, MMX2_SRAM + 0x0162, bytearray([0x01]))

        await snes_flush_writes(ctx)

        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


def cmd_heal(self, amount: str = ""):
    """
    Request healing from EnergyLink.
    """
    if self.ctx.game != GAME_NAME:
        logger.warning("This command can only be used while playing Mega Man X2")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.heal_request_command is not None:
            logger.info(f"You already placed a healing request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much HP you will recover.")
                return
            self.ctx.client_handler.heal_request_command = amount
            logger.info(f"Requested {amount} HP from the energy pool.")
        else:
            logger.info(f"You need to specify how much HP you will request.")


def cmd_refill(self, amount: str = ""):
    """
    Request weapon energy from EnergyLink.
    """
    if self.ctx.game != GAME_NAME:
        logger.warning("This command can only be used while playing Mega Man X2")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.weapon_refill_request_command is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.weapon_refill_request_command = amount
            logger.info(f"Requested {amount} Weapon Energy from the energy pool.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")


def cmd_trade(self, amount: str = ""):
    """
    Trades HP to Weapon Energy. 1:1 ratio.
    """
    if self.ctx.game != GAME_NAME:
        logger.warning("This command can only be used while playing Mega Man X2")
    if (not self.ctx.server) or self.ctx.server.socket.closed or not self.ctx.client_handler.game_state:
        logger.info(f"Must be connected to server and in game.")
    else:
        if self.ctx.client_handler.trade_request is not None:
            logger.info(f"You already placed a weapon refill request.")
            return
        if amount:
            try:
                amount = int(amount)
            except:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            if amount <= 0:
                logger.info(f"You need to specify how much Weapon Energy you will recover.")
                return
            self.ctx.client_handler.trade_request = amount
            logger.info(f"Set up trade for {amount} Weapon Energy. Pause the game to process the trade.")
        else:
            logger.info(f"You need to specify how much Weapon Energy you will request.")
