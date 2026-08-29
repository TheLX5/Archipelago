from BaseClasses import MultiWorld, Region, ItemClassification, LocationProgressType, Location

from .options import XHunterBaseLevelUnlock
from .enums import Locations, Regions, Events
from .constants import *
from .stage_data import level_data
from .items import MMX2Item

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MMX2World

class MMX2Location(Location):
    game = GAME_NAME
    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, str(name), address, parent)

def create_regions(world: "MMX2World"):
    multiworld = world.multiworld
    player = world.player
    active_pickups = world.options.pickup_locations.value

    for stage_name, stage_data in level_data.items():
        for region_name in stage_data.regions:
            region = Region(region_name, player, multiworld)
            multiworld.regions.append(region)

            for location_data in stage_data.locations:
                if location_data.region != region.name:
                    continue

                if location_data.is_event:
                    event_loc = MMX2Location(player, location_data.name, None, region)
                    region.locations.append(event_loc)
                    if "(Rematch)" in location_data.name:
                        event_item = MMX2Item(Events.boss_rematch_clear.value, ItemClassification.progression_skip_balancing, None, player)
                    else:
                        event_item = MMX2Item(location_data.name, ItemClassification.progression_skip_balancing, None, player)
                    event_loc.place_locked_item(event_item)
                    continue

                if not active_pickups and (location_data.id & TYPE_MASK) == PICKUP:
                    continue
                region.locations.append(MMX2Location(player, location_data.name, location_data.id, region))
    


