from BaseClasses import Region, ItemClassification, Location

from .enums import Items
from .constants import *
from .stage_data import microgame_data, game_data, game_scores, score_only_games
from .items import WarioTwistedItem

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WarioTwistedWorld

class WarioTwistedLocation(Location):
    game = GAME_NAME
    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, str(name), address, parent)

def create_regions(world: "WarioTwistedWorld"):
    multiworld = world.multiworld
    player = world.player
    active_crowns = world.options.microgame_crowns.value
    active_stages = world.included_games
    active_hi_scores = world.options.stage_hi_scores.value

    # Menu region
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    # Create credits region
    credits_region = Region("Credits", player, multiworld)
    multiworld.regions.append(credits_region)
    menu_region.connect(credits_region)
    event = WarioTwistedLocation(player, "Credits", None, credits_region)
    event.place_locked_item(WarioTwistedItem(Items.victory, ItemClassification.progression_skip_balancing, None, player))
    credits_region.locations.append(event)

    # Create regions and locations for stages
    for stage_name, stage_id in game_data.items():
        region = Region(stage_name, player, multiworld)
        multiworld.regions.append(region)
        menu_region.connect(region)
        
        current_game_scores = game_scores[region.name].copy()
        if stage_name not in active_stages:
            continue
        if stage_name not in score_only_games:
            region.locations.append(WarioTwistedLocation(player, f"{stage_name.value} - Clear", STAGES | (stage_id << 16), region))
            if len(current_game_scores) != 0:
                for _ in range(2):
                    score = current_game_scores.pop(0)
                    region.locations.append(WarioTwistedLocation(player, f"{stage_name.value} - {score} Points", SCORE | (stage_id << 16) | score & 0xFFFF, region))
            if active_hi_scores:
                for score in current_game_scores:
                    region.locations.append(WarioTwistedLocation(player, f"{stage_name.value} - {score} Points", SCORE | (stage_id << 16) | score & 0xFFFF, region))
        else:
            for score in current_game_scores:
                region.locations.append(WarioTwistedLocation(player, f"{stage_name.value} - {score} Points", SCORE | (stage_id << 16) | score & 0xFFFF, region))
        

    # Create regions and locations for microgames
    for microgame_name, microgame_id in microgame_data.items():
        if microgame_id not in world.microgames:
            continue
        region = Region(microgame_name, player, multiworld)
        multiworld.regions.append(region)
        menu_region.connect(region)
        region.locations.append(WarioTwistedLocation(player, f"{microgame_name.value} - Clear", MICROGAME | microgame_id, region))
        if active_crowns:
            region.locations.append(WarioTwistedLocation(player, f"{microgame_name.value} - Crown", CROWN | microgame_id, region))
