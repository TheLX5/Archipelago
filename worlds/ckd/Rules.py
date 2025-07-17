from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import CKDWorld

from .Names import LocationName, ItemName, RegionName, EventName

from worlds.generic.Rules import CollectionRule, add_rule
from BaseClasses import CollectionState
  
class CKDRules:
    player: int
    world: "CKDWorld"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "CKDWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.dk_isle} -> {RegionName.kongo_jungle}":
                self.can_access_jungle,
            f"{RegionName.dk_isle} -> {RegionName.monkey_mines}":
                self.can_access_mines,
            f"{RegionName.dk_isle} -> {RegionName.vine_valley}":
                self.can_access_valley,
            f"{RegionName.dk_isle} -> {RegionName.gorilla_glacier}":
                self.can_access_glacier,
            f"{RegionName.dk_isle} -> {RegionName.kremkroc_industries}":
                self.can_access_industries,
            f"{RegionName.dk_isle} -> {RegionName.chimp_caverns}":
                self.can_access_caverns,
            f"{RegionName.dk_isle} -> {RegionName.gangplank_galleon}":
                self.can_access_ship,
            f"{RegionName.kongo_jungle} -> {RegionName.very_gnawty_lair_map}":
                self.can_access_very_gnawty,
            f"{RegionName.monkey_mines} -> {RegionName.necky_nuts_map}":
                self.can_access_master_necky,
            f"{RegionName.vine_valley} -> {RegionName.bumble_b_rumble_map}":
                self.can_access_queen_b,
            f"{RegionName.gorilla_glacier} -> {RegionName.really_gnawty_rampage_map}":
                self.can_access_really_gnawty,
            f"{RegionName.kremkroc_industries} -> {RegionName.boss_dumb_drum_map}":
                self.can_access_dumb_drum,
            f"{RegionName.chimp_caverns} -> {RegionName.necky_revenge_map}":
                self.can_access_master_necky_snr,
        }

    def can_access_jungle(self, state: CollectionState) -> bool:
        return state.has(ItemName.kongo_jungle, self.player)

    def can_access_mines(self, state: CollectionState) -> bool:
        return state.has(ItemName.monkey_mines, self.player)

    def can_access_valley(self, state: CollectionState) -> bool:
        return state.has(ItemName.vine_valley, self.player)

    def can_access_glacier(self, state: CollectionState) -> bool:
        return state.has(ItemName.gorilla_glacier, self.player)

    def can_access_industries(self, state: CollectionState) -> bool:
        return state.has(ItemName.kremkroc_industries, self.player)

    def can_access_caverns(self, state: CollectionState) -> bool:
        return state.has(ItemName.chimp_caverns, self.player)
    
    def can_access_ship(self, state: CollectionState) -> bool:
        return state.has(ItemName.boss_token, self.player, self.world.options.gangplank_tokens.value)
    
    def can_access_very_gnawty(self, state: CollectionState) -> bool:
        return state.has(EventName.jungle_level, self.player, self.world.options.required_jungle_levels.value)
    
    def can_access_master_necky(self, state: CollectionState) -> bool:
        return state.has(EventName.mines_level, self.player, self.world.options.required_mines_levels.value)
    
    def can_access_queen_b(self, state: CollectionState) -> bool:
        return state.has(EventName.valley_level, self.player, self.world.options.required_valley_levels.value)
    
    def can_access_really_gnawty(self, state: CollectionState) -> bool:
        return state.has(EventName.glacier_level, self.player, self.world.options.required_glacier_levels.value)
    
    def can_access_dumb_drum(self, state: CollectionState) -> bool:
        return state.has(EventName.industries_level, self.player, self.world.options.required_industries_levels.value)
    
    def can_access_master_necky_snr(self, state: CollectionState) -> bool:
        return state.has(EventName.caverns_level, self.player, self.world.options.required_caverns_levels.value)

    def has_donkey(self, state: CollectionState) -> bool:
        return state.has(ItemName.donkey, self.player)

    def has_diddy(self, state: CollectionState) -> bool:
        return state.has(ItemName.diddy, self.player)
    
    def has_both_kongs(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.donkey, ItemName.diddy}, self.player)
    
    def can_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.carry, self.player)
    
    def can_swim(self, state: CollectionState) -> bool:
        return state.has(ItemName.swim, self.player)
    
    def can_roll(self, state: CollectionState) -> bool:
        return state.has(ItemName.roll, self.player)
    
    def can_climb(self, state: CollectionState) -> bool:
        return state.has(ItemName.climb, self.player)
    
    def can_slap(self, state: CollectionState) -> bool:
        return state.has_all({ItemName.donkey, ItemName.slap}, self.player)
    
    def has_kannons(self, state: CollectionState) -> bool:
        return state.has(ItemName.kannons, self.player)
    
    def has_switches(self, state: CollectionState) -> bool:
        return state.has(ItemName.switches, self.player)
    
    def has_minecart(self, state: CollectionState) -> bool:
        return state.has(ItemName.minecart, self.player)
    
    def has_winky(self, state: CollectionState) -> bool:
        return state.has(ItemName.winky, self.player)
    
    def has_expresso(self, state: CollectionState) -> bool:
        return state.has(ItemName.expresso, self.player)
    
    def has_rambi(self, state: CollectionState) -> bool:
        return state.has(ItemName.rambi, self.player)
    
    def has_enguarde(self, state: CollectionState) -> bool:
        return state.has(ItemName.enguarde, self.player)
    
    def has_squawks(self, state: CollectionState) -> bool:
        return state.has(ItemName.squawks, self.player)
    
    def has_tires(self, state: CollectionState) -> bool:
        return state.has(ItemName.tires, self.player)
    
    def has_platforms(self, state: CollectionState) -> bool:
        return state.has(ItemName.platforms, self.player)
    
    def true(self, state: CollectionState) -> bool:
        return True
    
    def set_ckd_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
            
        multiworld.completion_condition[self.player] = lambda state: state.has(EventName.k_rool, self.player)
        
    # Universal Tracker: Append the next logic level rule that has UT's glitched item to the actual logic rule
    def set_ckd_glitched_rules(self) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                glitched_rule = lambda state, rule=self.location_rules[loc.name]: state.has(ItemName.glitched, self.player) and rule(state)
                add_rule(loc, glitched_rule, combine="or")
 


