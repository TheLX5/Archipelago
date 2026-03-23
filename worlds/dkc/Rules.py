

from typing import TYPE_CHECKING, override
if TYPE_CHECKING:
    from . import DKCWorld

from rule_builder.rules import Has, HasAll, Rule, True_, CanReachRegion
from .Names import LocationName, ItemName, RegionName, EventName

HasDonkey: Rule = Has(ItemName.donkey)
HasDiddy: Rule = Has(ItemName.diddy)
HasBothKongs: Rule = HasAll(ItemName.diddy, ItemName.donkey)
CanCarry: Rule = Has(ItemName.carry)
CanClimb: Rule = Has(ItemName.climb)
CanRoll: Rule = Has(ItemName.roll)
CanSwim: Rule = Has(ItemName.swim)
CanSlap: Rule = HasAll(ItemName.donkey, ItemName.slap)
HasRambi: Rule = Has(ItemName.rambi)
HasSquawks: Rule = Has(ItemName.squawks)
HasEnguarde: Rule = Has(ItemName.enguarde)
HasWinky: Rule = Has(ItemName.winky)
HasExpresso: Rule = Has(ItemName.expresso)
HasKannons: Rule = Has(ItemName.kannons)
HasSwitches: Rule = Has(ItemName.switches)
HasMinecart: Rule = Has(ItemName.minecart)
HasTires: Rule = Has(ItemName.tires)
HasPlatforms: Rule = Has(ItemName.platforms)

CanAccessJungle: Rule = Has(ItemName.kongo_jungle)
CanAccessMines: Rule = Has(ItemName.monkey_mines)
CanAccessValley: Rule = Has(ItemName.vine_valley)
CanAccessGlacier: Rule = Has(ItemName.gorilla_glacier)
CanAccessIndustries: Rule = Has(ItemName.kremkroc_industries)
CanAccessCaverns: Rule = Has(ItemName.chimp_caverns)


class DKCRules:
    player: int
    world: "DKCWorld"
    connection_rules: dict[str, Rule]
    region_rules: dict[str, Rule]
    location_rules: dict[str, Rule]

    def __init__(self, world: "DKCWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.dk_isle} -> {RegionName.kongo_jungle}":
                CanAccessJungle,
            f"{RegionName.dk_isle} -> {RegionName.monkey_mines}":
                CanAccessMines,
            f"{RegionName.dk_isle} -> {RegionName.vine_valley}":
                CanAccessValley,
            f"{RegionName.dk_isle} -> {RegionName.gorilla_glacier}":
                CanAccessGlacier,
            f"{RegionName.dk_isle} -> {RegionName.kremkroc_industries}":
                CanAccessIndustries,
            f"{RegionName.dk_isle} -> {RegionName.chimp_caverns}":
                CanAccessCaverns,
            f"{RegionName.dk_isle} -> {RegionName.gangplank_galleon}":
                Has(ItemName.boss_token, self.world.options.gangplank_tokens.value),
            f"{RegionName.kongo_jungle} -> {RegionName.very_gnawty_lair_map}":
                Has(EventName.jungle_level, self.world.options.required_jungle_levels.value),
            f"{RegionName.monkey_mines} -> {RegionName.necky_nuts_map}":
                Has(EventName.mines_level, self.world.options.required_mines_levels.value),
            f"{RegionName.vine_valley} -> {RegionName.bumble_b_rumble_map}":
                Has(EventName.valley_level, self.world.options.required_valley_levels.value),
            f"{RegionName.gorilla_glacier} -> {RegionName.really_gnawty_rampage_map}":
                Has(EventName.glacier_level, self.world.options.required_glacier_levels.value),
            f"{RegionName.kremkroc_industries} -> {RegionName.boss_dumb_drum_map}":
                Has(EventName.industries_level, self.world.options.required_industries_levels.value),
            f"{RegionName.chimp_caverns} -> {RegionName.necky_revenge_map}":
                Has(EventName.caverns_level, self.world.options.required_caverns_levels.value),
        }

    def set_dkc_rules(self) -> None:
        multiworld = self.world.multiworld

        print ("lolololol", self.world.options.glitched_world_access.value)
        if self.world.options.glitched_world_access.value:
            self.connection_rules.update(
                {
                    f"{RegionName.dk_isle} -> {RegionName.kongo_jungle}":
                        CanAccessJungle | (
                            CanReachRegion(RegionName.vine_valley) & HasBothKongs & CanCarry & (
                                HasExpresso | CanRoll
                            )
                        ),
                    f"{RegionName.dk_isle} -> {RegionName.monkey_mines}":
                        CanAccessMines | (
                            HasBothKongs & CanCarry & (
                                CanReachRegion(RegionName.chimp_caverns) | (
                                    CanReachRegion(RegionName.vine_valley) & HasExpresso
                                )
                            )
                        ),
                    f"{RegionName.dk_isle} -> {RegionName.vine_valley}":
                        CanAccessValley | CanAccessJungle,
                    f"{RegionName.dk_isle} -> {RegionName.gorilla_glacier}":
                        CanAccessGlacier | (
                            CanCarry & (
                                (CanReachRegion(RegionName.kongo_jungle) & HasDonkey) | 
                                (CanReachRegion(RegionName.chimp_caverns) & HasBothKongs) | 
                                (CanReachRegion(RegionName.vine_valley) & HasBothKongs & HasExpresso)
                            )                
                        ),
                    f"{RegionName.dk_isle} -> {RegionName.kremkroc_industries}":
                        CanAccessIndustries | (
                            CanReachRegion(RegionName.vine_valley) & HasBothKongs & CanCarry & HasExpresso
                        ),
                    f"{RegionName.dk_isle} -> {RegionName.chimp_caverns}":
                        CanAccessCaverns | (
                            CanReachRegion(RegionName.vine_valley) & HasBothKongs & CanCarry & HasExpresso
                        ),
                }
            )

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            self.world.set_rule(entrance, rule)
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                rule = self.location_rules[loc.name]
                self.world.set_rule(self.world.get_location(loc.name), rule)
            
        self.world.set_completion_rule(Has(EventName.k_rool))
        
    # Universal Tracker: Append the next logic level rule that has UT's glitched item to the actual logic rule
    def set_dkc_glitched_rules(self, non_glitched_rules: dict[str, Rule]) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                glitched_rule = non_glitched_rules[loc.name] | (self.location_rules[loc.name] & Has(ItemName.glitched))
                self.world.set_rule(self.world.get_location(loc.name), glitched_rule)
 

class DKCStrictRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                True_(),
            EventName.jungle_hijinxs_clear:
                True_(),
            LocationName.jungle_hijinxs_bonus_1:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_bonus_2:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_kong:
                True_(),
            LocationName.jungle_hijinxs_balloon_1:
                HasTires,
            LocationName.jungle_hijinxs_bunch_1:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_2:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_3:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_4:
                CanRoll,
            LocationName.jungle_hijinxs_bunch_5:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_6:
                CanSlap & CanRoll,
            LocationName.jungle_hijinxs_balloon_2:
                CanRoll,
            LocationName.jungle_hijinxs_bunch_7:
                CanSlap & CanRoll,
            LocationName.jungle_hijinxs_bunch_8:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_9:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_10:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_11:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_12:
                True_(),
            LocationName.jungle_hijinxs_balloon_3:
                CanRoll & HasDiddy,
            LocationName.jungle_hijinxs_bunch_13:
                CanRoll & CanSlap & HasDiddy,
            LocationName.jungle_hijinxs_balloon_4:
                CanRoll & HasDiddy,
            LocationName.jungle_hijinxs_token_1:
                True_(),
            LocationName.jungle_hijinxs_bunch_14:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_15:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_16:
                True_(),
            LocationName.jungle_hijinxs_bunch_17:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_18:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_19:
                True_(),
            LocationName.jungle_hijinxs_balloon_5:
                HasRambi & HasTires & HasKannons,
            LocationName.jungle_hijinxs_balloon_6:
                HasRambi & HasTires & HasKannons,

            LocationName.ropey_rampage_clear:
                CanClimb,
            EventName.ropey_rampage_clear:
                CanClimb,
            LocationName.ropey_rampage_bonus_1:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_bonus_2:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_kong:
                CanClimb,
            LocationName.ropey_rampage_bunch_1:
                CanRoll,
            LocationName.ropey_rampage_bunch_2:
                CanRoll,
            LocationName.ropey_rampage_bunch_3:
                CanRoll,
            LocationName.ropey_rampage_bunch_4:
                CanSlap,
            LocationName.ropey_rampage_bunch_5:
                CanSlap,
            LocationName.ropey_rampage_bunch_6:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_7:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_8:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_9:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_token_1:
                CanClimb,
            LocationName.ropey_rampage_bunch_10:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_11:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_12:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_13:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_14:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_15:
                CanSlap & CanClimb & CanRoll,
            LocationName.ropey_rampage_token_2:
                HasTires & CanClimb,
            LocationName.ropey_rampage_bunch_16:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_17:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_18:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_19:
                CanSlap & CanClimb,

            LocationName.reptile_rumble_clear:
                HasTires,
            EventName.reptile_rumble_clear:
                HasTires,
            LocationName.reptile_rumble_bonus_1:
                CanCarry,
            LocationName.reptile_rumble_bonus_2:
                HasKannons & HasTires,
            LocationName.reptile_rumble_bonus_3:
                CanCarry & HasTires,
            LocationName.reptile_rumble_kong:
                HasTires,
            LocationName.reptile_rumble_bunch_1:
                CanSlap,
            LocationName.reptile_rumble_bunch_2:
                CanSlap,
            LocationName.reptile_rumble_bunch_3:
                CanSlap,
            LocationName.reptile_rumble_bunch_4:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_5:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_6:
                HasTires,
            LocationName.reptile_rumble_bunch_7:
                HasTires,
            LocationName.reptile_rumble_bunch_8:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_9:
                HasTires & CanSlap & CanCarry,
            LocationName.reptile_rumble_bunch_10:
                HasTires & CanSlap,
            LocationName.reptile_rumble_token_1:
                HasTires,
            LocationName.reptile_rumble_bunch_11:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_12:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_13:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_14:
                HasTires & CanSlap,

            LocationName.coral_capers_clear:
                CanSwim,
            EventName.coral_capers_clear:
                CanSwim,
            LocationName.coral_capers_kong:
                CanSwim,
            LocationName.coral_capers_bunch_1:
                CanSwim,
            LocationName.coral_capers_balloon_1:
                CanSwim,
            LocationName.coral_capers_bunch_2:
                CanSwim,
            LocationName.coral_capers_token_1:
                CanSwim,

            LocationName.barrel_cannon_canyon_clear:
                HasKannons,
            EventName.barrel_cannon_canyon_clear:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                CanCarry & HasKannons,
            LocationName.barrel_cannon_canyon_kong:
                HasKannons,
            LocationName.barrel_cannon_canyon_token_1:
                HasDiddy & CanRoll & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_1:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_2:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_3:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_4:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_token_2:
                HasKannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_6:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_7:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_8:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_9:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_10:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_11:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_12:
                CanSlap & HasKannons,

            LocationName.very_gnawty_lair_clear:
                HasBothKongs,
            LocationName.defeated_gnawty_1:
                HasBothKongs,

            LocationName.winky_walkway_clear:
                True_(),
            EventName.winky_walkway_clear:
                True_(),
            LocationName.winky_walkway_bonus_1:
                HasKannons,
            LocationName.winky_walkway_kong:
                HasKannons & HasWinky,
            LocationName.winky_walkway_bunch_1:
                CanSlap,
            LocationName.winky_walkway_bunch_2:
                CanSlap,
            LocationName.winky_walkway_bunch_3:
                CanSlap,
            LocationName.winky_walkway_bunch_4:
                CanSlap,
            LocationName.winky_walkway_token_1:
                HasWinky,
            LocationName.winky_walkway_bunch_5:
                CanSlap,

            LocationName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            EventName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_kong:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_1:
                CanSlap,
            LocationName.mine_cart_carnage_bunch_2:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_token_1:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_3:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_balloon_1:
                HasKannons & HasMinecart,

            LocationName.bouncy_bonanza_clear:
                HasTires,
            EventName.bouncy_bonanza_clear:
                HasTires,
            LocationName.bouncy_bonanza_bonus_1:
                CanCarry,
            LocationName.bouncy_bonanza_bonus_2:
                HasTires & HasKannons,
            LocationName.bouncy_bonanza_kong:
                HasTires,
            LocationName.bouncy_bonanza_token_1:
                HasTires,
            LocationName.bouncy_bonanza_bunch_1:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_2:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_3:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_4:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_5:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_6:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_7:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_8:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_9:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_10:
                HasTires & CanSlap,

            LocationName.stop_go_station_clear:
                HasSwitches & HasTires,
            EventName.stop_go_station_clear:
                HasSwitches & HasTires,
            LocationName.stop_go_station_bonus_1:
                HasSwitches & HasTires & CanCarry,
            LocationName.stop_go_station_bonus_2:
                HasSwitches & HasTires & HasKannons,
            LocationName.stop_go_station_kong:
                HasSwitches & HasTires & CanRoll,
            LocationName.stop_go_station_bunch_1:
                CanSlap,
            LocationName.stop_go_station_bunch_2:
                HasSwitches & CanSlap,
            LocationName.stop_go_station_bunch_3:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_token_1:
                HasSwitches & HasTires & CanRoll,
            LocationName.stop_go_station_bunch_4:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_5:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_6:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_7:
                HasSwitches & HasTires & CanSlap,

            LocationName.millstone_mayhem_clear:
                HasTires & (CanRoll | HasWinky),
            EventName.millstone_mayhem_clear:
                HasTires & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bonus_1:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bonus_2:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bonus_3:
                HasTires & CanCarry,
            LocationName.millstone_mayhem_kong:
                HasTires & HasKannons & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_1:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_2:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_3:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_4:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_5:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_6:
                HasTires & CanSlap & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_7:
                HasTires & CanSlap & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_8:
                HasTires & CanSlap & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_9:
                HasTires & CanSlap & (CanRoll | HasWinky),

            LocationName.necky_nuts_clear:
                HasBothKongs & HasTires,
            LocationName.defeated_necky_1:
                HasBothKongs & HasTires,

            LocationName.vulture_culture_clear:
                HasKannons,
            EventName.vulture_culture_clear:
                HasKannons,
            LocationName.vulture_culture_bonus_1:
                HasKannons & HasTires,
            LocationName.vulture_culture_bonus_2:
                HasKannons & CanCarry,
            LocationName.vulture_culture_bonus_3:
                HasKannons & CanCarry,
            LocationName.vulture_culture_kong:
                HasKannons & HasTires & CanCarry,
            LocationName.vulture_culture_bunch_1:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_2:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_3:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_4:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_5:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_6:
                HasKannons & CanSlap,

            LocationName.tree_top_town_clear:
                HasKannons & HasTires,
            EventName.tree_top_town_clear:
                HasKannons & HasTires,
            LocationName.tree_top_town_bonus_1:
                HasKannons,
            LocationName.tree_top_town_bonus_2:
                HasKannons,
            LocationName.tree_top_town_kong:
                HasKannons,
            LocationName.tree_top_town_bunch_1:
                CanSlap,
            LocationName.tree_top_town_bunch_2:
                HasKannons & CanSlap,
            LocationName.tree_top_town_bunch_3:
                HasKannons & CanSlap,
            LocationName.tree_top_town_bunch_4:
                HasKannons & CanSlap & HasTires,
            LocationName.tree_top_town_token_1:
                HasKannons & CanRoll & HasTires,

            LocationName.forest_frenzy_clear:
                CanClimb,
            EventName.forest_frenzy_clear:
                CanClimb,
            LocationName.forest_frenzy_bonus_1:
                CanClimb & HasKannons,
            LocationName.forest_frenzy_bonus_2:
                CanClimb & CanCarry,
            LocationName.forest_frenzy_kong:
                CanClimb & CanRoll,
            LocationName.forest_frenzy_bunch_1:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_2:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_3:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_4:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_5:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_balloon_1:
                CanClimb,

            LocationName.temple_tempest_clear:
                CanClimb & HasTires,
            EventName.temple_tempest_clear:
                CanClimb & HasTires,
            LocationName.temple_tempest_bonus_1:
                CanClimb & CanCarry,
            LocationName.temple_tempest_bonus_2:
                CanClimb & HasKannons,
            LocationName.temple_tempest_kong:
                CanClimb & HasTires & HasKannons,
            LocationName.temple_tempest_token_1:
                HasDiddy,
            LocationName.temple_tempest_bunch_1:
                CanSlap,
            LocationName.temple_tempest_bunch_2:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_3:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_4:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_5:
                CanClimb & HasTires & CanSlap,
            LocationName.temple_tempest_bunch_6:
                CanClimb & HasTires & CanSlap,
            LocationName.temple_tempest_bunch_7:
                CanClimb & HasTires,
            LocationName.temple_tempest_bunch_8:
                CanClimb & HasTires,

            LocationName.orang_utan_gang_clear:
                True_(),
            EventName.orang_utan_gang_clear:
                True_(),
            LocationName.orang_utan_gang_bonus_1:
                HasExpresso,
            LocationName.orang_utan_gang_bonus_2:
                CanCarry & HasExpresso,
            LocationName.orang_utan_gang_bonus_3:
                CanCarry,
            LocationName.orang_utan_gang_bonus_4:
                CanCarry,
            LocationName.orang_utan_gang_bonus_5:
                CanCarry,
            LocationName.orang_utan_gang_kong:
                CanCarry & CanRoll & HasTires,
            LocationName.orang_utan_gang_bunch_1:
                CanSlap,
            LocationName.orang_utan_gang_bunch_2:
                CanSlap,
            LocationName.orang_utan_gang_bunch_3:
                CanSlap,
            LocationName.orang_utan_gang_bunch_4:
                CanRoll,
            LocationName.orang_utan_gang_bunch_5:
                CanSlap,
            LocationName.orang_utan_gang_bunch_6:
                HasExpresso,
            LocationName.orang_utan_gang_token_1:
                HasTires & HasExpresso,
            LocationName.orang_utan_gang_bunch_7:
                CanSlap,
            LocationName.orang_utan_gang_bunch_8:
                HasExpresso,
            LocationName.orang_utan_gang_bunch_9:
                HasExpresso,

            LocationName.clam_city_clear:
                CanSwim & HasEnguarde,
            EventName.clam_city_clear:
                CanSwim & HasEnguarde,
            LocationName.clam_city_kong:
                CanSwim & HasEnguarde,
            LocationName.clam_city_bunch_1:
                CanSwim,
            LocationName.clam_city_bunch_2:
                CanSwim & HasEnguarde,
            LocationName.clam_city_token_1:
                CanSwim & HasEnguarde,

            LocationName.bumble_b_rumble_clear:
                HasBothKongs & CanCarry,
            LocationName.defeated_bumble_b:
                HasBothKongs & CanCarry,

            LocationName.snow_barrel_blast_clear:
                HasKannons,
            EventName.snow_barrel_blast_clear:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_1:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_2:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_3:
                HasKannons,
            LocationName.snow_barrel_blast_kong:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_1:
                CanSlap,
            LocationName.snow_barrel_blast_balloon_1:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_2:
                HasKannons & CanSlap,
            LocationName.snow_barrel_blast_bunch_3:
                HasKannons & CanSlap,
            LocationName.snow_barrel_blast_token_1:
                HasKannons,
            LocationName.snow_barrel_blast_balloon_2:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_4:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_5:
                HasKannons & CanSlap,

            LocationName.slipslide_ride_clear:
                CanClimb & HasKannons,
            EventName.slipslide_ride_clear:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bonus_1:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_2:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_kong:
                CanClimb & HasKannons & CanCarry,
            LocationName.slipslide_ride_bunch_1:
                CanClimb,
            LocationName.slipslide_ride_bunch_2:
                CanClimb & CanSlap,
            LocationName.slipslide_ride_bunch_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_4:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_5:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_6:
                CanClimb & HasKannons & CanCarry,
            LocationName.slipslide_ride_bunch_7:
                CanClimb & HasKannons & CanCarry,
            LocationName.slipslide_ride_bunch_8:
                CanClimb & HasKannons & CanSlap,
            LocationName.slipslide_ride_bunch_9:
                CanClimb & HasKannons & CanSlap,
            LocationName.slipslide_ride_token_1:
                CanClimb & HasKannons,

            LocationName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            EventName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            LocationName.ice_age_alley_bonus_1:
                CanClimb & HasKannons,
            LocationName.ice_age_alley_bonus_2:
                HasExpresso & HasKannons,
            LocationName.ice_age_alley_kong:
                CanRoll & HasExpresso,
            LocationName.ice_age_alley_bunch_1:
                CanSlap,
            LocationName.ice_age_alley_bunch_2:
                ((CanClimb & HasKannons) | HasExpresso) & CanSlap,
            LocationName.ice_age_alley_bunch_3:
                ((CanClimb & HasKannons) | HasExpresso) & CanRoll,

            LocationName.croctopus_chase_clear:
                CanSwim,
            EventName.croctopus_chase_clear:
                CanSwim,
            LocationName.croctopus_chase_kong:
                CanSwim,
            LocationName.croctopus_chase_bunch_1:
                CanSwim,
            LocationName.croctopus_chase_token_1:
                CanSwim,
            LocationName.croctopus_chase_token_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_3:
                CanSwim,
            LocationName.croctopus_chase_bunch_4:
                CanSwim,
            LocationName.croctopus_chase_bunch_5:
                CanSwim,
            LocationName.croctopus_chase_balloon_1:
                CanSwim,

            LocationName.torchlight_trouble_clear:
                HasDonkey & HasSquawks,
            EventName.torchlight_trouble_clear:
                HasDonkey & HasSquawks,
            LocationName.torchlight_trouble_bonus_1:
                HasDonkey & HasSquawks & CanCarry,
            LocationName.torchlight_trouble_bonus_2:
                HasDonkey & HasSquawks & CanCarry,
            LocationName.torchlight_trouble_kong:
                HasDonkey & HasSquawks & CanCarry & CanRoll & HasTires,
            LocationName.torchlight_trouble_bunch_1:
                HasDonkey & HasSquawks & CanSlap,

            LocationName.rope_bridge_rumble_clear:
                HasTires,
            EventName.rope_bridge_rumble_clear:
                HasTires,
            LocationName.rope_bridge_rumble_bonus_1:
                HasTires & HasKannons,
            LocationName.rope_bridge_rumble_bonus_2:
                HasTires & HasKannons,
            LocationName.rope_bridge_rumble_kong:
                HasTires & CanRoll,
            LocationName.rope_bridge_rumble_bunch_1:
                HasTires & CanRoll,

            LocationName.really_gnawty_rampage_clear:
                HasBothKongs,
            LocationName.defeated_gnawty_2:
                HasBothKongs,

            LocationName.oil_drum_alley_clear:
                HasTires & HasKannons,
            EventName.oil_drum_alley_clear:
                HasTires & HasKannons,
            LocationName.oil_drum_alley_bonus_1:
                CanClimb & CanCarry & HasKannons,
            LocationName.oil_drum_alley_bonus_2:
                HasTires & CanCarry,
            LocationName.oil_drum_alley_bonus_3:
                HasTires & CanCarry,
            LocationName.oil_drum_alley_bonus_4:
                HasTires & (CanCarry | HasRambi) & HasKannons,
            LocationName.oil_drum_alley_kong:
                HasTires & CanRoll & HasKannons & (CanCarry & HasRambi),
            LocationName.oil_drum_alley_bunch_1:
                HasTires & HasKannons,
            LocationName.oil_drum_alley_bunch_2:
                HasTires & HasKannons,

            LocationName.trick_track_trek_clear:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            EventName.trick_track_trek_clear:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_bonus_1:
                HasPlatforms & HasKannons & CanRoll,
            LocationName.trick_track_trek_bonus_2:
                HasPlatforms & HasKannons,
            LocationName.trick_track_trek_bonus_3:
                HasPlatforms & HasKannons & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_kong:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_bunch_1:
                HasPlatforms,
            LocationName.trick_track_trek_token_1:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),

            LocationName.elevator_antics_clear:
                CanClimb & HasTires,
            EventName.elevator_antics_clear:
                CanClimb & HasTires,
            LocationName.elevator_antics_bonus_1:
                CanClimb & CanRoll,
            LocationName.elevator_antics_bonus_2:
                CanClimb,
            LocationName.elevator_antics_bonus_3:
                CanClimb & HasTires,
            LocationName.elevator_antics_kong:
                CanClimb & HasKannons,
            LocationName.elevator_antics_bunch_1:
                True_(),
            LocationName.elevator_antics_bunch_2:
                CanClimb,
            LocationName.elevator_antics_bunch_3:
                CanClimb,

            LocationName.poison_pond_clear:
                CanSwim & HasEnguarde,
            EventName.poison_pond_clear:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_kong:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_1:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_2:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_3:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_4:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_5:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_token_1:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_token_2:
                CanSwim & HasEnguarde,
            LocationName.poison_pond_bunch_6:
                CanSwim & HasEnguarde,

            LocationName.mine_cart_madness_clear:
                HasMinecart,
            EventName.mine_cart_madness_clear:
                HasMinecart,
            LocationName.mine_cart_madness_bonus_1:
                HasMinecart & CanClimb & HasKannons,
            LocationName.mine_cart_madness_bonus_2:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_bonus_3:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_kong:
                HasMinecart & HasTires,
            LocationName.mine_cart_madness_token_1:
                HasMinecart,
            LocationName.mine_cart_madness_bunch_1:
                HasMinecart,

            LocationName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            EventName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            LocationName.blackout_basement_bonus_1:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_bonus_2:
                CanClimb & HasTires & HasPlatforms & CanCarry & HasKannons,
            LocationName.blackout_basement_kong:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_token_1:
                CanRoll,
            LocationName.blackout_basement_bunch_1:
                CanClimb & HasTires & HasPlatforms,

            LocationName.boss_dumb_drum_clear:
                HasBothKongs,
            LocationName.defeated_boss_dumb_drum:
                HasBothKongs,

            LocationName.tanked_up_trouble_clear:
                HasPlatforms & HasTires & HasKannons,
            EventName.tanked_up_trouble_clear:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bonus_1:
                HasPlatforms & HasKannons,
            LocationName.tanked_up_trouble_kong:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bunch_1:
                HasPlatforms,
            LocationName.tanked_up_trouble_bunch_2:
                HasPlatforms,
            LocationName.tanked_up_trouble_token_1:
                HasPlatforms & HasKannons,
            LocationName.tanked_up_trouble_bunch_3:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bunch_4:
                HasPlatforms & HasTires & HasKannons,

            LocationName.manic_mincers_clear:
                HasTires,
            EventName.manic_mincers_clear:
                HasTires,
            LocationName.manic_mincers_bonus_1:
                CanCarry | HasRambi,
            LocationName.manic_mincers_bonus_2:
                CanCarry | HasRambi,
            LocationName.manic_mincers_kong:
                True_(),
            LocationName.manic_mincers_bunch_1:
                True_(),
            LocationName.manic_mincers_bunch_2:
                True_(),
            LocationName.manic_mincers_token_1:
                CanRoll,

            LocationName.misty_mine_clear:
                CanClimb,
            EventName.misty_mine_clear:
                CanClimb,
            LocationName.misty_mine_bonus_1:
                CanClimb,
            LocationName.misty_mine_bonus_2:
                CanClimb & CanCarry,
            LocationName.misty_mine_kong:
                CanClimb,
            LocationName.misty_mine_token_1:
                CanClimb & CanCarry,
            LocationName.misty_mine_bunch_1:
                CanCarry,
            LocationName.misty_mine_bunch_2:
                CanClimb,
            LocationName.misty_mine_token_2:
                CanClimb & HasExpresso,

            LocationName.loopy_lights_clear:
                HasSwitches & HasTires,
            EventName.loopy_lights_clear:
                HasSwitches & HasTires,
            LocationName.loopy_lights_bonus_1:
                HasSwitches & HasKannons,
            LocationName.loopy_lights_bonus_2:
                HasSwitches & HasTires & CanCarry,
            LocationName.loopy_lights_kong:
                HasSwitches & HasTires & HasKannons & CanRoll & CanCarry,
            LocationName.loopy_lights_bunch_1:
                HasSwitches & HasTires,
            LocationName.loopy_lights_bunch_2:
                HasSwitches & HasTires,

            LocationName.platform_perils_clear:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            EventName.platform_perils_clear:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            LocationName.platform_perils_bonus_1:
                HasPlatforms & CanCarry & HasKannons,
            LocationName.platform_perils_bonus_2:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires & HasKannons,
            LocationName.platform_perils_kong:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            LocationName.platform_perils_token_1:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll),
            LocationName.platform_perils_bunch_1:
                HasPlatforms & CanCarry & HasTires,

            LocationName.necky_revenge_clear:
                HasBothKongs & HasTires,
            LocationName.defeated_necky_2:
                HasBothKongs & HasTires,
        }

class DKCLooseRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                True_(),
            EventName.jungle_hijinxs_clear:
                True_(),
            LocationName.jungle_hijinxs_bonus_1:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_bonus_2:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_kong:
                True_(),
            LocationName.jungle_hijinxs_balloon_1:
                HasTires,
            LocationName.jungle_hijinxs_bunch_1:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_2:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_3:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_4:
                HasRambi | CanRoll,
            LocationName.jungle_hijinxs_bunch_5:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_6:
                CanSlap,
            LocationName.jungle_hijinxs_balloon_2:
                CanRoll,
            LocationName.jungle_hijinxs_bunch_7:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_8:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_9:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_10:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_11:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_12:
                True_(),
            LocationName.jungle_hijinxs_balloon_3:
                CanRoll & HasDiddy,
            LocationName.jungle_hijinxs_bunch_13:
                CanRoll & CanSlap,
            LocationName.jungle_hijinxs_balloon_4:
                CanRoll & HasDiddy,
            LocationName.jungle_hijinxs_token_1:
                True_(),
            LocationName.jungle_hijinxs_bunch_14:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_15:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_16:
                True_(),
            LocationName.jungle_hijinxs_bunch_17:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_18:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_19:
                True_(),
            LocationName.jungle_hijinxs_balloon_5:
                HasRambi & HasTires,
            LocationName.jungle_hijinxs_balloon_6:
                HasRambi & HasTires,

            LocationName.ropey_rampage_clear:
                CanClimb,
            EventName.ropey_rampage_clear:
                CanClimb,
            LocationName.ropey_rampage_bonus_1:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_bonus_2:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_kong:
                CanClimb,
            LocationName.ropey_rampage_bunch_1:
                True_(),
            LocationName.ropey_rampage_bunch_2:
                True_(),
            LocationName.ropey_rampage_bunch_3:
                True_(),
            LocationName.ropey_rampage_bunch_4:
                CanSlap,
            LocationName.ropey_rampage_bunch_5:
                CanSlap,
            LocationName.ropey_rampage_bunch_6:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_7:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_8:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_9:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_token_1:
                CanClimb,
            LocationName.ropey_rampage_bunch_10:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_11:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_12:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_13:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_14:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_15:
                CanSlap & CanClimb & (CanRoll | HasDiddy),
            LocationName.ropey_rampage_token_2:
                HasTires & CanClimb,
            LocationName.ropey_rampage_bunch_16:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_17:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_18:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_19:
                CanSlap & CanClimb,

            LocationName.reptile_rumble_clear:
                HasTires | HasDiddy,
            EventName.reptile_rumble_clear:
                HasTires | HasDiddy,
            LocationName.reptile_rumble_bonus_1:
                CanCarry,
            LocationName.reptile_rumble_bonus_2:
                HasKannons & (HasTires | HasDiddy),
            LocationName.reptile_rumble_bonus_3:
                CanCarry & HasTires,
            LocationName.reptile_rumble_kong:
                HasTires | HasDiddy,
            LocationName.reptile_rumble_bunch_1:
                CanSlap,
            LocationName.reptile_rumble_bunch_2:
                CanSlap,
            LocationName.reptile_rumble_bunch_3:
                CanSlap,
            LocationName.reptile_rumble_bunch_4:
                (HasTires | HasDiddy) & CanSlap,
            LocationName.reptile_rumble_bunch_5:
                (HasTires | HasDiddy) & CanSlap,
            LocationName.reptile_rumble_bunch_6:
                HasTires,
            LocationName.reptile_rumble_bunch_7:
                HasTires,
            LocationName.reptile_rumble_bunch_8:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_9:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_10:
                HasTires & CanSlap,
            LocationName.reptile_rumble_token_1:
                HasTires,
            LocationName.reptile_rumble_bunch_11:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_12:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_13:
                HasTires & CanSlap,
            LocationName.reptile_rumble_bunch_14:
                HasTires & CanSlap,

            LocationName.coral_capers_clear:
                CanSwim,
            EventName.coral_capers_clear:
                CanSwim,
            LocationName.coral_capers_kong:
                CanSwim,
            LocationName.coral_capers_bunch_1:
                CanSwim,
            LocationName.coral_capers_balloon_1:
                CanSwim,
            LocationName.coral_capers_bunch_2:
                CanSwim,
            LocationName.coral_capers_token_1:
                CanSwim,

            LocationName.barrel_cannon_canyon_clear:
                HasKannons,
            EventName.barrel_cannon_canyon_clear:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                CanCarry & HasKannons,
            LocationName.barrel_cannon_canyon_kong:
                HasKannons,
            LocationName.barrel_cannon_canyon_token_1:
                CanRoll & (HasDiddy | (HasKannons & HasDonkey)),
            LocationName.barrel_cannon_canyon_bunch_1:
                CanSlap & (HasKannons | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_2:
                CanSlap & (HasKannons | (HasDiddy & CanRoll)),
            LocationName.barrel_cannon_canyon_bunch_3:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_4:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_token_2:
                HasKannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_6:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_7:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_8:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_9:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_10:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_11:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_12:
                CanSlap & HasKannons,

            LocationName.very_gnawty_lair_clear:
                True_(),
            LocationName.defeated_gnawty_1:
                True_(),

            LocationName.winky_walkway_clear:
                True_(),
            EventName.winky_walkway_clear:
                True_(),
            LocationName.winky_walkway_bonus_1:
                HasKannons,
            LocationName.winky_walkway_kong:
                HasKannons,
            LocationName.winky_walkway_bunch_1:
                CanSlap,
            LocationName.winky_walkway_bunch_2:
                CanSlap,
            LocationName.winky_walkway_bunch_3:
                CanSlap,
            LocationName.winky_walkway_bunch_4:
                CanSlap,
            LocationName.winky_walkway_token_1:
                HasWinky,
            LocationName.winky_walkway_bunch_5:
                CanSlap,

            LocationName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            EventName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_kong:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_1:
                CanSlap,
            LocationName.mine_cart_carnage_bunch_2:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_token_1:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_3:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_balloon_1:
                HasKannons & HasMinecart,

            LocationName.bouncy_bonanza_clear:
                HasTires,
            EventName.bouncy_bonanza_clear:
                HasTires,
            LocationName.bouncy_bonanza_bonus_1:
                CanCarry,
            LocationName.bouncy_bonanza_bonus_2:
                HasTires & HasKannons,
            LocationName.bouncy_bonanza_kong:
                HasTires,
            LocationName.bouncy_bonanza_token_1:
                HasTires,
            LocationName.bouncy_bonanza_bunch_1:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_2:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_3:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_4:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_5:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_6:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_7:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_8:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_9:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_10:
                HasTires & CanSlap,

            LocationName.stop_go_station_clear:
                HasSwitches & HasTires,
            EventName.stop_go_station_clear:
                HasSwitches & HasTires,
            LocationName.stop_go_station_bonus_1:
                HasSwitches & HasTires & CanCarry,
            LocationName.stop_go_station_bonus_2:
                HasSwitches & HasTires & HasKannons,
            LocationName.stop_go_station_kong:
                HasSwitches & HasTires & CanRoll,
            LocationName.stop_go_station_bunch_1:
                CanSlap,
            LocationName.stop_go_station_bunch_2:
                HasSwitches & CanSlap,
            LocationName.stop_go_station_bunch_3:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_token_1:
                HasSwitches & HasTires & CanRoll,
            LocationName.stop_go_station_bunch_4:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_5:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_6:
                HasSwitches & HasTires & CanSlap,
            LocationName.stop_go_station_bunch_7:
                HasSwitches & HasTires & CanSlap,

            LocationName.millstone_mayhem_clear:
                HasTires,
            EventName.millstone_mayhem_clear:
                HasTires,
            LocationName.millstone_mayhem_bonus_1:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bonus_2:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bonus_3:
                HasTires & CanCarry,
            LocationName.millstone_mayhem_kong:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bunch_1:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_2:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_3:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_4:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_5:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_6:
                HasTires & CanSlap,
            LocationName.millstone_mayhem_bunch_7:
                HasTires & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_8:
                HasTires & (CanRoll | HasWinky),
            LocationName.millstone_mayhem_bunch_9:
                HasTires & CanSlap,

            LocationName.necky_nuts_clear:
                HasTires,
            LocationName.defeated_necky_1:
                HasTires,

            LocationName.vulture_culture_clear:
                HasKannons,
            EventName.vulture_culture_clear:
                HasKannons,
            LocationName.vulture_culture_bonus_1:
                HasKannons & HasTires,
            LocationName.vulture_culture_bonus_2:
                HasKannons & CanCarry,
            LocationName.vulture_culture_bonus_3:
                HasKannons & CanCarry,
            LocationName.vulture_culture_kong:
                HasKannons & HasTires & CanCarry,
            LocationName.vulture_culture_bunch_1:
                (HasKannons | HasDiddy) & CanSlap,
            LocationName.vulture_culture_bunch_2:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_3:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_4:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_5:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_6:
                HasKannons & CanSlap,

            LocationName.tree_top_town_clear:
                HasKannons & HasDiddy,
            EventName.tree_top_town_clear:
                HasKannons & HasDiddy,
            LocationName.tree_top_town_bonus_1:
                HasKannons,
            LocationName.tree_top_town_bonus_2:
                HasKannons,
            LocationName.tree_top_town_kong:
                HasKannons,
            LocationName.tree_top_town_bunch_1:
                CanSlap,
            LocationName.tree_top_town_bunch_2:
                HasKannons & CanSlap,
            LocationName.tree_top_town_bunch_3:
                HasKannons & CanSlap,
            LocationName.tree_top_town_bunch_4:
                HasKannons & CanSlap & HasTires,
            LocationName.tree_top_town_token_1:
                HasKannons & CanRoll & HasTires,

            LocationName.forest_frenzy_clear:
                CanClimb,
            EventName.forest_frenzy_clear:
                CanClimb,
            LocationName.forest_frenzy_bonus_1:
                CanClimb & HasKannons,
            LocationName.forest_frenzy_bonus_2:
                CanClimb & CanCarry,
            LocationName.forest_frenzy_kong:
                CanClimb & CanRoll,
            LocationName.forest_frenzy_bunch_1:
                (CanClimb | (HasDiddy & CanRoll)) & CanSlap,
            LocationName.forest_frenzy_bunch_2:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_3:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_4:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_bunch_5:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_balloon_1:
                CanClimb,

            LocationName.temple_tempest_clear:
                CanClimb & HasTires,
            EventName.temple_tempest_clear:
                CanClimb & HasTires,
            LocationName.temple_tempest_bonus_1:
                (CanClimb | (HasDiddy & CanRoll)) & CanCarry,
            LocationName.temple_tempest_bonus_2:
                CanClimb & HasKannons,
            LocationName.temple_tempest_kong:
                CanClimb & HasTires & HasKannons,
            LocationName.temple_tempest_token_1:
                True_(),
            LocationName.temple_tempest_bunch_1:
                CanSlap,
            LocationName.temple_tempest_bunch_2:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_3:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_4:
                CanClimb & CanSlap,
            LocationName.temple_tempest_bunch_5:
                CanClimb & HasTires & CanSlap,
            LocationName.temple_tempest_bunch_6:
                CanClimb & HasTires & CanSlap,
            LocationName.temple_tempest_bunch_7:
                CanClimb & HasTires,
            LocationName.temple_tempest_bunch_8:
                CanClimb & HasTires,

            LocationName.orang_utan_gang_clear:
                True_(),
            EventName.orang_utan_gang_clear:
                True_(),
            LocationName.orang_utan_gang_bonus_1:
                HasExpresso,
            LocationName.orang_utan_gang_bonus_2:
                CanCarry & (HasExpresso | (HasDiddy & CanRoll)),
            LocationName.orang_utan_gang_bonus_3:
                CanCarry,
            LocationName.orang_utan_gang_bonus_4:
                CanCarry,
            LocationName.orang_utan_gang_bonus_5:
                True_(),
            LocationName.orang_utan_gang_kong:
                CanCarry & CanRoll & HasTires,
            LocationName.orang_utan_gang_bunch_1:
                CanSlap,
            LocationName.orang_utan_gang_bunch_2:
                CanCarry | CanSlap,
            LocationName.orang_utan_gang_bunch_3:
                CanSlap,
            LocationName.orang_utan_gang_bunch_4:
                CanRoll,
            LocationName.orang_utan_gang_bunch_5:
                CanSlap,
            LocationName.orang_utan_gang_bunch_6:
                HasExpresso | (HasDiddy & CanRoll),
            LocationName.orang_utan_gang_token_1:
                HasTires & HasExpresso,
            LocationName.orang_utan_gang_bunch_7:
                CanSlap,
            LocationName.orang_utan_gang_bunch_8:
                True_(),
            LocationName.orang_utan_gang_bunch_9:
                True_(),

            LocationName.clam_city_clear:
                CanSwim,
            EventName.clam_city_clear:
                CanSwim,
            LocationName.clam_city_kong:
                CanSwim,
            LocationName.clam_city_bunch_1:
                CanSwim,
            LocationName.clam_city_bunch_2:
                CanSwim,
            LocationName.clam_city_token_1:
                CanSwim,

            LocationName.bumble_b_rumble_clear:
                CanCarry,
            LocationName.defeated_bumble_b:
                CanCarry,

            LocationName.snow_barrel_blast_clear:
                HasKannons,
            EventName.snow_barrel_blast_clear:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_1:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_2:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_3:
                HasKannons,
            LocationName.snow_barrel_blast_kong:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_1:
                HasKannons | CanSlap,
            LocationName.snow_barrel_blast_balloon_1:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_2:
                HasKannons & CanSlap,
            LocationName.snow_barrel_blast_bunch_3:
                HasKannons & CanSlap,
            LocationName.snow_barrel_blast_token_1:
                HasKannons,
            LocationName.snow_barrel_blast_balloon_2:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_4:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_5:
                HasKannons & CanSlap,

            LocationName.slipslide_ride_clear:
                CanClimb & HasKannons,
            EventName.slipslide_ride_clear:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bonus_1:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_2:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_kong:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_1:
                CanClimb,
            LocationName.slipslide_ride_bunch_2:
                CanClimb & CanSlap,
            LocationName.slipslide_ride_bunch_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_4:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_5:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_6:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_7:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_8:
                CanClimb & HasKannons & CanSlap,
            LocationName.slipslide_ride_bunch_9:
                CanClimb & HasKannons & CanSlap,
            LocationName.slipslide_ride_token_1:
                CanClimb & HasKannons,

            LocationName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            EventName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            LocationName.ice_age_alley_bonus_1:
                (CanClimb | HasExpresso) & HasKannons,
            LocationName.ice_age_alley_bonus_2:
                HasExpresso & HasKannons,
            LocationName.ice_age_alley_kong:
                CanRoll & HasExpresso,
            LocationName.ice_age_alley_bunch_1:
                CanSlap,
            LocationName.ice_age_alley_bunch_2:
                ((CanClimb & HasKannons) | HasExpresso) & CanSlap,
            LocationName.ice_age_alley_bunch_3:
                (CanClimb & HasKannons) | HasExpresso,

            LocationName.croctopus_chase_clear:
                CanSwim,
            EventName.croctopus_chase_clear:
                CanSwim,
            LocationName.croctopus_chase_kong:
                CanSwim,
            LocationName.croctopus_chase_bunch_1:
                CanSwim,
            LocationName.croctopus_chase_token_1:
                CanSwim,
            LocationName.croctopus_chase_token_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_3:
                CanSwim,
            LocationName.croctopus_chase_bunch_4:
                CanSwim,
            LocationName.croctopus_chase_bunch_5:
                CanSwim,
            LocationName.croctopus_chase_balloon_1:
                CanSwim,

            LocationName.torchlight_trouble_clear:
                HasSquawks,
            EventName.torchlight_trouble_clear:
                HasSquawks,
            LocationName.torchlight_trouble_bonus_1:
                HasSquawks & CanCarry,
            LocationName.torchlight_trouble_bonus_2:
                HasSquawks & CanCarry,
            LocationName.torchlight_trouble_kong:
                HasSquawks & CanCarry & CanRoll,
            LocationName.torchlight_trouble_bunch_1:
                HasSquawks & CanSlap,

            LocationName.rope_bridge_rumble_clear:
                HasTires,
            EventName.rope_bridge_rumble_clear:
                HasTires,
            LocationName.rope_bridge_rumble_bonus_1:
                HasKannons,
            LocationName.rope_bridge_rumble_bonus_2:
                HasTires & HasKannons,
            LocationName.rope_bridge_rumble_kong:
                HasTires & CanRoll,
            LocationName.rope_bridge_rumble_bunch_1:
                HasTires & CanRoll,

            LocationName.really_gnawty_rampage_clear:
                True_(),
            LocationName.defeated_gnawty_2:
                True_(),

            LocationName.oil_drum_alley_clear:
                HasTires & HasKannons,
            EventName.oil_drum_alley_clear:
                HasTires & HasKannons,
            LocationName.oil_drum_alley_bonus_1:
                CanClimb & CanCarry & HasKannons,
            LocationName.oil_drum_alley_bonus_2:
                HasTires & CanCarry,
            LocationName.oil_drum_alley_bonus_3:
                HasTires & CanCarry,
            LocationName.oil_drum_alley_bonus_4:
                (
                    (
                    (HasTires & HasRambi) |
                    (HasTires & CanCarry) |
                    (CanRoll & CanCarry)
                    )
                & HasKannons),
            LocationName.oil_drum_alley_kong:
                HasTires & CanRoll & HasKannons & (CanCarry | HasRambi),
            LocationName.oil_drum_alley_bunch_1:
                HasTires & HasKannons,
            LocationName.oil_drum_alley_bunch_2:
                HasTires & HasKannons,

            LocationName.trick_track_trek_clear:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            EventName.trick_track_trek_clear:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_bonus_1:
                HasPlatforms & HasKannons & CanRoll,
            LocationName.trick_track_trek_bonus_2:
                HasPlatforms & HasKannons,
            LocationName.trick_track_trek_bonus_3:
                HasPlatforms & HasKannons & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_kong:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),
            LocationName.trick_track_trek_bunch_1:
                HasPlatforms,
            LocationName.trick_track_trek_token_1:
                HasPlatforms & (HasDonkey | (HasDiddy & CanRoll)),

            LocationName.elevator_antics_clear:
                CanClimb & HasTires,
            EventName.elevator_antics_clear:
                CanClimb & HasTires,
            LocationName.elevator_antics_bonus_1:
                CanClimb & CanRoll,
            LocationName.elevator_antics_bonus_2:
                CanClimb,
            LocationName.elevator_antics_bonus_3:
                CanClimb & HasTires,
            LocationName.elevator_antics_kong:
                CanClimb & HasKannons,
            LocationName.elevator_antics_bunch_1:
                True_(),
            LocationName.elevator_antics_bunch_2:
                CanClimb,
            LocationName.elevator_antics_bunch_3:
                CanClimb,

            LocationName.poison_pond_clear:
                CanSwim & (HasEnguarde | HasBothKongs),
            EventName.poison_pond_clear:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_kong:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_1:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_2:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_3:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_4:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_5:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_token_1:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_token_2:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_6:
                CanSwim & (HasEnguarde | HasBothKongs),

            LocationName.mine_cart_madness_clear:
                HasMinecart,
            EventName.mine_cart_madness_clear:
                HasMinecart,
            LocationName.mine_cart_madness_bonus_1:
                HasMinecart & CanClimb & HasKannons,
            LocationName.mine_cart_madness_bonus_2:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_bonus_3:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_kong:
                HasMinecart & (HasTires | HasDonkey),
            LocationName.mine_cart_madness_token_1:
                HasMinecart,
            LocationName.mine_cart_madness_bunch_1:
                HasMinecart,

            LocationName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            EventName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            LocationName.blackout_basement_bonus_1:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_bonus_2:
                CanClimb & HasTires & HasPlatforms & CanCarry & HasKannons,
            LocationName.blackout_basement_kong:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_token_1:
                CanRoll,
            LocationName.blackout_basement_bunch_1:
                CanClimb & HasTires & HasPlatforms,

            LocationName.boss_dumb_drum_clear:
                (HasDiddy & CanRoll) | HasDonkey,
            LocationName.defeated_boss_dumb_drum:
                (HasDiddy & CanRoll) | HasDonkey,

            LocationName.tanked_up_trouble_clear:
                HasPlatforms & HasTires & HasKannons,
            EventName.tanked_up_trouble_clear:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bonus_1:
                HasPlatforms & HasKannons,
            LocationName.tanked_up_trouble_kong:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bunch_1:
                HasPlatforms,
            LocationName.tanked_up_trouble_bunch_2:
                HasPlatforms,
            LocationName.tanked_up_trouble_token_1:
                HasPlatforms & HasKannons,
            LocationName.tanked_up_trouble_bunch_3:
                HasPlatforms & HasTires & HasKannons,
            LocationName.tanked_up_trouble_bunch_4:
                HasPlatforms & HasTires & HasKannons,

            LocationName.manic_mincers_clear:
                HasTires,
            EventName.manic_mincers_clear:
                HasTires,
            LocationName.manic_mincers_bonus_1:
                CanCarry | HasRambi,
            LocationName.manic_mincers_bonus_2:
                CanCarry | HasRambi,
            LocationName.manic_mincers_kong:
                True_(),
            LocationName.manic_mincers_bunch_1:
                True_(),
            LocationName.manic_mincers_bunch_2:
                True_(),
            LocationName.manic_mincers_token_1:
                True_(),

            LocationName.misty_mine_clear:
                CanClimb,
            EventName.misty_mine_clear:
                CanClimb,
            LocationName.misty_mine_bonus_1:
                CanClimb,
            LocationName.misty_mine_bonus_2:
                CanClimb & CanCarry,
            LocationName.misty_mine_kong:
                CanClimb,
            LocationName.misty_mine_token_1:
                CanCarry,
            LocationName.misty_mine_bunch_1:
                CanCarry,
            LocationName.misty_mine_bunch_2:
                CanClimb,
            LocationName.misty_mine_token_2:
                CanClimb & (HasExpresso | CanRoll),

            LocationName.loopy_lights_clear:
                HasSwitches & HasTires,
            EventName.loopy_lights_clear:
                HasSwitches & HasTires,
            LocationName.loopy_lights_bonus_1:
                HasSwitches & HasKannons,
            LocationName.loopy_lights_bonus_2:
                HasSwitches & HasTires & CanCarry,
            LocationName.loopy_lights_kong:
                HasSwitches & HasTires & HasKannons & CanRoll & CanCarry,
            LocationName.loopy_lights_bunch_1:
                HasSwitches & HasTires,
            LocationName.loopy_lights_bunch_2:
                HasSwitches & HasTires,

            LocationName.platform_perils_clear:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            EventName.platform_perils_clear:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            LocationName.platform_perils_bonus_1:
                HasPlatforms & CanCarry & HasKannons,
            LocationName.platform_perils_bonus_2:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires & HasKannons,
            LocationName.platform_perils_kong:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll) & HasTires,
            LocationName.platform_perils_token_1:
                HasPlatforms & CanCarry & (HasDonkey | CanRoll),
            LocationName.platform_perils_bunch_1:
                HasPlatforms & CanCarry & HasTires,

            LocationName.necky_revenge_clear:
                HasTires,
            LocationName.defeated_necky_2:
                HasTires,
        }

    def set_dkc_rules(self) -> None:
        super().set_dkc_rules()


