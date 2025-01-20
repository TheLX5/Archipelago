from BaseClasses import MultiWorld, Region, ItemClassification
from .Locations import PerfectDarkLocation, carrington_locations
from .Items import PDItem
from .Names import LocationName, RegionName, EventName, ItemName
from worlds.AutoWorld import World

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PerfectDarkWorld

def create_regions(world: "PerfectDarkWorld", active_locations):
    multiworld = world.multiworld
    player = world.player

    menu = create_region(multiworld, player, active_locations, 'Menu')
    carrington_institute = create_region(multiworld, player, active_locations, RegionName.carrington_institute,
                                         [location for location in carrington_locations])
    mission_1 = create_region(multiworld, player, active_locations, RegionName.mission_1,
                              [
                                LocationName.mission_1_1_a,
                                LocationName.mission_1_1_sa,
                                LocationName.mission_1_1_pa,
                                LocationName.mission_1_2_a,
                                LocationName.mission_1_2_sa,
                                LocationName.mission_1_2_pa,
                                LocationName.mission_1_3_a,
                                LocationName.mission_1_3_sa,
                                LocationName.mission_1_3_pa,
                            ])
    mission_2 = create_region(multiworld, player, active_locations, RegionName.mission_2,
                              [
                                LocationName.mission_2_1_a,
                                LocationName.mission_2_1_sa,
                                LocationName.mission_2_1_pa,
                            ])
    mission_3 = create_region(multiworld, player, active_locations, RegionName.mission_3,
                              [
                                LocationName.mission_3_1_a,
                                LocationName.mission_3_1_sa,
                                LocationName.mission_3_1_pa,
                                LocationName.mission_3_2_a,
                                LocationName.mission_3_2_sa,
                                LocationName.mission_3_2_pa,
                            ])
    mission_4 = create_region(multiworld, player, active_locations, RegionName.mission_4,
                              [
                                LocationName.mission_4_1_a,
                                LocationName.mission_4_1_sa,
                                LocationName.mission_4_1_pa,
                                LocationName.mission_4_2_a,
                                LocationName.mission_4_2_sa,
                                LocationName.mission_4_2_pa,
                                LocationName.mission_4_3_a,
                                LocationName.mission_4_3_sa,
                                LocationName.mission_4_3_pa,
                            ])
    mission_5 = create_region(multiworld, player, active_locations, RegionName.mission_5,
                              [
                                LocationName.mission_5_1_a,
                                LocationName.mission_5_1_sa,
                                LocationName.mission_5_1_pa,
                                LocationName.mission_5_2_a,
                                LocationName.mission_5_2_sa,
                                LocationName.mission_5_2_pa,
                                LocationName.mission_5_3_a,
                                LocationName.mission_5_3_sa,
                                LocationName.mission_5_3_pa,
                            ])
    mission_6 = create_region(multiworld, player, active_locations, RegionName.mission_6,
                              [
                                LocationName.mission_6_1_a,
                                LocationName.mission_6_1_sa,
                                LocationName.mission_6_1_pa,
                                LocationName.mission_6_2_a,
                                LocationName.mission_6_2_sa,
                                LocationName.mission_6_2_pa,
                            ])
    mission_7 = create_region(multiworld, player, active_locations, RegionName.mission_7,
                              [
                                LocationName.mission_7_1_a,
                                LocationName.mission_7_1_sa,
                                LocationName.mission_7_1_pa,
                            ])
    mission_8 = create_region(multiworld, player, active_locations, RegionName.mission_8,
                              [
                                LocationName.mission_8_1_a,
                                LocationName.mission_8_1_sa,
                                LocationName.mission_8_1_pa,
                            ])
    mission_9 = create_region(multiworld, player, active_locations, RegionName.mission_9,
                              [
                                LocationName.mission_9_1_a,
                                LocationName.mission_9_1_sa,
                                LocationName.mission_9_1_pa,
                            ])
    special_assignments = create_region(multiworld, player, active_locations, RegionName.special_assignments,
                                        [
                                            LocationName.special_1_a,
                                            LocationName.special_1_sa,
                                            LocationName.special_1_pa,
                                            LocationName.special_2_a,
                                            LocationName.special_2_sa,
                                            LocationName.special_2_pa,
                                            LocationName.special_3_a,
                                            LocationName.special_3_sa,
                                            LocationName.special_3_pa,
                                            LocationName.special_4_a,
                                            LocationName.special_4_sa,
                                            LocationName.special_4_pa,
                                        ])
    
    falcon_2 = create_region(multiworld, player, active_locations, RegionName.falcon_2,
                              [
                                LocationName.falcon_2_bronze,
                                LocationName.falcon_2_silver,
                                LocationName.falcon_2_gold,
                            ])
    falcon_2_silencer = create_region(multiworld, player, active_locations, RegionName.falcon_2_silencer,
                              [
                                LocationName.falcon_2_silencer_bronze,
                                LocationName.falcon_2_silencer_silver,
                                LocationName.falcon_2_silencer_gold,
                            ])
    falcon_2_scope = create_region(multiworld, player, active_locations, RegionName.falcon_2_scope,
                              [
                                LocationName.falcon_2_scope_bronze,
                                LocationName.falcon_2_scope_silver,
                                LocationName.falcon_2_scope_gold,
                            ])
    magsec_4 = create_region(multiworld, player, active_locations, RegionName.magsec_4,
                              [
                                LocationName.magsec_4_bronze,
                                LocationName.magsec_4_silver,
                                LocationName.magsec_4_gold,
                            ])
    mauler = create_region(multiworld, player, active_locations, RegionName.mauler,
                              [
                                LocationName.mauler_bronze,
                                LocationName.mauler_silver,
                                LocationName.mauler_gold,
                            ])
    phoenix = create_region(multiworld, player, active_locations, RegionName.phoenix,
                              [
                                LocationName.phoenix_bronze,
                                LocationName.phoenix_silver,
                                LocationName.phoenix_gold,
                            ])
    dy357_magnum = create_region(multiworld, player, active_locations, RegionName.dy357_magnum,
                              [
                                LocationName.dy357_magnum_bronze,
                                LocationName.dy357_magnum_silver,
                                LocationName.dy357_magnum_gold,
                            ])
    dy357_lx = create_region(multiworld, player, active_locations, RegionName.dy357_lx,
                              [
                                LocationName.dy357_lx_bronze,
                                LocationName.dy357_lx_silver,
                                LocationName.dy357_lx_gold,
                            ])
    cmp150 = create_region(multiworld, player, active_locations, RegionName.cmp150,
                              [
                                LocationName.cmp150_bronze,
                                LocationName.cmp150_silver,
                                LocationName.cmp150_gold,
                            ])
    cyclone = create_region(multiworld, player, active_locations, RegionName.cyclone,
                              [
                                LocationName.cyclone_bronze,
                                LocationName.cyclone_silver,
                                LocationName.cyclone_gold,
                            ])
    callisto_ntg = create_region(multiworld, player, active_locations, RegionName.callisto_ntg,
                              [
                                LocationName.callisto_ntg_bronze,
                                LocationName.callisto_ntg_silver,
                                LocationName.callisto_ntg_gold,
                            ])
    rc_p120 = create_region(multiworld, player, active_locations, RegionName.rc_p120,
                              [
                                LocationName.rc_p120_bronze,
                                LocationName.rc_p120_silver,
                                LocationName.rc_p120_gold,
                            ])
    laptop_gun = create_region(multiworld, player, active_locations, RegionName.laptop_gun,
                              [
                                LocationName.laptop_gun_bronze,
                                LocationName.laptop_gun_silver,
                                LocationName.laptop_gun_gold,
                            ])
    dragon = create_region(multiworld, player, active_locations, RegionName.dragon,
                              [
                                LocationName.dragon_bronze,
                                LocationName.dragon_silver,
                                LocationName.dragon_gold,
                            ])
    k7_avenger = create_region(multiworld, player, active_locations, RegionName.k7_avenger,
                              [
                                LocationName.k7_avenger_bronze,
                                LocationName.k7_avenger_silver,
                                LocationName.k7_avenger_gold,
                            ])
    ar34 = create_region(multiworld, player, active_locations, RegionName.ar34,
                              [
                                LocationName.ar34_bronze,
                                LocationName.ar34_silver,
                                LocationName.ar34_gold,
                            ])
    superdragon = create_region(multiworld, player, active_locations, RegionName.superdragon,
                              [
                                LocationName.superdragon_bronze,
                                LocationName.superdragon_silver,
                                LocationName.superdragon_gold,
                            ])
    shotgun = create_region(multiworld, player, active_locations, RegionName.shotgun,
                              [
                                LocationName.shotgun_bronze,
                                LocationName.shotgun_silver,
                                LocationName.shotgun_gold,
                            ])
    reaper = create_region(multiworld, player, active_locations, RegionName.reaper,
                              [
                                LocationName.reaper_bronze,
                                LocationName.reaper_silver,
                                LocationName.reaper_gold,
                            ])
    sniper_rifle = create_region(multiworld, player, active_locations, RegionName.sniper_rifle,
                              [
                                LocationName.sniper_rifle_bronze,
                                LocationName.sniper_rifle_silver,
                                LocationName.sniper_rifle_gold,
                            ])
    farsight_xr_20 = create_region(multiworld, player, active_locations, RegionName.farsight_xr_20,
                              [
                                LocationName.farsight_xr_20_bronze,
                                LocationName.farsight_xr_20_silver,
                                LocationName.farsight_xr_20_gold,
                            ])
    devastator = create_region(multiworld, player, active_locations, RegionName.devastator,
                              [
                                LocationName.devastator_bronze,
                                LocationName.devastator_silver,
                                LocationName.devastator_gold,
                            ])
    rocket_launcher = create_region(multiworld, player, active_locations, RegionName.rocket_launcher,
                              [
                                LocationName.rocket_launcher_bronze,
                                LocationName.rocket_launcher_silver,
                                LocationName.rocket_launcher_gold,
                            ])
    slayer = create_region(multiworld, player, active_locations, RegionName.slayer,
                              [
                                LocationName.slayer_bronze,
                                LocationName.slayer_silver,
                                LocationName.slayer_gold,
                            ])
    combat_knife = create_region(multiworld, player, active_locations, RegionName.combat_knife,
                              [
                                LocationName.combat_knife_bronze,
                                LocationName.combat_knife_silver,
                                LocationName.combat_knife_gold,
                            ])
    crossbow = create_region(multiworld, player, active_locations, RegionName.crossbow,
                              [
                                LocationName.crossbow_bronze,
                                LocationName.crossbow_silver,
                                LocationName.crossbow_gold,
                            ])
    tranquilizer = create_region(multiworld, player, active_locations, RegionName.tranquilizer,
                              [
                                LocationName.tranquilizer_bronze,
                                LocationName.tranquilizer_silver,
                                LocationName.tranquilizer_gold,
                            ])
    laser = create_region(multiworld, player, active_locations, RegionName.laser,
                              [
                                LocationName.laser_bronze,
                                LocationName.laser_silver,
                                LocationName.laser_gold,
                            ])
    grenade = create_region(multiworld, player, active_locations, RegionName.grenade,
                              [
                                LocationName.grenade_bronze,
                                LocationName.grenade_silver,
                                LocationName.grenade_gold,
                            ])
    timed_mine = create_region(multiworld, player, active_locations, RegionName.timed_mine,
                              [
                                LocationName.timed_mine_bronze,
                                LocationName.timed_mine_silver,
                                LocationName.timed_mine_gold,
                            ])
    proximity_mine = create_region(multiworld, player, active_locations, RegionName.proximity_mine,
                              [
                                LocationName.proximity_mine_bronze,
                                LocationName.proximity_mine_silver,
                                LocationName.proximity_mine_gold,
                            ])
    remote_mine = create_region(multiworld, player, active_locations, RegionName.remote_mine,
                              [
                                LocationName.remote_mine_bronze,
                                LocationName.remote_mine_silver,
                                LocationName.remote_mine_gold,
                            ])

    multiworld.regions += [
        menu,
        carrington_institute,
        mission_1,
        mission_2,
        mission_3,
        mission_4,
        mission_5,
        mission_6,
        mission_7,
        mission_8,
        mission_9,
        special_assignments,
        falcon_2,
        falcon_2_silencer,
        falcon_2_scope,
        magsec_4,
        mauler,
        phoenix,
        dy357_magnum,
        dy357_lx,
        cmp150,
        cyclone,
        callisto_ntg,
        rc_p120,
        laptop_gun,
        dragon,
        k7_avenger,
        ar34,
        superdragon,
        shotgun,
        reaper,
        sniper_rifle,
        farsight_xr_20,
        devastator,
        rocket_launcher,
        slayer,
        combat_knife,
        crossbow,
        tranquilizer,
        laser,
        grenade,
        timed_mine,
        proximity_mine,
        remote_mine,
    ]

    add_event_to_region(multiworld, player, RegionName.mission_1, EventName.mission_1_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_1, EventName.mission_1_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_1, EventName.mission_1_3, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_2, EventName.mission_2_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_3, EventName.mission_3_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_3, EventName.mission_3_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_4, EventName.mission_4_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_4, EventName.mission_4_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_4, EventName.mission_4_3, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_5, EventName.mission_5_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_5, EventName.mission_5_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_5, EventName.mission_5_3, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_6, EventName.mission_6_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_6, EventName.mission_6_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_7, EventName.mission_7_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_8, EventName.mission_8_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.mission_9, EventName.mission_9_1, ItemName.victory)
    add_event_to_region(multiworld, player, RegionName.special_assignments, EventName.special_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.special_assignments, EventName.special_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.special_assignments, EventName.special_3, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.special_assignments, EventName.special_4, ItemName.medal)

    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.falcon_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.falcon_2_silencer, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.falcon_2_scope, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.magsec_4, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.mauler, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.phoenix, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.dy357_magnum, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.dy357_lx, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.cmp150, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.cyclone, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.callisto_ntg, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.rc_p120, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.laptop_gun, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.dragon, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.k7_avenger, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.ar34, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.superdragon, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.shotgun, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.reaper, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.sniper_rifle, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.farsight_xr_20, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.devastator, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.rocket_launcher, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.slayer, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.combat_knife, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.crossbow, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.tranquilizer, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.laser, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.grenade, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.timed_mine, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.proximity_mine, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.remote_mine, ItemName.medal)

    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.data_uplink, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.ecm_mine, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.cam_spy, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.night_vision, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.door_decoder, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.r_tracker, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.ir_scanner, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.x_ray_scanner, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.cloaking_device, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.disguise, ItemName.medal)

    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_1, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_2, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_3, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_4, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_5, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_6, ItemName.medal)
    add_event_to_region(multiworld, player, RegionName.carrington_institute, EventName.holo_7, ItemName.medal)

