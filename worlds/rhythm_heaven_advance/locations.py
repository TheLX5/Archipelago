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
    all_locations[f"{region_name.value} - Clear"] = CLEAR | level_id
    all_locations[f"{region_name.value} - OK"] = OK | level_id
    all_locations[f"{region_name.value} - Superb"] = SUPERB | level_id
    superb_locations[f"{region_name.value} - Superb"] = SUPERB | level_id
    all_locations[f"{region_name.value} - Perfect"] = PERFECT | level_id
    perfect_locations[f"{region_name.value} - Perfect"] = PERFECT | level_id

def count_locations_active(world: "RHAWorld"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count

location_groups = {
    region.value: [
        name for name in all_locations.keys() if f"{region.value} -" in name
    ] for region in level_data.keys()
}
