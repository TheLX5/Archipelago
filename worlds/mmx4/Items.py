import logging

from BaseClasses import Item, ItemClassification

from .Types import ItemData, MMX4Item
from .Locations import get_total_locations
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMX4World

def create_itempool(world: "MMX4World") -> List[Item]:
    itempool: List[Item] = []
    
    stage_selected = world.random.randint(0, 7)
    i = 0
    for name, data in stage_access_items.items():
        if i == stage_selected:
            world.multiworld.get_location("Intro Stage Completed", world.player).place_locked_item(create_item(world, name))
        else:
            itempool += [create_item(world, name)]
        i = i + 1

    for name, data in mmx4_items.items():
        for i in range(data.count):
            itempool += [create_item(world, name)]

    victory = create_item(world, "Victory")
    world.multiworld.get_location("Sigma Defeated", world.player).place_locked_item(victory)

    itempool += create_junk_items(world, get_total_locations(world) - len(itempool) - 2)

    return itempool

def create_item(world: "MMX4World", name: str) -> Item:
    data = item_table[name]
    return MMX4Item(name, data.classification, data.ap_code, world.player)

def create_multiple_items(world: "MMX4World", name: str, count: int,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [MMX4Item(name, item_type, data.ap_code, world.player)]

    return itemlist

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
    "Lightning Web": ItemData(14575100, ItemClassification.progression),
    "Aiming Laser": ItemData(14575101, ItemClassification.progression),
    "Double Cyclone": ItemData(14575102, ItemClassification.progression),
    "Rising Fire": ItemData(14575103, ItemClassification.progression),
    "Ground Hunter": ItemData(14575104, ItemClassification.progression),
    "Soul Body": ItemData(14575105, ItemClassification.progression),
    "Twin Slasher": ItemData(14575106, ItemClassification.progression),
    "Frost Tower": ItemData(14575107, ItemClassification.progression),
    # Armor Upgrades
    "Helmet Upgrade": ItemData(14575108, ItemClassification.progression),
    "Body Upgrade": ItemData(14575109, ItemClassification.progression),
    "Plasma Shot Upgrade": ItemData(14575110, ItemClassification.progression),
    "Stock Charge Upgrade": ItemData(14575111, ItemClassification.progression),
    "Legs Upgrade": ItemData(14575112, ItemClassification.progression),
    # Tanks
    "Heart Tank": ItemData(14575113, ItemClassification.progression, 8),
    "Sub Tank": ItemData(14575114, ItemClassification.progression, 2),
    "Weapon Energy Tank": ItemData(14575115, ItemClassification.progression, 1),
    "Extra Lives Tank": ItemData(14575116, ItemClassification.progression, 1),
}

stage_access_items = {
    "Web Spider Stage Access": ItemData(14575200, ItemClassification.progression | ItemClassification.useful),
    "Cyber Peacock Stage Access": ItemData(14575201, ItemClassification.progression | ItemClassification.useful),
    "Storm Owl Stage Access": ItemData(14575202, ItemClassification.progression | ItemClassification.useful),
    "Magma Dragoon Stage Access": ItemData(14575203, ItemClassification.progression | ItemClassification.useful),
    "Jet Stingray Stage Access": ItemData(14575204, ItemClassification.progression | ItemClassification.useful),
    "Split Mushroom Stage Access": ItemData(14575205, ItemClassification.progression | ItemClassification.useful),
    "Slash Beast Stage Access": ItemData(14575206, ItemClassification.progression | ItemClassification.useful),
    "Frost Walrus Stage Access": ItemData(14575207, ItemClassification.progression | ItemClassification.useful),
}

junk_items = {
    "Small Energy": ItemData(14575300, ItemClassification.filler),
    "Large Energy": ItemData(14575301, ItemClassification.filler),
    "Small Weapon Energy": ItemData(14575302, ItemClassification.filler),
    "Large Weapon Energy": ItemData(14575303, ItemClassification.filler),
    "Extra Life": ItemData(14575304, ItemClassification.filler),
}

event_items = {
    "Victory": ItemData(14575400, ItemClassification.progression),
}

item_table = {
    **mmx4_items,
    **stage_access_items,
    **junk_items,
    **event_items,
}