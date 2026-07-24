from BaseClasses import MultiWorld, Region, ItemClassification, LocationProgressType, Location

from .enums import Items
from .constants import *
from .stage_data import level_data
from .items import RHAItem

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import RHAWorld

class RHALocation(Location):
    game = GAME_NAME
    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, str(name), address, parent)

def create_regions(world: "RHAWorld"):
    multiworld = world.multiworld
    player = world.player
    active_perfects = world.options.perfects.value
    active_superbs = world.options.superbs.value

    # Menu region
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    # Create credits region
    credits_region = Region("Credits", player, multiworld)
    multiworld.regions.append(credits_region)
    menu_region.connect(credits_region)
    event = RHALocation(player, "Credits", None, credits_region)
    event.place_locked_item(RHAItem(Items.victory, ItemClassification.progression_skip_balancing, None, player))
    credits_region.locations.append(event)

    # Create regions and locations for everything
    for stage_name, stage_id in level_data.items():
        region = Region(stage_name, player, multiworld)
        multiworld.regions.append(region)
        menu_region.connect(region)
        region.locations.append(RHALocation(player, f"{stage_name.value} - Clear", CLEAR | stage_id, region))
        region.locations.append(RHALocation(player, f"{stage_name.value} - OK", OK | stage_id, region))
        if active_superbs:
            region.locations.append(RHALocation(player, f"{stage_name.value} - Superb", SUPERB | stage_id, region))
        if active_perfects:
            region.locations.append(RHALocation(player, f"{stage_name.value} - Perfect", PERFECT | stage_id, region))