class CKDStrictRules(CKDRules):
    def __init__(self, world: "CKDWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                self.true,
            LocationName.jungle_hijinxs_bonus_2:
                self.true,
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_4:
                self.true,
            LocationName.jungle_hijinxs_bunch_5:
                self.true,
            LocationName.jungle_hijinxs_bunch_6:
                self.true,
            LocationName.jungle_hijinxs_balloon_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_7:
                self.true,
            LocationName.jungle_hijinxs_bunch_8:
                self.true,
            LocationName.jungle_hijinxs_bunch_9:
                self.true,
            LocationName.jungle_hijinxs_bunch_10:
                self.true,
            LocationName.jungle_hijinxs_bunch_11:
                self.true,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_13:
                self.true,
            LocationName.jungle_hijinxs_balloon_4:
                self.true,
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                self.true,
            LocationName.jungle_hijinxs_bunch_15:
                self.true,
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                self.true,
            LocationName.jungle_hijinxs_bunch_18:
                self.true,
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                self.true,
            LocationName.jungle_hijinxs_balloon_6:
                self.true,

            LocationName.ropey_rampage_clear:
                self.true,
            EventName.ropey_rampage_clear:
                self.true,
            LocationName.ropey_rampage_bonus_1:
                self.true,
            LocationName.ropey_rampage_bonus_2:
                self.true,
            LocationName.ropey_rampage_kong:
                self.true,
            LocationName.ropey_rampage_bunch_1:
                self.true,
            LocationName.ropey_rampage_bunch_2:
                self.true,
            LocationName.ropey_rampage_bunch_3:
                self.true,
            LocationName.ropey_rampage_bunch_4:
                self.true,
            LocationName.ropey_rampage_bunch_5:
                self.true,
            LocationName.ropey_rampage_bunch_6:
                self.true,
            LocationName.ropey_rampage_bunch_7:
                self.true,
            LocationName.ropey_rampage_bunch_8:
                self.true,
            LocationName.ropey_rampage_bunch_9:
                self.true,
            LocationName.ropey_rampage_token_1:
                self.true,
            LocationName.ropey_rampage_bunch_10:
                self.true,
            LocationName.ropey_rampage_bunch_11:
                self.true,
            LocationName.ropey_rampage_bunch_12:
                self.true,
            LocationName.ropey_rampage_bunch_13:
                self.true,
            LocationName.ropey_rampage_bunch_14:
                self.true,
            LocationName.ropey_rampage_bunch_15:
                self.true,
            LocationName.ropey_rampage_token_2:
                self.true,
            LocationName.ropey_rampage_bunch_16:
                self.true,
            LocationName.ropey_rampage_bunch_17:
                self.true,
            LocationName.ropey_rampage_bunch_18:
                self.true,
            LocationName.ropey_rampage_bunch_19:
                self.true,

            LocationName.reptile_rumble_clear:
                self.true,
            EventName.reptile_rumble_clear:
                self.true,
            LocationName.reptile_rumble_bonus_1:
                self.true,
            LocationName.reptile_rumble_bonus_2:
                self.true,
            LocationName.reptile_rumble_bonus_3:
                self.true,
            LocationName.reptile_rumble_kong:
                self.true,
            LocationName.reptile_rumble_bunch_1:
                self.true,
            LocationName.reptile_rumble_bunch_2:
                self.true,
            LocationName.reptile_rumble_bunch_3:
                self.true,
            LocationName.reptile_rumble_bunch_4:
                self.true,
            LocationName.reptile_rumble_bunch_5:
                self.true,
            LocationName.reptile_rumble_bunch_6:
                self.true,
            LocationName.reptile_rumble_bunch_7:
                self.true,
            LocationName.reptile_rumble_bunch_8:
                self.true,
            LocationName.reptile_rumble_bunch_9:
                self.true,
            LocationName.reptile_rumble_bunch_10:
                self.true,
            LocationName.reptile_rumble_token_1:
                self.true,
            LocationName.reptile_rumble_bunch_11:
                self.true,
            LocationName.reptile_rumble_bunch_12:
                self.true,
            LocationName.reptile_rumble_bunch_13:
                self.true,
            LocationName.reptile_rumble_bunch_14:
                self.true,

            LocationName.coral_capers_clear:
                self.true,
            EventName.coral_capers_clear:
                self.true,
            LocationName.coral_capers_kong:
                self.true,
            LocationName.coral_capers_bunch_1:
                self.true,
            LocationName.coral_capers_balloon_1:
                self.true,
            LocationName.coral_capers_bunch_2:
                self.true,
            LocationName.coral_capers_token_1:
                self.true,

            LocationName.barrel_cannon_canyon_clear:
                self.true,
            EventName.barrel_cannon_canyon_clear:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_2:
                self.true,
            LocationName.barrel_cannon_canyon_kong:
                self.true,
            LocationName.barrel_cannon_canyon_token_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_3:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_4:
                self.true,
            LocationName.barrel_cannon_canyon_token_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_5:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_6:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_7:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_8:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_9:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_10:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_11:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_12:
                self.true,

            LocationName.very_gnawty_lair_clear:
                self.true,
            LocationName.defeated_gnawty_1:
                self.true,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.true,
            LocationName.winky_walkway_kong:
                self.true,
            LocationName.winky_walkway_bunch_1:
                self.true,
            LocationName.winky_walkway_bunch_2:
                self.true,
            LocationName.winky_walkway_bunch_3:
                self.true,
            LocationName.winky_walkway_bunch_4:
                self.true,
            LocationName.winky_walkway_token_1:
                self.true,
            LocationName.winky_walkway_bunch_5:
                self.true,

            LocationName.mine_cart_carnage_clear:
                self.true,
            EventName.mine_cart_carnage_clear:
                self.true,
            LocationName.mine_cart_carnage_kong:
                self.true,
            LocationName.mine_cart_carnage_bunch_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_2:
                self.true,
            LocationName.mine_cart_carnage_token_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_3:
                self.true,
            LocationName.mine_cart_carnage_balloon_1:
                self.true,

            LocationName.bouncy_bonanza_clear:
                self.true,
            EventName.bouncy_bonanza_clear:
                self.true,
            LocationName.bouncy_bonanza_bonus_1:
                self.true,
            LocationName.bouncy_bonanza_bonus_2:
                self.true,
            LocationName.bouncy_bonanza_kong:
                self.true,
            LocationName.bouncy_bonanza_token_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_2:
                self.true,
            LocationName.bouncy_bonanza_bunch_3:
                self.true,
            LocationName.bouncy_bonanza_bunch_4:
                self.true,
            LocationName.bouncy_bonanza_bunch_5:
                self.true,
            LocationName.bouncy_bonanza_bunch_6:
                self.true,
            LocationName.bouncy_bonanza_bunch_7:
                self.true,
            LocationName.bouncy_bonanza_bunch_8:
                self.true,
            LocationName.bouncy_bonanza_bunch_9:
                self.true,
            LocationName.bouncy_bonanza_bunch_10:
                self.true,

            LocationName.stop_go_station_clear:
                self.true,
            EventName.stop_go_station_clear:
                self.true,
            LocationName.stop_go_station_bonus_1:
                self.true,
            LocationName.stop_go_station_bonus_2:
                self.true,
            LocationName.stop_go_station_kong:
                self.true,
            LocationName.stop_go_station_bunch_1:
                self.true,
            LocationName.stop_go_station_bunch_2:
                self.true,
            LocationName.stop_go_station_bunch_3:
                self.true,
            LocationName.stop_go_station_token_1:
                self.true,
            LocationName.stop_go_station_bunch_4:
                self.true,
            LocationName.stop_go_station_bunch_5:
                self.true,
            LocationName.stop_go_station_bunch_6:
                self.true,
            LocationName.stop_go_station_bunch_7:
                self.true,

            LocationName.millstone_mayhem_clear:
                self.true,
            EventName.millstone_mayhem_clear:
                self.true,
            LocationName.millstone_mayhem_bonus_1:
                self.true,
            LocationName.millstone_mayhem_bonus_2:
                self.true,
            LocationName.millstone_mayhem_bonus_3:
                self.true,
            LocationName.millstone_mayhem_kong:
                self.true,
            LocationName.millstone_mayhem_bunch_1:
                self.true,
            LocationName.millstone_mayhem_bunch_2:
                self.true,
            LocationName.millstone_mayhem_bunch_3:
                self.true,
            LocationName.millstone_mayhem_bunch_4:
                self.true,
            LocationName.millstone_mayhem_bunch_5:
                self.true,
            LocationName.millstone_mayhem_bunch_6:
                self.true,
            LocationName.millstone_mayhem_bunch_7:
                self.true,
            LocationName.millstone_mayhem_bunch_8:
                self.true,
            LocationName.millstone_mayhem_bunch_9:
                self.true,

            LocationName.necky_nuts_clear:
                self.true,
            LocationName.defeated_necky_1:
                self.true,

            LocationName.vulture_culture_clear:
                self.true,
            EventName.vulture_culture_clear:
                self.true,
            LocationName.vulture_culture_bonus_1:
                self.true,
            LocationName.vulture_culture_bonus_2:
                self.true,
            LocationName.vulture_culture_bonus_3:
                self.true,
            LocationName.vulture_culture_kong:
                self.true,
            LocationName.vulture_culture_bunch_1:
                self.true,
            LocationName.vulture_culture_bunch_2:
                self.true,
            LocationName.vulture_culture_bunch_3:
                self.true,
            LocationName.vulture_culture_bunch_4:
                self.true,
            LocationName.vulture_culture_bunch_5:
                self.true,
            LocationName.vulture_culture_bunch_6:
                self.true,

            LocationName.tree_top_town_clear:
                self.true,
            EventName.tree_top_town_clear:
                self.true,
            LocationName.tree_top_town_bonus_1:
                self.true,
            LocationName.tree_top_town_bonus_2:
                self.true,
            LocationName.tree_top_town_kong:
                self.true,
            LocationName.tree_top_town_bunch_1:
                self.true,
            LocationName.tree_top_town_bunch_2:
                self.true,
            LocationName.tree_top_town_bunch_3:
                self.true,
            LocationName.tree_top_town_bunch_4:
                self.true,
            LocationName.tree_top_town_token_1:
                self.true,

            LocationName.forest_frenzy_clear:
                self.true,
            EventName.forest_frenzy_clear:
                self.true,
            LocationName.forest_frenzy_bonus_1:
                self.true,
            LocationName.forest_frenzy_bonus_2:
                self.true,
            LocationName.forest_frenzy_kong:
                self.true,
            LocationName.forest_frenzy_bunch_1:
                self.true,
            LocationName.forest_frenzy_bunch_2:
                self.true,
            LocationName.forest_frenzy_bunch_3:
                self.true,
            LocationName.forest_frenzy_bunch_4:
                self.true,
            LocationName.forest_frenzy_bunch_5:
                self.true,
            LocationName.forest_frenzy_balloon_1:
                self.true,

            LocationName.temple_tempest_clear:
                self.true,
            EventName.temple_tempest_clear:
                self.true,
            LocationName.temple_tempest_bonus_1:
                self.true,
            LocationName.temple_tempest_bonus_2:
                self.true,
            LocationName.temple_tempest_kong:
                self.true,
            LocationName.temple_tempest_token_1:
                self.true,
            LocationName.temple_tempest_bunch_1:
                self.true,
            LocationName.temple_tempest_bunch_2:
                self.true,
            LocationName.temple_tempest_bunch_3:
                self.true,
            LocationName.temple_tempest_bunch_4:
                self.true,
            LocationName.temple_tempest_bunch_5:
                self.true,
            LocationName.temple_tempest_bunch_6:
                self.true,
            LocationName.temple_tempest_bunch_7:
                self.true,
            LocationName.temple_tempest_bunch_8:
                self.true,

            LocationName.orang_utan_gang_clear:
                self.true,
            EventName.orang_utan_gang_clear:
                self.true,
            LocationName.orang_utan_gang_bonus_1:
                self.true,
            LocationName.orang_utan_gang_bonus_2:
                self.true,
            LocationName.orang_utan_gang_bonus_3:
                self.true,
            LocationName.orang_utan_gang_bonus_4:
                self.true,
            LocationName.orang_utan_gang_bonus_5:
                self.true,
            LocationName.orang_utan_gang_kong:
                self.true,
            LocationName.orang_utan_gang_bunch_1:
                self.true,
            LocationName.orang_utan_gang_bunch_2:
                self.true,
            LocationName.orang_utan_gang_bunch_3:
                self.true,
            LocationName.orang_utan_gang_bunch_4:
                self.true,
            LocationName.orang_utan_gang_bunch_5:
                self.true,
            LocationName.orang_utan_gang_bunch_6:
                self.true,
            LocationName.orang_utan_gang_token_1:
                self.true,
            LocationName.orang_utan_gang_bunch_7:
                self.true,
            LocationName.orang_utan_gang_bunch_8:
                self.true,
            LocationName.orang_utan_gang_bunch_9:
                self.true,

            LocationName.clam_city_clear:
                self.true,
            EventName.clam_city_clear:
                self.true,
            LocationName.clam_city_kong:
                self.true,
            LocationName.clam_city_bunch_1:
                self.true,
            LocationName.clam_city_bunch_2:
                self.true,
            LocationName.clam_city_token_1:
                self.true,

            LocationName.bumble_b_rumble_clear:
                self.true,
            LocationName.defeated_bumble_b:
                self.true,

            LocationName.snow_barrel_blast_clear:
                self.true,
            EventName.snow_barrel_blast_clear:
                self.true,
            LocationName.snow_barrel_blast_bonus_1:
                self.true,
            LocationName.snow_barrel_blast_bonus_2:
                self.true,
            LocationName.snow_barrel_blast_bonus_3:
                self.true,
            LocationName.snow_barrel_blast_kong:
                self.true,
            LocationName.snow_barrel_blast_bunch_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_1:
                self.true,
            LocationName.snow_barrel_blast_bunch_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_3:
                self.true,
            LocationName.snow_barrel_blast_token_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_4:
                self.true,
            LocationName.snow_barrel_blast_bunch_5:
                self.true,

            LocationName.slipslide_ride_clear:
                self.true,
            EventName.slipslide_ride_clear:
                self.true,
            LocationName.slipslide_ride_bonus_1:
                self.true,
            LocationName.slipslide_ride_bonus_2:
                self.true,
            LocationName.slipslide_ride_bonus_3:
                self.true,
            LocationName.slipslide_ride_kong:
                self.true,
            LocationName.slipslide_ride_bunch_1:
                self.true,
            LocationName.slipslide_ride_bunch_2:
                self.true,
            LocationName.slipslide_ride_bunch_3:
                self.true,
            LocationName.slipslide_ride_bunch_4:
                self.true,
            LocationName.slipslide_ride_bunch_5:
                self.true,
            LocationName.slipslide_ride_bunch_6:
                self.true,
            LocationName.slipslide_ride_bunch_7:
                self.true,
            LocationName.slipslide_ride_bunch_8:
                self.true,
            LocationName.slipslide_ride_bunch_9:
                self.true,
            LocationName.slipslide_ride_token_1:
                self.true,

            LocationName.ice_age_alley_clear:
                self.true,
            EventName.ice_age_alley_clear:
                self.true,
            LocationName.ice_age_alley_bonus_1:
                self.true,
            LocationName.ice_age_alley_bonus_2:
                self.true,
            LocationName.ice_age_alley_kong:
                self.true,
            LocationName.ice_age_alley_bunch_1:
                self.true,
            LocationName.ice_age_alley_bunch_2:
                self.true,
            LocationName.ice_age_alley_bunch_3:
                self.true,

            LocationName.croctopus_chase_clear:
                self.true,
            EventName.croctopus_chase_clear:
                self.true,
            LocationName.croctopus_chase_kong:
                self.true,
            LocationName.croctopus_chase_bunch_1:
                self.true,
            LocationName.croctopus_chase_token_1:
                self.true,
            LocationName.croctopus_chase_token_2:
                self.true,
            LocationName.croctopus_chase_bunch_2:
                self.true,
            LocationName.croctopus_chase_bunch_3:
                self.true,
            LocationName.croctopus_chase_bunch_4:
                self.true,
            LocationName.croctopus_chase_bunch_5:
                self.true,
            LocationName.croctopus_chase_balloon_1:
                self.true,

            LocationName.torchlight_trouble_clear:
                self.true,
            EventName.torchlight_trouble_clear:
                self.true,
            LocationName.torchlight_trouble_bonus_1:
                self.true,
            LocationName.torchlight_trouble_bonus_2:
                self.true,
            LocationName.torchlight_trouble_kong:
                self.true,
            LocationName.torchlight_trouble_bunch_1:
                self.true,

            LocationName.rope_bridge_rumble_clear:
                self.true,
            EventName.rope_bridge_rumble_clear:
                self.true,
            LocationName.rope_bridge_rumble_bonus_2:
                self.true,
            LocationName.rope_bridge_rumble_bonus_1:
                self.true,
            LocationName.rope_bridge_rumble_kong:
                self.true,
            LocationName.rope_bridge_rumble_bunch_1:
                self.true,

            LocationName.really_gnawty_rampage_clear:
                self.true,
            LocationName.defeated_gnawty_2:
                self.true,

            LocationName.oil_drum_alley_clear:
                self.true,
            EventName.oil_drum_alley_clear:
                self.true,
            LocationName.oil_drum_alley_bonus_1:
                self.true,
            LocationName.oil_drum_alley_bonus_2:
                self.true,
            LocationName.oil_drum_alley_bonus_3:
                self.true,
            LocationName.oil_drum_alley_bonus_4:
                self.true,
            LocationName.oil_drum_alley_kong:
                self.true,
            LocationName.oil_drum_alley_bunch_1:
                self.true,
            LocationName.oil_drum_alley_bunch_2:
                self.true,

            LocationName.trick_track_trek_clear:
                self.true,
            EventName.trick_track_trek_clear:
                self.true,
            LocationName.trick_track_trek_bonus_1:
                self.true,
            LocationName.trick_track_trek_bonus_2:
                self.true,
            LocationName.trick_track_trek_bonus_3:
                self.true,
            LocationName.trick_track_trek_kong:
                self.true,
            LocationName.trick_track_trek_bunch_1:
                self.true,
            LocationName.trick_track_trek_token_1:
                self.true,

            LocationName.elevator_antics_clear:
                self.true,
            EventName.elevator_antics_clear:
                self.true,
            LocationName.elevator_antics_bonus_1:
                self.true,
            LocationName.elevator_antics_bonus_2:
                self.true,
            LocationName.elevator_antics_bonus_3:
                self.true,
            LocationName.elevator_antics_kong:
                self.true,
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.true,
            LocationName.elevator_antics_bunch_3:
                self.true,

            LocationName.poison_pond_clear:
                self.true,
            EventName.poison_pond_clear:
                self.true,
            LocationName.poison_pond_kong:
                self.true,
            LocationName.poison_pond_bunch_1:
                self.true,
            LocationName.poison_pond_bunch_2:
                self.true,
            LocationName.poison_pond_bunch_3:
                self.true,
            LocationName.poison_pond_bunch_4:
                self.true,
            LocationName.poison_pond_bunch_5:
                self.true,
            LocationName.poison_pond_token_1:
                self.true,
            LocationName.poison_pond_token_2:
                self.true,
            LocationName.poison_pond_bunch_6:
                self.true,

            LocationName.mine_cart_madness_clear:
                self.true,
            EventName.mine_cart_madness_clear:
                self.true,
            LocationName.mine_cart_madness_bonus_1:
                self.true,
            LocationName.mine_cart_madness_bonus_2:
                self.true,
            LocationName.mine_cart_madness_bonus_3:
                self.true,
            LocationName.mine_cart_madness_kong:
                self.true,
            LocationName.mine_cart_madness_token_1:
                self.true,
            LocationName.mine_cart_madness_bunch_1:
                self.true,

            LocationName.blackout_basement_clear:
                self.true,
            EventName.blackout_basement_clear:
                self.true,
            LocationName.blackout_basement_bonus_1:
                self.true,
            LocationName.blackout_basement_bonus_2:
                self.true,
            LocationName.blackout_basement_kong:
                self.true,
            LocationName.blackout_basement_token_1:
                self.true,
            LocationName.blackout_basement_bunch_1:
                self.true,

            LocationName.boss_dumb_drum_clear:
                self.true,
            LocationName.defeated_boss_dumb_drum:
                self.true,

            LocationName.tanked_up_trouble_clear:
                self.true,
            EventName.tanked_up_trouble_clear:
                self.true,
            LocationName.tanked_up_trouble_bonus_1:
                self.true,
            LocationName.tanked_up_trouble_kong:
                self.true,
            LocationName.tanked_up_trouble_bunch_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_2:
                self.true,
            LocationName.tanked_up_trouble_token_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_3:
                self.true,
            LocationName.tanked_up_trouble_bunch_4:
                self.true,

            LocationName.manic_mincers_clear:
                self.true,
            EventName.manic_mincers_clear:
                self.true,
            LocationName.manic_mincers_bonus_1:
                self.true,
            LocationName.manic_mincers_bonus_2:
                self.true,
            LocationName.manic_mincers_kong:
                self.true,
            LocationName.manic_mincers_bunch_1:
                self.true,
            LocationName.manic_mincers_bunch_2:
                self.true,
            LocationName.manic_mincers_token_1:
                self.true,

            LocationName.misty_mine_clear:
                self.true,
            EventName.misty_mine_clear:
                self.true,
            LocationName.misty_mine_bonus_1:
                self.true,
            LocationName.misty_mine_bonus_2:
                self.true,
            LocationName.misty_mine_kong:
                self.true,
            LocationName.misty_mine_token_1:
                self.true,
            LocationName.misty_mine_bunch_1:
                self.true,
            LocationName.misty_mine_bunch_2:
                self.true,
            LocationName.misty_mine_token_2:
                self.true,

            LocationName.loopy_lights_clear:
                self.true,
            EventName.loopy_lights_clear:
                self.true,
            LocationName.loopy_lights_bonus_1:
                self.true,
            LocationName.loopy_lights_bonus_2:
                self.true,
            LocationName.loopy_lights_kong:
                self.true,
            LocationName.loopy_lights_bunch_1:
                self.true,
            LocationName.loopy_lights_bunch_2:
                self.true,

            LocationName.platform_perils_clear:
                self.true,
            EventName.platform_perils_clear:
                self.true,
            LocationName.platform_perils_bonus_1:
                self.true,
            LocationName.platform_perils_bonus_2:
                self.true,
            LocationName.platform_perils_kong:
                self.true,
            LocationName.platform_perils_token_1:
                self.true,
            LocationName.platform_perils_bunch_1:
                self.true,

            LocationName.necky_revenge_clear:
                self.true,
            LocationName.defeated_necky_2:
                self.true,
        }

