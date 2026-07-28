from .constants import *
from .enums import Locations, Regions
from .stage_data import level_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import RHAWorld

all_locations = {}
superb_locations = {}
perfect_locations = {}

for region_name, level_id in level_data.items():
    all_locations[f"{region_name.value} - Clear"] = PAD | CLEAR | level_id
    all_locations[f"{region_name.value} - OK"] = PAD | OK | level_id
    all_locations[f"{region_name.value} - Superb"] = PAD | SUPERB | level_id
    superb_locations[f"{region_name.value} - Superb"] = PAD | SUPERB | level_id
    all_locations[f"{region_name.value} - Perfect"] = PAD | PERFECT | level_id
    perfect_locations[f"{region_name.value} - Perfect"] = PAD | PERFECT | level_id

def count_locations_active(world: "RHAWorld"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count

level_groups = {
    region.value: [
        name for name in all_locations.keys() if f"{region.value} -" in name
    ] for region in level_data.keys()
}

clear_groups = {
    "Perfect Clears": [name for name in all_locations.keys() if "- Perfect" in name],
    "Superb Clears": [name for name in all_locations.keys() if "- Superb" in name],
    "OK Clears": [name for name in all_locations.keys() if "- OK" in name],
    "Clears": [name for name in all_locations.keys() if "- Clear" in name],
}

location_groups = level_groups | clear_groups
