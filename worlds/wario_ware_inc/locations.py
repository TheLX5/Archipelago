from .constants import *
from .enums import Locations, Regions
from .stage_data import microgame_data, game_data, game_scores, score_only_games, game_groups

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WarioWareWorld

all_locations = {}

for region_name, stage_id in game_data.items():
    if region_name not in score_only_games:
        all_locations[f"{region_name.value} - Clear"] = STAGES | (stage_id << 16)
    for score in game_scores[region_name]:
        all_locations[f"{region_name.value} - {score} Points"] = SCORE | (stage_id << 16) | score & 0xFFFF

for region_name, game_id in microgame_data.items():
    all_locations[f"{region_name.value} - Clear"] = MICROGAME | game_id
    all_locations[f"{region_name.value} - Flower"] = FLOWER | game_id

def count_locations_active(world: "WarioWareWorld"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count

flower_groups = {
    "Flowers": [
        name for name in all_locations.keys() if f" - Flower" in name
    ]
}

location_groups = flower_groups
