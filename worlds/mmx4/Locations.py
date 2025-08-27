from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData
from .Names import LocationName, RegionName

if TYPE_CHECKING:
    from . import MMX4World

mmx4_locations = {
    # Intro
    LocationName.intro_boss_defeated: LocData(14574100, RegionName.intro_stage),
    LocationName.intro_clear: LocData(14574101, RegionName.intro_stage),
    # Web Spider
    LocationName.web_spider_capsule: LocData(14574102, RegionName.web_spider),
    LocationName.web_spider_heart_tank: LocData(14574103, RegionName.web_spider),
    LocationName.web_spider_defeated: LocData(14574104, RegionName.web_spider),
    LocationName.web_spider_weapon: LocData(14574105, RegionName.web_spider),
    # Cyber Peacock
    LocationName.cyber_peacock_heart_tank: LocData(14574106, RegionName.cyber_peacock),
    LocationName.cyber_peacock_sub_tank: LocData(14574107, RegionName.cyber_peacock),
    LocationName.cyber_peacock_capsule: LocData(14574108, RegionName.cyber_peacock),
    LocationName.cyber_peacock_defeated: LocData(14574109, RegionName.cyber_peacock),
    LocationName.cyber_peacock_weapon: LocData(14574110, RegionName.cyber_peacock),
    # Storm Owl
    LocationName.storm_owl_heart_tank: LocData(14574111, RegionName.storm_owl),
    LocationName.storm_owl_capsule_1: LocData(14574112, RegionName.storm_owl),
    LocationName.storm_owl_capsule_2: LocData(14574113, RegionName.storm_owl),
    LocationName.storm_owl_defeated: LocData(14574114, RegionName.storm_owl),
    LocationName.storm_owl_weapon: LocData(14574115, RegionName.storm_owl),
    # Magma Dragoon
    LocationName.magma_dragoon_heart_tank: LocData(14574116, RegionName.magma_dragoon),
    LocationName.magma_dragoon_capsule: LocData(14574117, RegionName.magma_dragoon),
    LocationName.magma_dragoon_defeated: LocData(14574118, RegionName.magma_dragoon),
    LocationName.magma_dragoon_weapon: LocData(14574119, RegionName.magma_dragoon),
    # Jet Stingray
    LocationName.jet_stingray_heart_tank: LocData(14574120, RegionName.jet_stingray),
    LocationName.jet_stingray_sub_tank: LocData(14574121, RegionName.jet_stingray),
    LocationName.jet_stingray_defeated: LocData(14574122, RegionName.jet_stingray),
    LocationName.jet_stingray_weapon: LocData(14574123, RegionName.jet_stingray),
    # Split Mushroom
    LocationName.split_mushroom_heart_tank: LocData(14574124, RegionName.split_mushroom),
    LocationName.split_mushroom_defeated: LocData(14574125, RegionName.split_mushroom),
    LocationName.split_mushroom_weapon: LocData(14574126, RegionName.split_mushroom),
    # Slash Beast
    LocationName.slash_beast_heart_tank: LocData(14574127, RegionName.slash_beast),
    LocationName.slash_beast_defeated: LocData(14574128, RegionName.slash_beast),
    LocationName.slash_beast_weapon: LocData(14574129, RegionName.slash_beast),
    # Frost Walrus
    LocationName.frost_walrus_heart_tank: LocData(14574130, RegionName.frost_walrus),
    LocationName.frost_walrus_extra_lives_tank: LocData(14574131, RegionName.frost_walrus),
    LocationName.frost_walrus_weapon_tank: LocData(14574132, RegionName.frost_walrus),
    LocationName.frost_walrus_defeated: LocData(14574133, RegionName.frost_walrus),
    LocationName.frost_walrus_weapon: LocData(14574134, RegionName.frost_walrus),
    # Special / End Stages
    LocationName.colonel_memorial_hall_defeated: LocData(14574135, RegionName.memorial_hall),
    LocationName.colonel_space_port_defeated: LocData(14574136, RegionName.space_port),
    LocationName.double_iris_defeated: LocData(14574137, RegionName.final_weapon_1),
    LocationName.general_defeated: LocData(14574138, RegionName.final_weapon_1),
    LocationName.rematch_web_spider: LocData(14574139, RegionName.final_weapon_2),
    LocationName.rematch_cyber_peacock: LocData(14574140, RegionName.final_weapon_2),
    LocationName.rematch_storm_owl: LocData(14574141, RegionName.final_weapon_2),
    LocationName.rematch_magma_dragoon: LocData(14574142, RegionName.final_weapon_2),
    LocationName.rematch_jet_stingray: LocData(14574143, RegionName.final_weapon_2),
    LocationName.rematch_split_mushroom: LocData(14574144, RegionName.final_weapon_2),
    LocationName.rematch_slash_beast: LocData(14574145, RegionName.final_weapon_2),
    LocationName.rematch_frost_walrus: LocData(14574146, RegionName.final_weapon_2),
}

