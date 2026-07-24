from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, Rule, False_, True_, CanReachLocation
from rule_builder.field_resolvers import FromOption

if TYPE_CHECKING:
    from . import RHAWorld

from .enums import Items, Regions
from .constants import *
from .options import Medals

class RHARules:
    world: "RHAWorld"
    connection_rules: dict[str, Rule]

    def __init__(self, world: "RHAWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"Menu -> Credits": Has(Items.medal, count=FromOption(Medals)),
                
            f"Menu -> {Regions.karate_man}": Has(Items.remix_1_column),
            f"Menu -> {Regions.rhythm_tweezers}": Has(Items.remix_1_column),
            f"Menu -> {Regions.marching_orders}": Has(Items.remix_1_column),
            f"Menu -> {Regions.spaceball}": Has(Items.remix_1_column),
            f"Menu -> {Regions.the_clappy_trio}": Has(Items.remix_1_column),
            f"Menu -> {Regions.remix_1}": Has(Items.remix_1_column),

            f"Menu -> {Regions.sneaky_spirits}": Has(Items.remix_2_column),
            f"Menu -> {Regions.samurai_slice}": Has(Items.remix_2_column),
            f"Menu -> {Regions.rat_race}": Has(Items.remix_2_column),
            f"Menu -> {Regions.sick_beats}": Has(Items.remix_2_column),
            f"Menu -> {Regions.the_bon_odori}": Has(Items.remix_2_column),
            f"Menu -> {Regions.remix_2}": Has(Items.remix_2_column),

            f"Menu -> {Regions.wizards_waltz}": Has(Items.remix_3_column),
            f"Menu -> {Regions.showtime}": Has(Items.remix_3_column),
            f"Menu -> {Regions.bunny_hop}": Has(Items.remix_3_column),
            f"Menu -> {Regions.tram_and_pauline}": Has(Items.remix_3_column),
            f"Menu -> {Regions.space_dance}": Has(Items.remix_3_column),
            f"Menu -> {Regions.remix_3}": Has(Items.remix_3_column),

            f"Menu -> {Regions.quiz_show}": Has(Items.remix_4_column),
            f"Menu -> {Regions.night_walk}": Has(Items.remix_4_column),
            f"Menu -> {Regions.power_calligraphy}": Has(Items.remix_4_column),
            f"Menu -> {Regions.polyrhythm}": Has(Items.remix_4_column),
            f"Menu -> {Regions.rapmen}": Has(Items.remix_4_column),
            f"Menu -> {Regions.remix_4}": Has(Items.remix_4_column),

            f"Menu -> {Regions.bouncy_road}": Has(Items.remix_5_column),
            f"Menu -> {Regions.ninja_bodyguard}": Has(Items.remix_5_column),
            f"Menu -> {Regions.toss_team}": Has(Items.remix_5_column),
            f"Menu -> {Regions.fireworks}": Has(Items.remix_5_column),
            f"Menu -> {Regions.tap_trial}": Has(Items.remix_5_column),
            f"Menu -> {Regions.remix_5}": Has(Items.remix_5_column),

            f"Menu -> {Regions.the_snappy_trio}": Has(Items.remix_6_column),
            f"Menu -> {Regions.the_bon_dance}": Has(Items.remix_6_column),
            f"Menu -> {Regions.cosmic_dance}": Has(Items.remix_6_column),
            f"Menu -> {Regions.rapwomen}": Has(Items.remix_6_column),
            f"Menu -> {Regions.tap_trial_2}": Has(Items.remix_6_column),
            f"Menu -> {Regions.remix_6}": Has(Items.remix_6_column),

            f"Menu -> {Regions.karate_man_2}": Has(Items.remix_7_column),
            f"Menu -> {Regions.rhythm_tweezers_2}": Has(Items.remix_7_column),
            f"Menu -> {Regions.ninja_descendant}": Has(Items.remix_7_column),
            f"Menu -> {Regions.night_walk_2}": Has(Items.remix_7_column),
            f"Menu -> {Regions.marching_orders_2}": Has(Items.remix_7_column),
            f"Menu -> {Regions.remix_7}": Has(Items.remix_7_column),

            f"Menu -> {Regions.bouncy_road_2}": Has(Items.remix_8_column),
            f"Menu -> {Regions.toss_team_2}": Has(Items.remix_8_column),
            f"Menu -> {Regions.polyrhythm_2}": Has(Items.remix_8_column),
            f"Menu -> {Regions.spaceball_2}": Has(Items.remix_8_column),
            f"Menu -> {Regions.sneaky_spirits_2}": Has(Items.remix_8_column),
            f"Menu -> {Regions.remix_8}": Has(Items.remix_8_column),
        }

    def set_rules(self) -> None:
        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = self.world.get_entrance(entrance_name)
                self.world.set_rule(entrance, rule)
            except KeyError:
                continue

        self.world.set_completion_rule(Has(Items.victory))
