import logging
import struct
import typing
import time
from struct import pack

from NetUtils import ClientStatus, NetworkItem, color
from worlds.AutoSNIClient import SNIClient
from .Items import trap_value_to_name, trap_name_to_value
from .Rom import item_values

if typing.TYPE_CHECKING:
    from SNIClient import SNIContext

snes_logger = logging.getLogger("SNES")

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

YOSHISISLAND_ROMHASH_START = 0x007FC0
ROMHASH_SIZE = 0x15

ITEMQUEUE_HIGH = WRAM_START + 0x1465
ITEM_RECEIVED = WRAM_START + 0x1467
DEATH_RECEIVED = WRAM_START + 0x7E23B0
GAME_MODE = WRAM_START + 0x0118
YOSHI_STATE = SRAM_START + 0x00AC
DEATHLINK_ADDR = ROM_START + 0x06FC8C
DEATHMUSIC_FLAG = WRAM_START + 0x004F
DEATHFLAG = WRAM_START + 0x00DB
DEATHLINKRECV = WRAM_START + 0x00E0
GOALFLAG = WRAM_START + 0x14B6

VALID_GAME_STATES = [0x0F, 0x10, 0x2C]


trap_list = [
    0x302090,
    0x302091,
    0x302092,
    0x302093,
]

