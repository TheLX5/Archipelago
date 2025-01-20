
from typing import Dict, TYPE_CHECKING
if TYPE_CHECKING:
    from . import PerfectDarkWorld

from .Names import LocationName, ItemName, RegionName, EventName

from worlds.generic.Rules import CollectionRule
from BaseClasses import CollectionState
  
class PerfectDarkRules:
    player: int
    world: "PerfectDarkWorld"
    connection_rules: Dict[str, CollectionRule]
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]

    def __init__(self, world: "PerfectDarkWorld") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.carrington_institute} -> {RegionName.mission_1}":
                self.can_access_mission_1,
            f"{RegionName.carrington_institute} -> {RegionName.mission_2}":
                self.can_access_mission_2,
            f"{RegionName.carrington_institute} -> {RegionName.mission_3}":
                self.can_access_mission_3,
            f"{RegionName.carrington_institute} -> {RegionName.mission_4}":
                self.can_access_mission_4,
            f"{RegionName.carrington_institute} -> {RegionName.mission_5}":
                self.can_access_mission_5,
            f"{RegionName.carrington_institute} -> {RegionName.mission_6}":
                self.can_access_mission_6,
            f"{RegionName.carrington_institute} -> {RegionName.mission_7}":
                self.can_access_mission_7,
            f"{RegionName.carrington_institute} -> {RegionName.mission_8}":
                self.can_access_mission_8,
            f"{RegionName.carrington_institute} -> {RegionName.mission_9}":
                self.can_access_mission_9,
            f"{RegionName.carrington_institute} -> {RegionName.special_assignments}":
                self.can_access_special_assignments,

            f"{RegionName.carrington_institute} -> {RegionName.falcon_2}":
                self.has_falcon_2,
            f"{RegionName.carrington_institute} -> {RegionName.falcon_2_silencer}":
                self.has_falcon_2_silencer,
            f"{RegionName.carrington_institute} -> {RegionName.falcon_2_scope}":
                self.has_falcon_2_scope,
            f"{RegionName.carrington_institute} -> {RegionName.magsec_4}":
                self.has_magsec_4,
            f"{RegionName.carrington_institute} -> {RegionName.mauler}":
                self.has_mauler,
            f"{RegionName.carrington_institute} -> {RegionName.phoenix}":
                self.has_phoenix,
            f"{RegionName.carrington_institute} -> {RegionName.dy357_magnum}":
                self.has_dy357_magnum,
            f"{RegionName.carrington_institute} -> {RegionName.dy357_lx}":
                self.has_dy357_lx,
            f"{RegionName.carrington_institute} -> {RegionName.cmp150}":
                self.has_cmp150,
            f"{RegionName.carrington_institute} -> {RegionName.cyclone}":
                self.has_cyclone,
            f"{RegionName.carrington_institute} -> {RegionName.callisto_ntg}":
                self.has_callisto_ntg,
            f"{RegionName.carrington_institute} -> {RegionName.rc_p120}":
                self.has_rc_p120,
            f"{RegionName.carrington_institute} -> {RegionName.laptop_gun}":
                self.has_laptop_gun,
            f"{RegionName.carrington_institute} -> {RegionName.dragon}":
                self.has_dragon,
            f"{RegionName.carrington_institute} -> {RegionName.k7_avenger}":
                self.has_k7_avenger,
            f"{RegionName.carrington_institute} -> {RegionName.ar34}":
                self.has_ar34,
            f"{RegionName.carrington_institute} -> {RegionName.superdragon}":
                self.has_superdragon,
            f"{RegionName.carrington_institute} -> {RegionName.shotgun}":
                self.has_shotgun,
            f"{RegionName.carrington_institute} -> {RegionName.reaper}":
                self.has_reaper,
            f"{RegionName.carrington_institute} -> {RegionName.sniper_rifle}":
                lambda state: self.has_sniper_rifle(state) and self.can_use_secondary_action(state),
            f"{RegionName.carrington_institute} -> {RegionName.farsight_xr_20}":
                self.has_farsight_xr_20,
            f"{RegionName.carrington_institute} -> {RegionName.devastator}":
                self.has_devastator,
            f"{RegionName.carrington_institute} -> {RegionName.rocket_launcher}":
                self.has_rocket_launcher,
            f"{RegionName.carrington_institute} -> {RegionName.slayer}":
                self.has_slayer,
            f"{RegionName.carrington_institute} -> {RegionName.combat_knife}":
                lambda state: self.has_combat_knife(state) and self.can_use_secondary_action(state),
            f"{RegionName.carrington_institute} -> {RegionName.crossbow}":
                self.has_crossbow,
            f"{RegionName.carrington_institute} -> {RegionName.tranquilizer}":
                self.has_tranquilizer,
            f"{RegionName.carrington_institute} -> {RegionName.laser}":
                self.has_laser,
            f"{RegionName.carrington_institute} -> {RegionName.grenade}":
                self.has_grenade,
            f"{RegionName.carrington_institute} -> {RegionName.timed_mine}":
                self.has_timed_mine,
            f"{RegionName.carrington_institute} -> {RegionName.proximity_mine}":
                self.has_proximity_mine,
            f"{RegionName.carrington_institute} -> {RegionName.remote_mine}":
                lambda state: self.has_remote_mine(state) and self.can_use_secondary_action(state),
        }

        self.location_rules = {
            LocationName.mission_1_1_a:
                self.has_falcon_2_silencer,
            LocationName.mission_1_1_sa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_ecm_mine(state),
            LocationName.mission_1_1_pa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_ecm_mine(state) and self.has_data_uplink(state),

            LocationName.mission_1_2_a:
                lambda state: self.has_falcon_2(state) and self.has_cam_spy(state) and self.has_data_uplink(state),
            LocationName.mission_1_2_sa:
                lambda state: self.has_falcon_2(state) and self.has_cam_spy(state) and self.has_data_uplink(state),
            LocationName.mission_1_2_pa:
                lambda state: self.has_falcon_2(state) and self.has_cam_spy(state) and self.has_data_uplink(state),

            LocationName.mission_1_3_a:
                lambda state: self.has_falcon_2_scope(state) and self.has_night_vision(state),
            LocationName.mission_1_3_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_night_vision(state) and (
                    self.has_shotgun(state) or self.has_cmp150(state)
                ),
            LocationName.mission_1_3_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_night_vision(state) and (
                    self.has_shotgun(state) or self.has_cmp150(state)
                ),

            LocationName.mission_2_1_a:
                self.has_sniper_rifle,
            LocationName.mission_2_1_sa:
                self.has_sniper_rifle,
            LocationName.mission_2_1_pa:
                self.has_laptop_gun,

            LocationName.mission_3_1_a:
                lambda state: self.has_falcon_2_scope(state) and self.has_data_uplink(state),
            LocationName.mission_3_1_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_data_uplink(state) and self.has_remote_mine(state),
            LocationName.mission_3_1_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_data_uplink(state) and self.has_remote_mine(state),

            LocationName.mission_3_2_a:
                lambda state: self.has_falcon_2_silencer(state) and self.has_cam_spy(state) and self.has_door_decoder(state),
            LocationName.mission_3_2_sa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_cam_spy(state) and self.has_door_decoder(state),
            LocationName.mission_3_2_pa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_cam_spy(state) and self.has_door_decoder(state),

            LocationName.mission_4_1_a:
                self.has_falcon_2,
            LocationName.mission_4_1_sa:
                self.has_falcon_2,
            LocationName.mission_4_1_pa:
                self.has_falcon_2,

            LocationName.mission_4_2_a:
                lambda state: self.has_falcon_2_silencer(state) and self.has_x_ray_scanner(state),
            LocationName.mission_4_2_sa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_x_ray_scanner(state),
            LocationName.mission_4_2_pa:
                lambda state: self.has_falcon_2_silencer(state) and self.has_x_ray_scanner(state),

            LocationName.mission_4_3_a:
                self.has_falcon_2_scope,
            LocationName.mission_4_3_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_superdragon(state),
            LocationName.mission_4_3_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_superdragon(state),

            LocationName.mission_5_1_a:
                lambda state: (self.has_crossbow(state) or self.has_drug_spy(state)) and (
                    (self.has_k7_avenger(state) or self.has_dragon(state))
                ),
            LocationName.mission_5_1_sa:
                lambda state: (self.has_crossbow(state) or self.has_drug_spy(state)) and (
                    (self.has_k7_avenger(state) or self.has_dragon(state))
                ),
            LocationName.mission_5_1_pa:
                lambda state: (self.has_crossbow(state) or self.has_drug_spy(state)) and (
                    (self.has_k7_avenger(state) or self.has_dragon(state))
                ),

            LocationName.mission_5_2_a:
                lambda state: self.has_laptop_gun(state) and self.has_timed_mine(state),
            LocationName.mission_5_2_sa:
                lambda state: self.has_laptop_gun(state) and self.has_timed_mine(state),
            LocationName.mission_5_2_pa:
                lambda state: self.has_laptop_gun(state) and self.has_timed_mine(state),

            LocationName.mission_5_3_a:
                lambda state: self.has_falcon_2_scope(state) or self.has_sniper_rifle(state),
            LocationName.mission_5_3_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_sniper_rifle(state),
            LocationName.mission_5_3_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_sniper_rifle(state),

            LocationName.mission_6_1_a:
                lambda state: self.has_x_ray_scanner(state) and (
                    self.has_falcon_2_silencer(state) or self.has_laptop_gun(state)
                ),
            LocationName.mission_6_1_sa:
                lambda state: self.has_x_ray_scanner(state) and (
                    self.has_falcon_2_silencer(state) or self.has_laptop_gun(state)
                ),
            LocationName.mission_6_1_pa:
                lambda state: self.has_x_ray_scanner(state) and (
                    self.has_falcon_2_silencer(state) or self.has_laptop_gun(state)
                ),

            LocationName.mission_6_2_a:
                lambda state: self.has_falcon_2_scope(state) and self.has_shotgun(state) and self.has_ir_scanner(state),
            LocationName.mission_6_2_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_shotgun(state) and self.has_ir_scanner(state),
            LocationName.mission_6_2_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_shotgun(state) and 
                    self.has_farsight_xr_20(state) and self.has_ir_scanner(state),

            LocationName.mission_7_1_a:
                lambda state: self.has_ar34(state) and self.has_data_uplink(state),
            LocationName.mission_7_1_sa:
                lambda state: self.has_ar34(state) and self.has_data_uplink(state),
            LocationName.mission_7_1_pa:
                lambda state: self.has_ar34(state) and self.has_data_uplink(state) and self.has_laser(state),

            LocationName.mission_8_1_a:
                lambda state: self.has_combat_knife(state) and self.has_mauler(state) and self.has_ar34(state), 
            LocationName.mission_8_1_sa:
                lambda state: self.has_combat_knife(state) and self.has_mauler(state) and self.has_ar34(state), 
            LocationName.mission_8_1_pa:
                lambda state: self.has_combat_knife(state) and self.has_mauler(state) and self.has_ar34(state), 

            LocationName.mission_9_1_a:
                lambda state: self.has_falcon_2_scope(state) and self.has_callisto_ntg(state) and 
                    self.has_devastator(state) and self.has_ir_scanner(state) and self.has_r_tracker(state),
            LocationName.mission_9_1_sa:
                lambda state: self.has_falcon_2_scope(state) and self.has_callisto_ntg(state) and 
                    self.has_devastator(state) and self.has_ir_scanner(state) and self.has_r_tracker(state),
            LocationName.mission_9_1_pa:
                lambda state: self.has_falcon_2_scope(state) and self.has_callisto_ntg(state) and 
                    self.has_devastator(state) and self.has_ir_scanner(state) and self.has_r_tracker(state),

            LocationName.special_1_a:
                lambda state: self.has_mauler(state) and self.has_cloaking_device(state) and self.has_bomb_spy(state),
            LocationName.special_1_sa:
                lambda state: self.has_mauler(state) and self.has_cloaking_device(state) and self.has_bomb_spy(state),
            LocationName.special_1_pa:
                lambda state: self.has_mauler(state) and self.has_cloaking_device(state) and self.has_bomb_spy(state),

            LocationName.special_2_a:
                lambda state: self.has_falcon_2(state) and self.has_dragon(state) and self.has_tranquilizer(state),
            LocationName.special_2_sa:
                lambda state: self.has_falcon_2(state) and self.has_dragon(state) and self.has_tranquilizer(state),
            LocationName.special_2_pa:
                lambda state: self.has_falcon_2(state) and self.has_dragon(state) and 
                    self.has_tranquilizer(state) and self.has_dy357_lx(state),

            LocationName.special_3_a:
                lambda state: self.has_phoenix(state) and self.has_mauler(state),
            LocationName.special_3_sa:
                lambda state: self.has_phoenix(state) and self.has_mauler(state),
            LocationName.special_3_pa:
                lambda state: self.has_phoenix(state) and self.has_mauler(state),

            LocationName.special_4_a:
                self.has_falcon_2_scope,
            LocationName.special_4_sa:
                self.has_falcon_2_scope,
            LocationName.special_4_pa:
                self.has_falcon_2_scope,

            LocationName.mission_1_1_w1:
                self.true,
            LocationName.mission_1_2_w1:
                self.true,
            LocationName.mission_1_2_w2:
                self.true,
            LocationName.mission_1_3_w1:
                self.true,
            LocationName.mission_2_1_w1:
                self.true,
            LocationName.mission_2_1_w2:
                self.true,
            LocationName.mission_3_1_w1:
                self.true,
            LocationName.mission_3_1_w2:
                self.true,
            LocationName.mission_3_2_w1:
                self.true,
            LocationName.mission_4_1_w1:
                self.true,
            LocationName.mission_4_2_w1:
                self.true,
            LocationName.mission_4_2_w2:
                self.true,
            LocationName.mission_4_3_w1:
                self.true,
            LocationName.mission_4_3_w2:
                self.true,
            LocationName.mission_5_1_w1:
                self.true,
            LocationName.mission_5_1_w2:
                self.true,
            LocationName.mission_5_2_w1:
                self.true,
            LocationName.mission_5_3_w1:
                self.true,
            LocationName.mission_5_3_w2:
                self.true,
            LocationName.mission_6_1_w1:
                self.true,
            LocationName.mission_6_2_w1:
                self.true,
            LocationName.mission_7_1_w1:
                self.true,
            LocationName.mission_8_1_w1:
                self.true,
            LocationName.mission_8_1_w2:
                self.true,
            LocationName.mission_9_1_w1:
                self.true,
            LocationName.special_1_w1:
                self.true,
            LocationName.special_2_w1:
                self.true,
            LocationName.special_2_w2:
                self.true,

            LocationName.falcon_2_bronze:
                self.true,
            LocationName.falcon_2_silver:
                self.true,
            LocationName.falcon_2_gold:
                self.true,

            LocationName.falcon_2_silencer_bronze:
                self.true,
            LocationName.falcon_2_silencer_silver:
                self.true,
            LocationName.falcon_2_silencer_gold:
                self.true,

            LocationName.falcon_2_scope_bronze:
                self.true,
            LocationName.falcon_2_scope_silver:
                self.true,
            LocationName.falcon_2_scope_gold:
                self.true,

            LocationName.magsec_4_bronze:
                self.true,
            LocationName.magsec_4_silver:
                self.true,
            LocationName.magsec_4_gold:
                self.true,

            LocationName.mauler_bronze:
                self.true,
            LocationName.mauler_silver:
                self.can_use_secondary_action,
            LocationName.mauler_gold:
                self.can_use_secondary_action,

            LocationName.phoenix_bronze:
                self.true,
            LocationName.phoenix_silver:
                self.can_use_secondary_action,
            LocationName.phoenix_gold:
                self.can_use_secondary_action,

            LocationName.dy357_magnum_bronze:
                self.true,
            LocationName.dy357_magnum_silver:
                self.true,
            LocationName.dy357_magnum_gold:
                self.true,

            LocationName.dy357_lx_bronze:
                self.true,
            LocationName.dy357_lx_silver:
                self.true,
            LocationName.dy357_lx_gold:
                self.true,

            LocationName.cmp150_bronze:
                self.true,
            LocationName.cmp150_silver:
                self.true,
            LocationName.cmp150_gold:
                self.true,

            LocationName.cyclone_bronze:
                self.true,
            LocationName.cyclone_silver:
                self.true,
            LocationName.cyclone_gold:
                self.true,

            LocationName.callisto_ntg_bronze:
                self.true,
            LocationName.callisto_ntg_silver:
                self.can_use_secondary_action,
            LocationName.callisto_ntg_gold:
                self.can_use_secondary_action,

            LocationName.rc_p120_bronze:
                self.true,
            LocationName.rc_p120_silver:
                self.can_use_secondary_action,
            LocationName.rc_p120_gold:
                self.can_use_secondary_action,

            LocationName.laptop_gun_bronze:
                self.true,
            LocationName.laptop_gun_silver:
                self.can_use_secondary_action,
            LocationName.laptop_gun_gold:
                self.true,

            LocationName.dragon_bronze:
                self.true,
            LocationName.dragon_silver:
                self.can_use_secondary_action,
            LocationName.dragon_gold:
                self.true,

            LocationName.k7_avenger_bronze:
                self.true,
            LocationName.k7_avenger_silver:
                self.can_use_secondary_action,
            LocationName.k7_avenger_gold:
                self.true,

            LocationName.ar34_bronze:
                self.true,
            LocationName.ar34_silver:
                self.true,
            LocationName.ar34_gold:
                self.can_use_secondary_action,

            LocationName.superdragon_bronze:
                self.true,
            LocationName.superdragon_silver:
                self.can_use_secondary_action,
            LocationName.superdragon_gold:
                self.can_use_secondary_action,

            LocationName.shotgun_bronze:
                self.true,
            LocationName.shotgun_silver:
                self.true,
            LocationName.shotgun_gold:
                self.true,

            LocationName.reaper_bronze:
                self.true,
            LocationName.reaper_silver:
                self.true,
            LocationName.reaper_gold:
                self.true,

            LocationName.sniper_rifle_bronze:
                self.true,
            LocationName.sniper_rifle_silver:
                self.true,
            LocationName.sniper_rifle_gold:
                self.true,

            LocationName.farsight_xr_20_bronze:
                self.true,
            LocationName.farsight_xr_20_silver:
                self.true,
            LocationName.farsight_xr_20_gold:
                self.true,

            LocationName.devastator_bronze:
                self.true,
            LocationName.devastator_silver:
                self.can_use_secondary_action,
            LocationName.devastator_gold:
                self.can_use_secondary_action,

            LocationName.rocket_launcher_bronze:
                self.true,
            LocationName.rocket_launcher_silver:
                self.true,
            LocationName.rocket_launcher_gold:
                self.true,
                
            LocationName.slayer_bronze:
                self.true,
            LocationName.slayer_silver:
                self.can_use_secondary_action,
            LocationName.slayer_gold:
                self.can_use_secondary_action,

            LocationName.combat_knife_bronze:
                self.true,
            LocationName.combat_knife_silver:
                self.true,
            LocationName.combat_knife_gold:
                self.true,

            LocationName.crossbow_bronze:
                self.true,
            LocationName.crossbow_silver:
                self.true,
            LocationName.crossbow_gold:
                self.true,

            LocationName.tranquilizer_bronze:
                self.true,
            LocationName.tranquilizer_silver:
                self.true,
            LocationName.tranquilizer_gold:
                self.true,

            LocationName.laser_bronze:
                self.true,
            LocationName.laser_silver:
                self.true,
            LocationName.laser_gold:
                self.true,

            LocationName.grenade_bronze:
                self.true,
            LocationName.grenade_silver:
                self.true,
            LocationName.grenade_gold:
                self.true,

            LocationName.timed_mine_bronze:
                self.true,
            LocationName.timed_mine_silver:
                self.true,
            LocationName.timed_mine_gold:
                self.true,

            LocationName.proximity_mine_bronze:
                self.true,
            LocationName.proximity_mine_silver:
                self.true,
            LocationName.proximity_mine_gold:
                self.true,

            LocationName.remote_mine_bronze:
                self.true,
            LocationName.remote_mine_silver:
                self.true,
            LocationName.remote_mine_gold:
                self.true,

            LocationName.data_uplink:
                self.has_data_uplink,
            LocationName.ecm_mine:
                self.has_ecm_mine,
            LocationName.cam_spy:
                self.has_cam_spy,
            LocationName.night_vision:
                self.has_night_vision,
            LocationName.door_decoder:
                self.has_door_decoder,
            LocationName.r_tracker:
                self.has_r_tracker,
            LocationName.ir_scanner:
                self.has_ir_scanner,
            LocationName.x_ray_scanner:
                self.has_x_ray_scanner,
            LocationName.cloaking_device:
                self.has_cloaking_device,
            LocationName.disguise:
                self.has_disguise,

            LocationName.holo_1:
                self.true,
            LocationName.holo_2:
                self.true,
            LocationName.holo_3:
                self.true,
            LocationName.holo_4:
                self.true,
            LocationName.holo_5:
                self.true,
            LocationName.holo_6:
                lambda state: self.can_use_secondary_action(state) and self.has_falcon_2(state),
            LocationName.holo_7:
                lambda state: self.can_use_secondary_action(state) and self.has_falcon_2(state),

            EventName.mission_1_1:
                lambda state: state.can_reach_location(LocationName.mission_1_1_a, self.player),
            EventName.mission_1_2:
                lambda state: state.can_reach_location(LocationName.mission_1_2_a, self.player),
            EventName.mission_1_3:
                lambda state: state.can_reach_location(LocationName.mission_1_3_a, self.player),
            EventName.mission_2_1:
                lambda state: state.can_reach_location(LocationName.mission_2_1_a, self.player),
            EventName.mission_3_1:
                lambda state: state.can_reach_location(LocationName.mission_3_1_a, self.player),
            EventName.mission_3_2:
                lambda state: state.can_reach_location(LocationName.mission_3_2_a, self.player),
            EventName.mission_4_1:
                lambda state: state.can_reach_location(LocationName.mission_4_1_a, self.player),
            EventName.mission_4_2:
                lambda state: state.can_reach_location(LocationName.mission_4_2_a, self.player),
            EventName.mission_4_3:
                lambda state: state.can_reach_location(LocationName.mission_4_3_a, self.player),
            EventName.mission_5_1:
                lambda state: state.can_reach_location(LocationName.mission_5_1_a, self.player),
            EventName.mission_5_2:
                lambda state: state.can_reach_location(LocationName.mission_5_2_a, self.player),
            EventName.mission_5_3:
                lambda state: state.can_reach_location(LocationName.mission_5_3_a, self.player),
            EventName.mission_6_1:
                lambda state: state.can_reach_location(LocationName.mission_6_1_a, self.player),
            EventName.mission_6_2:
                lambda state: state.can_reach_location(LocationName.mission_6_2_a, self.player),
            EventName.mission_7_1:
                lambda state: state.can_reach_location(LocationName.mission_7_1_a, self.player),
            EventName.mission_8_1:
                lambda state: state.can_reach_location(LocationName.mission_8_1_a, self.player),
            EventName.mission_9_1:
                lambda state: state.can_reach_location(LocationName.mission_9_1_a, self.player),
            EventName.special_1:
                lambda state: state.can_reach_location(LocationName.special_1_a, self.player),
            EventName.special_1:
                lambda state: state.can_reach_location(LocationName.special_2_a, self.player),
            EventName.special_1:
                lambda state: state.can_reach_location(LocationName.special_3_a, self.player),
            EventName.special_1:
                lambda state: state.can_reach_location(LocationName.special_4_a, self.player),

            EventName.falcon_2:
                lambda state: state.can_reach_location(LocationName.falcon_2_gold, self.player),
            EventName.falcon_2_silencer:
                lambda state: state.can_reach_location(LocationName.falcon_2_silencer_gold, self.player),
            EventName.falcon_2_scope:
                lambda state: state.can_reach_location(LocationName.falcon_2_scope_gold, self.player),
            EventName.magsec_4:
                lambda state: state.can_reach_location(LocationName.magsec_4_gold, self.player),
            EventName.mauler:
                lambda state: state.can_reach_location(LocationName.mauler_gold, self.player),
            EventName.phoenix:
                lambda state: state.can_reach_location(LocationName.phoenix_gold, self.player),
            EventName.dy357_magnum:
                lambda state: state.can_reach_location(LocationName.dy357_magnum_gold, self.player),
            EventName.dy357_lx:
                lambda state: state.can_reach_location(LocationName.dy357_lx_gold, self.player),
            EventName.cmp150:
                lambda state: state.can_reach_location(LocationName.cmp150_gold, self.player),
            EventName.cyclone:
                lambda state: state.can_reach_location(LocationName.cyclone_gold, self.player),
            EventName.callisto_ntg:
                lambda state: state.can_reach_location(LocationName.callisto_ntg_gold, self.player),
            EventName.rc_p120:
                lambda state: state.can_reach_location(LocationName.rc_p120_gold, self.player),
            EventName.laptop_gun:
                lambda state: state.can_reach_location(LocationName.laptop_gun_gold, self.player),
            EventName.dragon:
                lambda state: state.can_reach_location(LocationName.dragon_gold, self.player),
            EventName.k7_avenger:
                lambda state: state.can_reach_location(LocationName.k7_avenger_gold, self.player),
            EventName.ar34:
                lambda state: state.can_reach_location(LocationName.ar34_gold, self.player),
            EventName.superdragon:
                lambda state: state.can_reach_location(LocationName.superdragon_gold, self.player),
            EventName.shotgun:
                lambda state: state.can_reach_location(LocationName.shotgun_gold, self.player),
            EventName.reaper:
                lambda state: state.can_reach_location(LocationName.reaper_gold, self.player),
            EventName.sniper_rifle:
                lambda state: state.can_reach_location(LocationName.sniper_rifle_gold, self.player),
            EventName.farsight_xr_20:
                lambda state: state.can_reach_location(LocationName.farsight_xr_20_gold, self.player),
            EventName.devastator:
                lambda state: state.can_reach_location(LocationName.devastator_gold, self.player),
            EventName.rocket_launcher:
                lambda state: state.can_reach_location(LocationName.rocket_launcher_gold, self.player),
            EventName.slayer:
                lambda state: state.can_reach_location(LocationName.slayer_gold, self.player),
            EventName.combat_knife:
                lambda state: state.can_reach_location(LocationName.combat_knife_gold, self.player),
            EventName.crossbow:
                lambda state: state.can_reach_location(LocationName.crossbow_gold, self.player),
            EventName.tranquilizer:
                lambda state: state.can_reach_location(LocationName.tranquilizer_gold, self.player),
            EventName.laser:
                lambda state: state.can_reach_location(LocationName.laser_gold, self.player),
            EventName.grenade:
                lambda state: state.can_reach_location(LocationName.grenade_gold, self.player),
            EventName.timed_mine:
                lambda state: state.can_reach_location(LocationName.timed_mine_gold, self.player),
            EventName.proximity_mine:
                lambda state: state.can_reach_location(LocationName.proximity_mine_gold, self.player),
            EventName.remote_mine:
                lambda state: state.can_reach_location(LocationName.remote_mine_gold, self.player),

            EventName.data_uplink:
                lambda state: state.can_reach_location(LocationName.data_uplink, self.player),
            EventName.ecm_mine:
                lambda state: state.can_reach_location(LocationName.ecm_mine, self.player),
            EventName.cam_spy:
                lambda state: state.can_reach_location(LocationName.cam_spy, self.player),
            EventName.night_vision:
                lambda state: state.can_reach_location(LocationName.night_vision, self.player),
            EventName.door_decoder:
                lambda state: state.can_reach_location(LocationName.door_decoder, self.player),
            EventName.r_tracker:
                lambda state: state.can_reach_location(LocationName.r_tracker, self.player),
            EventName.ir_scanner:
                lambda state: state.can_reach_location(LocationName.ir_scanner, self.player),
            EventName.x_ray_scanner:
                lambda state: state.can_reach_location(LocationName.x_ray_scanner, self.player),
            EventName.cloaking_device:
                lambda state: state.can_reach_location(LocationName.cloaking_device, self.player),
            EventName.disguise:
                lambda state: state.can_reach_location(LocationName.disguise, self.player),

            EventName.holo_1:
                lambda state: state.can_reach_location(LocationName.holo_1, self.player),
            EventName.holo_2:
                lambda state: state.can_reach_location(LocationName.holo_2, self.player),
            EventName.holo_3:
                lambda state: state.can_reach_location(LocationName.holo_3, self.player),
            EventName.holo_4:
                lambda state: state.can_reach_location(LocationName.holo_4, self.player),
            EventName.holo_5:
                lambda state: state.can_reach_location(LocationName.holo_5, self.player),
            EventName.holo_6:
                lambda state: state.can_reach_location(LocationName.holo_6, self.player),
            EventName.holo_7:
                lambda state: state.can_reach_location(LocationName.holo_7, self.player),

        }

    def can_access_mission_1(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_1, self.player)
    
    def can_access_mission_2(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_2, self.player)
    
    def can_access_mission_3(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_3, self.player)
    
    def can_access_mission_4(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_4, self.player)
    
    def can_access_mission_5(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_5, self.player)
    
    def can_access_mission_6(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_6, self.player)
    
    def can_access_mission_7(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_7, self.player)
    
    def can_access_mission_8(self, state: CollectionState) -> bool:
        return state.has(ItemName.mission_8, self.player)
    
    def can_access_mission_9(self, state: CollectionState) -> bool:
        return state.has(ItemName.medal, self.player, 50)
    
    def can_access_special_assignments(self, state: CollectionState) -> bool:
        return state.has(ItemName.special_assignments, self.player)


    def has_falcon_2(self, state: CollectionState) -> bool:
        return state.has(ItemName.falcon_2, self.player)
    
    def has_falcon_2_silencer(self, state: CollectionState) -> bool:
        return state.has(ItemName.falcon_2_silencer, self.player)
    
    def has_falcon_2_scope(self, state: CollectionState) -> bool:
        return state.has(ItemName.falcon_2_scope, self.player)
    
    def has_magsec_4(self, state: CollectionState) -> bool:
        return state.has(ItemName.magsec_4, self.player)
    
    def has_mauler(self, state: CollectionState) -> bool:
        return state.has(ItemName.mauler, self.player)
    
    def has_phoenix(self, state: CollectionState) -> bool:
        return state.has(ItemName.phoenix, self.player)
    
    def has_dy357_magnum(self, state: CollectionState) -> bool:
        return state.has(ItemName.dy357_magnum, self.player)
    
    def has_dy357_lx(self, state: CollectionState) -> bool:
        return state.has(ItemName.dy357_lx, self.player)
    
    def has_cmp150(self, state: CollectionState) -> bool:
        return state.has(ItemName.cmp150, self.player)
    
    def has_cyclone(self, state: CollectionState) -> bool:
        return state.has(ItemName.cyclone, self.player)
    
    def has_callisto_ntg(self, state: CollectionState) -> bool:
        return state.has(ItemName.callisto_ntg, self.player)
    
    def has_rc_p120(self, state: CollectionState) -> bool:
        return state.has(ItemName.rc_p120, self.player)
    
    def has_laptop_gun(self, state: CollectionState) -> bool:
        return state.has(ItemName.laptop_gun, self.player)
    
    def has_dragon(self, state: CollectionState) -> bool:
        return state.has(ItemName.dragon, self.player)
    
    def has_k7_avenger(self, state: CollectionState) -> bool:
        return state.has(ItemName.k7_avenger, self.player)
    
    def has_ar34(self, state: CollectionState) -> bool:
        return state.has(ItemName.ar34, self.player)
    
    def has_superdragon(self, state: CollectionState) -> bool:
        return state.has(ItemName.superdragon, self.player)
    
    def has_shotgun(self, state: CollectionState) -> bool:
        return state.has(ItemName.shotgun, self.player)
    
    def has_reaper(self, state: CollectionState) -> bool:
        return state.has(ItemName.reaper, self.player)
    
    def has_sniper_rifle(self, state: CollectionState) -> bool:
        return state.has(ItemName.sniper_rifle, self.player)
    
    def has_farsight_xr_20(self, state: CollectionState) -> bool:
        return state.has(ItemName.farsight_xr_20, self.player)
    
    def has_devastator(self, state: CollectionState) -> bool:
        return state.has(ItemName.devastator, self.player)
    
    def has_rocket_launcher(self, state: CollectionState) -> bool:
        return state.has(ItemName.rocket_launcher, self.player)
    
    def has_slayer(self, state: CollectionState) -> bool:
        return state.has(ItemName.slayer, self.player)
    
    def has_combat_knife(self, state: CollectionState) -> bool:
        return state.has(ItemName.combat_knife, self.player)
    
    def has_crossbow(self, state: CollectionState) -> bool:
        return state.has(ItemName.crossbow, self.player)
    
    def has_tranquilizer(self, state: CollectionState) -> bool:
        return state.has(ItemName.tranquilizer, self.player)
    
    def has_laser(self, state: CollectionState) -> bool:
        return state.has(ItemName.laser, self.player)
    
    def has_grenade(self, state: CollectionState) -> bool:
        return state.has(ItemName.grenade, self.player)
    
    def has_timed_mine(self, state: CollectionState) -> bool:
        return state.has(ItemName.timed_mine, self.player)
    
    def has_proximity_mine(self, state: CollectionState) -> bool:
        return state.has(ItemName.proximity_mine, self.player)
    
    def has_remote_mine(self, state: CollectionState) -> bool:
        return state.has(ItemName.remote_mine, self.player)
    
    def has_data_uplink(self, state: CollectionState) -> bool:
        return state.has(ItemName.data_uplink, self.player)
    
    def has_ecm_mine(self, state: CollectionState) -> bool:
        return state.has(ItemName.ecm_mine, self.player)
    
    def has_cam_spy(self, state: CollectionState) -> bool:
        return state.has(ItemName.cam_spy, self.player)
    
    def has_drug_spy(self, state: CollectionState) -> bool:
        return state.has(ItemName.drug_spy, self.player)
    
    def has_bomb_spy(self, state: CollectionState) -> bool:
        return state.has(ItemName.bomb_spy, self.player)
    
    def has_night_vision(self, state: CollectionState) -> bool:
        return state.has(ItemName.night_vision, self.player)
    
    def has_door_decoder(self, state: CollectionState) -> bool:
        return state.has(ItemName.door_decoder, self.player)
    
    def has_r_tracker(self, state: CollectionState) -> bool:
        return state.has(ItemName.r_tracker, self.player)
    
    def has_ir_scanner(self, state: CollectionState) -> bool:
        return state.has(ItemName.ir_scanner, self.player)
    
    def has_x_ray_scanner(self, state: CollectionState) -> bool:
        return state.has(ItemName.x_ray_scanner, self.player)
    
    def has_cloaking_device(self, state: CollectionState) -> bool:
        return state.has(ItemName.cloaking_device, self.player)
    
    def has_disguise(self, state: CollectionState) -> bool:
        return state.has(ItemName.disguise, self.player)
    
    def has_shields(self, state: CollectionState) -> bool:
        return state.has(ItemName.shields, self.player, 1)
    
    def has_strong_shields(self, state: CollectionState) -> bool:
        return state.has(ItemName.shields, self.player, 2)
    
    def has_extra_health(self, state: CollectionState) -> bool:
        return state.has(ItemName.health, self.player, 1)
    
    def can_use_secondary_action(self, state: CollectionState) -> bool:
        return state.has(ItemName.secondary_action, self.player)
    

    def true(self, state: CollectionState) -> bool:
        return True
    
    def set_pd_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            entrance = multiworld.get_entrance(entrance_name, self.player)
            entrance.access_rule = rule
        for loc in multiworld.get_locations(self.player):
            if loc.name in self.location_rules:
                loc.access_rule = self.location_rules[loc.name]
                
        multiworld.completion_condition[self.player] = lambda state: state.has(ItemName.victory, self.player)
            