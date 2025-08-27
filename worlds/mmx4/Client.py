import logging
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds._bizhawk import get_memory_size

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

logger = logging.getLogger("Client")

# MMX4_ARCHIPELAGO
ADDRESS_PATCH_NAME = 0x0F1740
# Items
ADDRESS_STAGE_ACCESS = 0x0F1750
ADDRESS_ARMOR_FLAGS = 0x0F1770
ADDRESS_ARMS_FLAGS = 0x0F1771
ADDRESS_MAX_HEALTH = 0x0F1772
ADDRESS_WEAPONS_FLAGS = 0x0F1773
ADDRESS_TANK_FLAGS = 0x0F1774
# Locations
ADDRESS_ARMOR_PICKED_UP = 0x0F1790
ADDRESS_BOSSES_DEFEATED = 0x0F17A0
ADDRESS_ITEMS_PICKED_UP = 0x0EE558

class MMX4Client(BizHawkClient):
    game = "Mega Man X4"
    system = "PSX"
    patch_suffix = ".apmmx4"

    def __init__(self) -> None:
        self.ram = "MainRAM"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check memory size first
            if (await get_memory_size(ctx.bizhawk_ctx, self.ram)) < 0x0F1870:
                return False
            # Check ROM name/patch version
            # TODO: Read an unique string in RAM per generation to inform we're using the correct seed
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_PATCH_NAME, 0x10, self.ram)]))[0])
            if rom_name[:4] != b"MMX4":
                return False  # Not our patched ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        ctx.game = self.game
        ctx.items_handling = 0b111
        #ctx.want_slot_data = True
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None:
            return

        if ctx.slot is None:
            return
        try:
            # TODO: Rewrite this while saving an index inside the game's save data
            #       that way we can implement HP refills that are only given once
            await self.location_check(ctx)
            #await self.received_items_check(ctx)
            # Calculate our unlocked items
            unlocked_weapons_value = 0
            unlocked_armor_value = 0
            # 0x20 base
            max_health_value = 32
            unlocked_tanks_value = 0
            stage_access_writes = [0, 0, 0, 0, 0, 0, 0, 0, 1]
            for item in ctx.items_received:
                item_id = item.item
                # Weapons
                if item_id == 14575100:
                    unlocked_weapons_value |= 0b00000001
                if item_id == 14575101:
                    unlocked_weapons_value |= 0b00100000
                if item_id == 14575102:
                    unlocked_weapons_value |= 0b01000000
                if item_id == 14575103:
                    unlocked_weapons_value |= 0b00001000
                if item_id == 14575104:
                    unlocked_weapons_value |= 0b00010000
                if item_id == 14575105:
                    unlocked_weapons_value |= 0b00000100
                if item_id == 14575106:
                    unlocked_weapons_value |= 0b10000000
                if item_id == 14575107:
                    unlocked_weapons_value |= 0b00000010
                # Helmet
                if item_id == 14575108:
                    unlocked_armor_value |= 0b1
                # Body
                if item_id == 14575109:
                    unlocked_armor_value |= 0b10
                # Arms
                if item_id == 14575110 or item_id == 14575111:
                    unlocked_armor_value |= 0b100
                # Legs
                if item_id == 14575112:
                    unlocked_armor_value |= 0b1000
                # Heart Tanks
                if item_id == 14575113:
                    max_health_value += 2
                # Sub Tanks
                if item_id == 14575114:
                    if unlocked_tanks_value & 0b00010000 > 0:
                        unlocked_tanks_value |= 0b00100000
                    else:
                        unlocked_tanks_value |= 0b00010000
                # Weapon Energy Tank
                if item_id == 14575115:
                    unlocked_tanks_value |= 0b01000000
                # Extra Lives Tank
                if item_id == 14575116:
                    unlocked_tanks_value |= 0b10000000
                # Stage Access
                if item_id >= 14575200 and item_id <= 14575207:
                    index = item_id - 14575200
                    stage_access_writes[index] = 1
                # Victory
                if not ctx.finished_game and item_id == 14575400:
                    ctx.finished_game = True
                    await ctx.send_msgs([{
                        "cmd": "StatusUpdate",
                        "status": ClientStatus.CLIENT_GOAL
                    }])

            # Lock here before we do our edits
            await bizhawk.lock(ctx.bizhawk_ctx)
            # Write Weapons
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_WEAPONS_FLAGS, [unlocked_weapons_value], self.ram)])
            # Write Armor
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_ARMOR_FLAGS, [unlocked_armor_value], self.ram)])
            # Write Buster Type, Gamma forced for now
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_ARMS_FLAGS, [0b10], self.ram)])
            # Write Max Health
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_MAX_HEALTH, [max_health_value], self.ram)])
            # Write Tanks
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_TANK_FLAGS, [unlocked_tanks_value], self.ram)])
            # Write Stage Access
            await bizhawk.write(ctx.bizhawk_ctx, [(ADDRESS_STAGE_ACCESS, stage_access_writes, self.ram)])
            await bizhawk.unlock(ctx.bizhawk_ctx)
            return


        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass

    async def location_check(self, ctx: "BizHawkClientContext"):
        locs_to_send = set()

        from .Rom import boss_data, armor_data, item_data
        # Read Armor Picked Up
        unlocked_armor = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_ARMOR_PICKED_UP, 5, self.ram)]))[0]
        for idx, ram_read in enumerate(unlocked_armor):
            if ram_read <= 0:
                continue
            locs_to_send.add(armor_data[idx])

        # Read Bosses Defeated
        defeated_bosses = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_BOSSES_DEFEATED, 22, self.ram)]))[0]
        for idx, ram_read in enumerate(defeated_bosses):
            if ram_read <= 0:
                continue
            for loc_id in boss_data[idx]:
                locs_to_send.add(loc_id)

        # Read Items Picked Up
        offset = 0
        while True:
            items_picked_up = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_ITEMS_PICKED_UP + offset, 4, self.ram)]))[0]
            item_data_location = int.from_bytes(items_picked_up, "little")
            if item_data_location == 0:
                break
            elif item_data_location in item_data.keys():
                locs_to_send.add(item_data[item_data_location])
            offset += 4

        if locs_to_send is not None:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])
            

    async def received_items_check(self, ctx: "BizHawkClientContext") -> None:
        return