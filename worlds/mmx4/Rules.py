from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import MMX4World

from .Names import LocationName, ItemName, RegionName

from worlds.generic.Rules import CollectionRule
from BaseClasses import CollectionState

STAGE_LIST = [
    ItemName.web_spider,
    ItemName.cyber_peacock,
    ItemName.storm_owl,
    ItemName.magma_dragoon,
    ItemName.jet_stingray,
    ItemName.split_mushroom,
    ItemName.slash_beast,
    ItemName.frost_walrus,
]

class MMX4Rules:
    player: int
    world: "MMX4World"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "MMX4World") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.stage_select} -> {RegionName.web_spider}":
                lambda state: state.has(ItemName.web_spider, self.player),
            f"{RegionName.stage_select} -> {RegionName.cyber_peacock}":
                lambda state: state.has(ItemName.cyber_peacock, self.player),
            f"{RegionName.stage_select} -> {RegionName.storm_owl}":
                lambda state: state.has(ItemName.storm_owl, self.player),
            f"{RegionName.stage_select} -> {RegionName.magma_dragoon}":
                lambda state: state.has(ItemName.magma_dragoon, self.player),
            f"{RegionName.stage_select} -> {RegionName.jet_stingray}":
                lambda state: state.has(ItemName.jet_stingray, self.player),
            f"{RegionName.stage_select} -> {RegionName.split_mushroom}":
                lambda state: state.has(ItemName.split_mushroom, self.player),
            f"{RegionName.stage_select} -> {RegionName.slash_beast}":
                lambda state: state.has(ItemName.slash_beast, self.player),
            f"{RegionName.stage_select} -> {RegionName.frost_walrus}":
                lambda state: state.has(ItemName.frost_walrus, self.player),

            # These will change whenever we can edit requirements for accessing those
            f"{RegionName.stage_select} -> {RegionName.memorial_hall}":
                lambda state: state.count_from_list_unique(STAGE_LIST, self.player) >= 4,
            f"{RegionName.stage_select} -> {RegionName.space_port}":
                lambda state: state.count_from_list_unique(STAGE_LIST, self.player) >= 8,
        }

    def set_mmx4_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]

        multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)

class MMX4XRules(MMX4Rules):
    def __init__(self, world: "MMX4World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.web_spider_heart_tank:
                self.has_rising_fire,
            
            LocationName.cyber_peacock_heart_tank:
                self.has_soul_body,
            LocationName.cyber_peacock_sub_tank:
                self.has_soul_body,
            LocationName.cyber_peacock_capsule:
                self.has_soul_body,

            LocationName.storm_owl_capsule_1:
                self.has_lightning_web,
            LocationName.storm_owl_capsule_2:
                self.has_lightning_web,

            LocationName.magma_dragoon_heart_tank:
                self.has_lightning_web,
            LocationName.magma_dragoon_capsule:
                lambda state: self.has_lightning_web(state) and self.has_twin_slasher(state) and self.can_charge(state),
            
            LocationName.split_mushroom_heart_tank:
                self.has_lightning_web,

            LocationName.frost_walrus_heart_tank:
                self.has_rising_fire,
            LocationName.frost_walrus_extra_lives_tank:
                self.has_lightning_web,
            LocationName.frost_walrus_1up_1:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_3:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_4:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_5:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_6:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_7:
                self.has_lightning_web,
            LocationName.frost_walrus_hp_8:
                self.has_lightning_web,

            LocationName.final_weapon_hp_8:
                self.has_rising_fire,
            LocationName.final_weapon_clear:
                self.has_rising_fire,
        }
        
    def has_rising_fire(self, state: CollectionState) -> bool:
        return state.has(ItemName.rising_fire, self.player)
        
    def has_soul_body(self, state: CollectionState) -> bool:
        return state.has(ItemName.soul_body, self.player)
        
    def has_lightning_web(self, state: CollectionState) -> bool:
        return state.has(ItemName.lightning_web, self.player)
    
    def has_twin_slasher(self, state: CollectionState) -> bool:
        return state.has(ItemName.rising_fire, self.player)
        
    def has_legs(self, state: CollectionState) -> bool:
        return state.has(ItemName.legs, self.player)
    
    def can_charge(self, state: CollectionState) -> bool:
        return state.has_any([ItemName.arms_stock, ItemName.arms_plasma], self.player)