class YoshisIslandSNIClient(SNIClient):
    game = "Yoshi's Island"
    patch_suffix = ".apyi"

    def __init__(self):
        super().__init__()
        self.received_trap_link = None

    async def deathlink_kill_player(self, ctx: "SNIContext") -> None:
        from SNIClient import DeathState, snes_buffered_write, snes_flush_writes, snes_read
        game_state = await snes_read(ctx, GAME_MODE, 0x1)
        if game_state[0] != 0x0F:
            return

        yoshi_state = await snes_read(ctx, YOSHI_STATE, 0x1)
        if yoshi_state[0] != 0x00:
            return

        snes_buffered_write(ctx, WRAM_START + 0x026A, bytes([0x01]))
        snes_buffered_write(ctx, WRAM_START + 0x00E0, bytes([0x01]))
        await snes_flush_writes(ctx)
        ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()

    async def validate_rom(self, ctx: "SNIContext") -> bool:
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, YOSHISISLAND_ROMHASH_START, ROMHASH_SIZE)
        if rom_name is None or rom_name[:7] != b"YOSHIAP":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111  # remote items
        ctx.rom = rom_name

        death_link = await snes_read(ctx, DEATHLINK_ADDR, 1)
        if death_link[0] & 0x01:
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        if death_link[0] & 0x80:
            ctx.tags.add("TrapLink")

        await ctx.send_msgs([{"cmd": "ConnectUpdate", "tags": ctx.tags}])

        return True

    async def game_watcher(self, ctx: "SNIContext") -> None:
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read

        game_mode = await snes_read(ctx, GAME_MODE, 0x1)
        item_received = await snes_read(ctx, ITEM_RECEIVED, 0x1)
        game_music = await snes_read(ctx, DEATHMUSIC_FLAG, 0x1)
        goal_flag = await snes_read(ctx, GOALFLAG, 0x1)

        if "DeathLink" in ctx.tags and ctx.last_death_link + 1 < time.time():
            death_flag = await snes_read(ctx, DEATHFLAG, 0x1)
            deathlink_death = await snes_read(ctx, DEATHLINKRECV, 0x1)
            currently_dead = (game_music[0] == 0x07 or game_mode[0] == 0x12 or
                              (death_flag[0] == 0x00 and game_mode[0] == 0x11)) and deathlink_death[0] == 0x00
            await ctx.handle_deathlink_state(currently_dead)

        if game_mode is None:
            return

        elif game_mode[0] not in VALID_GAME_STATES:
            return
        elif item_received[0] > 0x00:
            return

        rom = await snes_read(ctx, YOSHISISLAND_ROMHASH_START, ROMHASH_SIZE)
        if rom != ctx.rom:
            ctx.rom = None
            return

        if goal_flag[0] != 0x00:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        if "TrapLink" in ctx.tags:
            await self.handle_trap_link(ctx)

        new_checks = []
        from .Rom import location_table

        location_ram_data = await snes_read(ctx, WRAM_START + 0x1440, 0x80)
        for loc_id, loc_data in location_table.items():
            if loc_id not in ctx.locations_checked:
                data = location_ram_data[loc_data[0] - 0x1440]
                masked_data = data & (1 << loc_data[1])
                bit_set = masked_data != 0
                invert_bit = ((len(loc_data) >= 3) and loc_data[2])
                if bit_set != invert_bit:
                    new_checks.append(loc_id)

        for new_check_id in new_checks:
            ctx.locations_checked.add(new_check_id)
            location = ctx.location_names.lookup_in_game(new_check_id)
            total_locations = len(ctx.missing_locations) + len(ctx.checked_locations)
            snes_logger.info(f"New Check: {location} ({len(ctx.locations_checked)}/{total_locations})")
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [new_check_id]}])

        recv_count = await snes_read(ctx, ITEMQUEUE_HIGH, 2)
        recv_index = struct.unpack("H", recv_count)[0]
        if recv_index < len(ctx.items_received):
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info("Received %s from %s (%s) (%d/%d in list)" % (
                color(ctx.item_names.lookup_in_game(item.item), "red", "bold"),
                color(ctx.player_names[item.player], "yellow"),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, ITEMQUEUE_HIGH, pack("H", recv_index))
            if item.item in item_values:
                item_count = await snes_read(ctx, WRAM_START + item_values[item.item][0], 0x1)
                increment = item_values[item.item][1]
                new_item_count = item_count[0]
                if increment > 1:
                    new_item_count = increment
                else:
                    new_item_count += increment

                snes_buffered_write(ctx, WRAM_START + item_values[item.item][0], bytes([new_item_count]))

                if "TrapLink" in ctx.tags and item.item in trap_value_to_name:
                        await self.send_trap_link(ctx, trap_value_to_name[item.item])

        await snes_flush_writes(ctx)

    async def handle_trap_link(self, ctx):
        from SNIClient import snes_buffered_write, snes_flush_writes, snes_read
        
        if self.received_trap_link:
            trap = self.received_trap_link
            print (trap)
            print ( not self.slot_data["traps_enabled"])
            print (trap.item in trap_list)
            if trap.item in trap_list and not self.slot_data["traps_enabled"]:
                # Exclude processing traps if they're not in the pool
                self.received_trap_link = None
                return
            
            print (trap)
            item_count = await snes_read(ctx, WRAM_START + item_values[trap.item][0], 0x1)
            increment = item_values[trap.item][1]
            new_item_count = item_count[0]
            if increment > 1:
                new_item_count = increment
            else:
                new_item_count += increment

            snes_buffered_write(ctx, WRAM_START + item_values[trap.item][0], bytes([new_item_count]))
            self.received_trap_link = None
            
            await snes_flush_writes(ctx)
            
    async def send_trap_link(self, ctx: SNIClient, trap_name: str):
        if "TrapLink" not in ctx.tags or ctx.slot == None:
            return

        await ctx.send_msgs([{
            "cmd": "Bounce", "tags": ["TrapLink"],
            "data": {
                "time": time.time(),
                "source": ctx.player_names[ctx.slot],
                "trap_name": trap_name
            }
        }])
        snes_logger.info(f"Sent linked {trap_name}")

    def on_package(self, ctx, cmd: str, args: dict):
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", None)

        elif cmd == "Bounced":
            if "tags" not in args:
                return
            
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()

            source_name = args["data"]["source"]
            if "TrapLink" in ctx.tags and "TrapLink" in args["tags"] and source_name != ctx.slot_info[ctx.slot].name:
                trap_name: str = args["data"]["trap_name"]
                if trap_name not in trap_name_to_value:
                    return
                
                self.received_trap_link = NetworkItem(trap_name_to_value[trap_name], None, None)