
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import SMWWorld

from .Names import LocationName, ItemName
from .Options import Goal

from worlds.generic.Rules import CollectionRule, add_rule
from BaseClasses import CollectionState

class SMWRules:
    player: int
    world: "SMWWorld"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "SMWWorld") -> None:
        self.player = world.player
        self.world = world

    def can_carry(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_carry, self.player)
    
    def can_spin_jump(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_spin_jump, self.player)
    
    def can_run(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_run, self.player)
    
    def can_swim(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_swim, self.player)
    
    def can_climb(self, state: CollectionState) -> bool:
        return state.has(ItemName.mario_climb, self.player)
    

    def has_mushroom(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 1)
    
    def has_fire_flower(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 2)
    
    def has_feather(self, state: CollectionState) -> bool:
        return state.has(ItemName.progressive_powerup, self.player, 3)
    
    def has_super_star(self, state: CollectionState) -> bool:
        return state.has(ItemName.super_star_active, self.player)
    
    def has_p_balloon(self, state: CollectionState) -> bool:
        return state.has(ItemName.p_balloon, self.player)
    
    def has_p_switch(self, state: CollectionState) -> bool:
        return state.has(ItemName.p_switch, self.player)
    
    def has_yoshi(self, state: CollectionState) -> bool:
        return state.has(ItemName.yoshi_activate, self.player)
    
    def has_special_world(self, state: CollectionState) -> bool:
        return state.has(ItemName.special_world_clear, self.player)
    

    def has_ysp(self, state: CollectionState) -> bool:
        return state.has(ItemName.yellow_switch_palace, self.player)
    
    def has_gsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.green_switch_palace, self.player)

    def has_rsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.red_switch_palace, self.player)

    def has_bsp(self, state: CollectionState) -> bool:
        return state.has(ItemName.blue_switch_palace, self.player)


    def has_tokens(self, state: CollectionState) -> bool:
        return state.has(ItemName.koopaling, self.player, self.world.options.bosses_required.value)


    def can_cape_fly(self, state: CollectionState) -> bool:
        return self.has_feather(state) and self.can_run(state)
    
    def can_yoshi_fly(self, state: CollectionState) -> bool:
        return self.has_yoshi(state) and self.can_carry(state) and self.has_special_world(state)
    
    def can_break_turn_blocks(self, state: CollectionState) -> bool:
        return self.has_mushroom(state) and self.can_spin_jump(state)
        
    def can_get_blue_yoshi(self, state: CollectionState) -> bool:
        return self.has_yoshi(state) and (
            state.can_reach_region(LocationName.cheese_bridge_region, self.player) or \
            state.can_reach_region(LocationName.star_road_2_region, self.player) or \
            state.can_reach_region(LocationName.valley_of_bowser_2_region, self.player)
        )
    
    def can_get_red_yoshi(self, state: CollectionState) -> bool:
        return self.has_yoshi(state) and (
            state.can_reach_region(LocationName.star_road_1_region, self.player) or \
            state.can_reach_region(LocationName.star_road_4_region, self.player)
        )

    def can_get_yellow_yoshi(self, state: CollectionState) -> bool:
        return self.has_yoshi(state) and (
            state.can_reach_region(LocationName.star_road_3_region, self.player) or \
            state.can_reach_region(LocationName.star_road_5_region, self.player)
        )



    def true(self, state: CollectionState) -> bool:
        return True
    

    def set_smw_rules(self) -> None:
        world = self.world
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]

        if world.options.goal == Goal.option_yoshi_egg_hunt:
            required_yoshi_eggs = world.required_egg_count

            add_rule(world.multiworld.get_location(LocationName.yoshis_house, world.player),
                    lambda state: state.has(ItemName.yoshi_egg, world.player, required_yoshi_eggs))
        else:
            add_rule(world.multiworld.get_location(LocationName.bowser, world.player), 
                     lambda state: state.has(ItemName.mario_carry, world.player))

        multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)

