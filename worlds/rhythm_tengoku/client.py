import logging

import base64
import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus, color, NetworkItem
from worlds._bizhawk.client import BizHawkClient
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

from .constants import *
from .locations import all_locations
from .stage_data import remix_groups, level_data, perfect_data

class TengokuClient(BizHawkClient):
    game = GAME_NAME
    system = "GBA"
    patch_suffix = ".aptengoku"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            identifiers = await bizhawk.read(ctx.bizhawk_ctx, [
                (ROM_NAME_START, 0x0C, "ROM"),
                (AUTH_NUMBER_START, 0x03, "ROM"),
            ])
            if identifiers[0].decode("ascii") != "RHYTHMTENGOK":
                return False
            if identifiers[1] == b'\x00\x00\x00':
                return False
            if identifiers[1].decode("ascii") != "RT-":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(AUTH_NUMBER_START, 21, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")


    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None or ctx.slot is None:
            return

        game_data = await bizhawk.read(ctx.bizhawk_ctx, [
            [LEVEL_STATES, 0x60, "EWRAM"],
            [SETTING_PERFECTS, 0x01, "ROM"],
            [SETTING_SUPERBS, 0x01, "ROM"],
            [SETTING_MEDALS, 0x01, "ROM"],
            [RECEIVED_INDEX, 0x02, "EWRAM"],
            [MC_MUFFIN_COUNT, 0x02, "EWRAM"],
            [SEEN_CREDITS, 0x02, "EWRAM"],
            [GAME_LOADED, 0x04, "IWRAM"],
            [LEVEL_PERFECTS, 0x60, "EWRAM"],
        ])
        game_loaded = int.from_bytes(bytearray(game_data[7]), "little")
        if game_loaded != 0x00FF00FE:
            return
        
        level_states = bytearray(game_data[0])
        level_perfects = bytearray(game_data[8])
        setting_perfects = int.from_bytes(bytearray(game_data[1]), "little")
        setting_superbs = int.from_bytes(bytearray(game_data[2]), "little")
        setting_medals = int.from_bytes(bytearray(game_data[3]), "little")
        received_index = int.from_bytes(bytearray(game_data[4]), "little")
        mc_muffins = int.from_bytes(bytearray(game_data[5]), "little")
        seen_credits = int.from_bytes(bytearray(game_data[6]), "little")

        for _, loc_id in all_locations.items():
            if loc_id in ctx.locations_checked:
                continue

            loc_type = loc_id & TYPE_MASK
            stage_id = loc_id & DATA_MASK

            if level_states[stage_id] <= 0x03:
                continue

            if loc_type == CLEAR and level_states[stage_id] >= 4:
                ctx.locations_checked.add(loc_id)
            elif loc_type == OK and level_states[stage_id] >= 4:
                ctx.locations_checked.add(loc_id)
            elif loc_type == SUPERB and setting_superbs and level_states[stage_id] >= 5:
                ctx.locations_checked.add(loc_id)
            elif loc_type == PERFECT and setting_perfects:
                perfect_id = perfect_data[stage_id]
                if level_perfects[perfect_id]:
                    ctx.locations_checked.add(loc_id)

        await ctx.check_locations(ctx.locations_checked)

        if not ctx.finished_game and seen_credits == 0xDEAD:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True

        writes: list[tuple[int, Sequence[int], str]] = []

        if received_index < len(ctx.items_received):
            item = ctx.items_received[received_index]
            received_index += 1
            writes.append((RECEIVED_INDEX, received_index.to_bytes(2, "little"), "EWRAM"))

            item_name = ctx.item_names.lookup_in_slot(item.item)
            item_code = item.item & 0xFFF

            if item_code == 0xC0:
                # give medals and open credits if needed
                mc_muffins += 1
                writes.append((MC_MUFFIN_COUNT, mc_muffins.to_bytes(2, "little"), "EWRAM"))
                writes.append((UPDATE_MEDALS, (0x01).to_bytes(2, "little"), "EWRAM"))
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Received a {item_name}!")
                if mc_muffins >= setting_medals:
                    writes.append((LEVEL_STATES+53, (0x03).to_bytes(1, "little"), "EWRAM"))
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked Credits Staff Level! (You can now goal the game)")

            elif item_code >= 0x100:
                # process columns
                for level_name in remix_groups[item_name]:
                    level_id = level_data[level_name]
                    if level_states[level_id] <= 0x02:
                        level_states[level_id] = 0x03
                    writes.append((LEVEL_STATES+level_id, (0x03).to_bytes(1, "little"), "EWRAM"))
                await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked {item_name}!")

            elif item_code <= 0x30:
                # process individual stages
                if level_states[item_code] <= 0x02:
                    level_states[item_code] = 0x03
                    writes.append((LEVEL_STATES+item_code, (0x03).to_bytes(1, "little"), "EWRAM"))
                    await bizhawk.display_message(ctx.bizhawk_ctx, f"Unlocked {item_name}!")

            await bizhawk.write(ctx.bizhawk_ctx, writes)

        else:
            for loc_id in ctx.checked_locations:
                if loc_id in ctx.locations_checked:
                    continue
                ctx.locations_checked.add(loc_id)

                loc_type = loc_id & TYPE_MASK
                stage_id = loc_id & DATA_MASK

                if loc_type == CLEAR and level_states[stage_id] < 4:
                    level_states[stage_id] = 0x04
                    writes.append((LEVEL_STATES+stage_id, (0x04).to_bytes(1, "little"), "EWRAM"))
                if loc_type == OK and level_states[stage_id] < 4:
                    level_states[stage_id] = 0x04
                    writes.append((LEVEL_STATES+stage_id, (0x04).to_bytes(1, "little"), "EWRAM"))
                elif loc_type == SUPERB and setting_superbs:
                    level_states[stage_id] = 0x05
                    writes.append((LEVEL_STATES+stage_id, (0x05).to_bytes(1, "little"), "EWRAM"))

            await bizhawk.write(ctx.bizhawk_ctx, writes)
