from .constants import *
from .enums import Locations
from .stage_data import level_data

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MMX2World

all_locations = {}
pickup_locations = {}

for region_name, region_data in level_data.items():
    for location_data in region_data.locations:
        if location_data.is_event:
            continue
        all_locations[location_data.name] = location_data.id
        if (location_data.id & TYPE_MASK) == PICKUP:
            pickup_locations[location_data.name] = location_data.id

location_groups = {
    "Mavericks": {
        Locations.wheel_gator_boss.value,
        Locations.bubble_crab_boss.value,
        Locations.flame_stag_boss.value,
        Locations.morph_moth_boss.value,
        Locations.magna_centipede_boss.value,
        Locations.crystal_snail_boss.value,
        Locations.overdrive_ostrich_boss.value,
        Locations.wire_sponge_boss.value,
    },
    "Bosses": {
        Locations.intro_stage_boss.value,
        Locations.wheel_gator_boss.value,
        Locations.bubble_crab_boss.value,
        Locations.flame_stag_boss.value,
        Locations.morph_moth_boss.value,
        Locations.morph_moth_mini_boss_1.value,
        Locations.morph_moth_mini_boss_2.value,
        Locations.magna_centipede_boss.value,
        Locations.magna_centipede_mini_boss_1.value,
        Locations.magna_centipede_mini_boss_2.value,
        Locations.crystal_snail_boss.value,
        Locations.crystal_snail_mini_boss_1.value,
        Locations.overdrive_ostrich_boss.value,
        Locations.wire_sponge_boss.value,
        Locations.agile_defeated.value,
        Locations.serges_defeated.value,
        Locations.violen_defeated.value,
        Locations.x_hunter_stage_1_boss.value,
        Locations.x_hunter_stage_2_boss.value,
        Locations.x_hunter_stage_3_boss.value,
        Locations.x_hunter_stage_5_zero.value,
        Locations.x_hunter_stage_5_sigma.value,
    },
    "Heart Tanks": {location for location in all_locations.keys() if "- Heart Tank" in location},
    "Sub Tanks": {location for location in all_locations.keys() if "- Sub Tank" in location},
    "Upgrade Capsules": {location for location in all_locations.keys() if "Capsule" in location},
    "Intro Stage": {location for location in all_locations.keys() if "Intro Stage - " in location},
    "Wheel Gator Stage": {location for location in all_locations.keys() if "Wheel Gator - " in location},
    "Bubble Crab Stage": {location for location in all_locations.keys() if "Bubble Crab - " in location},
    "Flame Stag Stage": {location for location in all_locations.keys() if "Flame Stag - " in location},
    "Morph Moth Stage": {location for location in all_locations.keys() if "Morph Moth - " in location},
    "Magna Centipede Stage": {location for location in all_locations.keys() if "Magna Centipede - " in location},
    "Crystal Snail Stage": {location for location in all_locations.keys() if "Crystal Snail - " in location},
    "Overdrive Ostrich Stage": {location for location in all_locations.keys() if "Overdrive Ostrich - " in location},
    "Wire Sponge Stage": {location for location in all_locations.keys() if "Wire Sponge - " in location},
    "X-Hunter Base 1": {location for location in all_locations.keys() if "X-Hunter Base 1 - " in location},
    "X-Hunter Base 2": {location for location in all_locations.keys() if "X-Hunter Base 2 - " in location},
    "X-Hunter Base 3": {location for location in all_locations.keys() if "X-Hunter Base 3 - " in location},
    "X-Hunter Base 4": {location for location in all_locations.keys() if "X-Hunter Base 4 - " in location},
}

def count_locations_active(world: "MMX2World"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count
