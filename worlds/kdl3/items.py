
from BaseClasses import Item, ItemClassification
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    type: ItemClassification = ItemClassification.filler



class KDL3Item(Item):
    game = "Kirby's Dream Land 3"


copy_ability_table = {
    "Burning": ItemData(0x770001, ItemClassification.progression),
    "Stone": ItemData(0x770002, ItemClassification.progression),
    "Ice": ItemData(0x770003, ItemClassification.progression),
    "Needle": ItemData(0x770004, ItemClassification.progression),
    "Clean": ItemData(0x770005, ItemClassification.progression),
    "Parasol": ItemData(0x770006, ItemClassification.progression),
    "Spark": ItemData(0x770007, ItemClassification.progression),
    "Cutter": ItemData(0x770008, ItemClassification.progression),
}

animal_friend_table = {
    "Rick": ItemData(0x770010, ItemClassification.progression),
    "Kine": ItemData(0x770011, ItemClassification.progression),
    "Coo": ItemData(0x770012, ItemClassification.progression),
    "Nago": ItemData(0x770013, ItemClassification.progression),
    "ChuChu": ItemData(0x770014, ItemClassification.progression),
    "Pitch": ItemData(0x770015, ItemClassification.progression),
}

animal_friend_spawn_table = {
    "Rick Spawn": ItemData(None, ItemClassification.progression),
    "Kine Spawn": ItemData(None, ItemClassification.progression),
    "Coo Spawn": ItemData(None, ItemClassification.progression),
    "Nago Spawn": ItemData(None, ItemClassification.progression),
    "ChuChu Spawn": ItemData(None, ItemClassification.progression),
    "Pitch Spawn": ItemData(None, ItemClassification.progression),
}

copy_ability_access_table = {
    "No Ability": ItemData(None, ItemClassification.filler),
    "Burning Ability": ItemData(None, ItemClassification.progression),
    "Stone Ability": ItemData(None, ItemClassification.progression),
    "Ice Ability": ItemData(None, ItemClassification.progression),
    "Needle Ability": ItemData(None, ItemClassification.progression),
    "Clean Ability": ItemData(None, ItemClassification.progression),
    "Parasol Ability": ItemData(None, ItemClassification.progression),
    "Spark Ability": ItemData(None, ItemClassification.progression),
    "Cutter Ability": ItemData(None, ItemClassification.progression),
}

misc_item_table = {
    "Heart Star": ItemData(0x770020, ItemClassification.progression_deprioritized_skip_balancing | ItemClassification.useful),
    "1-Up": ItemData(0x770021, ItemClassification.filler),
    "Maxim Tomato": ItemData(0x770022, ItemClassification.filler),
    "Invincible Candy": ItemData(0x770023, ItemClassification.filler),
    "Little Star": ItemData(0x770024, ItemClassification.filler),
    "Medium Star": ItemData(0x770025, ItemClassification.filler),
    "Big Star": ItemData(0x770026, ItemClassification.filler),
}

trap_item_table = {
    "Gooey Bag": ItemData(0x770040, ItemClassification.trap),
    "Slowness": ItemData(0x770041, ItemClassification.trap),
    "Eject Ability": ItemData(0x770042, ItemClassification.trap),
}

filler_item_weights = {
    "1-Up": 4,
    "Maxim Tomato": 2,
    "Invincible Candy": 2
}

star_item_weights = {
    "Little Star": 16,
    "Medium Star": 8,
    "Big Star": 4
}

total_filler_weights = {
    **filler_item_weights,
    **star_item_weights
}


item_table = {
    **copy_ability_table,
    **copy_ability_access_table,
    **animal_friend_table,
    **animal_friend_spawn_table,
    **misc_item_table,
    **trap_item_table
}

item_names = {
    "Copy Ability": set(copy_ability_table),
    "Animal Friend": set(animal_friend_table),
}

lookup_item_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