def connect_regions(world: "MMX2World"):
    # Connect Hunter Base
    connect(world, Regions.intro_stage, Regions.wheel_gator)
    connect(world, Regions.intro_stage, Regions.bubble_crab)
    connect(world, Regions.intro_stage, Regions.flame_stag)
    connect(world, Regions.intro_stage, Regions.morph_moth)
    connect(world, Regions.intro_stage, Regions.magna_centipede)
    connect(world, Regions.intro_stage, Regions.crystal_snail)
    connect(world, Regions.intro_stage, Regions.overdrive_ostrich)
    connect(world, Regions.intro_stage, Regions.wire_sponge)
    connect(world, Regions.intro_stage, Regions.x_hunter_stage)

    # Connect Wheel Gator
    connect(world, Regions.wheel_gator, Regions.wheel_gator_start)
    connect(world, Regions.wheel_gator_start, Regions.wheel_gator_mid)
    connect(world, Regions.wheel_gator_mid, Regions.wheel_gator_end)
    connect(world, Regions.wheel_gator_end, Regions.wheel_gator_boss)

    # Connect Bubble Crab
    connect(world, Regions.bubble_crab, Regions.bubble_crab_start)
    connect(world, Regions.bubble_crab_start, Regions.bubble_crab_open)
    connect(world, Regions.bubble_crab_open, Regions.bubble_crab_inside)
    connect(world, Regions.bubble_crab_inside, Regions.bubble_crab_boss)

    # Connect Flame Stag
    connect(world, Regions.flame_stag, Regions.flame_stag_start)
    connect(world, Regions.flame_stag_start, Regions.flame_stag_volcano)
    connect(world, Regions.flame_stag_volcano, Regions.flame_stag_gas)
    connect(world, Regions.flame_stag_gas, Regions.flame_stag_boss)

    # Connect Morph Moth
    connect(world, Regions.morph_moth, Regions.morph_moth_start)
    connect(world, Regions.morph_moth_start, Regions.morph_moth_parasite_1)
    connect(world, Regions.morph_moth_parasite_1, Regions.morph_moth_after_parasite_1)
    connect(world, Regions.morph_moth_after_parasite_1, Regions.morph_moth_parasite_2)
    connect(world, Regions.morph_moth_parasite_2, Regions.morph_moth_after_parasite_2)
    connect(world, Regions.morph_moth_after_parasite_2, Regions.morph_moth_boss)

    # Connect Magna Centipede
    connect(world, Regions.magna_centipede, Regions.magna_centipede_start)
    connect(world, Regions.magna_centipede_start, Regions.magna_centipede_blade)
    connect(world, Regions.magna_centipede_blade, Regions.magna_centipede_after_blade)
    connect(world, Regions.magna_centipede_after_blade, Regions.magna_centipede_security)
    connect(world, Regions.magna_centipede_security, Regions.magna_centipede_after_security)
    connect(world, Regions.magna_centipede_after_security, Regions.magna_centipede_boss)

    # Connect Crystal Snail
    connect(world, Regions.crystal_snail, Regions.crystal_snail_start)
    connect(world, Regions.crystal_snail_start, Regions.crystal_snail_quartz)
    connect(world, Regions.crystal_snail_quartz, Regions.crystal_snail_downhill)
    connect(world, Regions.crystal_snail_downhill, Regions.crystal_snail_uphill)
    connect(world, Regions.crystal_snail_uphill, Regions.crystal_snail_boss)
    connect(world, Regions.crystal_snail_start, Regions.crystal_snail_arena)
    connect(world, Regions.crystal_snail_arena, Regions.crystal_snail_after_arena)
    connect(world, Regions.crystal_snail_after_arena, Regions.crystal_snail_start)

    # Overdrive Ostrich
    connect(world, Regions.overdrive_ostrich, Regions.overdrive_ostrich_start)
    connect(world, Regions.overdrive_ostrich_start, Regions.overdrive_ostrich_inside)
    connect(world, Regions.overdrive_ostrich_start, Regions.overdrive_ostrich_arena)
    connect(world, Regions.overdrive_ostrich_inside, Regions.overdrive_ostrich_boss)

    # Wire Sponge
    connect(world, Regions.wire_sponge, Regions.wire_sponge_start)
    connect(world, Regions.wire_sponge_start, Regions.wire_sponge_elevator)
    connect(world, Regions.wire_sponge_elevator, Regions.wire_sponge_outside)
    connect(world, Regions.wire_sponge_outside, Regions.wire_sponge_boss)

    # Connect X-Hunter Arena
    connect(world, Regions.wheel_gator_mid, Regions.x_hunter_arena)
    connect(world, Regions.bubble_crab_open, Regions.x_hunter_arena)
    connect(world, Regions.flame_stag_volcano, Regions.x_hunter_arena)
    connect(world, Regions.morph_moth_after_parasite_1, Regions.x_hunter_arena)
    connect(world, Regions.magna_centipede_after_blade, Regions.x_hunter_arena)
    connect(world, Regions.crystal_snail_arena, Regions.x_hunter_arena)
    connect(world, Regions.overdrive_ostrich_arena, Regions.x_hunter_arena)
    connect(world, Regions.wire_sponge_elevator, Regions.x_hunter_arena)

    # Connect X-Hunter Stage 1
    connect(world, Regions.x_hunter_stage_1, Regions.x_hunter_stage_1_start)
    connect(world, Regions.x_hunter_stage_1_start, Regions.x_hunter_stage_1_boss)

    # Connect X-Hunter Stage 2
    connect(world, Regions.x_hunter_stage_2, Regions.x_hunter_stage_2_start)
    connect(world, Regions.x_hunter_stage_2_start, Regions.x_hunter_stage_2_boss)
    
    # Connect X-Hunter Stage 3
    connect(world, Regions.x_hunter_stage_3, Regions.x_hunter_stage_3_start)
    connect(world, Regions.x_hunter_stage_3_start, Regions.x_hunter_stage_3_boss)

    # Connect X-Hunter Stage 4
    connect(world, Regions.x_hunter_stage_4, Regions.x_hunter_stage_4_lobby)
    connect(world, Regions.x_hunter_stage_4_lobby, Regions.x_hunter_stage_4_voice)

    # Connect X-Hunter Stage 5
    connect(world, Regions.x_hunter_stage_5, Regions.x_hunter_stage_5_zero)
    connect(world, Regions.x_hunter_stage_5_zero, Regions.x_hunter_stage_5_sigma)

    # Connect checkpoints
    # Connect Morph Moth
    connect(world, Regions.morph_moth, Regions.morph_moth_after_parasite_1)
    connect(world, Regions.morph_moth, Regions.morph_moth_after_parasite_2)

    # Connect Magna Centipede
    connect(world, Regions.magna_centipede, Regions.magna_centipede_after_blade)
    connect(world, Regions.magna_centipede, Regions.magna_centipede_after_security)

    # Connect Crystal Snail
    connect(world, Regions.crystal_snail, Regions.crystal_snail_downhill)

    # Connect X-Hunter Stages
    if world.options.x_hunter_base_level_unlock == XHunterBaseLevelUnlock.option_vanilla:
        connect(world, Regions.x_hunter_stage, Regions.x_hunter_stage_1)
        connect(world, Regions.x_hunter_stage_1_boss, Regions.x_hunter_stage_2)
        connect(world, Regions.x_hunter_stage_2_boss, Regions.x_hunter_stage_3)
        connect(world, Regions.x_hunter_stage_3_boss, Regions.x_hunter_stage_4)
    else:
        connect(world, Regions.x_hunter_stage, Regions.x_hunter_stage_1)
        connect(world, Regions.x_hunter_stage, Regions.x_hunter_stage_2)
        connect(world, Regions.x_hunter_stage, Regions.x_hunter_stage_3)
        connect(world, Regions.x_hunter_stage, Regions.x_hunter_stage_4)
        
    connect(world, Regions.x_hunter_stage_4_voice, Regions.x_hunter_stage_5)


def connect(world: "MMX2World", source: str, target: str):
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    source_region.connect(target_region)