class DKCExpertRules(DKCRules):
    def __init__(self, world: "DKCWorld") -> None:
        super().__init__(world)

      
        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                True_(),
            EventName.jungle_hijinxs_clear:
                True_(),
            LocationName.jungle_hijinxs_bonus_1:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_bonus_2:
                HasRambi | CanCarry,
            LocationName.jungle_hijinxs_kong:
                True_(),
            LocationName.jungle_hijinxs_balloon_1:
                HasTires,
            LocationName.jungle_hijinxs_bunch_1:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_2:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_3:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_4:
                True_(),
            LocationName.jungle_hijinxs_bunch_5:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_6:
                CanSlap,
            LocationName.jungle_hijinxs_balloon_2:
                True_(),
            LocationName.jungle_hijinxs_bunch_7:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_8:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_9:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_10:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_11:
                CanSlap,
            LocationName.jungle_hijinxs_bunch_12:
                True_(),
            LocationName.jungle_hijinxs_balloon_3:
                (CanRoll & HasDiddy) | HasRambi,
            LocationName.jungle_hijinxs_bunch_13:
                CanRoll & CanSlap,
            LocationName.jungle_hijinxs_balloon_4:
                (CanRoll & HasDiddy) | HasRambi,
            LocationName.jungle_hijinxs_token_1:
                True_(),
            LocationName.jungle_hijinxs_bunch_14:
                CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_15:
                HasRambi | CanSlap,
            LocationName.jungle_hijinxs_bunch_16:
                True_(),
            LocationName.jungle_hijinxs_bunch_17:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_18:
                HasRambi | CanSlap | HasDiddy,
            LocationName.jungle_hijinxs_bunch_19:
                True_(),
            LocationName.jungle_hijinxs_balloon_5:
                HasRambi & HasTires,
            LocationName.jungle_hijinxs_balloon_6:
                HasRambi & HasTires,

            LocationName.ropey_rampage_clear:
                CanClimb,
            EventName.ropey_rampage_clear:
                CanClimb,
            LocationName.ropey_rampage_bonus_1:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_bonus_2:
                CanClimb & HasKannons,
            LocationName.ropey_rampage_kong:
                CanClimb,
            LocationName.ropey_rampage_bunch_1:
                True_(),
            LocationName.ropey_rampage_bunch_2:
                True_(),
            LocationName.ropey_rampage_bunch_3:
                True_(),
            LocationName.ropey_rampage_bunch_4:
                CanSlap | HasDiddy,
            LocationName.ropey_rampage_bunch_5:
                CanSlap,
            LocationName.ropey_rampage_bunch_6:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_7:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_8:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_9:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_token_1:
                (CanClimb | HasBothKongs) | (HasDiddy & CanRoll),
            LocationName.ropey_rampage_bunch_10:
                (CanSlap & CanClimb) | HasBothKongs,
            LocationName.ropey_rampage_bunch_11:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_12:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_13:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.ropey_rampage_bunch_14:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.ropey_rampage_bunch_15:
                CanSlap & CanClimb & (CanRoll | HasDiddy),
            LocationName.ropey_rampage_token_2:
                CanClimb,
            LocationName.ropey_rampage_bunch_16:
                CanSlap & CanClimb,
            LocationName.ropey_rampage_bunch_17:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_18:
                CanClimb & CanRoll,
            LocationName.ropey_rampage_bunch_19:
                CanClimb & (CanSlap | HasDiddy),

            LocationName.reptile_rumble_clear:
                HasTires | HasDiddy,
            EventName.reptile_rumble_clear:
                HasTires | HasDiddy,
            LocationName.reptile_rumble_bonus_1:
                CanCarry,
            LocationName.reptile_rumble_bonus_2:
                HasKannons,
            LocationName.reptile_rumble_bonus_3:
                CanCarry & HasTires,
            LocationName.reptile_rumble_kong:
                HasTires | HasDiddy,
            LocationName.reptile_rumble_bunch_1:
                CanSlap | HasDiddy,
            LocationName.reptile_rumble_bunch_2:
                CanSlap | HasDiddy,
            LocationName.reptile_rumble_bunch_3:
                CanSlap | HasDiddy,
            LocationName.reptile_rumble_bunch_4:
                CanSlap,
            LocationName.reptile_rumble_bunch_5:
                CanSlap | HasDiddy,
            LocationName.reptile_rumble_bunch_6:
                True_(),
            LocationName.reptile_rumble_bunch_7:
                True_(),
            LocationName.reptile_rumble_bunch_8:
                (HasTires | HasDiddy) & CanSlap,
            LocationName.reptile_rumble_bunch_9:
                CanSlap | (HasDiddy & CanRoll),
            LocationName.reptile_rumble_bunch_10:
                HasTires & CanSlap,
            LocationName.reptile_rumble_token_1:
                HasTires | HasDiddy,
            LocationName.reptile_rumble_bunch_11:
                (HasTires & CanSlap) | HasDiddy,
            LocationName.reptile_rumble_bunch_12:
                (HasTires & CanSlap) | HasDiddy,
            LocationName.reptile_rumble_bunch_13:
                (HasTires & CanSlap) | HasDiddy,
            LocationName.reptile_rumble_bunch_14:
                HasTires & CanSlap,

            LocationName.coral_capers_clear:
                CanSwim,
            EventName.coral_capers_clear:
                CanSwim,
            LocationName.coral_capers_kong:
                CanSwim,
            LocationName.coral_capers_bunch_1:
                CanSwim,
            LocationName.coral_capers_balloon_1:
                CanSwim,
            LocationName.coral_capers_bunch_2:
                CanSwim,
            LocationName.coral_capers_token_1:
                CanSwim,

            LocationName.barrel_cannon_canyon_clear:
                HasKannons,
            EventName.barrel_cannon_canyon_clear:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_1:
                HasKannons,
            LocationName.barrel_cannon_canyon_bonus_2:
                CanCarry & HasKannons,
            LocationName.barrel_cannon_canyon_kong:
                HasKannons,
            LocationName.barrel_cannon_canyon_token_1:
                CanRoll,
            LocationName.barrel_cannon_canyon_bunch_1:
                CanSlap,
            LocationName.barrel_cannon_canyon_bunch_2:
                CanSlap | HasDiddy,
            LocationName.barrel_cannon_canyon_bunch_3:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_4:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_token_2:
                HasKannons,
            LocationName.barrel_cannon_canyon_bunch_5:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_6:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_7:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_8:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.barrel_cannon_canyon_bunch_9:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_10:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_11:
                CanSlap & HasKannons,
            LocationName.barrel_cannon_canyon_bunch_12:
                HasKannons & (CanSlap | HasDiddy),

            LocationName.very_gnawty_lair_clear:
                True_(),
            LocationName.defeated_gnawty_1:
                True_(),

            LocationName.winky_walkway_clear:
                True_(),
            EventName.winky_walkway_clear:
                True_(),
            LocationName.winky_walkway_bonus_1:
                HasKannons,
            LocationName.winky_walkway_kong:
                HasKannons,
            LocationName.winky_walkway_bunch_1:
                CanSlap | HasDiddy,
            LocationName.winky_walkway_bunch_2:
                CanSlap | HasDiddy,
            LocationName.winky_walkway_bunch_3:
                CanSlap | HasDiddy,
            LocationName.winky_walkway_bunch_4:
                CanSlap | (HasDiddy & HasWinky),
            LocationName.winky_walkway_token_1:
                HasWinky | HasDonkey | HasBothKongs,
            LocationName.winky_walkway_bunch_5:
                CanSlap | HasDiddy,

            LocationName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            EventName.mine_cart_carnage_clear:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_kong:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_1:
                CanSlap,
            LocationName.mine_cart_carnage_bunch_2:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_token_1:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_bunch_3:
                HasKannons & HasMinecart,
            LocationName.mine_cart_carnage_balloon_1:
                HasKannons & HasMinecart,

            LocationName.bouncy_bonanza_clear:
                HasTires,
            EventName.bouncy_bonanza_clear:
                HasTires,
            LocationName.bouncy_bonanza_bonus_1:
                CanCarry,
            LocationName.bouncy_bonanza_bonus_2:
                HasTires & HasKannons,
            LocationName.bouncy_bonanza_kong:
                HasTires,
            LocationName.bouncy_bonanza_token_1:
                HasTires,
            LocationName.bouncy_bonanza_bunch_1:
                CanSlap,
            LocationName.bouncy_bonanza_bunch_2:
                CanSlap | HasDiddy,
            LocationName.bouncy_bonanza_bunch_3:
                CanSlap | HasDiddy,
            LocationName.bouncy_bonanza_bunch_4:
                (CanSlap & (
                    HasTires | CanCarry)) | (
                        HasDiddy & CanRoll
                    ) ,
            LocationName.bouncy_bonanza_bunch_5:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_6:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_7:
                HasTires & CanSlap,
            LocationName.bouncy_bonanza_bunch_8:
                HasTires & (CanSlap | HasDiddy),
            LocationName.bouncy_bonanza_bunch_9:
                HasTires & (CanSlap | HasDiddy),
            LocationName.bouncy_bonanza_bunch_10:
                HasTires & (CanSlap | HasDiddy),

            LocationName.stop_go_station_clear:
                True_(),
            EventName.stop_go_station_clear:
                True_(),
            LocationName.stop_go_station_bonus_1:
                CanCarry,
            LocationName.stop_go_station_bonus_2:
                HasTires & HasKannons,
            LocationName.stop_go_station_kong:
                CanRoll,
            LocationName.stop_go_station_bunch_1:
                CanSlap,
            LocationName.stop_go_station_bunch_2:
                CanSlap,
            LocationName.stop_go_station_bunch_3:
                CanSlap & (HasSwitches | HasBothKongs),
            LocationName.stop_go_station_token_1:
                True_(),
            LocationName.stop_go_station_bunch_4:
                CanSlap | HasDiddy,
            LocationName.stop_go_station_bunch_5:
                CanSlap | HasDiddy,
            LocationName.stop_go_station_bunch_6:
                CanSlap | HasDiddy,
            LocationName.stop_go_station_bunch_7:
                CanSlap,

            LocationName.millstone_mayhem_clear:
                HasDonkey | HasTires,
            EventName.millstone_mayhem_clear:
                HasDonkey | HasTires,
            LocationName.millstone_mayhem_bonus_1:
                HasKannons & (HasTires | HasDonkey),
            LocationName.millstone_mayhem_bonus_2:
                HasTires & HasKannons,
            LocationName.millstone_mayhem_bonus_3:
                CanCarry & (HasTires | HasDonkey),
            LocationName.millstone_mayhem_kong:
                HasKannons & (HasTires | HasDonkey),
            LocationName.millstone_mayhem_bunch_1:
                CanSlap | (
                    HasTires & HasDiddy & HasKannons),
            LocationName.millstone_mayhem_bunch_2:
                CanSlap | (HasTires & HasDiddy),
            LocationName.millstone_mayhem_bunch_3:
                CanSlap | (HasTires & HasDiddy),
            LocationName.millstone_mayhem_bunch_4:
                CanSlap | (
                    HasTires & HasDiddy & HasWinky),
            LocationName.millstone_mayhem_bunch_5:
                CanSlap | (
                    HasTires & HasDiddy & HasWinky),
            LocationName.millstone_mayhem_bunch_6:
                CanSlap | (
                    HasTires & HasDiddy & HasWinky),
            LocationName.millstone_mayhem_bunch_7:
                HasDonkey | HasTires,
            LocationName.millstone_mayhem_bunch_8:
                HasDonkey | HasTires,
            LocationName.millstone_mayhem_bunch_9:
                CanSlap | (
                    HasTires & HasDiddy & HasWinky),

            LocationName.necky_nuts_clear:
                True_(),
            LocationName.defeated_necky_1:
                True_(),

            LocationName.vulture_culture_clear:
                HasKannons,
            EventName.vulture_culture_clear:
                HasKannons,
            LocationName.vulture_culture_bonus_1:
                HasKannons & HasTires,
            LocationName.vulture_culture_bonus_2:
                HasKannons & CanCarry,
            LocationName.vulture_culture_bonus_3:
                HasKannons & CanCarry,
            LocationName.vulture_culture_kong:
                HasKannons & CanCarry,
            LocationName.vulture_culture_bunch_1:
                CanSlap,
            LocationName.vulture_culture_bunch_2:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_3:
                HasKannons & (CanSlap | HasBothKongs),
            LocationName.vulture_culture_bunch_4:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.vulture_culture_bunch_5:
                HasKannons & CanSlap,
            LocationName.vulture_culture_bunch_6:
                HasKannons & CanSlap,

            LocationName.tree_top_town_clear:
                HasKannons,
            EventName.tree_top_town_clear:
                HasKannons,
            LocationName.tree_top_town_bonus_1:
                HasKannons,
            LocationName.tree_top_town_bonus_2:
                HasKannons,
            LocationName.tree_top_town_kong:
                HasKannons,
            LocationName.tree_top_town_bunch_1:
                CanSlap | HasDiddy,
            LocationName.tree_top_town_bunch_2:
                HasKannons & CanSlap,
            LocationName.tree_top_town_bunch_3:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.tree_top_town_bunch_4:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.tree_top_town_token_1:
                HasKannons,

            LocationName.forest_frenzy_clear:
                CanClimb,
            EventName.forest_frenzy_clear:
                CanClimb,
            LocationName.forest_frenzy_bonus_1:
                CanClimb & HasKannons,
            LocationName.forest_frenzy_bonus_2:
                CanClimb & CanCarry,
            LocationName.forest_frenzy_kong:
                CanClimb & CanRoll,
            LocationName.forest_frenzy_bunch_1:
                (CanSlap & CanClimb) | 
                    (HasDiddy & (CanClimb | CanRoll)),
            LocationName.forest_frenzy_bunch_2:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.forest_frenzy_bunch_3:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.forest_frenzy_bunch_4:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.forest_frenzy_bunch_5:
                CanClimb & CanSlap,
            LocationName.forest_frenzy_balloon_1:
                CanClimb,

            LocationName.temple_tempest_clear:
                (CanClimb | (HasDiddy & CanRoll)) & 
                    (HasTires | (CanCarry & HasExpresso)),
            EventName.temple_tempest_clear:
                (CanClimb | (HasDiddy & CanRoll)) & 
                    (HasTires | (CanCarry & HasExpresso)),
            LocationName.temple_tempest_bonus_1:
                (CanClimb | (HasDiddy & CanRoll)) & CanCarry,
            LocationName.temple_tempest_bonus_2:
                HasKannons & (CanClimb | 
                    (CanCarry & HasExpresso & HasDiddy)),
            LocationName.temple_tempest_kong:
                (CanClimb & HasTires) | 
                    (CanCarry & HasExpresso & HasDiddy),
            LocationName.temple_tempest_token_1:
                True_(),
            LocationName.temple_tempest_bunch_1:
                CanSlap | HasDiddy,
            LocationName.temple_tempest_bunch_2:
                (CanSlap & CanClimb) | 
                    (HasDiddy & CanRoll & HasExpresso),
            LocationName.temple_tempest_bunch_3:
                CanSlap & (CanClimb | 
                    (HasDiddy & CanRoll & HasExpresso)),
            LocationName.temple_tempest_bunch_4:
                (CanSlap & CanClimb) | 
                    (HasDiddy & CanRoll & HasExpresso),
            LocationName.temple_tempest_bunch_5:
                (CanSlap & CanClimb) | 
                    (HasDiddy & CanRoll & HasExpresso),
            LocationName.temple_tempest_bunch_6:
                HasTires & CanSlap & (CanClimb | 
                    (HasDiddy & CanRoll & HasExpresso)),
            LocationName.temple_tempest_bunch_7:
                (CanClimb & HasTires) | 
                    (HasDiddy & CanRoll & HasExpresso),
            LocationName.temple_tempest_bunch_8:
                (CanClimb & HasTires) | 
                    (HasDiddy & CanRoll & HasExpresso),

            LocationName.orang_utan_gang_clear:
                True_(),
            EventName.orang_utan_gang_clear:
                True_(),
            LocationName.orang_utan_gang_bonus_1:
                HasExpresso,
            LocationName.orang_utan_gang_bonus_2:
                CanCarry & (HasExpresso | (HasDiddy & CanRoll)),
            LocationName.orang_utan_gang_bonus_3:
                CanCarry | HasExpresso,
            LocationName.orang_utan_gang_bonus_4:
                CanCarry | HasExpresso,
            LocationName.orang_utan_gang_bonus_5:
                True_(),
            LocationName.orang_utan_gang_kong:
                CanCarry & HasTires & 
                    (CanRoll | HasExpresso) ,
            LocationName.orang_utan_gang_bunch_1:
                CanSlap | HasDiddy,
            LocationName.orang_utan_gang_bunch_2:
                CanCarry | CanSlap | HasDiddy,
            LocationName.orang_utan_gang_bunch_3:
                CanSlap,
            LocationName.orang_utan_gang_bunch_4:
                CanRoll | HasExpresso,
            LocationName.orang_utan_gang_bunch_5:
                CanSlap | HasDiddy,
            LocationName.orang_utan_gang_bunch_6:
                HasExpresso | (HasDiddy & CanRoll),
            LocationName.orang_utan_gang_token_1:
                HasExpresso,
            LocationName.orang_utan_gang_bunch_7:
                CanSlap | HasDiddy,
            LocationName.orang_utan_gang_bunch_8:
                True_(),
            LocationName.orang_utan_gang_bunch_9:
                True_(),

            LocationName.clam_city_clear:
                CanSwim,
            EventName.clam_city_clear:
                CanSwim,
            LocationName.clam_city_kong:
                CanSwim,
            LocationName.clam_city_bunch_1:
                True_(),
            LocationName.clam_city_bunch_2:
                CanSwim,
            LocationName.clam_city_token_1:
                CanSwim,

            LocationName.bumble_b_rumble_clear:
                CanCarry,
            LocationName.defeated_bumble_b:
                CanCarry,

            LocationName.snow_barrel_blast_clear:
                HasKannons,
            EventName.snow_barrel_blast_clear:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_1:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_2:
                HasKannons,
            LocationName.snow_barrel_blast_bonus_3:
                HasKannons,
            LocationName.snow_barrel_blast_kong:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_1:
                HasKannons | CanSlap | HasDiddy,
            LocationName.snow_barrel_blast_balloon_1:
                HasKannons | HasDiddy,
            LocationName.snow_barrel_blast_bunch_2:
                (HasKannons & 
                    (CanSlap | HasDiddy)) | HasBothKongs,
            LocationName.snow_barrel_blast_bunch_3:
                HasKannons & (CanSlap | HasDiddy),
            LocationName.snow_barrel_blast_token_1:
                HasKannons,
            LocationName.snow_barrel_blast_balloon_2:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_4:
                HasKannons,
            LocationName.snow_barrel_blast_bunch_5:
                HasKannons & (CanSlap | HasDiddy),

            LocationName.slipslide_ride_clear:
                CanClimb & HasKannons,
            EventName.slipslide_ride_clear:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bonus_1:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_2:
                CanClimb & CanCarry,
            LocationName.slipslide_ride_bonus_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_kong:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_1:
                CanClimb,
            LocationName.slipslide_ride_bunch_2:
                CanClimb & (CanSlap | HasDiddy),
            LocationName.slipslide_ride_bunch_3:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_4:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_5:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_6:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_7:
                CanClimb & HasKannons,
            LocationName.slipslide_ride_bunch_8:
                CanClimb & HasKannons & 
                    (CanSlap | HasDiddy),
            LocationName.slipslide_ride_bunch_9:
                CanClimb & HasKannons & 
                    (CanSlap | HasDiddy),
            LocationName.slipslide_ride_token_1:
                CanClimb & HasKannons,

            LocationName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            EventName.ice_age_alley_clear:
                (CanClimb & HasKannons) | HasExpresso,
            LocationName.ice_age_alley_bonus_1:
                (CanClimb | HasExpresso) & HasKannons,
            LocationName.ice_age_alley_bonus_2:
                HasExpresso & HasKannons,
            LocationName.ice_age_alley_kong:
                HasExpresso,
            LocationName.ice_age_alley_bunch_1:
                CanSlap | (HasExpresso & HasDiddy),
            LocationName.ice_age_alley_bunch_2:
                ((CanClimb & HasKannons) | 
                    HasExpresso) & (CanSlap | HasDiddy),
            LocationName.ice_age_alley_bunch_3:
                (CanClimb & HasKannons) | HasExpresso,

            LocationName.croctopus_chase_clear:
                CanSwim,
            EventName.croctopus_chase_clear:
                CanSwim,
            LocationName.croctopus_chase_kong:
                CanSwim,
            LocationName.croctopus_chase_bunch_1:
                CanSwim,
            LocationName.croctopus_chase_token_1:
                CanSwim,
            LocationName.croctopus_chase_token_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_2:
                CanSwim,
            LocationName.croctopus_chase_bunch_3:
                CanSwim,
            LocationName.croctopus_chase_bunch_4:
                CanSwim,
            LocationName.croctopus_chase_bunch_5:
                CanSwim,
            LocationName.croctopus_chase_balloon_1:
                CanSwim,

            LocationName.torchlight_trouble_clear:
                True_(),
            EventName.torchlight_trouble_clear:
                True_(),
            LocationName.torchlight_trouble_bonus_1:
                CanCarry,
            LocationName.torchlight_trouble_bonus_2:
                CanCarry,
            LocationName.torchlight_trouble_kong:
                CanCarry & CanRoll,
            LocationName.torchlight_trouble_bunch_1:
                CanSlap | HasDiddy,

            LocationName.rope_bridge_rumble_clear:
                HasTires,
            EventName.rope_bridge_rumble_clear:
                HasTires,
            LocationName.rope_bridge_rumble_bonus_1:
                HasKannons,
            LocationName.rope_bridge_rumble_bonus_2:
                HasTires & HasKannons,
            LocationName.rope_bridge_rumble_kong:
                HasTires & CanRoll,
            LocationName.rope_bridge_rumble_bunch_1:
                HasTires & CanRoll,

            LocationName.really_gnawty_rampage_clear:
                True_(),
            LocationName.defeated_gnawty_2:
                True_(),

            LocationName.oil_drum_alley_clear:
                HasKannons & 
                    (HasTires | (HasDiddy & 
                         (HasRambi | CanRoll))),
            EventName.oil_drum_alley_clear:
                HasKannons & 
                    (HasTires | (HasDiddy & 
                         (HasRambi | CanRoll))),
            LocationName.oil_drum_alley_bonus_1:
                CanCarry & HasKannons,
            LocationName.oil_drum_alley_bonus_2:
                CanCarry,
            LocationName.oil_drum_alley_bonus_3:
                CanCarry,
            LocationName.oil_drum_alley_bonus_4:
                HasKannons,
            LocationName.oil_drum_alley_kong:
                HasKannons & 
                    (HasTires | (HasDiddy & 
                         (HasRambi | CanRoll))),
            LocationName.oil_drum_alley_bunch_1:
                HasKannons,
            LocationName.oil_drum_alley_bunch_2:
                HasKannons,

            LocationName.trick_track_trek_clear:
                HasPlatforms | (CanRoll & HasKannons),
            EventName.trick_track_trek_clear:
                HasPlatforms | (CanRoll & HasKannons),
            LocationName.trick_track_trek_bonus_1:
                HasPlatforms & HasKannons & CanRoll,
            LocationName.trick_track_trek_bonus_2:
                HasPlatforms & HasKannons,
            LocationName.trick_track_trek_bonus_3:
                HasPlatforms | (CanRoll & HasKannons),
            LocationName.trick_track_trek_kong:
                HasPlatforms,
            LocationName.trick_track_trek_bunch_1:
                HasPlatforms,
            LocationName.trick_track_trek_token_1:
                HasPlatforms | (CanRoll & HasKannons),

            LocationName.elevator_antics_clear:
                CanClimb,
            EventName.elevator_antics_clear:
                CanClimb,
            LocationName.elevator_antics_bonus_1:
                CanClimb & (CanRoll | HasDiddy),
            LocationName.elevator_antics_bonus_2:
                CanClimb,
            LocationName.elevator_antics_bonus_3:
                CanClimb,
            LocationName.elevator_antics_kong:
                CanClimb & HasKannons,
            LocationName.elevator_antics_bunch_1:
                True_(),
            LocationName.elevator_antics_bunch_2:
                CanClimb,
            LocationName.elevator_antics_bunch_3:
                CanClimb,

            LocationName.poison_pond_clear:
                CanSwim & (HasEnguarde | HasBothKongs),
            EventName.poison_pond_clear:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_kong:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_1:
                True_(),
            LocationName.poison_pond_bunch_2:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_3:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_4:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_5:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_token_1:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_token_2:
                CanSwim & (HasEnguarde | HasBothKongs),
            LocationName.poison_pond_bunch_6:
                CanSwim & (HasEnguarde | HasBothKongs),

            LocationName.mine_cart_madness_clear:
                HasMinecart,
            EventName.mine_cart_madness_clear:
                HasMinecart,
            LocationName.mine_cart_madness_bonus_1:
                HasMinecart & CanClimb & HasKannons,
            LocationName.mine_cart_madness_bonus_2:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_bonus_3:
                HasMinecart & HasTires & HasKannons,
            LocationName.mine_cart_madness_kong:
                HasMinecart & (HasTires | HasDonkey),
            LocationName.mine_cart_madness_token_1:
                HasMinecart,
            LocationName.mine_cart_madness_bunch_1:
                HasMinecart,

            LocationName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            EventName.blackout_basement_clear:
                CanClimb & HasTires & HasPlatforms,
            LocationName.blackout_basement_bonus_1:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_bonus_2:
                CanClimb & HasTires & HasPlatforms & CanCarry & HasKannons,
            LocationName.blackout_basement_kong:
                CanClimb & HasTires & HasPlatforms & HasKannons,
            LocationName.blackout_basement_token_1:
                True_(),
            LocationName.blackout_basement_bunch_1:
                CanClimb & HasTires,

            LocationName.boss_dumb_drum_clear:
                (HasDiddy & CanRoll) | HasDonkey,
            LocationName.defeated_boss_dumb_drum:
                (HasDiddy & CanRoll) | HasDonkey,

            LocationName.tanked_up_trouble_clear:
                HasPlatforms & HasTires,
            EventName.tanked_up_trouble_clear:
                HasPlatforms & HasTires,
            LocationName.tanked_up_trouble_bonus_1:
                HasPlatforms & HasKannons,
            LocationName.tanked_up_trouble_kong:
                HasPlatforms & HasTires,
            LocationName.tanked_up_trouble_bunch_1:
                HasPlatforms,
            LocationName.tanked_up_trouble_bunch_2:
                HasPlatforms,
            LocationName.tanked_up_trouble_token_1:
                HasPlatforms,
            LocationName.tanked_up_trouble_bunch_3:
                HasPlatforms & HasTires,
            LocationName.tanked_up_trouble_bunch_4:
                HasPlatforms & HasTires,

            LocationName.manic_mincers_clear:
                HasTires | CanCarry | 
                    HasRambi | HasBothKongs,
            EventName.manic_mincers_clear:
                HasTires | CanCarry | 
                    HasRambi | HasBothKongs,
            LocationName.manic_mincers_bonus_1:
                CanCarry | HasRambi,
            LocationName.manic_mincers_bonus_2:
                CanCarry | HasRambi,
            LocationName.manic_mincers_kong:
                True_(),
            LocationName.manic_mincers_bunch_1:
                True_(),
            LocationName.manic_mincers_bunch_2:
                True_(),
            LocationName.manic_mincers_token_1:
                True_(),

            LocationName.misty_mine_clear:
                CanClimb,
            EventName.misty_mine_clear:
                CanClimb,
            LocationName.misty_mine_bonus_1:
                CanClimb,
            LocationName.misty_mine_bonus_2:
                CanClimb & (CanCarry | HasExpresso),
            LocationName.misty_mine_kong:
                CanClimb,
            LocationName.misty_mine_token_1:
                CanCarry,
            LocationName.misty_mine_bunch_1:
                CanCarry,
            LocationName.misty_mine_bunch_2:
                True_(),
            LocationName.misty_mine_token_2:
                CanClimb & (HasExpresso | CanRoll),

            LocationName.loopy_lights_clear:
                HasTires,
            EventName.loopy_lights_clear:
                HasTires,
            LocationName.loopy_lights_bonus_1:
                HasKannons,
            LocationName.loopy_lights_bonus_2:
                CanCarry & (HasTires | CanRoll),
            LocationName.loopy_lights_kong:
                HasTires & HasKannons & CanRoll & CanCarry,
            LocationName.loopy_lights_bunch_1:
                HasTires | CanRoll,
            LocationName.loopy_lights_bunch_2:
                HasTires,

            LocationName.platform_perils_clear:
                HasPlatforms & HasTires & 
                    (HasBothKongs | CanRoll | CanCarry),
            EventName.platform_perils_clear:
                HasPlatforms & HasTires & 
                    (HasBothKongs | CanRoll | CanCarry),
            LocationName.platform_perils_bonus_1:
                HasPlatforms & HasKannons,
            LocationName.platform_perils_bonus_2:
                HasPlatforms & 
                    HasTires & HasKannons & 
                    (HasBothKongs | CanRoll | CanCarry),
            LocationName.platform_perils_kong:
                HasPlatforms & HasTires & 
                    (HasBothKongs | CanRoll | CanCarry),
            LocationName.platform_perils_token_1:
                HasPlatforms,
            LocationName.platform_perils_bunch_1:
                HasPlatforms & CanCarry,

            LocationName.necky_revenge_clear:
                True_(),
            LocationName.defeated_necky_2:
                True_(),
        }

    def set_dkc_rules(self) -> None:
        super().set_dkc_rules()
