import logging
from collections import deque
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

    def __init__(self) -> None:
        self.ram = "MainRAM"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check memory size first
            if (await get_memory_size(ctx.bizhawk_ctx, self.ram)) < 0x0F1870:
                return False
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_PATCH_NAME, 0x10, self.ram)]))[0])
            rom_name = rom_name.decode("ascii")
            if rom_name != "MMX4_ARCHIPELAGO":
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
        # Read Armor Picked Up
        unlocked_armor = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_ARMOR_PICKED_UP, 5, self.ram)]))[0]
        for i in range(0, 5):
            if unlocked_armor[i] > 0:
                # Head
                if i == 0:
                    locs_to_send.add(14574108)
                # Body
                elif i == 1:
                    locs_to_send.add(14574117)
                # Arms 1
                elif i == 2:
                    locs_to_send.add(14574112)
                # Arms 2
                elif i == 3:
                    locs_to_send.add(14574113)
                # Legs
                elif i == 4:
                    locs_to_send.add(14574102)

        # Read Bosses Defeated
        defeated_bosses = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_BOSSES_DEFEATED, 22, self.ram)]))[0]
        if len(defeated_bosses) == 22:
            for i in range(0, 22):
                if defeated_bosses[i] > 0:
                    # Intro Boss
                    if i == 0:
                        locs_to_send.add(14574100)
                        locs_to_send.add(14574101)
                    # Web Spider
                    elif i == 1:
                        locs_to_send.add(14574104)
                        locs_to_send.add(14574105)
                    # Cyber Peacock
                    elif i == 2:
                        locs_to_send.add(14574109)
                        locs_to_send.add(14574110)
                    # Storm Owl
                    elif i == 3:
                        locs_to_send.add(14574114)
                        locs_to_send.add(14574115)
                    # Magma Dragoon
                    elif i == 4:
                        locs_to_send.add(14574118)
                        locs_to_send.add(14574119)
                    # Jet Stingray
                    elif i == 5:
                        locs_to_send.add(14574122)
                        locs_to_send.add(14574123)
                    # Split Mushroom
                    elif i == 6:
                        locs_to_send.add(14574125)
                        locs_to_send.add(14574126)
                    # Slash Beast
                    elif i == 7:
                        locs_to_send.add(14574128)
                        locs_to_send.add(14574129)
                    # Frost Walrus
                    elif i == 8:
                        locs_to_send.add(14574133)
                        locs_to_send.add(14574134)
                    # Memorial Hall Colonel
                    elif i == 9:
                        locs_to_send.add(14574135)
                    # Space Port Colonel
                    elif i == 10:
                        locs_to_send.add(14574136)
                    # Double / Iris
                    elif i == 11:
                        locs_to_send.add(14574137)
                    # General
                    elif i == 12:
                        locs_to_send.add(14574138)
                    # Web Spider Rematch
                    elif i == 13:
                        locs_to_send.add(14574139)
                    # Cyber Peacock Rematch
                    elif i == 14:
                        locs_to_send.add(14574140)
                    # Storm Owl Rematch
                    elif i == 15:
                        locs_to_send.add(14574141)
                    # Magma Dragoon Rematch
                    elif i == 16:
                        locs_to_send.add(14574142)
                    # Jet Stingray Rematch
                    elif i == 17:
                        locs_to_send.add(14574143)
                    # Split Mushroom Rematch
                    elif i == 18:
                        locs_to_send.add(14574144)
                    # Slash Beast Rematch
                    elif i == 19:
                        locs_to_send.add(14574145)
                    # Frost Walrus Rematch
                    elif i == 20:
                        locs_to_send.add(14574146)
                    # Sigma
                    elif i == 21:
                        locs_to_send.add(14574300)

        # Read Items Picked Up
        offset = 0
        while True:
            items_picked_up = (await bizhawk.read(ctx.bizhawk_ctx, [(ADDRESS_ITEMS_PICKED_UP + offset, 4, self.ram)]))[0]
            item_data_location = int.from_bytes(items_picked_up, "little")
            if item_data_location == 0:
                break
            # Intro Stage
            elif item_data_location == 0x800F4D30:
                locs_to_send.add(14574200)
            elif item_data_location == 0x800F4D40:
                locs_to_send.add(14574201)
            elif item_data_location == 0x800F4D38:
                locs_to_send.add(14574202)
            # Web Spider
            elif item_data_location == 0x800F52B0:
                locs_to_send.add(14574203)
            elif item_data_location == 0x800F52C0:
                locs_to_send.add(14574204)
            elif item_data_location == 0x800F52B8:
                locs_to_send.add(14574103)
            # Cyber Peacock
            elif item_data_location == 0x800F7438:
                locs_to_send.add(14574106)
            elif item_data_location == 0x800F7440:
                locs_to_send.add(14574107)
            # Storm Owl
            elif item_data_location == 0x800F7700:
                locs_to_send.add(14574205)
            elif item_data_location == 0x800F7978:
                locs_to_send.add(14574206)
            elif item_data_location == 0x800F76F8:
                locs_to_send.add(14574111)
            # Magma Dragoon
            elif item_data_location == 0x800F6854:
                locs_to_send.add(14574116)
            elif item_data_location == 0x800F66B4:
                locs_to_send.add(14574207)
            elif item_data_location == 0x800F66BC:
                locs_to_send.add(14574208)
            elif item_data_location == 0x800F685C:
                locs_to_send.add(14574209)
            # Jet Stingray
            elif item_data_location == 0x800F6C40:
                locs_to_send.add(14574120)
            elif item_data_location == 0x800F6E98:
                locs_to_send.add(14574121)
            elif item_data_location == 0x800F6EA0:
                locs_to_send.add(14574210)
            # Split Mushroom
            elif item_data_location == 0x800F6320:
                locs_to_send.add(14574124)
            elif item_data_location == 0x800F6328:
                locs_to_send.add(14574211)
            elif item_data_location == 0x800F6330:
                locs_to_send.add(14574212)
            # Slash Beast
            elif item_data_location == 0x800F7D3C:
                locs_to_send.add(14574127)
            elif item_data_location == 0x800F7D44:
                locs_to_send.add(14574213)
            # Frost Walrus
            elif item_data_location == 0x800F56C0:
                locs_to_send.add(14574214)
            elif item_data_location == 0x800F56C8:
                locs_to_send.add(14574215)
            elif item_data_location == 0x800F56B8:
                locs_to_send.add(14574216)
            elif item_data_location == 0x800F56B0:
                locs_to_send.add(14574217)
            elif item_data_location == 0x800F5660:
                locs_to_send.add(14574218)
            elif item_data_location == 0x800F5680:
                locs_to_send.add(14574219)
            elif item_data_location == 0x800F5688:
                locs_to_send.add(14574220)
            elif item_data_location == 0x800F5690:
                locs_to_send.add(14574221)
            elif item_data_location == 0x800F5698:
                locs_to_send.add(14574222)
            elif item_data_location == 0x800F56A0:
                locs_to_send.add(14574223)
            elif item_data_location == 0x800F56A8:
                locs_to_send.add(14574224)
            elif item_data_location == 0x800F5668:
                locs_to_send.add(14574225)
            elif item_data_location == 0x800F5678:
                locs_to_send.add(14574226)
            elif item_data_location == 0x800F5868:
                locs_to_send.add(14574227)
            elif item_data_location == 0x800F5658:
                locs_to_send.add(14574130)
            elif item_data_location == 0x800F5670:
                locs_to_send.add(14574131)
            elif item_data_location == 0x800F5860:
                locs_to_send.add(14574132)
            # Final Weapon 1
            elif item_data_location == 0x800F86CC:
                locs_to_send.add(14574228)
            elif item_data_location == 0x800F8564:
                locs_to_send.add(14574229)
            elif item_data_location == 0x800F855C:
                locs_to_send.add(14574230)
            # Final Weapon 2
            elif item_data_location == 0x800F87E0:
                locs_to_send.add(14574231)
            elif item_data_location == 0x800F87E8:
                locs_to_send.add(14574232)
            elif item_data_location == 0x800F87F0:
                locs_to_send.add(14574233)
            elif item_data_location == 0x800F87F8:
                locs_to_send.add(14574234)
            elif item_data_location == 0x800F8910:
                locs_to_send.add(14574235)
            elif item_data_location == 0x800F8918:
                locs_to_send.add(14574236)
            elif item_data_location == 0x800F8920:
                locs_to_send.add(14574237)
            offset += 4

        if locs_to_send is not None:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": list(locs_to_send)}])
        return

    async def received_items_check(self, ctx: "BizHawkClientContext") -> None:
        return