class SMWOriginalRules(SMWRules):
    def __init__(self, world: "SMWWorld") -> None:
        super().__init__(world)

        self.connection_rules = {
            f"{LocationName.yoshis_island_1_region} -> {LocationName.yoshis_island_1_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_2_region} -> {LocationName.yoshis_island_2_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_3_region} -> {LocationName.yoshis_island_3_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_4_region} -> {LocationName.yoshis_island_4_exit_1}": 
                self.true,
            f"{LocationName.yoshis_island_castle_region} -> {LocationName.yoshis_island_castle}": 
                self.can_climb,
                
            f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_1_region} -> {LocationName.donut_plains_1_exit_2}": 
                lambda state: self.can_carry(state) and (
                    self.has_yoshi(state) or 
                    self.has_gsp(state) or
                    self.can_cape_fly(state)
                ),
            f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_2_region} -> {LocationName.donut_plains_2_exit_2}": 
                lambda state: self.can_carry(state) and (
                    (self.can_climb(state) and self.can_break_turn_blocks(state)) or 
                    self.has_yoshi(state)
                ),
            f"{LocationName.donut_plains_3_region} -> {LocationName.donut_plains_3_exit_1}": 
                self.true,
            f"{LocationName.donut_plains_4_region} -> {LocationName.donut_plains_4_exit_1}": 
                self.true,
            f"{LocationName.donut_secret_1_region} -> {LocationName.donut_secret_1_exit_1}": 
                self.can_swim,
            f"{LocationName.donut_secret_1_region} -> {LocationName.donut_secret_1_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state),
            f"{LocationName.donut_secret_2_region} -> {LocationName.donut_secret_2_exit_1}": 
                self.true,
            f"{LocationName.donut_ghost_house_region} -> {LocationName.donut_ghost_house_exit_1}": 
                self.can_cape_fly,
            f"{LocationName.donut_ghost_house_region} -> {LocationName.donut_ghost_house_exit_2}": 
                lambda state: self.can_climb(state) or self.can_cape_fly(state),
            f"{LocationName.donut_secret_house_region} -> {LocationName.donut_secret_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.donut_secret_house_region} -> {LocationName.donut_secret_house_exit_2}": 
                lambda state: self.has_p_switch(state) and self.can_carry(state) and (
                    self.can_climb(state) or self.can_cape_fly(state)
                ),
            f"{LocationName.donut_plains_castle_region} -> {LocationName.donut_plains_castle}": 
                self.true,

            f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_1}": 
                lambda state: self.can_run(state) and (
                    self.has_super_star(state) or self.has_mushroom(state)
                ),
            f"{LocationName.vanilla_dome_1_region} -> {LocationName.vanilla_dome_1_exit_2}": 
                lambda state: self.can_carry(state) and (
                    (self.has_rsp(state) and self.can_climb(state)) or 
                    (self.has_yoshi(state) and self.can_climb(state)) or
                    (self.has_yoshi(state) and self.has_rsp(state))
                ),
            f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_1}": 
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            f"{LocationName.vanilla_dome_2_region} -> {LocationName.vanilla_dome_2_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            f"{LocationName.vanilla_dome_3_region} -> {LocationName.vanilla_dome_3_exit_1}": 
                self.true,
            f"{LocationName.vanilla_dome_4_region} -> {LocationName.vanilla_dome_4_exit_1}": 
                self.true,
            f"{LocationName.vanilla_secret_1_region} -> {LocationName.vanilla_secret_1_exit_1}": 
                self.can_climb,
            f"{LocationName.vanilla_secret_1_region} -> {LocationName.vanilla_secret_1_exit_2}": 
                lambda state: self.can_climb(state) and (
                    self.can_carry(state) and self.has_bsp(state)
                ),
            f"{LocationName.vanilla_secret_2_region} -> {LocationName.vanilla_secret_2_exit_1}": 
                self.true,
            f"{LocationName.vanilla_secret_3_region} -> {LocationName.vanilla_secret_3_exit_1}": 
                self.can_swim,
            f"{LocationName.vanilla_ghost_house_region} -> {LocationName.vanilla_ghost_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.vanilla_fortress_region} -> {LocationName.vanilla_fortress}": 
                self.can_swim,
            f"{LocationName.vanilla_dome_castle_region} -> {LocationName.vanilla_dome_castle}": 
                self.true,

            f"{LocationName.butter_bridge_1_region} -> {LocationName.butter_bridge_1_exit_1}": 
                self.true,
            f"{LocationName.butter_bridge_2_region} -> {LocationName.butter_bridge_2_exit_1}": 
                self.true,
            f"{LocationName.cheese_bridge_region} -> {LocationName.cheese_bridge_exit_1}": 
                self.can_climb,
            f"{LocationName.cheese_bridge_region} -> {LocationName.cheese_bridge_exit_2}": 
                self.can_cape_fly,
            f"{LocationName.soda_lake_region} -> {LocationName.soda_lake_exit_1}": 
                self.can_swim,
            f"{LocationName.cookie_mountain_region} -> {LocationName.cookie_mountain_exit_1}": 
                self.true,
            f"{LocationName.twin_bridges_castle_region} -> {LocationName.twin_bridges_castle}": 
                lambda state: self.can_run(state) and self.can_climb(state),

            f"{LocationName.forest_of_illusion_1_region} -> {LocationName.forest_of_illusion_1_exit_1}": 
                self.true,
            f"{LocationName.forest_of_illusion_1_region} -> {LocationName.forest_of_illusion_1_exit_2}": 
                lambda state: self.can_carry(state) and self.has_p_balloon(state),
            f"{LocationName.forest_of_illusion_2_region} -> {LocationName.forest_of_illusion_2_exit_1}": 
                self.can_swim,
            f"{LocationName.forest_of_illusion_2_region} -> {LocationName.forest_of_illusion_2_exit_2}": 
                lambda state: self.can_carry(state) and self.can_swim(state),
            f"{LocationName.forest_of_illusion_3_region} -> {LocationName.forest_of_illusion_3_exit_1}": 
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            f"{LocationName.forest_of_illusion_3_region} -> {LocationName.forest_of_illusion_3_exit_2}": 
                lambda state: self.can_carry(state) and self.can_break_turn_blocks(state),
            f"{LocationName.forest_of_illusion_4_region} -> {LocationName.forest_of_illusion_4_exit_1}": 
                self.true,
            f"{LocationName.forest_of_illusion_4_region} -> {LocationName.forest_of_illusion_4_exit_2}":
                self.can_carry,
            f"{LocationName.forest_ghost_house_region} -> {LocationName.forest_ghost_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.forest_ghost_house_region} -> {LocationName.forest_ghost_house_exit_2}": 
                self.has_p_switch,
            f"{LocationName.forest_secret_region} -> {LocationName.forest_secret_exit_1}": 
                self.true,
            f"{LocationName.forest_fortress_region} -> {LocationName.forest_fortress}": 
                self.true,
            f"{LocationName.forest_castle_region} -> {LocationName.forest_castle}": 
                self.true,

            f"{LocationName.chocolate_island_1_region} -> {LocationName.chocolate_island_1_exit_1}": 
                lambda state: self.has_p_switch(state) or self.has_yoshi(state),
            f"{LocationName.chocolate_island_2_region} -> {LocationName.chocolate_island_2_exit_1}": 
                self.true,
            f"{LocationName.chocolate_island_2_region} -> {LocationName.chocolate_island_2_exit_2}": 
                self.can_carry,
            f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_1}": 
                self.can_climb,
            f"{LocationName.chocolate_island_3_region} -> {LocationName.chocolate_island_3_exit_2}": 
                self.can_cape_fly,
            f"{LocationName.chocolate_island_4_region} -> {LocationName.chocolate_island_4_exit_1}": 
                self.true,
            f"{LocationName.chocolate_island_5_region} -> {LocationName.chocolate_island_5_exit_1}": 
                self.true,
            f"{LocationName.chocolate_ghost_house_region} -> {LocationName.chocolate_ghost_house_exit_1}": 
                self.true,
            f"{LocationName.chocolate_fortress_region} -> {LocationName.chocolate_fortress}": 
                self.true,
            f"{LocationName.chocolate_secret_region} -> {LocationName.chocolate_secret_exit_1}": 
                self.can_run,
            f"{LocationName.chocolate_castle_region} -> {LocationName.chocolate_castle}": 
                self.has_mushroom,
            f"{LocationName.sunken_ghost_ship_region} -> {LocationName.sunken_ghost_ship}": 
                self.can_swim,

            f"{LocationName.valley_of_bowser_1_region} -> {LocationName.valley_of_bowser_1_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_2_region} -> {LocationName.valley_of_bowser_2_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_2_region} -> {LocationName.valley_of_bowser_2_exit_2}": 
                self.can_carry,
            f"{LocationName.valley_of_bowser_3_region} -> {LocationName.valley_of_bowser_3_exit_1}": 
                self.true,
            f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_1}": 
                self.can_climb,
            f"{LocationName.valley_of_bowser_4_region} -> {LocationName.valley_of_bowser_4_exit_2}": 
                lambda state: self.can_carry(state) and self.has_yoshi(state) and self.can_climb(state),
            f"{LocationName.valley_ghost_house_region} -> {LocationName.valley_ghost_house_exit_1}": 
                self.has_p_switch,
            f"{LocationName.valley_ghost_house_region} -> {LocationName.valley_ghost_house_exit_2}": 
                lambda state: self.has_p_switch(state) and self.can_carry(state) and self.can_run(state),
            f"{LocationName.valley_fortress_region} -> {LocationName.valley_fortress}": 
                self.has_mushroom,
            f"{LocationName.valley_castle_region} -> {LocationName.valley_castle}": 
                self.true,
            f"{LocationName.front_door} -> {LocationName.bowser_region}": 
                lambda state: self.can_climb(state) and self.can_run(state) and self.can_swim(state) and 
                    self.has_mushroom(state) and self.has_tokens(state),
            f"{LocationName.back_door} -> {LocationName.bowser_region}": 
                self.has_tokens,

            f"{LocationName.star_road_1_region} -> {LocationName.star_road_1_exit_1}": 
                self.can_break_turn_blocks,
            f"{LocationName.star_road_1_region} -> {LocationName.star_road_1_exit_2}": 
                lambda state: self.can_break_turn_blocks(state) and self.can_carry(state),
            f"{LocationName.star_road_2_region} -> {LocationName.star_road_2_exit_1}": 
                self.can_swim,
            f"{LocationName.star_road_2_region} -> {LocationName.star_road_2_exit_2}": 
                lambda state: self.can_swim(state) and self.can_carry(state),
            f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_1}": 
                self.true,
            f"{LocationName.star_road_3_region} -> {LocationName.star_road_3_exit_2}": 
                self.can_carry,
            f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_1}": 
                self.true,
            f"{LocationName.star_road_4_region} -> {LocationName.star_road_4_exit_2}": 
                lambda state: self.can_carry(state) and (
                    self.has_yoshi(state) or (self.has_gsp(state) and self.has_rsp(state))
                ),
            f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_1}": 
                self.has_p_switch,
            f"{LocationName.star_road_5_region} -> {LocationName.star_road_5_exit_2}": 
                lambda state: self.can_carry(state) and self.can_climb(state) and self.has_p_switch(state) and 
                    self.has_ysp(state) and self.has_gsp(state) and self.has_rsp(state) and self.has_bsp(state),

            f"{LocationName.special_zone_1_region} -> {LocationName.special_zone_1_exit_1}": 
                lambda state: self.can_climb(state) and (
                    self.has_p_switch(state) or self.can_cape_fly(state)
                ),
            f"{LocationName.special_zone_2_region} -> {LocationName.special_zone_2_exit_1}": 
                self.has_p_balloon,
            f"{LocationName.special_zone_3_region} -> {LocationName.special_zone_3_exit_1}": 
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            f"{LocationName.special_zone_4_region} -> {LocationName.special_zone_4_exit_1}": 
                lambda state: self.has_fire_flower(state) or self.has_super_star(state),
            f"{LocationName.special_zone_5_region} -> {LocationName.special_zone_5_exit_1}": 
                self.has_mushroom,
            f"{LocationName.special_zone_6_region} -> {LocationName.special_zone_6_exit_1}": 
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            f"{LocationName.special_zone_7_region} -> {LocationName.special_zone_7_exit_1}": 
                self.has_mushroom,
            f"{LocationName.special_zone_8_region} -> {LocationName.special_zone_8_exit_1}": 
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
        }
    
        self.location_rules = {
            LocationName.yoshis_island_1_dragon:
                self.can_break_turn_blocks,
            LocationName.yoshis_island_1_moon:
                lambda state: self.can_cape_fly(state) or self.has_yoshi(state),
            LocationName.yoshis_island_1_flying_block_1:
                self.true,
            LocationName.yoshis_island_1_yellow_block_1:
                self.has_ysp,
            LocationName.yoshis_island_1_life_block_1:
                self.true,
            LocationName.yoshis_island_1_powerup_block_1:
                self.true,

            LocationName.yoshis_island_2_dragon:
                lambda state: self.has_yoshi(state) or self.can_climb(state),
            LocationName.yoshis_island_2_flying_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_2:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_3:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_4:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_5:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_flying_block_6:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.yoshis_island_2_coin_block_1:
                self.true,
            LocationName.yoshis_island_2_yellow_block_1:
                self.has_ysp,
            LocationName.yoshis_island_2_coin_block_2:
                self.true,
            LocationName.yoshis_island_2_coin_block_3:
                self.true,
            LocationName.yoshis_island_2_yoshi_block_1:
                self.true,
            LocationName.yoshis_island_2_coin_block_4:
                self.true,
            LocationName.yoshis_island_2_yoshi_block_2:
                self.true,
            LocationName.yoshis_island_2_coin_block_5:
                self.true,
            LocationName.yoshis_island_2_vine_block_1:
                self.true,
            LocationName.yoshis_island_2_yellow_block_2:
                self.has_ysp,

            LocationName.yoshis_island_3_dragon:
                self.has_p_switch,
            LocationName.yoshis_island_3_bonus_block:
                self.true,
            LocationName.yoshis_island_3_yellow_block_1:
                self.has_ysp,
            LocationName.yoshis_island_3_yellow_block_2:
                self.has_ysp,
            LocationName.yoshis_island_3_yellow_block_3:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_4:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_5:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_6:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_7:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_8:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_yellow_block_9:
                lambda state: self.has_ysp(state) and (
                    self.can_carry(state) or self.has_yoshi(state)
                ),
            LocationName.yoshis_island_3_coin_block_1:
                self.true,
            LocationName.yoshis_island_3_yoshi_block_1:
                self.true,
            LocationName.yoshis_island_3_coin_block_2:
                self.true,
            LocationName.yoshis_island_3_powerup_block_1:
                self.true,
            LocationName.yoshis_island_3_yellow_block_10:
                self.has_ysp,
            LocationName.yoshis_island_3_yellow_block_11:
                self.has_ysp,
            LocationName.yoshis_island_3_yellow_block_12:
                self.has_ysp,
            LocationName.yoshis_island_3_bonus_block_1:
                self.true,

            LocationName.yoshis_island_4_dragon:
                lambda state: self.has_yoshi(state) or self.can_swim(state) or self.has_p_switch(state),
            LocationName.yoshis_island_4_hidden_1up:
                lambda state: self.has_yoshi(state) or self.can_cape_fly(state),
            LocationName.yoshis_island_4_yellow_block_1:
                self.has_ysp,
            LocationName.yoshis_island_4_powerup_block_1:
                self.true,
            LocationName.yoshis_island_4_multi_coin_block_1:
                self.true,
            LocationName.yoshis_island_4_star_block_1:
                self.true,
                
            LocationName.yoshis_island_castle_coin_block_1:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_2:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_powerup_block_1:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_3:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_coin_block_4:
                lambda state: self.can_carry(state) or self.can_climb(state),
            LocationName.yoshis_island_castle_flying_block_1:
                self.can_climb,

            LocationName.yellow_switch_palace:
                self.true,

            LocationName.donut_plains_1_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state) or self.can_cape_fly(state),
            LocationName.donut_plains_1_hidden_1up:
                self.true,
            LocationName.donut_plains_1_coin_block_1:
                self.true,
            LocationName.donut_plains_1_coin_block_2:
                self.true,
            LocationName.donut_plains_1_yoshi_block_1:
                self.true,
            LocationName.donut_plains_1_vine_block_1:
                self.true,
            LocationName.donut_plains_1_green_block_1:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_2:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_3:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_4:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_5:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_6:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_7:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_8:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_9:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_10:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_11:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_12:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_13:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_14:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_15:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_green_block_16:
                lambda state: self.has_gsp(state) and self.has_feather(state),
            LocationName.donut_plains_1_yellow_block_1:
                self.has_ysp,
            LocationName.donut_plains_1_yellow_block_2:
                self.has_ysp,
            LocationName.donut_plains_1_yellow_block_3:
                self.has_ysp,

            LocationName.donut_plains_2_dragon:
                self.true,
            LocationName.donut_plains_2_coin_block_1:
                self.true,
            LocationName.donut_plains_2_coin_block_2:
                self.true,
            LocationName.donut_plains_2_coin_block_3:
                self.true,
            LocationName.donut_plains_2_yellow_block_1:
                self.has_ysp,
            LocationName.donut_plains_2_powerup_block_1:
                self.true,
            LocationName.donut_plains_2_multi_coin_block_1:
                self.true,
            LocationName.donut_plains_2_flying_block_1:
                self.true,
            LocationName.donut_plains_2_green_block_1:
                self.has_gsp,
            LocationName.donut_plains_2_yellow_block_2:
                self.has_ysp,
            LocationName.donut_plains_2_vine_block_1:
                lambda state: (self.can_break_turn_blocks(state) and self.can_carry(state)) or self.has_yoshi(state),

            LocationName.donut_plains_3_dragon:
                lambda state: (self.can_break_turn_blocks(state) and self.can_climb(state)) or self.has_yoshi(state) or
                    self.can_cape_fly(state),
            LocationName.donut_plains_3_bonus_block:
                self.true,
            LocationName.donut_plains_3_green_block_1:
                self.has_gsp,
            LocationName.donut_plains_3_coin_block_1:
                self.true,
            LocationName.donut_plains_3_coin_block_2:
                self.true,
            LocationName.donut_plains_3_vine_block_1:
                self.can_break_turn_blocks,
            LocationName.donut_plains_3_powerup_block_1:
                self.true,
            LocationName.donut_plains_3_bonus_block_1:
                self.true,

            LocationName.donut_plains_4_dragon:
                self.true,
            LocationName.donut_plains_4_moon:
                self.can_cape_fly,
            LocationName.donut_plains_4_hidden_1up:
                self.can_cape_fly,
            LocationName.donut_plains_4_coin_block_1:
                self.true,
            LocationName.donut_plains_4_powerup_block_1:
                self.true,
            LocationName.donut_plains_4_coin_block_2:
                self.true,
            LocationName.donut_plains_4_yoshi_block_1:
                self.true,

            LocationName.donut_secret_1_dragon:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_1:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_2:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_1:
                self.can_swim,
            LocationName.donut_secret_1_coin_block_3:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_2:
                self.can_swim,
            LocationName.donut_secret_1_powerup_block_3:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_life_block_1:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_powerup_block_4:
                lambda state: self.can_swim(state) and self.has_p_balloon(state),
            LocationName.donut_secret_1_powerup_block_5:
                self.can_swim,
            LocationName.donut_secret_1_key_block_1:
                lambda state: self.can_swim(state) and self.can_carry(state) and self.has_p_switch(state),

            LocationName.donut_secret_2_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.donut_secret_2_directional_coin_block_1:
                self.true,
            LocationName.donut_secret_2_vine_block_1:
                self.true,
            LocationName.donut_secret_2_star_block_1:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.donut_secret_2_powerup_block_1:
                self.true,
            LocationName.donut_secret_2_star_block_2:
                self.true,

            LocationName.donut_ghost_house_vine_block_1:
                self.true,
            LocationName.donut_ghost_house_directional_coin_block_1:
                self.has_p_switch,
            LocationName.donut_ghost_house_life_block_1:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_2:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_3:
                self.can_cape_fly,
            LocationName.donut_ghost_house_life_block_4:
                self.can_cape_fly,

            LocationName.donut_secret_house_powerup_block_1:
                self.true,
            LocationName.donut_secret_house_multi_coin_block_1:
                self.true,
            LocationName.donut_secret_house_life_block_1:
                self.has_p_switch,
            LocationName.donut_secret_house_vine_block_1:
                self.has_p_switch,
            LocationName.donut_secret_house_directional_coin_block_1:
                self.has_p_switch,

            LocationName.donut_plains_castle_hidden_1up:
                self.true,
            LocationName.donut_plains_castle_yellow_block_1:
                self.has_ysp,
            LocationName.donut_plains_castle_coin_block_1:
                self.true,
            LocationName.donut_plains_castle_powerup_block_1:
                self.true,
            LocationName.donut_plains_castle_coin_block_2:
                self.true,
            LocationName.donut_plains_castle_vine_block_1:
                self.true,
            LocationName.donut_plains_castle_invis_life_block_1:
                self.can_climb,
            LocationName.donut_plains_castle_coin_block_3:
                self.true,
            LocationName.donut_plains_castle_coin_block_4:
                self.true,
            LocationName.donut_plains_castle_coin_block_5:
                self.true,
            LocationName.donut_plains_castle_green_block_1:
                self.has_gsp,

            LocationName.green_switch_palace:
                self.true,

            LocationName.vanilla_dome_1_dragon:
                lambda state: self.can_carry(state) and self.can_run(state) and (
                    self.has_super_star(state) or self.has_mushroom(state)
                ),
            LocationName.vanilla_dome_1_flying_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_1_coin_block_1:
                self.true,
            LocationName.vanilla_dome_1_life_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_3:
                self.true,
            LocationName.vanilla_dome_1_vine_block_1:
                lambda state: self.has_rsp(state) or self.can_carry(state) or self.has_yoshi(state),
            LocationName.vanilla_dome_1_star_block_1:
                self.true,
            LocationName.vanilla_dome_1_powerup_block_4:
                lambda state: self.can_run(state) and (
                    self.has_super_star(state) or self.has_mushroom(state)
                ),
            LocationName.vanilla_dome_1_coin_block_2:
                lambda state: self.can_run(state) and (
                    self.has_super_star(state) or self.has_mushroom(state)
                ),

            LocationName.vanilla_dome_2_dragon:
                lambda state: self.can_swim(state) and self.has_p_switch(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_powerup_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_coin_block_2:
                self.can_swim,
            LocationName.vanilla_dome_2_coin_block_3:
                self.can_swim,
            LocationName.vanilla_dome_2_vine_block_1:
                self.can_swim,
            LocationName.vanilla_dome_2_invis_life_block_1:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_4:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_coin_block_5:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_2:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_3:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_4:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_powerup_block_5:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_multi_coin_block_1:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),
            LocationName.vanilla_dome_2_multi_coin_block_2:
                lambda state: self.can_swim(state) and (
                    self.can_climb(state) or self.has_yoshi(state)
                ),

            LocationName.vanilla_dome_3_dragon:
                self.true,
            LocationName.vanilla_dome_3_moon:
                self.can_cape_fly,
            LocationName.vanilla_dome_3_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_2:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_3_flying_block_3:
                self.true,
            LocationName.vanilla_dome_3_invis_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_3_multi_coin_block_1:
                self.true,
            LocationName.vanilla_dome_3_powerup_block_3:
                self.true,
            LocationName.vanilla_dome_3_yoshi_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.vanilla_dome_3_powerup_block_4:
                self.true,
            LocationName.vanilla_dome_3_pswitch_coin_block_1:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_2:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_3:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_4:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_5:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),
            LocationName.vanilla_dome_3_pswitch_coin_block_6:
                lambda state: self.can_cape_fly(state) and self.has_p_switch(state),

            LocationName.vanilla_dome_4_dragon:
                self.true,
            LocationName.vanilla_dome_4_hidden_1up:
                self.true,
            LocationName.vanilla_dome_4_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_4_powerup_block_2:
                self.true,
            LocationName.vanilla_dome_4_coin_block_1:
                self.true,
            LocationName.vanilla_dome_4_coin_block_2:
                self.true,
            LocationName.vanilla_dome_4_coin_block_3:
                self.true,
            LocationName.vanilla_dome_4_life_block_1:
                self.true,
            LocationName.vanilla_dome_4_coin_block_4:
                self.true,
            LocationName.vanilla_dome_4_coin_block_5:
                self.true,
            LocationName.vanilla_dome_4_coin_block_6:
                self.true,
            LocationName.vanilla_dome_4_coin_block_7:
                self.true,
            LocationName.vanilla_dome_4_coin_block_8:
                self.can_carry,

            LocationName.vanilla_secret_1_dragon:
                lambda state: self.can_climb(state) and self.can_carry(state),
            LocationName.vanilla_secret_1_coin_block_1:
                self.true,
            LocationName.vanilla_secret_1_powerup_block_1:
                self.true,
            LocationName.vanilla_secret_1_multi_coin_block_1:
                self.true,
            LocationName.vanilla_secret_1_vine_block_1:
                self.true,
            LocationName.vanilla_secret_1_vine_block_2:
                self.can_climb,
            LocationName.vanilla_secret_1_coin_block_2:
                self.can_climb,
            LocationName.vanilla_secret_1_coin_block_3:
                self.can_climb,
            LocationName.vanilla_secret_1_powerup_block_2:
                self.can_climb,

            LocationName.vanilla_secret_2_dragon:
                self.can_cape_fly,
            LocationName.vanilla_secret_2_yoshi_block_1:
                self.true,
            LocationName.vanilla_secret_2_green_block_1:
                self.has_gsp,
            LocationName.vanilla_secret_2_powerup_block_1:
                self.true,
            LocationName.vanilla_secret_2_powerup_block_2:
                self.true,
            LocationName.vanilla_secret_2_multi_coin_block_1:
                self.true,
            LocationName.vanilla_secret_2_gray_pow_block_1:
                self.true,
            LocationName.vanilla_secret_2_coin_block_1:
                self.true,
            LocationName.vanilla_secret_2_coin_block_2:
                self.true,
            LocationName.vanilla_secret_2_coin_block_3:
                self.true,
            LocationName.vanilla_secret_2_coin_block_4:
                self.true,
            LocationName.vanilla_secret_2_coin_block_5:
                self.true,
            LocationName.vanilla_secret_2_coin_block_6:
                self.true,

            LocationName.vanilla_secret_3_dragon:
                self.can_swim,
            LocationName.vanilla_secret_3_powerup_block_1:
                self.can_swim,
            LocationName.vanilla_secret_3_powerup_block_2:
                self.can_swim,

            LocationName.vanilla_ghost_house_dragon:
                self.can_climb,
            LocationName.vanilla_ghost_house_hidden_1up:
                self.true,
            LocationName.vanilla_ghost_house_powerup_block_1:
                self.true,
            LocationName.vanilla_ghost_house_vine_block_1:
                self.true,
            LocationName.vanilla_ghost_house_powerup_block_2:
                self.true,
            LocationName.vanilla_ghost_house_multi_coin_block_1:
                self.true,
            LocationName.vanilla_ghost_house_blue_pow_block_1:
                self.true,
                
            LocationName.vanilla_fortress_hidden_1up:
                self.can_swim,
            LocationName.vanilla_fortress_powerup_block_1:
                self.can_swim,
            LocationName.vanilla_fortress_powerup_block_2:
                self.can_swim,
            LocationName.vanilla_fortress_yellow_block_1:
                lambda state: self.can_swim(state) and self.has_ysp(state),

            LocationName.vanilla_dome_castle_life_block_1:
                self.has_mushroom,
            LocationName.vanilla_dome_castle_life_block_2:
                self.has_mushroom,
            LocationName.vanilla_dome_castle_powerup_block_1:
                self.true,
            LocationName.vanilla_dome_castle_life_block_3:
                self.has_p_switch,
            LocationName.vanilla_dome_castle_green_block_1:
                self.has_gsp,

            LocationName.red_switch_palace:
                self.true,

            LocationName.butter_bridge_1_dragon:
                self.true,
            LocationName.butter_bridge_1_bonus_block:
                self.true,
            LocationName.butter_bridge_1_powerup_block_1:
                self.true,
            LocationName.butter_bridge_1_multi_coin_block_1:
                self.true,
            LocationName.butter_bridge_1_multi_coin_block_2:
                self.true,
            LocationName.butter_bridge_1_multi_coin_block_3:
                self.true,
            LocationName.butter_bridge_1_life_block_1:
                self.true,
            LocationName.butter_bridge_1_bonus_block_1:
                self.true,

            LocationName.butter_bridge_2_dragon:
                self.can_cape_fly,
            LocationName.butter_bridge_2_powerup_block_1:
                self.can_carry,
            LocationName.butter_bridge_2_green_block_1:
                self.has_gsp,
            LocationName.butter_bridge_2_yoshi_block_1:
                self.can_carry,

            LocationName.cheese_bridge_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.cheese_bridge_moon:
                self.can_cape_fly,
            LocationName.cheese_bridge_powerup_block_1:
                self.true,
            LocationName.cheese_bridge_powerup_block_2:
                self.true,
            LocationName.cheese_bridge_wings_block_1:
                self.true,
            LocationName.cheese_bridge_powerup_block_3:
                self.true,

            LocationName.cookie_mountain_dragon:
                lambda state: self.can_climb(state) or self.has_yoshi(state),
            LocationName.cookie_mountain_hidden_1up:
                lambda state: self.can_swim(state),
            LocationName.cookie_mountain_coin_block_1:
                self.true,
            LocationName.cookie_mountain_coin_block_2:
                self.true,
            LocationName.cookie_mountain_coin_block_3:
                self.true,
            LocationName.cookie_mountain_coin_block_4:
                self.true,
            LocationName.cookie_mountain_coin_block_5:
                self.true,
            LocationName.cookie_mountain_coin_block_6:
                self.true,
            LocationName.cookie_mountain_coin_block_7:
                self.true,
            LocationName.cookie_mountain_coin_block_8:
                self.true,
            LocationName.cookie_mountain_coin_block_9:
                self.true,
            LocationName.cookie_mountain_powerup_block_1:
                self.true,
            LocationName.cookie_mountain_life_block_1:
                self.can_climb,
            LocationName.cookie_mountain_vine_block_1:
                self.true,
            LocationName.cookie_mountain_yoshi_block_1:
                self.has_rsp,
            LocationName.cookie_mountain_coin_block_10:
                self.true,
            LocationName.cookie_mountain_coin_block_11:
                self.true,
            LocationName.cookie_mountain_powerup_block_2:
                self.true,
            LocationName.cookie_mountain_coin_block_12:
                self.true,
            LocationName.cookie_mountain_coin_block_13:
                self.true,
            LocationName.cookie_mountain_coin_block_14:
                self.true,
            LocationName.cookie_mountain_coin_block_15:
                self.true,
            LocationName.cookie_mountain_coin_block_16:
                self.true,
            LocationName.cookie_mountain_coin_block_17:
                self.true,
            LocationName.cookie_mountain_coin_block_18:
                self.true,
            LocationName.cookie_mountain_coin_block_19:
                self.true,
            LocationName.cookie_mountain_coin_block_20:
                self.true,
            LocationName.cookie_mountain_coin_block_21:
                self.true,
            LocationName.cookie_mountain_coin_block_22:
                self.true,
            LocationName.cookie_mountain_coin_block_23:
                self.true,
            LocationName.cookie_mountain_coin_block_24:
                self.true,
            LocationName.cookie_mountain_coin_block_25:
                self.true,
            LocationName.cookie_mountain_coin_block_26:
                self.true,
            LocationName.cookie_mountain_coin_block_27:
                self.true,
            LocationName.cookie_mountain_coin_block_28:
                self.true,
            LocationName.cookie_mountain_coin_block_29:
                self.true,
            LocationName.cookie_mountain_coin_block_30:
                self.true,

            LocationName.soda_lake_dragon:
                self.can_swim,
            LocationName.soda_lake_powerup_block_1:
                self.can_swim,

            LocationName.twin_bridges_castle_powerup_block_1:
                lambda state: self.can_run(state) and self.can_climb(state),

            LocationName.forest_of_illusion_1_powerup_block_1:
                self.true,
            LocationName.forest_of_illusion_1_yoshi_block_1:
                self.true,
            LocationName.forest_of_illusion_1_powerup_block_2:
                self.true,
            LocationName.forest_of_illusion_1_key_block_1:
                self.has_p_balloon,
            LocationName.forest_of_illusion_1_life_block_1:
                self.true,

            LocationName.forest_of_illusion_2_dragon:
                self.can_swim,
            LocationName.forest_of_illusion_2_green_block_1:
                lambda state: self.has_gsp(state) and self.can_swim(state),
            LocationName.forest_of_illusion_2_powerup_block_1:
                self.can_swim,
            LocationName.forest_of_illusion_2_invis_coin_block_1:
                self.can_swim,
            LocationName.forest_of_illusion_2_invis_coin_block_2:
                self.can_swim,
            LocationName.forest_of_illusion_2_invis_life_block_1:
                self.can_swim,
            LocationName.forest_of_illusion_2_invis_coin_block_3:
                self.can_swim,
            LocationName.forest_of_illusion_2_yellow_block_1:
                lambda state: self.has_ysp(state) and self.can_swim(state),

            LocationName.forest_of_illusion_3_dragon:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_hidden_1up:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_yoshi_block_1:
                self.true,
            LocationName.forest_of_illusion_3_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_3_multi_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_3_coin_block_2:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_multi_coin_block_2:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_3:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_4:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_5:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_6:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_7:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_8:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_9:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_10:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_11:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_12:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_13:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_14:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_15:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_16:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_17:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_18:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_19:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_20:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_21:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_22:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_23:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.forest_of_illusion_3_coin_block_24:
                lambda state: self.can_carry(state) or self.has_yoshi(state),

            LocationName.forest_of_illusion_4_dragon:
                lambda state: self.has_yoshi(state) or self.can_carry(state) or 
                    self.has_p_switch(state) or self.has_fire_flower(state),
            LocationName.forest_of_illusion_4_multi_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_2:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_3:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_4:
                self.true,
            LocationName.forest_of_illusion_4_powerup_block_1:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_5:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_6:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_7:
                self.true,
            LocationName.forest_of_illusion_4_powerup_block_2:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_8:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_9:
                self.true,
            LocationName.forest_of_illusion_4_coin_block_10:
                self.true,

            LocationName.forest_ghost_house_dragon:
                self.has_p_switch,
            LocationName.forest_ghost_house_moon:
                self.has_p_switch,
            LocationName.forest_ghost_house_coin_block_1:
                self.true,
            LocationName.forest_ghost_house_powerup_block_1:
                self.true,
            LocationName.forest_ghost_house_flying_block_1:
                self.true,
            LocationName.forest_ghost_house_powerup_block_2:
                self.true,
            LocationName.forest_ghost_house_life_block_1:
                self.true,

            LocationName.forest_secret_dragon:
                self.true,
            LocationName.forest_secret_powerup_block_1:
                self.true,
            LocationName.forest_secret_powerup_block_2:
                self.true,
            LocationName.forest_secret_life_block_1:
                self.has_bsp,

            LocationName.forest_fortress_yellow_block_1:
                self.has_ysp,
            LocationName.forest_fortress_powerup_block_1:
                self.true,
            LocationName.forest_fortress_life_block_1:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_2:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_3:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_4:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_5:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_6:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_7:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_8:
                self.can_cape_fly,
            LocationName.forest_fortress_life_block_9:
                self.can_cape_fly,

            LocationName.forest_castle_dragon:
                self.true,
            LocationName.forest_castle_green_block_1:
                self.has_gsp,

            LocationName.blue_switch_palace:
                self.true,

            LocationName.chocolate_island_1_dragon:
                lambda state: self.has_p_switch(state) or self.has_yoshi(state),
            LocationName.chocolate_island_1_moon:
                lambda state: self.can_cape_fly(state) or self.has_yoshi(state),
            LocationName.chocolate_island_1_flying_block_1:
                self.true,
            LocationName.chocolate_island_1_flying_block_2:
                lambda state: self.has_p_switch(state) or self.has_yoshi(state),
            LocationName.chocolate_island_1_yoshi_block_1:
                lambda state: self.has_p_switch(state) or self.has_yoshi(state),
            LocationName.chocolate_island_1_green_block_1:
                lambda state: self.has_p_switch(state) or self.has_yoshi(state) and (
                    (self.has_gsp(state) and self.has_bsp(state)) or
                    (self.has_ysp(state) and self.has_bsp(state))
                ),
            LocationName.chocolate_island_1_life_block_1:
                lambda state: self.has_p_switch(state) or self.has_yoshi(state),
                
            LocationName.chocolate_island_2_dragon:
                lambda state: self.has_bsp(state) and (
                    self.has_p_switch(state) or self.has_gsp(state) or self.has_yoshi(state) or (
                        self.has_ysp(state) and self.has_rsp(state)
                    )),
            LocationName.chocolate_island_2_hidden_1up:
                self.true,
            LocationName.chocolate_island_2_multi_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_invis_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_yoshi_block_1:
                self.true,
            LocationName.chocolate_island_2_coin_block_1:
                self.true,
            LocationName.chocolate_island_2_coin_block_2:
                self.true,
            LocationName.chocolate_island_2_multi_coin_block_2:
                self.true,
            LocationName.chocolate_island_2_powerup_block_1:
                self.true,
            LocationName.chocolate_island_2_blue_pow_block_1:
                self.true,
            LocationName.chocolate_island_2_yellow_block_1:
                self.has_ysp,
            LocationName.chocolate_island_2_yellow_block_2:
                self.has_ysp,
            LocationName.chocolate_island_2_green_block_1:
                self.has_gsp,
            LocationName.chocolate_island_2_green_block_2:
                self.has_gsp,
            LocationName.chocolate_island_2_green_block_3:
                self.has_gsp,
            LocationName.chocolate_island_2_green_block_4:
                self.has_gsp,
            LocationName.chocolate_island_2_green_block_5:
                self.has_gsp,
            LocationName.chocolate_island_2_green_block_6:
                self.has_gsp,

            LocationName.chocolate_island_3_dragon:
                self.true,
            LocationName.chocolate_island_3_bonus_block:
                self.true,
            LocationName.chocolate_island_3_powerup_block_1:
                self.true,
            LocationName.chocolate_island_3_powerup_block_2:
                self.true,
            LocationName.chocolate_island_3_powerup_block_3:
                self.true,
            LocationName.chocolate_island_3_green_block_1:
                self.has_gsp,
            LocationName.chocolate_island_3_bonus_block_1:
                self.true,
            LocationName.chocolate_island_3_vine_block_1:
                self.true,
            LocationName.chocolate_island_3_life_block_1:
                self.can_cape_fly,
            LocationName.chocolate_island_3_life_block_2:
                self.can_cape_fly,
            LocationName.chocolate_island_3_life_block_3:
                self.can_cape_fly,

            LocationName.chocolate_island_4_dragon:
                lambda state: self.has_p_switch(state) and self.has_feather(state),
            LocationName.chocolate_island_4_yellow_block_1:
                lambda state: self.has_ysp(state) and  self.has_bsp(state),
            LocationName.chocolate_island_4_blue_pow_block_1:
                self.true,
            LocationName.chocolate_island_4_powerup_block_1:
                self.true,

            LocationName.chocolate_island_5_dragon:
                self.true,
            LocationName.chocolate_island_5_yoshi_block_1:
                self.true,
            LocationName.chocolate_island_5_powerup_block_1:
                self.true,
            LocationName.chocolate_island_5_life_block_1:
                lambda state: self.can_carry(state) and self.has_p_switch(state),
            LocationName.chocolate_island_5_yellow_block_1:
                lambda state: self.has_ysp(state) and self.can_carry(state) and self.has_p_switch(state),

            LocationName.chocolate_ghost_house_powerup_block_1:
                self.true,
            LocationName.chocolate_ghost_house_powerup_block_2:
                self.true,
            LocationName.chocolate_ghost_house_life_block_1:
                self.true,

            LocationName.chocolate_secret_powerup_block_1:
                self.true,
            LocationName.chocolate_secret_powerup_block_2:
                self.can_run,
                
            LocationName.chocolate_fortress_powerup_block_1:
                self.true,
            LocationName.chocolate_fortress_powerup_block_2:
                self.true,
            LocationName.chocolate_fortress_coin_block_1:
                self.true,
            LocationName.chocolate_fortress_coin_block_2:
                self.true,
            LocationName.chocolate_fortress_green_block_1:
                self.has_gsp,

            LocationName.chocolate_castle_hidden_1up:
                self.has_mushroom,
            LocationName.chocolate_castle_yellow_block_1:
                lambda state: self.has_mushroom(state) and self.has_ysp(state),
            LocationName.chocolate_castle_yellow_block_2:
                lambda state: self.has_mushroom(state) and self.has_ysp(state),
            LocationName.chocolate_castle_green_block_1:
                lambda state: self.has_mushroom(state) and self.has_gsp(state),

            LocationName.sunken_ghost_ship_dragon:
                self.can_swim,
            LocationName.sunken_ghost_ship_powerup_block_1:
                self.can_swim,
            LocationName.sunken_ghost_ship_star_block_1:
                self.can_swim,

            LocationName.valley_of_bowser_1_dragon:
                self.true,
            LocationName.valley_of_bowser_1_moon:
                self.true,
            LocationName.valley_of_bowser_1_green_block_1:
                self.has_gsp,
            LocationName.valley_of_bowser_1_invis_coin_block_1:
                self.true,
            LocationName.valley_of_bowser_1_invis_coin_block_2:
                self.true,
            LocationName.valley_of_bowser_1_invis_coin_block_3:
                self.true,
            LocationName.valley_of_bowser_1_yellow_block_1:
                lambda state: self.has_ysp(state) and self.has_feather(state),
            LocationName.valley_of_bowser_1_yellow_block_2:
                lambda state: self.has_ysp(state) and self.has_feather(state),
            LocationName.valley_of_bowser_1_yellow_block_3:
                lambda state: self.has_ysp(state) and self.has_feather(state),
            LocationName.valley_of_bowser_1_yellow_block_4:
                lambda state: self.has_ysp(state) and self.has_feather(state),
            LocationName.valley_of_bowser_1_vine_block_1:
                self.true,

            LocationName.valley_of_bowser_2_dragon:
                self.has_yoshi,
            LocationName.valley_of_bowser_2_hidden_1up:
                self.true,
            LocationName.valley_of_bowser_2_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_2_yellow_block_1:
                self.has_ysp,
            LocationName.valley_of_bowser_2_powerup_block_2:
                self.true,
            LocationName.valley_of_bowser_2_wings_block_1:
                self.true,

            LocationName.valley_of_bowser_3_dragon:
                self.true,
            LocationName.valley_of_bowser_3_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_3_powerup_block_2:
                self.can_carry,

            LocationName.valley_of_bowser_4_yellow_block_1:
                self.has_ysp,
            LocationName.valley_of_bowser_4_powerup_block_1:
                self.true,
            LocationName.valley_of_bowser_4_vine_block_1:
                self.true,
            LocationName.valley_of_bowser_4_yoshi_block_1:
                self.can_climb,
            LocationName.valley_of_bowser_4_life_block_1:
                lambda state: self.can_climb(state) and self.can_break_turn_blocks(state),
            LocationName.valley_of_bowser_4_powerup_block_2:
                lambda state: self.has_ysp(state) and self.can_climb(state),

            LocationName.valley_ghost_house_dragon:
                self.has_p_switch,
            LocationName.valley_ghost_house_pswitch_coin_block_1:
                self.has_p_switch,
            LocationName.valley_ghost_house_multi_coin_block_1:
                self.has_p_switch,
            LocationName.valley_ghost_house_powerup_block_1:
                self.true,
            LocationName.valley_ghost_house_directional_coin_block_1:
                self.has_p_switch,

            LocationName.valley_fortress_green_block_1:
                lambda state: self.has_mushroom(state) and self.has_gsp(state),
            LocationName.valley_fortress_yellow_block_1:
                lambda state: self.has_mushroom(state) and self.has_ysp(state),
                
            LocationName.valley_castle_dragon:
                self.true,
            LocationName.valley_castle_hidden_1up:
                self.true,
            LocationName.valley_castle_yellow_block_1:
                self.has_ysp,
            LocationName.valley_castle_yellow_block_2:
                self.has_ysp,
            LocationName.valley_castle_green_block_1:
                self.has_gsp,

            LocationName.star_road_1_dragon:
                self.can_break_turn_blocks,

            LocationName.star_road_2_star_block_1:
                self.can_swim,

            LocationName.star_road_3_key_block_1:
                lambda state: self.has_fire_flower(state) or self.can_carry(state),

            LocationName.star_road_4_powerup_block_1:
                self.true,
            LocationName.star_road_4_green_block_1:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_2:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_3:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_4:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_5:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_6:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_green_block_7:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_4_key_block_1:
                lambda state: self.can_carry(state) and (
                    self.has_yoshi(state) or (self.has_gsp(state) and self.has_rsp(state))
                ),

            LocationName.star_road_5_directional_coin_block_1:
                self.true,
            LocationName.star_road_5_life_block_1:
                self.has_p_switch,
            LocationName.star_road_5_vine_block_1:
                self.has_p_switch,
            LocationName.star_road_5_yellow_block_1:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_2:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_3:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_4:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_5:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_6:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_7:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_8:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_9:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_10:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_11:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_12:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_13:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_14:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_15:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_16:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_17:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_18:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_yellow_block_19:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state) and self.has_gsp(state),
            LocationName.star_road_5_yellow_block_20:
                lambda state: self.has_ysp(state) and self.can_yoshi_fly(state) and self.has_gsp(state),
            LocationName.star_road_5_green_block_1:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_2:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_3:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_4:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_5:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_6:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_7:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_8:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_9:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_10:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_11:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_12:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_13:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_14:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_15:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_16:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_17:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_18:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_19:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),
            LocationName.star_road_5_green_block_20:
                lambda state: self.has_gsp(state) and self.can_yoshi_fly(state),


            LocationName.special_zone_1_dragon:
                self.can_climb,
            LocationName.special_zone_1_hidden_1up:
                self.can_climb,
            LocationName.special_zone_1_vine_block_1:
                self.true,
            LocationName.special_zone_1_vine_block_2:
                self.true,
            LocationName.special_zone_1_vine_block_3:
                self.true,
            LocationName.special_zone_1_vine_block_4:
                self.true,
            LocationName.special_zone_1_life_block_1:
                self.can_climb,
            LocationName.special_zone_1_vine_block_5:
                self.can_climb,
            LocationName.special_zone_1_blue_pow_block_1:
                self.can_climb,
            LocationName.special_zone_1_vine_block_6:
                self.can_climb,
            LocationName.special_zone_1_powerup_block_1:
                self.can_climb,
            LocationName.special_zone_1_pswitch_coin_block_1:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_2:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_3:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_4:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_5:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_6:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_7:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_8:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_9:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_10:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_11:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_12:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),
            LocationName.special_zone_1_pswitch_coin_block_13:
                lambda state: self.can_climb(state) and self.has_p_switch(state) and self.has_feather(state),

            LocationName.special_zone_2_dragon:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_1:
                self.true,
            LocationName.special_zone_2_coin_block_1:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_2:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_2:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_3:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_4:
                self.has_p_balloon,
            LocationName.special_zone_2_powerup_block_3:
                self.has_p_balloon,
            LocationName.special_zone_2_multi_coin_block_1:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_5:
                self.has_p_balloon,
            LocationName.special_zone_2_coin_block_6:
                self.has_p_balloon,

            LocationName.special_zone_3_dragon:
                self.has_yoshi,
            LocationName.special_zone_3_powerup_block_1:
                self.true,
            LocationName.special_zone_3_yoshi_block_1:
                self.true,
            LocationName.special_zone_3_wings_block_1:
                self.true,

            LocationName.special_zone_4_dragon:
                self.has_fire_flower,
            LocationName.special_zone_4_powerup_block_1:
                self.has_fire_flower,
            LocationName.special_zone_4_star_block_1:
                lambda state: self.has_fire_flower(state) and self.can_carry(state),

            LocationName.special_zone_5_dragon:
                self.has_mushroom,
            LocationName.special_zone_5_yoshi_block_1:
                self.has_mushroom,

            LocationName.special_zone_6_dragon:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_powerup_block_1:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_1:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_2:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_yoshi_block_1:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_life_block_1:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_multi_coin_block_1:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_3:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_4:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_5:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_6:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_7:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_8:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_9:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_10:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_11:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_12:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_13:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_14:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_15:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_16:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_17:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_18:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_19:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_20:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_21:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_22:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_23:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_24:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_25:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_26:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_27:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_28:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_powerup_block_2:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_29:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_30:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_31:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_32:
                lambda state: self.can_swim(state) and self.has_mushroom(state),
            LocationName.special_zone_6_coin_block_33:
                lambda state: self.can_swim(state) and self.has_mushroom(state),

            LocationName.special_zone_7_dragon:
                self.has_mushroom,
            LocationName.special_zone_7_powerup_block_1:
                self.has_mushroom,
            LocationName.special_zone_7_yoshi_block_1:
                self.has_mushroom,
            LocationName.special_zone_7_coin_block_1:
                self.has_mushroom,
            LocationName.special_zone_7_powerup_block_2:
                self.has_mushroom,
            LocationName.special_zone_7_coin_block_2:
                self.has_mushroom,

            LocationName.special_zone_8_dragon:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_yoshi_block_1:
                lambda state: self.can_carry(state) or self.has_yoshi(state),
            LocationName.special_zone_8_coin_block_1:
                self.true,
            LocationName.special_zone_8_coin_block_2:
                self.true,
            LocationName.special_zone_8_coin_block_3:
                self.true,
            LocationName.special_zone_8_coin_block_4:
                self.true,
            LocationName.special_zone_8_coin_block_5:
                self.true,
            LocationName.special_zone_8_blue_pow_block_1:
                self.true,
            LocationName.special_zone_8_powerup_block_1:
                self.true,
            LocationName.special_zone_8_star_block_1:
                self.true,
            LocationName.special_zone_8_coin_block_6:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_7:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_8:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_9:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_10:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_11:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_12:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_13:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_14:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_15:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_16:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_17:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_18:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_multi_coin_block_1:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_19:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_20:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_21:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_22:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_coin_block_23:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_powerup_block_2:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
            LocationName.special_zone_8_flying_block_1:
                lambda state: self.can_break_turn_blocks(state) or self.has_feather(state) or
                    self.has_yoshi(state) or self.can_carry(state),
        }

    def set_smw_rules(self) -> None:
        super().set_smw_rules()