def connect_regions(world: "PerfectDarkWorld"):
    connect(world, "Menu", RegionName.carrington_institute)
    connect(world, RegionName.carrington_institute, RegionName.mission_1)
    connect(world, RegionName.carrington_institute, RegionName.mission_2)
    connect(world, RegionName.carrington_institute, RegionName.mission_3)
    connect(world, RegionName.carrington_institute, RegionName.mission_4)
    connect(world, RegionName.carrington_institute, RegionName.mission_5)
    connect(world, RegionName.carrington_institute, RegionName.mission_6)
    connect(world, RegionName.carrington_institute, RegionName.mission_7)
    connect(world, RegionName.carrington_institute, RegionName.mission_8)
    connect(world, RegionName.carrington_institute, RegionName.mission_9)
    connect(world, RegionName.carrington_institute, RegionName.special_assignments)

    connect(world, RegionName.carrington_institute, RegionName.falcon_2)
    connect(world, RegionName.carrington_institute, RegionName.falcon_2_silencer)
    connect(world, RegionName.carrington_institute, RegionName.falcon_2_scope)
    connect(world, RegionName.carrington_institute, RegionName.magsec_4)
    connect(world, RegionName.carrington_institute, RegionName.mauler)
    connect(world, RegionName.carrington_institute, RegionName.phoenix)
    connect(world, RegionName.carrington_institute, RegionName.dy357_magnum)
    connect(world, RegionName.carrington_institute, RegionName.dy357_lx)
    connect(world, RegionName.carrington_institute, RegionName.cmp150)
    connect(world, RegionName.carrington_institute, RegionName.cyclone)
    connect(world, RegionName.carrington_institute, RegionName.callisto_ntg)
    connect(world, RegionName.carrington_institute, RegionName.rc_p120)
    connect(world, RegionName.carrington_institute, RegionName.laptop_gun)
    connect(world, RegionName.carrington_institute, RegionName.dragon)
    connect(world, RegionName.carrington_institute, RegionName.k7_avenger)
    connect(world, RegionName.carrington_institute, RegionName.ar34)
    connect(world, RegionName.carrington_institute, RegionName.superdragon)
    connect(world, RegionName.carrington_institute, RegionName.shotgun)
    connect(world, RegionName.carrington_institute, RegionName.reaper)
    connect(world, RegionName.carrington_institute, RegionName.sniper_rifle)
    connect(world, RegionName.carrington_institute, RegionName.farsight_xr_20)
    connect(world, RegionName.carrington_institute, RegionName.devastator)
    connect(world, RegionName.carrington_institute, RegionName.rocket_launcher)
    connect(world, RegionName.carrington_institute, RegionName.slayer)
    connect(world, RegionName.carrington_institute, RegionName.combat_knife)
    connect(world, RegionName.carrington_institute, RegionName.crossbow)
    connect(world, RegionName.carrington_institute, RegionName.tranquilizer)
    connect(world, RegionName.carrington_institute, RegionName.laser)
    connect(world, RegionName.carrington_institute, RegionName.grenade)
    connect(world, RegionName.carrington_institute, RegionName.timed_mine)
    connect(world, RegionName.carrington_institute, RegionName.proximity_mine)
    connect(world, RegionName.carrington_institute, RegionName.remote_mine)


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = PerfectDarkLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret


def add_event_to_region(multiworld: MultiWorld, player: int, region_name: str, event_name: str, event_item=None):
    region = multiworld.get_region(region_name, player)
    event = PerfectDarkLocation(player, event_name, None, region)
    if event_item:
        event.place_locked_item(PDItem(event_item, ItemClassification.progression, None, player))
    else:
        event.place_locked_item(PDItem(event_name, ItemClassification.progression, None, player))
    region.locations.append(event)


def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = PerfectDarkLocation(player, location_name, loc_id, region)
        region.locations.append(location)


def connect(world: "PerfectDarkWorld", source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
