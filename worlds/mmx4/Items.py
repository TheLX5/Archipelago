import logging

from BaseClasses import Item, ItemClassification

from .Types import ItemData, MMX4Item
from .Names import ItemName, LocationName
from typing import List, Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from . import MMX4World

def create_itempool(world: "MMX4World") -> List[Item]:
    itempool: List[Item] = []
    
    stage_selected = world.random.randint(0, 7)
    i = 0
    for name, data in stage_access_items.items():
        if i == stage_selected:
            world.multiworld.get_location(LocationName.intro_clear, world.player).place_locked_item(create_item(world, name))
        else:
            itempool += [create_item(world, name)]
        i = i + 1

    for name, data in mmx4_items.items():
        for i in range(data.count):
            itempool += [create_item(world, name)]

    victory = create_item(world, ItemName.victory)
    world.multiworld.get_location(LocationName.final_weapon_clear, world.player).place_locked_item(victory)

    itempool += create_junk_items(world, len(world.location_table.keys()) - len(itempool) - 2)

    return itempool

def create_item(world: "MMX4World", name: str) -> Item:
    data = item_table[name]
    return MMX4Item(name, data.classification, data.ap_code, world.player)


def create_junk_items(world: "MMX4World", count: int) -> List[Item]:
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    trap_list: Dict[str, int] = {}

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = 1

    for i in range(count):
        junk_pool.append(world.create_item(
            world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))

    return junk_pool

mmx4_items = {
    # Maverick Weapons
    ItemName.lightning_web:         ItemData(14575100, ItemClassification.progression),
    ItemName.aiming_laser:          ItemData(14575101, ItemClassification.progression),
    ItemName.double_cyclone:        ItemData(14575102, ItemClassification.progression),
    ItemName.rising_fire:           ItemData(14575103, ItemClassification.progression),
    ItemName.ground_hunter:         ItemData(14575104, ItemClassification.progression),
    ItemName.soul_body:             ItemData(14575105, ItemClassification.progression),
    ItemName.twin_slasher:          ItemData(14575106, ItemClassification.progression),
    ItemName.frost_tower:           ItemData(14575107, ItemClassification.progression),

    # Armor Upgrades
    ItemName.helmet:                ItemData(14575108, ItemClassification.useful),
    ItemName.body:                  ItemData(14575109, ItemClassification.useful),
    ItemName.arms_plasma:           ItemData(14575110, ItemClassification.progression),
    ItemName.arms_stock:            ItemData(14575111, ItemClassification.progression),
    ItemName.legs:                  ItemData(14575112, ItemClassification.progression),
    # Tanks
    ItemName.heart_tank:            ItemData(14575113, ItemClassification.useful, 8),
    ItemName.sub_tank:              ItemData(14575114, ItemClassification.useful, 2),
    ItemName.weapon_energy_tank:    ItemData(14575115, ItemClassification.useful, 1),
    ItemName.extra_lives_tank:      ItemData(14575116, ItemClassification.useful, 1),
}

stage_access_items = {
    ItemName.web_spider:            ItemData(14575200, ItemClassification.progression | ItemClassification.useful),
    ItemName.cyber_peacock:         ItemData(14575201, ItemClassification.progression | ItemClassification.useful),
    ItemName.storm_owl:             ItemData(14575202, ItemClassification.progression | ItemClassification.useful),
    ItemName.magma_dragoon:         ItemData(14575203, ItemClassification.progression | ItemClassification.useful),
    ItemName.jet_stingray:          ItemData(14575204, ItemClassification.progression | ItemClassification.useful),
    ItemName.split_mushroom:        ItemData(14575205, ItemClassification.progression | ItemClassification.useful),
    ItemName.slash_beast:           ItemData(14575206, ItemClassification.progression | ItemClassification.useful),
    ItemName.frost_walrus:          ItemData(14575207, ItemClassification.progression | ItemClassification.useful),
}

junk_items = {
    ItemName.small_hp:              ItemData(14575300, ItemClassification.filler),
    ItemName.large_hp:              ItemData(14575301, ItemClassification.filler),
    ItemName.small_weapon:          ItemData(14575302, ItemClassification.filler),
    ItemName.large_weapon:          ItemData(14575303, ItemClassification.filler),
    ItemName.extra_life:            ItemData(14575304, ItemClassification.filler),
}

event_items = {
    ItemName.victory:               ItemData(14575400, ItemClassification.progression_skip_balancing),
}

item_table = {
    **mmx4_items,
    **stage_access_items,
    **junk_items,
    **event_items,
}