from BaseClasses import Region, MultiWorld
from .Types import MMX4Location, LocData
from .Locations import mmx4_locations
from .Names import RegionName
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from . import MMX4World

def create_regions(world: "MMX4World"):
    multiworld = world.multiworld
    player = world.player

    menu = Region("Menu", player, multiworld)
    intro_stage = Region(RegionName.intro_stage, player, multiworld)
    stage_select = Region(RegionName.stage_select, player, multiworld)
    web_spider = Region(RegionName.web_spider, player, multiworld)
    cyber_peacock = Region(RegionName.cyber_peacock, player, multiworld)
    storm_owl = Region(RegionName.storm_owl, player, multiworld)
    magma_dragoon = Region(RegionName.magma_dragoon, player, multiworld)
    jet_stingray = Region(RegionName.jet_stingray, player, multiworld)
    split_mushroom = Region(RegionName.split_mushroom, player, multiworld)
    slash_beast = Region(RegionName.slash_beast, player, multiworld)
    frost_walrus = Region(RegionName.frost_walrus, player, multiworld)
    memorial_hall = Region(RegionName.memorial_hall, player, multiworld)
    space_port = Region(RegionName.space_port, player, multiworld)
    final_weapon_1 = Region(RegionName.final_weapon_1, player, multiworld)
    final_weapon_2 = Region(RegionName.final_weapon_2, player, multiworld)

    multiworld.regions += [
        menu,
        intro_stage,
        stage_select,
        web_spider,
        cyber_peacock,
        storm_owl,
        magma_dragoon,
        jet_stingray,
        split_mushroom,
        slash_beast,
        frost_walrus,
        memorial_hall,
        space_port,
        final_weapon_1,
        final_weapon_2,
    ]

    for loc_name, loc_data in world.location_table.items():
        add_location_to_region(multiworld, player, loc_data, loc_name)


def add_location_to_region(multiworld: MultiWorld, player: int, location_data: LocData, location_name: str):
    region = multiworld.get_region(location_data.region, player)
    location = MMX4Location(player, location_name, location_data.ap_code, region)
    region.locations.append(location)


def connect_regions(world: "MMX4World"):
    connect(world, "Menu", RegionName.intro_stage)
    connect(world, RegionName.intro_stage, RegionName.stage_select)

    connect(world, RegionName.stage_select, RegionName.web_spider)
    connect(world, RegionName.stage_select, RegionName.cyber_peacock)
    connect(world, RegionName.stage_select, RegionName.storm_owl)
    connect(world, RegionName.stage_select, RegionName.magma_dragoon)
    connect(world, RegionName.stage_select, RegionName.jet_stingray)
    connect(world, RegionName.stage_select, RegionName.split_mushroom)
    connect(world, RegionName.stage_select, RegionName.slash_beast)
    connect(world, RegionName.stage_select, RegionName.frost_walrus)

    connect(world, RegionName.stage_select, RegionName.memorial_hall)
    connect(world, RegionName.stage_select, RegionName.space_port)
    connect(world, RegionName.space_port, RegionName.final_weapon_1)
    connect(world, RegionName.final_weapon_1, RegionName.final_weapon_2)


def connect(world: "MMX4World", source: str, target: str):
    source_region: Region = world.multiworld.get_region(source, world.player)
    target_region: Region = world.multiworld.get_region(target, world.player)
    source_region.connect(target_region)
