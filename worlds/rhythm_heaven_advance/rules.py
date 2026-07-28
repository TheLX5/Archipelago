from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAny, Rule, False_, True_, CanReachLocation
from rule_builder.field_resolvers import FromWorldAttr

if TYPE_CHECKING:
    from . import RHAWorld

from .enums import Items, Regions
from .constants import *

class RHARules:
    world: "RHAWorld"
    connection_rules: dict[str, Rule]

    def __init__(self, world: "RHAWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"Menu -> Credits": Has(Items.medal, count=FromWorldAttr("required_medals")),
                
            f"Menu -> {Regions.karate_man}": HasAny(Items.remix_1_column, Items.karate_man_stage),
            f"Menu -> {Regions.rhythm_tweezers}": HasAny(Items.remix_1_column, Items.rhythm_tweezers_stage),
            f"Menu -> {Regions.marching_orders}": HasAny(Items.remix_1_column, Items.marching_orders_stage),
            f"Menu -> {Regions.spaceball}": HasAny(Items.remix_1_column, Items.spaceball_stage),
            f"Menu -> {Regions.the_clappy_trio}": HasAny(Items.remix_1_column, Items.the_clappy_trio_stage),
            f"Menu -> {Regions.remix_1}": HasAny(Items.remix_1_column, Items.remix_1_stage),

            f"Menu -> {Regions.sneaky_spirits}": HasAny(Items.remix_2_column, Items.sneaky_spirits_stage),
            f"Menu -> {Regions.samurai_slice}": HasAny(Items.remix_2_column, Items.samurai_slice_stage),
            f"Menu -> {Regions.rat_race}": HasAny(Items.remix_2_column, Items.rat_race_stage),
            f"Menu -> {Regions.sick_beats}": HasAny(Items.remix_2_column, Items.sick_beats_stage),
            f"Menu -> {Regions.the_bon_odori}": HasAny(Items.remix_2_column, Items.the_bon_odori_stage),
            f"Menu -> {Regions.remix_2}": HasAny(Items.remix_2_column, Items.remix_2_stage),

            f"Menu -> {Regions.wizards_waltz}": HasAny(Items.remix_3_column, Items.wizards_waltz_stage),
            f"Menu -> {Regions.showtime}": HasAny(Items.remix_3_column, Items.showtime_stage),
            f"Menu -> {Regions.bunny_hop}": HasAny(Items.remix_3_column, Items.bunny_hop_stage),
            f"Menu -> {Regions.tram_and_pauline}": HasAny(Items.remix_3_column, Items.tram_and_pauline_stage),
            f"Menu -> {Regions.space_dance}": HasAny(Items.remix_3_column, Items.space_dance_stage),
            f"Menu -> {Regions.remix_3}": HasAny(Items.remix_3_column, Items.remix_3_stage),

            f"Menu -> {Regions.quiz_show}": HasAny(Items.remix_4_column, Items.quiz_show_stage),
            f"Menu -> {Regions.night_walk}": HasAny(Items.remix_4_column, Items.night_walk_stage),
            f"Menu -> {Regions.power_calligraphy}": HasAny(Items.remix_4_column, Items.power_calligraphy_stage),
            f"Menu -> {Regions.polyrhythm}": HasAny(Items.remix_4_column, Items.polyrhythm_stage),
            f"Menu -> {Regions.rapmen}": HasAny(Items.remix_4_column, Items.rapmen_stage),
            f"Menu -> {Regions.remix_4}": HasAny(Items.remix_4_column, Items.remix_4_stage),

            f"Menu -> {Regions.bouncy_road}": HasAny(Items.remix_5_column, Items.bouncy_road_stage),
            f"Menu -> {Regions.ninja_bodyguard}": HasAny(Items.remix_5_column, Items.ninja_bodyguard_stage),
            f"Menu -> {Regions.toss_team}": HasAny(Items.remix_5_column, Items.toss_team_stage),
            f"Menu -> {Regions.fireworks}": HasAny(Items.remix_5_column, Items.fireworks_stage),
            f"Menu -> {Regions.tap_trial}": HasAny(Items.remix_5_column, Items.tap_trial_stage),
            f"Menu -> {Regions.remix_5}": HasAny(Items.remix_5_column, Items.remix_5_stage),

            f"Menu -> {Regions.the_snappy_trio}": HasAny(Items.remix_6_column, Items.the_snappy_trio_stage),
            f"Menu -> {Regions.the_bon_dance}": HasAny(Items.remix_6_column, Items.the_bon_dance_stage),
            f"Menu -> {Regions.cosmic_dance}": HasAny(Items.remix_6_column, Items.cosmic_dance_stage),
            f"Menu -> {Regions.rapwomen}": HasAny(Items.remix_6_column, Items.rapwomen_stage),
            f"Menu -> {Regions.tap_trial_2}": HasAny(Items.remix_6_column, Items.tap_trial_2_stage),
            f"Menu -> {Regions.remix_6}": HasAny(Items.remix_6_column, Items.remix_6_stage),

            f"Menu -> {Regions.karate_man_2}": HasAny(Items.remix_7_column, Items.karate_man_2_stage),
            f"Menu -> {Regions.rhythm_tweezers_2}": HasAny(Items.remix_7_column, Items.rhythm_tweezers_2_stage),
            f"Menu -> {Regions.ninja_descendant}": HasAny(Items.remix_7_column, Items.ninja_descendant_stage),
            f"Menu -> {Regions.night_walk_2}": HasAny(Items.remix_7_column, Items.night_walk_2_stage),
            f"Menu -> {Regions.marching_orders_2}": HasAny(Items.remix_7_column, Items.marching_orders_2_stage),
            f"Menu -> {Regions.remix_7}": HasAny(Items.remix_7_column, Items.remix_7_stage),

            f"Menu -> {Regions.bouncy_road_2}": HasAny(Items.remix_8_column, Items.bouncy_road_2_stage),
            f"Menu -> {Regions.toss_team_2}": HasAny(Items.remix_8_column, Items.toss_team_2_stage),
            f"Menu -> {Regions.polyrhythm_2}": HasAny(Items.remix_8_column, Items.polyrhythm_2_stage),
            f"Menu -> {Regions.spaceball_2}": HasAny(Items.remix_8_column, Items.spaceball_2_stage),
            f"Menu -> {Regions.sneaky_spirits_2}": HasAny(Items.remix_8_column, Items.sneaky_spirits_2_stage),
            f"Menu -> {Regions.remix_8}": HasAny(Items.remix_8_column, Items.remix_8_stage),
        }

    def set_rules(self) -> None:
        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = self.world.get_entrance(entrance_name)
                self.world.set_rule(entrance, rule)
            except KeyError:
                continue

        self.world.set_completion_rule(Has(Items.victory))
