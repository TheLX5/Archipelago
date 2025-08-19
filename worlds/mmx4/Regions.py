from BaseClasses import Region
from .Types import MMX4Location
from .Locations import location_table, is_valid_location
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMX4World

def create_regions(world: "MMX4World"):
    # Intro
    menu = create_region(world, "Menu")
    intro_stage = create_region_and_connect(world, "Intro Stage", "Menu -> Intro Stage", menu)
    stage_select = create_region_and_connect(world, "Stage Select", "Intro Stage -> Stage Select", intro_stage)
    # Main Stages
    web_spider = create_region_and_connect(world, "Web Spider", "Stage Select -> Web Spider", stage_select)
    cyber_peacock = create_region_and_connect(world, "Cyber Peacock", "Stage Select -> Cyber Peacock", stage_select)
    storm_owl = create_region_and_connect(world, "Storm Owl", "Stage Select -> Storm Owl", stage_select)
    magma_dragoon = create_region_and_connect(world, "Magma Dragoon", "Stage Select -> Magma Dragoon", stage_select)
    jet_stingray = create_region_and_connect(world, "Jet Stingray", "Stage Select -> Jet Stingray", stage_select)
    split_mushroom = create_region_and_connect(world, "Split Mushroom", "Stage Select -> Split Mushroom", stage_select)
    slash_beast = create_region_and_connect(world, "Slash Beast", "Stage Select -> Slash Beast", stage_select)
    frost_walrus = create_region_and_connect(world, "Frost Walrus", "Stage Select -> Frost Walrus", stage_select)
    # Special / End Stages
    memorial_hall = create_region_and_connect(world, "Memorial Hall", "Stage Select -> Memorial Hall", stage_select)
    space_port = create_region_and_connect(world, "Space Port", "Stage Select -> Space Port", stage_select)
    final_weapon_1 = create_region_and_connect(world, "Final Weapon 1", "Space Port -> Final Weapon 1", space_port)
    final_weapon_2 = create_region_and_connect(world, "Final Weapon 2", "Final Weapon 1 -> Final Weapon 2", final_weapon_1)

def create_region(world: "MMX4World", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for key, data in location_table.items():
        if data.region == name:
            if not is_valid_location(world, key):
                continue
            location = MMX4Location(world.player, key, data.ap_code, reg)
            reg.locations.append(location)
    
    world.multiworld.regions.append(reg)
    return reg

def create_region_and_connect(world: "MMX4World",
                               name: str, entrancename: str, connected_region: Region) -> Region:
    reg: Region = create_region(world, name)
    connected_region.connect(reg, entrancename)
    return reg