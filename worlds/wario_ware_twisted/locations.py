from .constants import *
from .enums import Items
from .stage_data import microgame_data, game_data, game_scores, game_groups, score_only_games

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WarioTwistedWorld

all_locations = {}

for region_name, stage_id in game_data.items():
    if region_name not in score_only_games:
        all_locations[f"{region_name.value} - Clear"] = STAGES | (stage_id << 16)
    for score in game_scores[region_name]:
        all_locations[f"{region_name.value} - {score} Points"] = SCORE | (stage_id << 16) | score & 0xFFFF

for region_name, game_id in microgame_data.items():
    all_locations[f"{region_name.value} - Clear"] = MICROGAME | game_id
    all_locations[f"{region_name.value} - Crown"] = CROWN | game_id

def count_locations_active(world: "WarioTwistedWorld"):
    total_count = 0
    for loc in world.get_locations():
        if loc.is_event is None:
            continue
        if loc.item is None:
            total_count += 1
    return total_count

crown_groups = {
    "Crowns": [
        name for name in all_locations.keys() if f" - Crown" in name
    ],
}

location_groups = {
    "Wario": [name for name in all_locations.keys() if "Wario -" in name],
    "Mona": [name for name in all_locations.keys() if "Mona -" in name],
    "Jimmy": [name for name in all_locations.keys() if "Jimmy -" in name],
    "Kat & Ana": [name for name in all_locations.keys() if "Kat & Ana -" in name],
    "Dribble & Spitz": [name for name in all_locations.keys() if "Dribble & Spitz -" in name],
    "Dribble": [name for name in all_locations.keys() if "Dribble & Spitz -" in name],
    "Dr. Crygor": [name for name in all_locations.keys() if "Dr. Crygor" in name],
    "Orbulon": [name for name in all_locations.keys() if "Orbulon -" in name],
    "9-Volt": [name for name in all_locations.keys() if "9-Volt -" in name],
    "Wario-Man": [name for name in all_locations.keys() if "Wario-Man -" in name],
    "Jimmy's Folks": [name for name in all_locations.keys() if "Jimmy's Folks -" in name],
    "Jimmy Folks": [name for name in all_locations.keys() if "Jimmy's Folks -" in name],
    "WarioWatch": [name for name in all_locations.keys() if "WarioWatch -" in name],
    "WarioWatch 2": [name for name in all_locations.keys() if "WarioWatch 2 -" in name],
    "Skyscraper": [name for name in all_locations.keys() if "Skyscraper -" in name],
    "Tower": [name for name in all_locations.keys() if "Tower -" in name],
    "Mansion": [name for name in all_locations.keys() if "Mansion -" in name],
    "Crowns": [name for name in all_locations.keys() if f" - Crown" in name],
    "Mona Microgames": [entry for name in game_groups[Items.mona_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Jimmy Microgames": [entry for name in game_groups[Items.jimmy_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Kat & Ana Microgames": [entry for name in game_groups[Items.kat_ana_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Dribble & Spitz Microgames": [entry for name in game_groups[Items.dribble_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Dribble Microgames": [entry for name in game_groups[Items.dribble_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Dr. Crygor Microgames": [entry for name in game_groups[Items.crygor_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Crygor Microgames": [entry for name in game_groups[Items.crygor_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Orbulon Microgames": [entry for name in game_groups[Items.orbulon_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "9-Volt Microgames": [entry for name in game_groups[Items.nine_volt_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Wario-Man Microgames": [entry for name in game_groups[Items.wario_man_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "WarioWatch Microgames": [entry for name in game_groups[Items.wariowatch_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
    "Fronk Microgames": [entry for name in game_groups[Items.fronk_bundle] for entry in [f"{name} - Clear", f"{name} - Crown"]],
}

ut_location_id_to_alias: dict[int, str] = {}

for group_name, microgames in game_groups.items():
    current_group = group_name.replace(" Microgame Bundle", "")
    for microgame_name in microgames:
        clear_id = all_locations[f"{microgame_name} - Clear"]
        crown_id = all_locations[f"{microgame_name} - Crown"]
        ut_location_id_to_alias[clear_id] = current_group
        ut_location_id_to_alias[crown_id] = current_group