class CKDLooseRules(CKDRules):
    def __init__(self, world: "CKDWorld") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                self.true,
            LocationName.jungle_hijinxs_bonus_2:
                self.true,
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_4:
                self.true,
            LocationName.jungle_hijinxs_bunch_5:
                self.true,
            LocationName.jungle_hijinxs_bunch_6:
                self.true,
            LocationName.jungle_hijinxs_balloon_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_7:
                self.true,
            LocationName.jungle_hijinxs_bunch_8:
                self.true,
            LocationName.jungle_hijinxs_bunch_9:
                self.true,
            LocationName.jungle_hijinxs_bunch_10:
                self.true,
            LocationName.jungle_hijinxs_bunch_11:
                self.true,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_13:
                self.true,
            LocationName.jungle_hijinxs_balloon_4:
                self.true,
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                self.true,
            LocationName.jungle_hijinxs_bunch_15:
                self.true,
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                self.true,
            LocationName.jungle_hijinxs_bunch_18:
                self.true,
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                self.true,
            LocationName.jungle_hijinxs_balloon_6:
                self.true,

            LocationName.ropey_rampage_clear:
                self.true,
            EventName.ropey_rampage_clear:
                self.true,
            LocationName.ropey_rampage_bonus_1:
                self.true,
            LocationName.ropey_rampage_bonus_2:
                self.true,
            LocationName.ropey_rampage_kong:
                self.true,
            LocationName.ropey_rampage_bunch_1:
                self.true,
            LocationName.ropey_rampage_bunch_2:
                self.true,
            LocationName.ropey_rampage_bunch_3:
                self.true,
            LocationName.ropey_rampage_bunch_4:
                self.true,
            LocationName.ropey_rampage_bunch_5:
                self.true,
            LocationName.ropey_rampage_bunch_6:
                self.true,
            LocationName.ropey_rampage_bunch_7:
                self.true,
            LocationName.ropey_rampage_bunch_8:
                self.true,
            LocationName.ropey_rampage_bunch_9:
                self.true,
            LocationName.ropey_rampage_token_1:
                self.true,
            LocationName.ropey_rampage_bunch_10:
                self.true,
            LocationName.ropey_rampage_bunch_11:
                self.true,
            LocationName.ropey_rampage_bunch_12:
                self.true,
            LocationName.ropey_rampage_bunch_13:
                self.true,
            LocationName.ropey_rampage_bunch_14:
                self.true,
            LocationName.ropey_rampage_bunch_15:
                self.true,
            LocationName.ropey_rampage_token_2:
                self.true,
            LocationName.ropey_rampage_bunch_16:
                self.true,
            LocationName.ropey_rampage_bunch_17:
                self.true,
            LocationName.ropey_rampage_bunch_18:
                self.true,
            LocationName.ropey_rampage_bunch_19:
                self.true,

            LocationName.reptile_rumble_clear:
                self.true,
            EventName.reptile_rumble_clear:
                self.true,
            LocationName.reptile_rumble_bonus_1:
                self.true,
            LocationName.reptile_rumble_bonus_2:
                self.true,
            LocationName.reptile_rumble_bonus_3:
                self.true,
            LocationName.reptile_rumble_kong:
                self.true,
            LocationName.reptile_rumble_bunch_1:
                self.true,
            LocationName.reptile_rumble_bunch_2:
                self.true,
            LocationName.reptile_rumble_bunch_3:
                self.true,
            LocationName.reptile_rumble_bunch_4:
                self.true,
            LocationName.reptile_rumble_bunch_5:
                self.true,
            LocationName.reptile_rumble_bunch_6:
                self.true,
            LocationName.reptile_rumble_bunch_7:
                self.true,
            LocationName.reptile_rumble_bunch_8:
                self.true,
            LocationName.reptile_rumble_bunch_9:
                self.true,
            LocationName.reptile_rumble_bunch_10:
                self.true,
            LocationName.reptile_rumble_token_1:
                self.true,
            LocationName.reptile_rumble_bunch_11:
                self.true,
            LocationName.reptile_rumble_bunch_12:
                self.true,
            LocationName.reptile_rumble_bunch_13:
                self.true,
            LocationName.reptile_rumble_bunch_14:
                self.true,

            LocationName.coral_capers_clear:
                self.true,
            EventName.coral_capers_clear:
                self.true,
            LocationName.coral_capers_kong:
                self.true,
            LocationName.coral_capers_bunch_1:
                self.true,
            LocationName.coral_capers_balloon_1:
                self.true,
            LocationName.coral_capers_bunch_2:
                self.true,
            LocationName.coral_capers_token_1:
                self.true,

            LocationName.barrel_cannon_canyon_clear:
                self.true,
            EventName.barrel_cannon_canyon_clear:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_2:
                self.true,
            LocationName.barrel_cannon_canyon_kong:
                self.true,
            LocationName.barrel_cannon_canyon_token_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_3:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_4:
                self.true,
            LocationName.barrel_cannon_canyon_token_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_5:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_6:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_7:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_8:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_9:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_10:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_11:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_12:
                self.true,

            LocationName.very_gnawty_lair_clear:
                self.true,
            LocationName.defeated_gnawty_1:
                self.true,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.true,
            LocationName.winky_walkway_kong:
                self.true,
            LocationName.winky_walkway_bunch_1:
                self.true,
            LocationName.winky_walkway_bunch_2:
                self.true,
            LocationName.winky_walkway_bunch_3:
                self.true,
            LocationName.winky_walkway_bunch_4:
                self.true,
            LocationName.winky_walkway_token_1:
                self.true,
            LocationName.winky_walkway_bunch_5:
                self.true,

            LocationName.mine_cart_carnage_clear:
                self.true,
            EventName.mine_cart_carnage_clear:
                self.true,
            LocationName.mine_cart_carnage_kong:
                self.true,
            LocationName.mine_cart_carnage_bunch_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_2:
                self.true,
            LocationName.mine_cart_carnage_token_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_3:
                self.true,
            LocationName.mine_cart_carnage_balloon_1:
                self.true,

            LocationName.bouncy_bonanza_clear:
                self.true,
            EventName.bouncy_bonanza_clear:
                self.true,
            LocationName.bouncy_bonanza_bonus_1:
                self.true,
            LocationName.bouncy_bonanza_bonus_2:
                self.true,
            LocationName.bouncy_bonanza_kong:
                self.true,
            LocationName.bouncy_bonanza_token_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_2:
                self.true,
            LocationName.bouncy_bonanza_bunch_3:
                self.true,
            LocationName.bouncy_bonanza_bunch_4:
                self.true,
            LocationName.bouncy_bonanza_bunch_5:
                self.true,
            LocationName.bouncy_bonanza_bunch_6:
                self.true,
            LocationName.bouncy_bonanza_bunch_7:
                self.true,
            LocationName.bouncy_bonanza_bunch_8:
                self.true,
            LocationName.bouncy_bonanza_bunch_9:
                self.true,
            LocationName.bouncy_bonanza_bunch_10:
                self.true,

            LocationName.stop_go_station_clear:
                self.true,
            EventName.stop_go_station_clear:
                self.true,
            LocationName.stop_go_station_bonus_1:
                self.true,
            LocationName.stop_go_station_bonus_2:
                self.true,
            LocationName.stop_go_station_kong:
                self.true,
            LocationName.stop_go_station_bunch_1:
                self.true,
            LocationName.stop_go_station_bunch_2:
                self.true,
            LocationName.stop_go_station_bunch_3:
                self.true,
            LocationName.stop_go_station_token_1:
                self.true,
            LocationName.stop_go_station_bunch_4:
                self.true,
            LocationName.stop_go_station_bunch_5:
                self.true,
            LocationName.stop_go_station_bunch_6:
                self.true,
            LocationName.stop_go_station_bunch_7:
                self.true,

            LocationName.millstone_mayhem_clear:
                self.true,
            EventName.millstone_mayhem_clear:
                self.true,
            LocationName.millstone_mayhem_bonus_1:
                self.true,
            LocationName.millstone_mayhem_bonus_2:
                self.true,
            LocationName.millstone_mayhem_bonus_3:
                self.true,
            LocationName.millstone_mayhem_kong:
                self.true,
            LocationName.millstone_mayhem_bunch_1:
                self.true,
            LocationName.millstone_mayhem_bunch_2:
                self.true,
            LocationName.millstone_mayhem_bunch_3:
                self.true,
            LocationName.millstone_mayhem_bunch_4:
                self.true,
            LocationName.millstone_mayhem_bunch_5:
                self.true,
            LocationName.millstone_mayhem_bunch_6:
                self.true,
            LocationName.millstone_mayhem_bunch_7:
                self.true,
            LocationName.millstone_mayhem_bunch_8:
                self.true,
            LocationName.millstone_mayhem_bunch_9:
                self.true,

            LocationName.necky_nuts_clear:
                self.true,
            LocationName.defeated_necky_1:
                self.true,

            LocationName.vulture_culture_clear:
                self.true,
            EventName.vulture_culture_clear:
                self.true,
            LocationName.vulture_culture_bonus_1:
                self.true,
            LocationName.vulture_culture_bonus_2:
                self.true,
            LocationName.vulture_culture_bonus_3:
                self.true,
            LocationName.vulture_culture_kong:
                self.true,
            LocationName.vulture_culture_bunch_1:
                self.true,
            LocationName.vulture_culture_bunch_2:
                self.true,
            LocationName.vulture_culture_bunch_3:
                self.true,
            LocationName.vulture_culture_bunch_4:
                self.true,
            LocationName.vulture_culture_bunch_5:
                self.true,
            LocationName.vulture_culture_bunch_6:
                self.true,

            LocationName.tree_top_town_clear:
                self.true,
            EventName.tree_top_town_clear:
                self.true,
            LocationName.tree_top_town_bonus_1:
                self.true,
            LocationName.tree_top_town_bonus_2:
                self.true,
            LocationName.tree_top_town_kong:
                self.true,
            LocationName.tree_top_town_bunch_1:
                self.true,
            LocationName.tree_top_town_bunch_2:
                self.true,
            LocationName.tree_top_town_bunch_3:
                self.true,
            LocationName.tree_top_town_bunch_4:
                self.true,
            LocationName.tree_top_town_token_1:
                self.true,

            LocationName.forest_frenzy_clear:
                self.true,
            EventName.forest_frenzy_clear:
                self.true,
            LocationName.forest_frenzy_bonus_1:
                self.true,
            LocationName.forest_frenzy_bonus_2:
                self.true,
            LocationName.forest_frenzy_kong:
                self.true,
            LocationName.forest_frenzy_bunch_1:
                self.true,
            LocationName.forest_frenzy_bunch_2:
                self.true,
            LocationName.forest_frenzy_bunch_3:
                self.true,
            LocationName.forest_frenzy_bunch_4:
                self.true,
            LocationName.forest_frenzy_bunch_5:
                self.true,
            LocationName.forest_frenzy_balloon_1:
                self.true,

            LocationName.temple_tempest_clear:
                self.true,
            EventName.temple_tempest_clear:
                self.true,
            LocationName.temple_tempest_bonus_1:
                self.true,
            LocationName.temple_tempest_bonus_2:
                self.true,
            LocationName.temple_tempest_kong:
                self.true,
            LocationName.temple_tempest_token_1:
                self.true,
            LocationName.temple_tempest_bunch_1:
                self.true,
            LocationName.temple_tempest_bunch_2:
                self.true,
            LocationName.temple_tempest_bunch_3:
                self.true,
            LocationName.temple_tempest_bunch_4:
                self.true,
            LocationName.temple_tempest_bunch_5:
                self.true,
            LocationName.temple_tempest_bunch_6:
                self.true,
            LocationName.temple_tempest_bunch_7:
                self.true,
            LocationName.temple_tempest_bunch_8:
                self.true,

            LocationName.orang_utan_gang_clear:
                self.true,
            EventName.orang_utan_gang_clear:
                self.true,
            LocationName.orang_utan_gang_bonus_1:
                self.true,
            LocationName.orang_utan_gang_bonus_2:
                self.true,
            LocationName.orang_utan_gang_bonus_3:
                self.true,
            LocationName.orang_utan_gang_bonus_4:
                self.true,
            LocationName.orang_utan_gang_bonus_5:
                self.true,
            LocationName.orang_utan_gang_kong:
                self.true,
            LocationName.orang_utan_gang_bunch_1:
                self.true,
            LocationName.orang_utan_gang_bunch_2:
                self.true,
            LocationName.orang_utan_gang_bunch_3:
                self.true,
            LocationName.orang_utan_gang_bunch_4:
                self.true,
            LocationName.orang_utan_gang_bunch_5:
                self.true,
            LocationName.orang_utan_gang_bunch_6:
                self.true,
            LocationName.orang_utan_gang_token_1:
                self.true,
            LocationName.orang_utan_gang_bunch_7:
                self.true,
            LocationName.orang_utan_gang_bunch_8:
                self.true,
            LocationName.orang_utan_gang_bunch_9:
                self.true,

            LocationName.clam_city_clear:
                self.true,
            EventName.clam_city_clear:
                self.true,
            LocationName.clam_city_kong:
                self.true,
            LocationName.clam_city_bunch_1:
                self.true,
            LocationName.clam_city_bunch_2:
                self.true,
            LocationName.clam_city_token_1:
                self.true,

            LocationName.bumble_b_rumble_clear:
                self.true,
            LocationName.defeated_bumble_b:
                self.true,

            LocationName.snow_barrel_blast_clear:
                self.true,
            EventName.snow_barrel_blast_clear:
                self.true,
            LocationName.snow_barrel_blast_bonus_1:
                self.true,
            LocationName.snow_barrel_blast_bonus_2:
                self.true,
            LocationName.snow_barrel_blast_bonus_3:
                self.true,
            LocationName.snow_barrel_blast_kong:
                self.true,
            LocationName.snow_barrel_blast_bunch_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_1:
                self.true,
            LocationName.snow_barrel_blast_bunch_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_3:
                self.true,
            LocationName.snow_barrel_blast_token_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_4:
                self.true,
            LocationName.snow_barrel_blast_bunch_5:
                self.true,

            LocationName.slipslide_ride_clear:
                self.true,
            EventName.slipslide_ride_clear:
                self.true,
            LocationName.slipslide_ride_bonus_1:
                self.true,
            LocationName.slipslide_ride_bonus_2:
                self.true,
            LocationName.slipslide_ride_bonus_3:
                self.true,
            LocationName.slipslide_ride_kong:
                self.true,
            LocationName.slipslide_ride_bunch_1:
                self.true,
            LocationName.slipslide_ride_bunch_2:
                self.true,
            LocationName.slipslide_ride_bunch_3:
                self.true,
            LocationName.slipslide_ride_bunch_4:
                self.true,
            LocationName.slipslide_ride_bunch_5:
                self.true,
            LocationName.slipslide_ride_bunch_6:
                self.true,
            LocationName.slipslide_ride_bunch_7:
                self.true,
            LocationName.slipslide_ride_bunch_8:
                self.true,
            LocationName.slipslide_ride_bunch_9:
                self.true,
            LocationName.slipslide_ride_token_1:
                self.true,

            LocationName.ice_age_alley_clear:
                self.true,
            EventName.ice_age_alley_clear:
                self.true,
            LocationName.ice_age_alley_bonus_1:
                self.true,
            LocationName.ice_age_alley_bonus_2:
                self.true,
            LocationName.ice_age_alley_kong:
                self.true,
            LocationName.ice_age_alley_bunch_1:
                self.true,
            LocationName.ice_age_alley_bunch_2:
                self.true,
            LocationName.ice_age_alley_bunch_3:
                self.true,

            LocationName.croctopus_chase_clear:
                self.true,
            EventName.croctopus_chase_clear:
                self.true,
            LocationName.croctopus_chase_kong:
                self.true,
            LocationName.croctopus_chase_bunch_1:
                self.true,
            LocationName.croctopus_chase_token_1:
                self.true,
            LocationName.croctopus_chase_token_2:
                self.true,
            LocationName.croctopus_chase_bunch_2:
                self.true,
            LocationName.croctopus_chase_bunch_3:
                self.true,
            LocationName.croctopus_chase_bunch_4:
                self.true,
            LocationName.croctopus_chase_bunch_5:
                self.true,
            LocationName.croctopus_chase_balloon_1:
                self.true,

            LocationName.torchlight_trouble_clear:
                self.true,
            EventName.torchlight_trouble_clear:
                self.true,
            LocationName.torchlight_trouble_bonus_1:
                self.true,
            LocationName.torchlight_trouble_bonus_2:
                self.true,
            LocationName.torchlight_trouble_kong:
                self.true,
            LocationName.torchlight_trouble_bunch_1:
                self.true,

            LocationName.rope_bridge_rumble_clear:
                self.true,
            EventName.rope_bridge_rumble_clear:
                self.true,
            LocationName.rope_bridge_rumble_bonus_2:
                self.true,
            LocationName.rope_bridge_rumble_bonus_1:
                self.true,
            LocationName.rope_bridge_rumble_kong:
                self.true,
            LocationName.rope_bridge_rumble_bunch_1:
                self.true,

            LocationName.really_gnawty_rampage_clear:
                self.true,
            LocationName.defeated_gnawty_2:
                self.true,

            LocationName.oil_drum_alley_clear:
                self.true,
            EventName.oil_drum_alley_clear:
                self.true,
            LocationName.oil_drum_alley_bonus_1:
                self.true,
            LocationName.oil_drum_alley_bonus_2:
                self.true,
            LocationName.oil_drum_alley_bonus_3:
                self.true,
            LocationName.oil_drum_alley_bonus_4:
                self.true,
            LocationName.oil_drum_alley_kong:
                self.true,
            LocationName.oil_drum_alley_bunch_1:
                self.true,
            LocationName.oil_drum_alley_bunch_2:
                self.true,

            LocationName.trick_track_trek_clear:
                self.true,
            EventName.trick_track_trek_clear:
                self.true,
            LocationName.trick_track_trek_bonus_1:
                self.true,
            LocationName.trick_track_trek_bonus_2:
                self.true,
            LocationName.trick_track_trek_bonus_3:
                self.true,
            LocationName.trick_track_trek_kong:
                self.true,
            LocationName.trick_track_trek_bunch_1:
                self.true,
            LocationName.trick_track_trek_token_1:
                self.true,

            LocationName.elevator_antics_clear:
                self.true,
            EventName.elevator_antics_clear:
                self.true,
            LocationName.elevator_antics_bonus_1:
                self.true,
            LocationName.elevator_antics_bonus_2:
                self.true,
            LocationName.elevator_antics_bonus_3:
                self.true,
            LocationName.elevator_antics_kong:
                self.true,
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.true,
            LocationName.elevator_antics_bunch_3:
                self.true,

            LocationName.poison_pond_clear:
                self.true,
            EventName.poison_pond_clear:
                self.true,
            LocationName.poison_pond_kong:
                self.true,
            LocationName.poison_pond_bunch_1:
                self.true,
            LocationName.poison_pond_bunch_2:
                self.true,
            LocationName.poison_pond_bunch_3:
                self.true,
            LocationName.poison_pond_bunch_4:
                self.true,
            LocationName.poison_pond_bunch_5:
                self.true,
            LocationName.poison_pond_token_1:
                self.true,
            LocationName.poison_pond_token_2:
                self.true,
            LocationName.poison_pond_bunch_6:
                self.true,

            LocationName.mine_cart_madness_clear:
                self.true,
            EventName.mine_cart_madness_clear:
                self.true,
            LocationName.mine_cart_madness_bonus_1:
                self.true,
            LocationName.mine_cart_madness_bonus_2:
                self.true,
            LocationName.mine_cart_madness_bonus_3:
                self.true,
            LocationName.mine_cart_madness_kong:
                self.true,
            LocationName.mine_cart_madness_token_1:
                self.true,
            LocationName.mine_cart_madness_bunch_1:
                self.true,

            LocationName.blackout_basement_clear:
                self.true,
            EventName.blackout_basement_clear:
                self.true,
            LocationName.blackout_basement_bonus_1:
                self.true,
            LocationName.blackout_basement_bonus_2:
                self.true,
            LocationName.blackout_basement_kong:
                self.true,
            LocationName.blackout_basement_token_1:
                self.true,
            LocationName.blackout_basement_bunch_1:
                self.true,

            LocationName.boss_dumb_drum_clear:
                self.true,
            LocationName.defeated_boss_dumb_drum:
                self.true,

            LocationName.tanked_up_trouble_clear:
                self.true,
            EventName.tanked_up_trouble_clear:
                self.true,
            LocationName.tanked_up_trouble_bonus_1:
                self.true,
            LocationName.tanked_up_trouble_kong:
                self.true,
            LocationName.tanked_up_trouble_bunch_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_2:
                self.true,
            LocationName.tanked_up_trouble_token_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_3:
                self.true,
            LocationName.tanked_up_trouble_bunch_4:
                self.true,

            LocationName.manic_mincers_clear:
                self.true,
            EventName.manic_mincers_clear:
                self.true,
            LocationName.manic_mincers_bonus_1:
                self.true,
            LocationName.manic_mincers_bonus_2:
                self.true,
            LocationName.manic_mincers_kong:
                self.true,
            LocationName.manic_mincers_bunch_1:
                self.true,
            LocationName.manic_mincers_bunch_2:
                self.true,
            LocationName.manic_mincers_token_1:
                self.true,

            LocationName.misty_mine_clear:
                self.true,
            EventName.misty_mine_clear:
                self.true,
            LocationName.misty_mine_bonus_1:
                self.true,
            LocationName.misty_mine_bonus_2:
                self.true,
            LocationName.misty_mine_kong:
                self.true,
            LocationName.misty_mine_token_1:
                self.true,
            LocationName.misty_mine_bunch_1:
                self.true,
            LocationName.misty_mine_bunch_2:
                self.true,
            LocationName.misty_mine_token_2:
                self.true,

            LocationName.loopy_lights_clear:
                self.true,
            EventName.loopy_lights_clear:
                self.true,
            LocationName.loopy_lights_bonus_1:
                self.true,
            LocationName.loopy_lights_bonus_2:
                self.true,
            LocationName.loopy_lights_kong:
                self.true,
            LocationName.loopy_lights_bunch_1:
                self.true,
            LocationName.loopy_lights_bunch_2:
                self.true,

            LocationName.platform_perils_clear:
                self.true,
            EventName.platform_perils_clear:
                self.true,
            LocationName.platform_perils_bonus_1:
                self.true,
            LocationName.platform_perils_bonus_2:
                self.true,
            LocationName.platform_perils_kong:
                self.true,
            LocationName.platform_perils_token_1:
                self.true,
            LocationName.platform_perils_bunch_1:
                self.true,

            LocationName.necky_revenge_clear:
                self.true,
            LocationName.defeated_necky_2:
                self.true,
        }

    def set_ckd_rules(self) -> None:
        super().set_ckd_rules()


