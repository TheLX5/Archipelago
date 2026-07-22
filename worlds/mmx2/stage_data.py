from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMX2World

from rule_builder.rules import True_, Rule

from .enums import Regions, Events, Locations
from .constants import *

class MMXLevelLocation:
    name: str
    region: str
    id: None | int
    rule: None | Rule
    is_event: bool

    def __init__(self,
                 name: Locations,
                 region: Regions,
                 id: int | None,
                 rule: Rule | None = None):
        self.name = str(name)
        self.region = str(region)
        self.id = id
        self.rule = rule
        if isinstance(name, Events):
            self.is_event = True
        else:
            self.is_event = False


class MMXLevel:
    name: str
    regions: list[str]
    locations: list[MMXLevelLocation]
    pickups: dict[str, int]

    def __init__(self,
                 name: str,
                 regions: list[Regions],
                 locations: list[MMXLevelLocation],
                 ):
        self.name = name
        self.regions = [str(region) for region in regions]
        self.locations = [location for location in locations]


level_data: dict[Regions, MMXLevel] = {
    Regions.intro_stage: MMXLevel(
        name=Regions.intro_stage,
        regions=[
            Regions.intro_stage,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.intro_stage_boss,
                region=Regions.intro_stage,
                id=X2 | ENEMY | INTRO | 0x18,
            ),
            MMXLevelLocation(
                name=Locations.intro_stage_clear,
                region=Regions.intro_stage,
                id=X2 | CLEAR | INTRO | 0x00,
            ),
            MMXLevelLocation(
                name=Locations.intro_stage_hp_1,
                region=Regions.intro_stage,
                id=X2 | PICKUP | INTRO | 0x00,
            ),
            MMXLevelLocation(
                name=Locations.intro_stage_hp_2,
                region=Regions.intro_stage,
                id=X2 | PICKUP | INTRO | 0x01,
            ),
        ]
    ),
    Regions.wheel_gator: MMXLevel(
        name=Regions.wheel_gator,
        regions=[
            Regions.wheel_gator,
            Regions.wheel_gator_start,
            Regions.wheel_gator_mid,
            Regions.wheel_gator_end,
            Regions.wheel_gator_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.wheel_gator_boss,
                region=Regions.wheel_gator_boss,
                id=X2 | ENEMY | GATOR | 0x00,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_clear,
                region=Regions.wheel_gator_boss,
                id=X2 | CLEAR | GATOR | 0x06,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_heart_tank,
                region=Regions.wheel_gator_mid,
                id=X2 | HEART | GATOR | 0x20,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_arms,
                region=Regions.wheel_gator_start,
                id=X2 | UPGRADE | GATOR | 0x02,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_1,
                region=Regions.wheel_gator_start,
                id=X2 | PICKUP | GATOR | 0x02,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_2,
                region=Regions.wheel_gator_start,
                id=X2 | PICKUP | GATOR | 0x03,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_1up,
                region=Regions.wheel_gator_mid,
                id=X2 | PICKUP | GATOR | 0x04,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_energy_1,
                region=Regions.wheel_gator_mid,
                id=X2 | PICKUP | GATOR | 0x05,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_3,
                region=Regions.wheel_gator_end,
                id=X2 | PICKUP | GATOR | 0x06,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_4,
                region=Regions.wheel_gator_end,
                id=X2 | PICKUP | GATOR | 0x07,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_5,
                region=Regions.wheel_gator_end,
                id=X2 | PICKUP | GATOR | 0x4A,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_6,
                region=Regions.wheel_gator_end,
                id=X2 | PICKUP | GATOR | 0x4B,
            ),
            MMXLevelLocation(
                name=Locations.wheel_gator_hp_7,
                region=Regions.wheel_gator_end,
                id=X2 | PICKUP | GATOR | 0x4C,
            ),
        ],
    ),
    Regions.bubble_crab: MMXLevel(
        name=Regions.bubble_crab,
        regions=[
            Regions.bubble_crab,
            Regions.bubble_crab_start,
            Regions.bubble_crab_open,
            Regions.bubble_crab_inside,
            Regions.bubble_crab_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.bubble_crab_boss,
                region=Regions.bubble_crab_boss,
                id=X2 | CRAB | ENEMY | 0x01,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_clear,
                region=Regions.bubble_crab_boss,
                id=X2 | CRAB | CLEAR | 0x02,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_heart_tank,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | HEART | 0x40,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_sub_tank,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | UPGRADE | 0x80,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_1up,
                region=Regions.bubble_crab_start,
                id=X2 | CRAB | PICKUP | 0x08,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_1,
                region=Regions.bubble_crab_start,
                id=X2 | CRAB | PICKUP | 0x09,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_2,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0A,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_energy_1,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0B,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_3,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0C,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_4,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0D,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_energy_2,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0E,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_5,
                region=Regions.bubble_crab_open,
                id=X2 | CRAB | PICKUP | 0x0F,
            ),
            MMXLevelLocation(
                name=Locations.bubble_crab_hp_6,
                region=Regions.bubble_crab_inside,
                id=X2 | CRAB | PICKUP | 0x10,
            ),
        ],
    ),
    Regions.flame_stag: MMXLevel(
        name=Regions.flame_stag,
        regions=[
            Regions.flame_stag,
            Regions.flame_stag_start,
            Regions.flame_stag_volcano,
            Regions.flame_stag_gas,
            Regions.flame_stag_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.flame_stag_boss,
                region=Regions.flame_stag_boss,
                id=X2 | STAG | ENEMY | 0x02,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_clear,
                region=Regions.flame_stag_boss,
                id=X2 | STAG | CLEAR | 0x0E,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_heart_tank,
                region=Regions.flame_stag_start,
                id=X2 | STAG | HEART | 0x02,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_sub_tank,
                region=Regions.flame_stag_start,
                id=X2 | STAG | UPGRADE | 0x20,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_1up_1,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x11,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_1,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x12,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_energy_1,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x13,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_2,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x14,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_energy_2,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x15,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_3,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x16,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_4,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x17,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_1up_2,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x18,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_5,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x19,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_energy_3,
                region=Regions.flame_stag_start,
                id=X2 | STAG | PICKUP | 0x1A,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_6,
                region=Regions.flame_stag_volcano,
                id=X2 | STAG | PICKUP | 0x1B,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_7,
                region=Regions.flame_stag_volcano,
                id=X2 | STAG | PICKUP | 0x1C,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_energy_4,
                region=Regions.flame_stag_volcano,
                id=X2 | STAG | PICKUP | 0x1D,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_8,
                region=Regions.flame_stag_volcano,
                id=X2 | STAG | PICKUP | 0x1E,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_1up_3,
                region=Regions.flame_stag_volcano,
                id=X2 | STAG | PICKUP | 0x1F,
            ),
            MMXLevelLocation(
                name=Locations.flame_stag_hp_9,
                region=Regions.flame_stag_gas,
                id=X2 | STAG | PICKUP | 0x20,
            ),
        ],
    ),
    Regions.morph_moth: MMXLevel(
        name=Regions.morph_moth,
        regions=[
            Regions.morph_moth,
            Regions.morph_moth_start,
            Regions.morph_moth_parasite_1,
            Regions.morph_moth_after_parasite_1,
            Regions.morph_moth_parasite_2,
            Regions.morph_moth_after_parasite_2,
            Regions.morph_moth_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.morph_moth_boss,
                region=Regions.morph_moth_boss,
                id=X2 | MOTH | ENEMY | 0x03,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_clear,
                region=Regions.morph_moth_boss,
                id=X2 | MOTH | CLEAR | 0x04,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_heart_tank,
                region=Regions.morph_moth_start,
                id=X2 | MOTH | HEART | 0x01,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_body,
                region=Regions.morph_moth_start,
                id=X2 | MOTH | UPGRADE | 0x04,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_mini_boss_1,
                region=Regions.morph_moth_parasite_1,
                id=X2 | MOTH | ENEMY | 0x19,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_mini_boss_2,
                region=Regions.morph_moth_parasite_2,
                id=X2 | MOTH | ENEMY | 0x1D,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_1up_1,
                region=Regions.morph_moth_start,
                id=X2 | MOTH | PICKUP | 0x21,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_1up_2,
                region=Regions.morph_moth_start,
                id=X2 | MOTH | PICKUP | 0x22,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_hp_1,
                region=Regions.morph_moth_after_parasite_1,
                id=X2 | MOTH | PICKUP | 0x23,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_hp_2,
                region=Regions.morph_moth_after_parasite_1,
                id=X2 | MOTH | PICKUP | 0x24,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_hp_3,
                region=Regions.morph_moth_after_parasite_1,
                id=X2 | MOTH | PICKUP | 0x25,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_hp_4,
                region=Regions.morph_moth_after_parasite_1,
                id=X2 | MOTH | PICKUP | 0x26,
            ),
            MMXLevelLocation(
                name=Locations.morph_moth_hp_5,
                region=Regions.morph_moth_after_parasite_1,
                id=X2 | MOTH | PICKUP | 0x27,
            ),
        ],
    ),
    Regions.magna_centipede: MMXLevel(
        name=Regions.magna_centipede,
        regions=[
            Regions.magna_centipede,
            Regions.magna_centipede_start,
            Regions.magna_centipede_blade,
            Regions.magna_centipede_after_blade,
            Regions.magna_centipede_security,
            Regions.magna_centipede_after_security,
            Regions.magna_centipede_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.magna_centipede_boss,
                region=Regions.magna_centipede_boss,
                id=X2 | MAGNA | ENEMY | 0x04,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_clear,
                region=Regions.magna_centipede_boss,
                id=X2 | MAGNA | CLEAR | 0x0C,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_heart_tank,
                region=Regions.magna_centipede_start,
                id=X2 | MAGNA | HEART | 0x08,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_sub_tank,
                region=Regions.magna_centipede_start,
                id=X2 | MAGNA | UPGRADE | 0x10,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_mini_boss_1,
                region=Regions.magna_centipede_blade,
                id=X2 | MAGNA | ENEMY | 0x1A,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_mini_boss_2,
                region=Regions.magna_centipede_security,
                id=X2 | MAGNA | ENEMY | 0x1B,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_hp_1,
                region=Regions.magna_centipede_after_blade,
                id=X2 | MAGNA | PICKUP | 0x28,
            ),
            MMXLevelLocation(
                name=Locations.magna_centipede_hp_2,
                region=Regions.magna_centipede_after_blade,
                id=X2 | MAGNA | PICKUP | 0x29,
            ),
        ],
    ),
    Regions.crystal_snail: MMXLevel(
        name=Regions.crystal_snail,
        regions=[
            Regions.crystal_snail,
            Regions.crystal_snail_start,
            Regions.crystal_snail_after_arena,
            Regions.crystal_snail_arena,
            Regions.crystal_snail_quartz,
            Regions.crystal_snail_downhill,
            Regions.crystal_snail_uphill,
            Regions.crystal_snail_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.crystal_snail_boss,
                region=Regions.crystal_snail_boss,
                id=X2 | SNAIL | ENEMY | 0x05,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_clear,
                region=Regions.crystal_snail_boss,
                id=X2 | SNAIL | CLEAR | 0x00,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_heart_tank,
                region=Regions.crystal_snail_start,
                id=X2 | SNAIL | HEART | 0x10,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_helmet,
                region=Regions.crystal_snail_uphill,
                id=X2 | SNAIL | UPGRADE | 0x01,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_mini_boss_1,
                region=Regions.crystal_snail_quartz,
                id=X2 | SNAIL | ENEMY | 0x1C,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_hp_1,
                region=Regions.crystal_snail_start,
                id=X2 | SNAIL | PICKUP | 0x2A,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_energy_1,
                region=Regions.crystal_snail_start,
                id=X2 | SNAIL | PICKUP | 0x2B,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_hp_2,
                region=Regions.crystal_snail_after_arena,
                id=X2 | SNAIL | PICKUP | 0x2E,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_hp_3,
                region=Regions.crystal_snail_start,
                id=X2 | SNAIL | PICKUP | 0x2C,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_1up_1,
                region=Regions.crystal_snail_start,
                id=X2 | SNAIL | PICKUP | 0x2D,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_hp_4,
                region=Regions.crystal_snail_downhill,
                id=X2 | SNAIL | PICKUP | 0x4D,
            ),
            MMXLevelLocation(
                name=Locations.crystal_snail_1up_2,
                region=Regions.crystal_snail_uphill,
                id=X2 | SNAIL | PICKUP | 0x2F,
            ),
        ],
    ),
    Regions.overdrive_ostrich: MMXLevel(
        name=Regions.overdrive_ostrich,
        regions=[
            Regions.overdrive_ostrich,
            Regions.overdrive_ostrich_start,
            Regions.overdrive_ostrich_arena,
            Regions.overdrive_ostrich_inside,
            Regions.overdrive_ostrich_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_boss,
                region=Regions.overdrive_ostrich_boss,
                id=X2 | OSTRICH | ENEMY | 0x06,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_clear,
                region=Regions.overdrive_ostrich_boss,
                id=X2 | OSTRICH | CLEAR | 0x08,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_heart_tank,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | HEART | 0x04,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_leg,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | UPGRADE | 0x08,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_hp_1,
                region=Regions.overdrive_ostrich_start,
                id=X2 | OSTRICH | PICKUP | 0x30,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_1up,
                region=Regions.overdrive_ostrich_start,
                id=X2 | OSTRICH | PICKUP | 0x31,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_hp_2,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | PICKUP | 0x32,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_energy_1,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | PICKUP | 0x33,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_hp_3,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | PICKUP | 0x34,
            ),
            MMXLevelLocation(
                name=Locations.overdrive_ostrich_energy_2,
                region=Regions.overdrive_ostrich_inside,
                id=X2 | OSTRICH | PICKUP | 0x35,
            ),
        ],
    ),
    Regions.wire_sponge: MMXLevel(
        name=Regions.wire_sponge,
        regions=[
            Regions.wire_sponge,
            Regions.wire_sponge_start,
            Regions.wire_sponge_elevator,
            Regions.wire_sponge_outside,
            Regions.wire_sponge_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.wire_sponge_boss,
                region=Regions.wire_sponge_boss,
                id=X2 | SPONGE | ENEMY | 0x07,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_clear,
                region=Regions.wire_sponge_boss,
                id=X2 | SPONGE | CLEAR | 0x0A,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_heart_tank,
                region=Regions.wire_sponge_start,
                id=X2 | SPONGE | HEART | 0x80,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_sub_tank,
                region=Regions.wire_sponge_start,
                id=X2 | SPONGE | UPGRADE | 0x40,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_1up_1,
                region=Regions.wire_sponge_start,
                id=X2 | SPONGE | PICKUP | 0x36,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_hp_1,
                region=Regions.wire_sponge_elevator,
                id=X2 | SPONGE | PICKUP | 0x37,
            ),
            MMXLevelLocation(
                name=Locations.wire_sponge_hp_2,
                region=Regions.wire_sponge_outside,
                id=X2 | SPONGE | PICKUP | 0x38,
            ),
        ],
    ),
    Regions.x_hunter_arena: MMXLevel(
        name=Regions.x_hunter_arena,
        regions=[
            Regions.x_hunter_arena,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.agile_defeated,
                region=Regions.x_hunter_arena,
                id=X2 | HUNTER | ENEMY | 0x08,
            ),
            MMXLevelLocation(
                name=Locations.serges_defeated,
                region=Regions.x_hunter_arena,
                id=X2 | HUNTER | ENEMY | 0x09,
            ),
            MMXLevelLocation(
                name=Locations.violen_defeated,
                region=Regions.x_hunter_arena,
                id=X2 | HUNTER | ENEMY | 0x0A,
            ),
        ],
    ),
    Regions.x_hunter_stage: MMXLevel(
        name=Regions.x_hunter_stage,
        regions=[
            Regions.x_hunter_stage,
        ],
        locations=[],
    ),
    Regions.x_hunter_stage_1: MMXLevel(
        name=Regions.x_hunter_stage_1,
        regions=[
            Regions.x_hunter_stage_1,
            Regions.x_hunter_stage_1_start,
            Regions.x_hunter_stage_1_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.x_hunter_stage_1_boss,
                region=Regions.x_hunter_stage_1_boss,
                id=X2 | BASE1 | ENEMY | 0x0B,
            ),
            MMXLevelLocation(
                name=Events.x_hunter_stage_1_clear,
                region=Regions.x_hunter_stage_1_boss,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_1_1up_1,
                region=Regions.x_hunter_stage_1_start,
                id=X2 | BASE1 | PICKUP | 0x39,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_1_hp,
                region=Regions.x_hunter_stage_1_start,
                id=X2 | BASE1 | PICKUP | 0x3A,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_1_1up_2,
                region=Regions.x_hunter_stage_1_start,
                id=X2 | BASE1 | PICKUP | 0x3B,
            ),
        ],
    ),
    Regions.x_hunter_stage_2: MMXLevel(
        name=Regions.x_hunter_stage_2,
        regions=[
            Regions.x_hunter_stage_2,
            Regions.x_hunter_stage_2_start,
            Regions.x_hunter_stage_2_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.x_hunter_stage_2_boss,
                region=Regions.x_hunter_stage_2_boss,
                id=X2 | BASE2 | ENEMY | 0x0C,
            ),
            MMXLevelLocation(
                name=Events.x_hunter_stage_2_clear,
                region=Regions.x_hunter_stage_2_boss,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_2_hp,
                region=Regions.x_hunter_stage_2_start,
                id=X2 | BASE2 | PICKUP | 0x3C,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_2_1up,
                region=Regions.x_hunter_stage_2_start,
                id=X2 | BASE2 | PICKUP | 0x3D,
            ),
        ],
    ),
    Regions.x_hunter_stage_3: MMXLevel(
        name=Regions.x_hunter_stage_3,
        regions=[
            Regions.x_hunter_stage_3,
            Regions.x_hunter_stage_3_start,
            Regions.x_hunter_stage_3_boss,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_boss,
                region=Regions.x_hunter_stage_3_boss,
                id=X2 | BASE3 | ENEMY | 0x0D,
            ),
            MMXLevelLocation(
                name=Events.x_hunter_stage_3_clear,
                region=Regions.x_hunter_stage_3_boss,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_shoryuken,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | SPECIAL | 0x00,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_1,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x3E,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_1up_1,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x3F,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_2,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x40,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_3,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x41,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_4,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x42,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_5,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x43,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_6,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x44,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_1up_2,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x45,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_7,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x46,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_hp_8,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x47,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_1up_3,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x48,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_3_1up_4,
                region=Regions.x_hunter_stage_3_start,
                id=X2 | BASE3 | PICKUP | 0x49,
            ),
        ],
    ),
    Regions.x_hunter_stage_4: MMXLevel(
        name=Regions.x_hunter_stage_4,
        regions=[
            Regions.x_hunter_stage_4,
            Regions.x_hunter_stage_4_lobby,
            Regions.x_hunter_stage_4_voice,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_clear,
                region=Regions.x_hunter_stage_4_voice,
                id=X2 | BASE4 | CLEAR | 0x1F,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_wheel_gator,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x0E,
            ),
            MMXLevelLocation(
                name=Events.wheel_gator_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_bubble_crab,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x0F,
            ),
            MMXLevelLocation(
                name=Events.bubble_crab_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_flame_stag,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x10,
            ),
            MMXLevelLocation(
                name=Events.flame_stag_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_morph_moth,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x11,
            ),
            MMXLevelLocation(
                name=Events.morph_moth_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_magna_centipede,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x12,
            ),
            MMXLevelLocation(
                name=Events.magna_centipede_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_crystal_snail,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x13,
            ),
            MMXLevelLocation(
                name=Events.crystal_snail_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_overdrive_ostrich,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x14,
            ),
            MMXLevelLocation(
                name=Events.overdrive_ostrich_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_4_wire_sponge,
                region=Regions.x_hunter_stage_4_lobby,
                id=X2 | BASE4 | ENEMY | 0x15,
            ),
            MMXLevelLocation(
                name=Events.wire_sponge_rematch,
                region=Regions.x_hunter_stage_4_lobby,
                id=None,
            ),
        ],
    ),
    Regions.x_hunter_stage_5: MMXLevel(
        name=Regions.x_hunter_stage_5,
        regions=[
            Regions.x_hunter_stage_5,
            Regions.x_hunter_stage_5_zero,
            Regions.x_hunter_stage_5_sigma,
        ],
        locations=[
            MMXLevelLocation(
                name=Locations.x_hunter_stage_5_zero,
                region=Regions.x_hunter_stage_5_zero,
                id=X2 | BASE5 | ENEMY | 0x16,
            ),
            MMXLevelLocation(
                name=Locations.x_hunter_stage_5_sigma,
                region=Regions.x_hunter_stage_5_sigma,
                id=X2 | BASE5 | ENEMY | 0x17,
            ),
        ],
    ),
}