pickup_locations = {
    LocationName.intro_hp_1: LocData(14574200, RegionName.intro_stage),
    LocationName.intro_hp_2: LocData(14574201, RegionName.intro_stage),
    LocationName.intro_1up: LocData(14574202, RegionName.intro_stage),
    LocationName.web_spider_hp_1: LocData(14574203, RegionName.web_spider),
    LocationName.web_spider_hp_2: LocData(14574204, RegionName.web_spider),
    LocationName.storm_owl_hp_1: LocData(14574205, RegionName.storm_owl),
    LocationName.storm_owl_hp_2: LocData(14574206, RegionName.storm_owl),
    LocationName.magma_dragoon_hp_1: LocData(14574207, RegionName.magma_dragoon),
    LocationName.magma_dragoon_hp_2: LocData(14574208, RegionName.magma_dragoon),
    LocationName.magma_dragoon_hp_3: LocData(14574209, RegionName.magma_dragoon),
    LocationName.jet_stingray_hp_1: LocData(14574210, RegionName.jet_stingray),
    LocationName.split_mushroom_hp_1: LocData(14574211, RegionName.split_mushroom),
    LocationName.split_mushroom_wpn_1: LocData(14574212, RegionName.split_mushroom),
    LocationName.slash_beast_hp_1: LocData(14574213, RegionName.slash_beast),
    LocationName.frost_walrus_wpn_1: LocData(14574214, RegionName.frost_walrus),
    LocationName.frost_walrus_wpn_2: LocData(14574215, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_1: LocData(14574216, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_2: LocData(14574217, RegionName.frost_walrus),
    LocationName.frost_walrus_1up_1: LocData(14574218, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_3: LocData(14574219, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_4: LocData(14574220, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_5: LocData(14574221, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_6: LocData(14574222, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_7: LocData(14574223, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_8: LocData(14574224, RegionName.frost_walrus),
    LocationName.frost_walrus_1up_2: LocData(14574225, RegionName.frost_walrus),
    LocationName.frost_walrus_hp_9: LocData(14574226, RegionName.frost_walrus),
    LocationName.frost_walrus_wpn_3: LocData(14574227, RegionName.frost_walrus),
    LocationName.final_weapon_hp_1: LocData(14574228, RegionName.final_weapon_1),
    LocationName.final_weapon_hp_2: LocData(14574229, RegionName.final_weapon_1),
    LocationName.final_weapon_hp_3: LocData(14574230, RegionName.final_weapon_1),
    LocationName.final_weapon_hp_4: LocData(14574231, RegionName.final_weapon_2),
    LocationName.final_weapon_hp_5: LocData(14574232, RegionName.final_weapon_2),
    LocationName.final_weapon_hp_6: LocData(14574233, RegionName.final_weapon_2),
    LocationName.final_weapon_wpn_1: LocData(14574234, RegionName.final_weapon_2),
    LocationName.final_weapon_hp_7: LocData(14574235, RegionName.final_weapon_2),
    LocationName.final_weapon_wpn_2: LocData(14574236, RegionName.final_weapon_2),
    LocationName.final_weapon_hp_8: LocData(14574237, RegionName.final_weapon_2),
}

event_locations = {
    LocationName.final_weapon_clear: LocData(14574300, RegionName.final_weapon_2),
}

all_locations = {
    **mmx4_locations,
    **pickup_locations,
    **event_locations,
}

def setup_locations(world: "MMX4World"):
    location_table = {
        **mmx4_locations,
        **event_locations,
    }

    if world.options.pickupsanity:
        location_table.update(pickup_locations)

    return location_table

lookup_id_to_name: Dict[int, str] = {loc_data.ap_code: name for name, loc_data in all_locations.items()}