class CKDExpertRules(CKDRules):
    def __init__(self, world: "CKDWorld") -> None:
        super().__init__(world)

      
        self.location_rules = {
            LocationName.jungle_hijinxs_clear:
                self.true,
            EventName.jungle_hijinxs_clear:
                self.true,
            LocationName.jungle_hijinxs_bonus_1:
                self.true,
            LocationName.jungle_hijinxs_bonus_2:
                self.true,
            LocationName.jungle_hijinxs_kong:
                self.true,
            LocationName.jungle_hijinxs_balloon_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_4:
                self.true,
            LocationName.jungle_hijinxs_bunch_5:
                self.true,
            LocationName.jungle_hijinxs_bunch_6:
                self.true,
            LocationName.jungle_hijinxs_balloon_2:
                self.true,
            LocationName.jungle_hijinxs_bunch_7:
                self.true,
            LocationName.jungle_hijinxs_bunch_8:
                self.true,
            LocationName.jungle_hijinxs_bunch_9:
                self.true,
            LocationName.jungle_hijinxs_bunch_10:
                self.true,
            LocationName.jungle_hijinxs_bunch_11:
                self.true,
            LocationName.jungle_hijinxs_bunch_12:
                self.true,
            LocationName.jungle_hijinxs_balloon_3:
                self.true,
            LocationName.jungle_hijinxs_bunch_13:
                self.true,
            LocationName.jungle_hijinxs_balloon_4:
                self.true,
            LocationName.jungle_hijinxs_token_1:
                self.true,
            LocationName.jungle_hijinxs_bunch_14:
                self.true,
            LocationName.jungle_hijinxs_bunch_15:
                self.true,
            LocationName.jungle_hijinxs_bunch_16:
                self.true,
            LocationName.jungle_hijinxs_bunch_17:
                self.true,
            LocationName.jungle_hijinxs_bunch_18:
                self.true,
            LocationName.jungle_hijinxs_bunch_19:
                self.true,
            LocationName.jungle_hijinxs_balloon_5:
                self.true,
            LocationName.jungle_hijinxs_balloon_6:
                self.true,

            LocationName.ropey_rampage_clear:
                self.true,
            EventName.ropey_rampage_clear:
                self.true,
            LocationName.ropey_rampage_bonus_1:
                self.true,
            LocationName.ropey_rampage_bonus_2:
                self.true,
            LocationName.ropey_rampage_kong:
                self.true,
            LocationName.ropey_rampage_bunch_1:
                self.true,
            LocationName.ropey_rampage_bunch_2:
                self.true,
            LocationName.ropey_rampage_bunch_3:
                self.true,
            LocationName.ropey_rampage_bunch_4:
                self.true,
            LocationName.ropey_rampage_bunch_5:
                self.true,
            LocationName.ropey_rampage_bunch_6:
                self.true,
            LocationName.ropey_rampage_bunch_7:
                self.true,
            LocationName.ropey_rampage_bunch_8:
                self.true,
            LocationName.ropey_rampage_bunch_9:
                self.true,
            LocationName.ropey_rampage_token_1:
                self.true,
            LocationName.ropey_rampage_bunch_10:
                self.true,
            LocationName.ropey_rampage_bunch_11:
                self.true,
            LocationName.ropey_rampage_bunch_12:
                self.true,
            LocationName.ropey_rampage_bunch_13:
                self.true,
            LocationName.ropey_rampage_bunch_14:
                self.true,
            LocationName.ropey_rampage_bunch_15:
                self.true,
            LocationName.ropey_rampage_token_2:
                self.true,
            LocationName.ropey_rampage_bunch_16:
                self.true,
            LocationName.ropey_rampage_bunch_17:
                self.true,
            LocationName.ropey_rampage_bunch_18:
                self.true,
            LocationName.ropey_rampage_bunch_19:
                self.true,

            LocationName.reptile_rumble_clear:
                self.true,
            EventName.reptile_rumble_clear:
                self.true,
            LocationName.reptile_rumble_bonus_1:
                self.true,
            LocationName.reptile_rumble_bonus_2:
                self.true,
            LocationName.reptile_rumble_bonus_3:
                self.true,
            LocationName.reptile_rumble_kong:
                self.true,
            LocationName.reptile_rumble_bunch_1:
                self.true,
            LocationName.reptile_rumble_bunch_2:
                self.true,
            LocationName.reptile_rumble_bunch_3:
                self.true,
            LocationName.reptile_rumble_bunch_4:
                self.true,
            LocationName.reptile_rumble_bunch_5:
                self.true,
            LocationName.reptile_rumble_bunch_6:
                self.true,
            LocationName.reptile_rumble_bunch_7:
                self.true,
            LocationName.reptile_rumble_bunch_8:
                self.true,
            LocationName.reptile_rumble_bunch_9:
                self.true,
            LocationName.reptile_rumble_bunch_10:
                self.true,
            LocationName.reptile_rumble_token_1:
                self.true,
            LocationName.reptile_rumble_bunch_11:
                self.true,
            LocationName.reptile_rumble_bunch_12:
                self.true,
            LocationName.reptile_rumble_bunch_13:
                self.true,
            LocationName.reptile_rumble_bunch_14:
                self.true,

            LocationName.coral_capers_clear:
                self.true,
            EventName.coral_capers_clear:
                self.true,
            LocationName.coral_capers_kong:
                self.true,
            LocationName.coral_capers_bunch_1:
                self.true,
            LocationName.coral_capers_balloon_1:
                self.true,
            LocationName.coral_capers_bunch_2:
                self.true,
            LocationName.coral_capers_token_1:
                self.true,

            LocationName.barrel_cannon_canyon_clear:
                self.true,
            EventName.barrel_cannon_canyon_clear:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_1:
                self.true,
            LocationName.barrel_cannon_canyon_bonus_2:
                self.true,
            LocationName.barrel_cannon_canyon_kong:
                self.true,
            LocationName.barrel_cannon_canyon_token_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_1:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_3:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_4:
                self.true,
            LocationName.barrel_cannon_canyon_token_2:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_5:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_6:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_7:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_8:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_9:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_10:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_11:
                self.true,
            LocationName.barrel_cannon_canyon_bunch_12:
                self.true,

            LocationName.very_gnawty_lair_clear:
                self.true,
            LocationName.defeated_gnawty_1:
                self.true,

            LocationName.winky_walkway_clear:
                self.true,
            EventName.winky_walkway_clear:
                self.true,
            LocationName.winky_walkway_bonus_1:
                self.true,
            LocationName.winky_walkway_kong:
                self.true,
            LocationName.winky_walkway_bunch_1:
                self.true,
            LocationName.winky_walkway_bunch_2:
                self.true,
            LocationName.winky_walkway_bunch_3:
                self.true,
            LocationName.winky_walkway_bunch_4:
                self.true,
            LocationName.winky_walkway_token_1:
                self.true,
            LocationName.winky_walkway_bunch_5:
                self.true,

            LocationName.mine_cart_carnage_clear:
                self.true,
            EventName.mine_cart_carnage_clear:
                self.true,
            LocationName.mine_cart_carnage_kong:
                self.true,
            LocationName.mine_cart_carnage_bunch_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_2:
                self.true,
            LocationName.mine_cart_carnage_token_1:
                self.true,
            LocationName.mine_cart_carnage_bunch_3:
                self.true,
            LocationName.mine_cart_carnage_balloon_1:
                self.true,

            LocationName.bouncy_bonanza_clear:
                self.true,
            EventName.bouncy_bonanza_clear:
                self.true,
            LocationName.bouncy_bonanza_bonus_1:
                self.true,
            LocationName.bouncy_bonanza_bonus_2:
                self.true,
            LocationName.bouncy_bonanza_kong:
                self.true,
            LocationName.bouncy_bonanza_token_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_1:
                self.true,
            LocationName.bouncy_bonanza_bunch_2:
                self.true,
            LocationName.bouncy_bonanza_bunch_3:
                self.true,
            LocationName.bouncy_bonanza_bunch_4:
                self.true,
            LocationName.bouncy_bonanza_bunch_5:
                self.true,
            LocationName.bouncy_bonanza_bunch_6:
                self.true,
            LocationName.bouncy_bonanza_bunch_7:
                self.true,
            LocationName.bouncy_bonanza_bunch_8:
                self.true,
            LocationName.bouncy_bonanza_bunch_9:
                self.true,
            LocationName.bouncy_bonanza_bunch_10:
                self.true,

            LocationName.stop_go_station_clear:
                self.true,
            EventName.stop_go_station_clear:
                self.true,
            LocationName.stop_go_station_bonus_1:
                self.true,
            LocationName.stop_go_station_bonus_2:
                self.true,
            LocationName.stop_go_station_kong:
                self.true,
            LocationName.stop_go_station_bunch_1:
                self.true,
            LocationName.stop_go_station_bunch_2:
                self.true,
            LocationName.stop_go_station_bunch_3:
                self.true,
            LocationName.stop_go_station_token_1:
                self.true,
            LocationName.stop_go_station_bunch_4:
                self.true,
            LocationName.stop_go_station_bunch_5:
                self.true,
            LocationName.stop_go_station_bunch_6:
                self.true,
            LocationName.stop_go_station_bunch_7:
                self.true,

            LocationName.millstone_mayhem_clear:
                self.true,
            EventName.millstone_mayhem_clear:
                self.true,
            LocationName.millstone_mayhem_bonus_1:
                self.true,
            LocationName.millstone_mayhem_bonus_2:
                self.true,
            LocationName.millstone_mayhem_bonus_3:
                self.true,
            LocationName.millstone_mayhem_kong:
                self.true,
            LocationName.millstone_mayhem_bunch_1:
                self.true,
            LocationName.millstone_mayhem_bunch_2:
                self.true,
            LocationName.millstone_mayhem_bunch_3:
                self.true,
            LocationName.millstone_mayhem_bunch_4:
                self.true,
            LocationName.millstone_mayhem_bunch_5:
                self.true,
            LocationName.millstone_mayhem_bunch_6:
                self.true,
            LocationName.millstone_mayhem_bunch_7:
                self.true,
            LocationName.millstone_mayhem_bunch_8:
                self.true,
            LocationName.millstone_mayhem_bunch_9:
                self.true,

            LocationName.necky_nuts_clear:
                self.true,
            LocationName.defeated_necky_1:
                self.true,

            LocationName.vulture_culture_clear:
                self.true,
            EventName.vulture_culture_clear:
                self.true,
            LocationName.vulture_culture_bonus_1:
                self.true,
            LocationName.vulture_culture_bonus_2:
                self.true,
            LocationName.vulture_culture_bonus_3:
                self.true,
            LocationName.vulture_culture_kong:
                self.true,
            LocationName.vulture_culture_bunch_1:
                self.true,
            LocationName.vulture_culture_bunch_2:
                self.true,
            LocationName.vulture_culture_bunch_3:
                self.true,
            LocationName.vulture_culture_bunch_4:
                self.true,
            LocationName.vulture_culture_bunch_5:
                self.true,
            LocationName.vulture_culture_bunch_6:
                self.true,

            LocationName.tree_top_town_clear:
                self.true,
            EventName.tree_top_town_clear:
                self.true,
            LocationName.tree_top_town_bonus_1:
                self.true,
            LocationName.tree_top_town_bonus_2:
                self.true,
            LocationName.tree_top_town_kong:
                self.true,
            LocationName.tree_top_town_bunch_1:
                self.true,
            LocationName.tree_top_town_bunch_2:
                self.true,
            LocationName.tree_top_town_bunch_3:
                self.true,
            LocationName.tree_top_town_bunch_4:
                self.true,
            LocationName.tree_top_town_token_1:
                self.true,

            LocationName.forest_frenzy_clear:
                self.true,
            EventName.forest_frenzy_clear:
                self.true,
            LocationName.forest_frenzy_bonus_1:
                self.true,
            LocationName.forest_frenzy_bonus_2:
                self.true,
            LocationName.forest_frenzy_kong:
                self.true,
            LocationName.forest_frenzy_bunch_1:
                self.true,
            LocationName.forest_frenzy_bunch_2:
                self.true,
            LocationName.forest_frenzy_bunch_3:
                self.true,
            LocationName.forest_frenzy_bunch_4:
                self.true,
            LocationName.forest_frenzy_bunch_5:
                self.true,
            LocationName.forest_frenzy_balloon_1:
                self.true,

            LocationName.temple_tempest_clear:
                self.true,
            EventName.temple_tempest_clear:
                self.true,
            LocationName.temple_tempest_bonus_1:
                self.true,
            LocationName.temple_tempest_bonus_2:
                self.true,
            LocationName.temple_tempest_kong:
                self.true,
            LocationName.temple_tempest_token_1:
                self.true,
            LocationName.temple_tempest_bunch_1:
                self.true,
            LocationName.temple_tempest_bunch_2:
                self.true,
            LocationName.temple_tempest_bunch_3:
                self.true,
            LocationName.temple_tempest_bunch_4:
                self.true,
            LocationName.temple_tempest_bunch_5:
                self.true,
            LocationName.temple_tempest_bunch_6: 
                self.true,
            LocationName.temple_tempest_bunch_7:
                self.true,
            LocationName.temple_tempest_bunch_8:
                self.true,

            LocationName.orang_utan_gang_clear:
                self.true,
            EventName.orang_utan_gang_clear:
                self.true,
            LocationName.orang_utan_gang_bonus_1:
                self.true,
            LocationName.orang_utan_gang_bonus_2:
                self.true,
            LocationName.orang_utan_gang_bonus_3:
                self.true,
            LocationName.orang_utan_gang_bonus_4:
                self.true,
            LocationName.orang_utan_gang_bonus_5:
                self.true,
            LocationName.orang_utan_gang_kong:
                self.true,
            LocationName.orang_utan_gang_bunch_1:
                self.true,
            LocationName.orang_utan_gang_bunch_2:
                self.true,
            LocationName.orang_utan_gang_bunch_3:
                self.true,
            LocationName.orang_utan_gang_bunch_4:
                self.true,
            LocationName.orang_utan_gang_bunch_5:
                self.true,
            LocationName.orang_utan_gang_bunch_6:
                self.true,
            LocationName.orang_utan_gang_token_1:
                self.true,
            LocationName.orang_utan_gang_bunch_7:
                self.true,
            LocationName.orang_utan_gang_bunch_8:
                self.true,
            LocationName.orang_utan_gang_bunch_9:
                self.true,

            LocationName.clam_city_clear:
                self.true,
            EventName.clam_city_clear:
                self.true,
            LocationName.clam_city_kong:
                self.true,
            LocationName.clam_city_bunch_1:
                self.true,
            LocationName.clam_city_bunch_2:
                self.true,
            LocationName.clam_city_token_1:
                self.true,

            LocationName.bumble_b_rumble_clear:
                self.true,
            LocationName.defeated_bumble_b:
                self.true,

            LocationName.snow_barrel_blast_clear:
                self.true,
            EventName.snow_barrel_blast_clear:
                self.true,
            LocationName.snow_barrel_blast_bonus_1:
                self.true,
            LocationName.snow_barrel_blast_bonus_2:
                self.true,
            LocationName.snow_barrel_blast_bonus_3:
                self.true,
            LocationName.snow_barrel_blast_kong:
                self.true,
            LocationName.snow_barrel_blast_bunch_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_1:
                self.true,
            LocationName.snow_barrel_blast_bunch_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_3:
                self.true,
            LocationName.snow_barrel_blast_token_1:
                self.true,
            LocationName.snow_barrel_blast_balloon_2:
                self.true,
            LocationName.snow_barrel_blast_bunch_4:
                self.true,
            LocationName.snow_barrel_blast_bunch_5:
                self.true,

            LocationName.slipslide_ride_clear:
                self.true,
            EventName.slipslide_ride_clear:
                self.true,
            LocationName.slipslide_ride_bonus_1:
                self.true,
            LocationName.slipslide_ride_bonus_2:
                self.true,
            LocationName.slipslide_ride_bonus_3:
                self.true,
            LocationName.slipslide_ride_kong:
                self.true,
            LocationName.slipslide_ride_bunch_1:
                self.true,
            LocationName.slipslide_ride_bunch_2:
                self.true,
            LocationName.slipslide_ride_bunch_3:
                self.true,
            LocationName.slipslide_ride_bunch_4:
                self.true,
            LocationName.slipslide_ride_bunch_5:
                self.true,
            LocationName.slipslide_ride_bunch_6:
                self.true,
            LocationName.slipslide_ride_bunch_7:
                self.true,
            LocationName.slipslide_ride_bunch_8:
                self.true,
            LocationName.slipslide_ride_bunch_9:
                self.true,
            LocationName.slipslide_ride_token_1:
                self.true,

            LocationName.ice_age_alley_clear:
                self.true,
            EventName.ice_age_alley_clear:
                self.true,
            LocationName.ice_age_alley_bonus_1:
                self.true,
            LocationName.ice_age_alley_bonus_2:
                self.true,
            LocationName.ice_age_alley_kong:
                self.true,
            LocationName.ice_age_alley_bunch_1:
                self.true,
            LocationName.ice_age_alley_bunch_2:
                self.true,
            LocationName.ice_age_alley_bunch_3:
                self.true,

            LocationName.croctopus_chase_clear:
                self.true,
            EventName.croctopus_chase_clear:
                self.true,
            LocationName.croctopus_chase_kong:
                self.true,
            LocationName.croctopus_chase_bunch_1:
                self.true,
            LocationName.croctopus_chase_token_1:
                self.true,
            LocationName.croctopus_chase_token_2:
                self.true,
            LocationName.croctopus_chase_bunch_2:
                self.true,
            LocationName.croctopus_chase_bunch_3:
                self.true,
            LocationName.croctopus_chase_bunch_4:
                self.true,
            LocationName.croctopus_chase_bunch_5:
                self.true,
            LocationName.croctopus_chase_balloon_1:
                self.true,

            LocationName.torchlight_trouble_clear:
                self.true,
            EventName.torchlight_trouble_clear:
                self.true,
            LocationName.torchlight_trouble_bonus_1:
                self.true,
            LocationName.torchlight_trouble_bonus_2:
                self.true,
            LocationName.torchlight_trouble_kong:
                self.true,
            LocationName.torchlight_trouble_bunch_1:
                self.true,

            LocationName.rope_bridge_rumble_clear:
                self.true,
            EventName.rope_bridge_rumble_clear:
                self.true,
            LocationName.rope_bridge_rumble_bonus_2:
                self.true,
            LocationName.rope_bridge_rumble_bonus_1:
                self.true,
            LocationName.rope_bridge_rumble_kong:
                self.true,
            LocationName.rope_bridge_rumble_bunch_1:
                self.true,

            LocationName.really_gnawty_rampage_clear:
                self.true,
            LocationName.defeated_gnawty_2:
                self.true,

            LocationName.oil_drum_alley_clear:
                self.true,
            EventName.oil_drum_alley_clear:
                self.true,
            LocationName.oil_drum_alley_bonus_1:
                self.true,
            LocationName.oil_drum_alley_bonus_2:
                self.true,
            LocationName.oil_drum_alley_bonus_3:
                self.true,
            LocationName.oil_drum_alley_bonus_4:
                self.true,
            LocationName.oil_drum_alley_kong:
                self.true,
            LocationName.oil_drum_alley_bunch_1:
                self.true,
            LocationName.oil_drum_alley_bunch_2:
                self.true,

            LocationName.trick_track_trek_clear:
                self.true,
            EventName.trick_track_trek_clear:
                self.true,
            LocationName.trick_track_trek_bonus_1:
                self.true,
            LocationName.trick_track_trek_bonus_2:
                self.true,
            LocationName.trick_track_trek_bonus_3:
                self.true,
            LocationName.trick_track_trek_kong:
                self.true,
            LocationName.trick_track_trek_bunch_1:
                self.true,
            LocationName.trick_track_trek_token_1:
                self.true,

            LocationName.elevator_antics_clear:
                self.true,
            EventName.elevator_antics_clear:
                self.true,
            LocationName.elevator_antics_bonus_1:
                self.true,
            LocationName.elevator_antics_bonus_2:
                self.true,
            LocationName.elevator_antics_bonus_3:
                self.true,
            LocationName.elevator_antics_kong:
                self.true,
            LocationName.elevator_antics_bunch_1:
                self.true,
            LocationName.elevator_antics_bunch_2:
                self.true,
            LocationName.elevator_antics_bunch_3:
                self.true,

            LocationName.poison_pond_clear:
                self.true,
            EventName.poison_pond_clear:
                self.true,
            LocationName.poison_pond_kong:
                self.true,
            LocationName.poison_pond_bunch_1:
                self.true,
            LocationName.poison_pond_bunch_2:
                self.true,
            LocationName.poison_pond_bunch_3:
                self.true,
            LocationName.poison_pond_bunch_4:
                self.true,
            LocationName.poison_pond_bunch_5:
                self.true,
            LocationName.poison_pond_token_1:
                self.true,
            LocationName.poison_pond_token_2:
                self.true,
            LocationName.poison_pond_bunch_6:
                self.true,

            LocationName.mine_cart_madness_clear:
                self.true,
            EventName.mine_cart_madness_clear:
                self.true,
            LocationName.mine_cart_madness_bonus_1:
                self.true,
            LocationName.mine_cart_madness_bonus_2:
                self.true,
            LocationName.mine_cart_madness_bonus_3:
                self.true,
            LocationName.mine_cart_madness_kong:
                self.true,
            LocationName.mine_cart_madness_token_1:
                self.true,
            LocationName.mine_cart_madness_bunch_1:
                self.true,

            LocationName.blackout_basement_clear:
                self.true,
            EventName.blackout_basement_clear:
                self.true,
            LocationName.blackout_basement_bonus_1:
                self.true,
            LocationName.blackout_basement_bonus_2:
                self.true,
            LocationName.blackout_basement_kong:
                self.true,
            LocationName.blackout_basement_token_1:
                self.true,
            LocationName.blackout_basement_bunch_1:
                self.true,

            LocationName.boss_dumb_drum_clear:
                self.true,
            LocationName.defeated_boss_dumb_drum:
                self.true,

            LocationName.tanked_up_trouble_clear:
                self.true,
            EventName.tanked_up_trouble_clear:
                self.true,
            LocationName.tanked_up_trouble_bonus_1:
                self.true,
            LocationName.tanked_up_trouble_kong:
                self.true,
            LocationName.tanked_up_trouble_bunch_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_2:
                self.true,
            LocationName.tanked_up_trouble_token_1:
                self.true,
            LocationName.tanked_up_trouble_bunch_3:
                self.true,
            LocationName.tanked_up_trouble_bunch_4:
                self.true,

            LocationName.manic_mincers_clear:
                self.true,
            EventName.manic_mincers_clear:
                self.true,
            LocationName.manic_mincers_bonus_1:
                self.true,
            LocationName.manic_mincers_bonus_2:
                self.true,
            LocationName.manic_mincers_kong:
                self.true,
            LocationName.manic_mincers_bunch_1:
                self.true,
            LocationName.manic_mincers_bunch_2:
                self.true,
            LocationName.manic_mincers_token_1:
                self.true,

            LocationName.misty_mine_clear:
                self.true,
            EventName.misty_mine_clear:
                self.true,
            LocationName.misty_mine_bonus_1:
                self.true,
            LocationName.misty_mine_bonus_2:
                self.true,
            LocationName.misty_mine_kong:
                self.true,
            LocationName.misty_mine_token_1:
                self.true,
            LocationName.misty_mine_bunch_1:
                self.true,
            LocationName.misty_mine_bunch_2:
                self.true,
            LocationName.misty_mine_token_2:
                self.true,

            LocationName.loopy_lights_clear:
                self.true,
            EventName.loopy_lights_clear:
                self.true,
            LocationName.loopy_lights_bonus_1:
                self.true,
            LocationName.loopy_lights_bonus_2:
                self.true,
            LocationName.loopy_lights_kong:
                self.true,
            LocationName.loopy_lights_bunch_1:
                self.true,
            LocationName.loopy_lights_bunch_2:
                self.true,

            LocationName.platform_perils_clear:
                self.true,
            EventName.platform_perils_clear:
                self.true,
            LocationName.platform_perils_bonus_1:
                self.true,
            LocationName.platform_perils_bonus_2:
                self.true,
            LocationName.platform_perils_kong:
                self.true,
            LocationName.platform_perils_token_1:
                self.true,
            LocationName.platform_perils_bunch_1:
                self.true,

            LocationName.necky_revenge_clear:
                self.true,
            LocationName.defeated_necky_2:
                self.true,
        }



    def set_ckd_rules(self) -> None:
        super().set_ckd_rules()
