from typing import TYPE_CHECKING, override

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, True_

if TYPE_CHECKING:
    from . import DKC2World

from BaseClasses import CollectionState, Location
from .Options import Logic, Goal, FlyingKrockTokens
from .Names import LocationName, ItemName, RegionName, EventName
import dataclasses

GAME_NAME = "Donkey Kong Country 2"

HasBothKongs: Rule = HasAll(ItemName.diddy, ItemName.dixie)
CanTeamAttack: Rule = HasBothKongs & Has(ItemName.team_attack)
CanHover: Rule = HasAll(ItemName.dixie, ItemName.helicopter_spin)
CanUseDiddyBarrels: Rule = HasAll(ItemName.diddy, ItemName.barrel_kong)
CanUseDixieBarrels: Rule = HasAll(ItemName.dixie, ItemName.barrel_kong)

class DKC2Rules:
    world: "DKC2World"
    location_rules: dict[str, Rule]

    def __init__(self, world: "DKC2World") -> None:
        self.player = world.player
        self.world = world


    def set_dkc2_rules(self) -> None:
        multiworld = self.world.multiworld

        location_rules: dict[str, Rule] = {}

        for loc in multiworld.get_locations(self.player):
            if "(Map Event)" in loc.name:
                continue
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        map_event.access_rule = loc.access_rule
                    except KeyError:
                        # Filter out missing locations
                        continue

        for location in location_rules:
            self.world.set_rule(self.world.get_location(location), location_rules[location])



class DKC2StrictRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                Has(ItemName.carry) | Has(ItemName.rambi),
            LocationName.pirate_panic_banana_coin_1:
                CanTeamAttack,
            #LocationName.pirate_panic_banana_bunch_1:
            #    True_,
            #LocationName.pirate_panic_red_balloon:
            #    True_,
            LocationName.pirate_panic_banana_coin_2:
                CanTeamAttack,
            #LocationName.pirate_panic_banana_coin_3:
            #    True_,
            LocationName.pirate_panic_green_balloon:
                Has(ItemName.rambi),
        }