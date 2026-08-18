from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, Rule, False_, True_, CanReachLocation
from rule_builder.field_resolvers import FromOption

if TYPE_CHECKING:
    from . import MMX2World

from .options import XHunterBaseLevelUnlock, XHunterBaseBossRematchCount, XHuntersArenaMedalCount

from .enums import Items, Events, Regions, Locations
from .constants import *
from .base_rules import (
    CAN_AIR_DASH,
    CAN_USE_CHECKPOINTS,
    CAN_CHARGE,
    SPIN_WHEEL,
    BUBBLE_SPLASH,
    SPEED_BURNER,
    CRYSTAL_HUNTER,
    STRIKE_CHAIN,
    SHORYUKEN,
    CAN_ENTER_BASE,
    HasHP,
)
from .boss_data import weapons

class MMX2Rules:
    world: "MMX2World"
    connection_rules: dict[str, Rule]
    region_rules: dict[str, Rule]
    location_rules: dict[str, Rule]

    def __init__(self, world: "MMX2World") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{Regions.intro_stage} -> {Regions.wheel_gator}":
                Has(Items.stage_wheel_gator),
            f"{Regions.intro_stage} -> {Regions.bubble_crab}":
                Has(Items.stage_bubble_crab),
            f"{Regions.intro_stage} -> {Regions.flame_stag}":
                Has(Items.stage_flame_stag),
            f"{Regions.intro_stage} -> {Regions.morph_moth}":
                Has(Items.stage_morph_moth),
            f"{Regions.intro_stage} -> {Regions.magna_centipede}":
                Has(Items.stage_magna_centipede),
            f"{Regions.intro_stage} -> {Regions.crystal_snail}":
                Has(Items.stage_crystal_snail),
            f"{Regions.intro_stage} -> {Regions.overdrive_ostrich}":
                Has(Items.stage_overdrive_ostrich),
            f"{Regions.intro_stage} -> {Regions.wire_sponge}":
                Has(Items.stage_wire_sponge),
                
            f"{Regions.intro_stage} -> {Regions.x_hunter_stage}":
                CAN_ENTER_BASE,

            f"{Regions.x_hunter_stage_2} -> {Regions.x_hunter_stage_2_start}":
                CAN_AIR_DASH | CRYSTAL_HUNTER | (CAN_CHARGE & SPEED_BURNER),

            f"{Regions.x_hunter_stage} -> {Regions.x_hunter_stage_5}":
                HasAll(Events.x_hunter_stage_1_clear, Events.x_hunter_stage_2_clear,
                        Events.x_hunter_stage_3_clear, Events.x_hunter_stage_4_clear),

            f"{Regions.x_hunter_stage_4} -> {Regions.x_hunter_stage_4_lobby}":
                HasAll(Events.x_hunter_stage_1_clear, Events.x_hunter_stage_2_clear,
                        Events.x_hunter_stage_3_clear),
            f"{Regions.x_hunter_stage_4_lobby} -> {Regions.x_hunter_stage_4_voice}":
                Has(Events.boss_rematch_clear, count=FromOption(XHunterBaseBossRematchCount)),

            # X-Hunter Arena entrances
            f"{Regions.wheel_gator_mid} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.bubble_crab_open} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.flame_stag_volcano} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.morph_moth_after_parasite_1} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.magna_centipede_after_blade} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.crystal_snail_arena} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),
            f"{Regions.crystal_snail_arena} -> {Regions.crystal_snail_after_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)) & (
                    CanReachLocation(Locations.agile_defeated) |
                    CanReachLocation(Locations.serges_defeated) |
                    CanReachLocation(Locations.violen_defeated)
                ),
            f"{Regions.overdrive_ostrich_arena} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)) & (
                    SPIN_WHEEL | SHORYUKEN
                ),
            f"{Regions.wire_sponge_elevator} -> {Regions.x_hunter_arena}":
                Has(Items.maverick_medal, count=FromOption(XHuntersArenaMedalCount)),

            # Helmet logic
            f"{Regions.morph_moth} -> {Regions.morph_moth_after_parasite_1}":
                CAN_USE_CHECKPOINTS,
            f"{Regions.morph_moth} -> {Regions.morph_moth_after_parasite_2}":
                CAN_USE_CHECKPOINTS,
            f"{Regions.magna_centipede} -> {Regions.magna_centipede_after_blade}":
                CAN_USE_CHECKPOINTS,
            f"{Regions.magna_centipede} -> {Regions.magna_centipede_after_security}":
                CAN_USE_CHECKPOINTS,
            f"{Regions.crystal_snail} -> {Regions.crystal_snail_downhill}":
                CAN_USE_CHECKPOINTS,
            f"{Regions.x_hunter_stage_2} -> {Regions.x_hunter_stage_2_boss}":
                CAN_USE_CHECKPOINTS,
        }

        self.location_rules = {
            Locations.wheel_gator_arms:
                CAN_AIR_DASH | (CAN_CHARGE & SPEED_BURNER),
            Locations.wheel_gator_heart_tank:
                CAN_CHARGE & SPEED_BURNER,

            Locations.bubble_crab_sub_tank:
                CAN_CHARGE & BUBBLE_SPLASH,
            Locations.bubble_crab_1up:
                SPIN_WHEEL,
            Locations.bubble_crab_energy_1:
                CAN_AIR_DASH | (CAN_CHARGE & (SPEED_BURNER | BUBBLE_SPLASH)),

            Locations.morph_moth_heart_tank:
                CRYSTAL_HUNTER,
            Locations.morph_moth_body:
                SPIN_WHEEL,
            Locations.morph_moth_1up_1:
                CRYSTAL_HUNTER,

            Locations.flame_stag_1up_3:
                CAN_AIR_DASH,

            Locations.magna_centipede_heart_tank:
                CAN_AIR_DASH | (CAN_CHARGE & SPEED_BURNER),
            Locations.magna_centipede_sub_tank:
                CAN_AIR_DASH | (CAN_CHARGE & SPEED_BURNER),

            # TODO: Figure out what should put this one in logic if having skill issue
            #       with the Ride Armor
            Locations.crystal_snail_heart_tank:
                True_(),
                #CAN_AIR_DASH | (CAN_CHARGE & SPEED_BURNER),

            Locations.overdrive_ostrich_leg:
                SPIN_WHEEL,
            Locations.overdrive_ostrich_hp_1:
                SPIN_WHEEL,
            
            Locations.x_hunter_stage_2_hp:
                SPIN_WHEEL,
            Locations.x_hunter_stage_2_1up:
                SPIN_WHEEL & CAN_AIR_DASH & CAN_CHARGE & SPEED_BURNER,
            
            Locations.x_hunter_stage_3_shoryuken:
                CAN_AIR_DASH & CAN_CHARGE & SPEED_BURNER & CRYSTAL_HUNTER,
            Locations.x_hunter_stage_3_hp_1:
                CAN_AIR_DASH & STRIKE_CHAIN,
            Locations.x_hunter_stage_3_1up_1:
                CAN_AIR_DASH & STRIKE_CHAIN,
            Locations.x_hunter_stage_3_1up_2:
                CRYSTAL_HUNTER,
            Locations.x_hunter_stage_3_hp_7:
                CRYSTAL_HUNTER,
            Locations.x_hunter_stage_3_hp_8:
                CRYSTAL_HUNTER,
            Locations.x_hunter_stage_3_1up_3:
                CAN_AIR_DASH & CAN_CHARGE & SPEED_BURNER & CRYSTAL_HUNTER,
            Locations.x_hunter_stage_3_1up_4:
                CAN_AIR_DASH | (CAN_CHARGE & SPEED_BURNER)
        }

        # Process base levels
        if world.options.x_hunter_base_level_unlock == XHunterBaseLevelUnlock.option_vanilla:
            self.connection_rules.update({
                f"{Regions.x_hunter_stage_1_boss} -> {Regions.x_hunter_stage_2}":
                    Has(Events.x_hunter_stage_1_clear),
                f"{Regions.x_hunter_stage_2_boss} -> {Regions.x_hunter_stage_3}":
                    Has(Events.x_hunter_stage_2_clear),
                f"{Regions.x_hunter_stage_3_boss} -> {Regions.x_hunter_stage_4}":
                    Has(Events.x_hunter_stage_3_clear),
            })
        elif world.options.x_hunter_base_level_unlock == XHunterBaseLevelUnlock.option_all_open:
            self.connection_rules.update({})
        # TODO: Revisit in a future update
        #elif world.options.x_hunter_base_level_unlock == XHunterBaseLevelUnlock.option_item_per_level:
        #    self.connection_rules.update({
        #        f"{Regions.x_hunter_stage} -> {Regions.x_hunter_stage_1}":
        #            Has(Items.stage_x_hunter_1),
        #        f"{Regions.x_hunter_stage} -> {Regions.x_hunter_stage_2}":
        #            Has(Items.stage_x_hunter_2),
        #        f"{Regions.x_hunter_stage} -> {Regions.x_hunter_stage_3}":
        #            Has(Items.stage_x_hunter_3),
        #        f"{Regions.x_hunter_stage} -> {Regions.x_hunter_stage_4}":
        #            Has(Items.stage_x_hunter_4),
        #    })

        # Apply boss weaknesses as rules
        for name, boss_data in self.world.boss_data.items():
            # Build weakness rules
            rule = False_()
            for weapon in boss_data.weakness:
                rule |= weapons[weapon].rule

            # TODO: Add HP rules to bosses
            #rule &= HasHP(10)

            # Combat logic for bosses
            if name == "Magna Centipede":
                rule &= CAN_AIR_DASH

            for entrance in boss_data.entrances:
                if entrance in self.connection_rules.keys():
                    self.connection_rules[entrance] &= rule
                else:
                    self.connection_rules[entrance] = rule

            for location in boss_data.locations:
                if location in self.location_rules.keys():
                    self.location_rules[location] &= rule
                else:
                    self.location_rules[location] = rule
                

    def set_rules(self) -> None:
        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = self.world.get_entrance(entrance_name)
                self.world.set_rule(entrance, rule)
            except KeyError:
                continue
        for location in self.world.get_locations():
            if location.name in self.location_rules.keys():
                self.world.set_rule(location, self.location_rules[location.name])
            
        self.world.set_completion_rule(Has(Items.victory))
