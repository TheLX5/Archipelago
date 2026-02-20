from typing import Dict, Set, Tuple, NamedTuple, Optional
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    category: str
    code: Optional[int]
    classification: ItemClassification
    amount: Optional[int] = 1

item_table: Dict[str, ItemData] = {
    "! Switch": ItemData("Items", 0x302050, ItemClassification.progression),
    "Dashed Platform": ItemData("Items", 0x302051, ItemClassification.progression | ItemClassification.useful),
    "Dashed Stairs": ItemData("Items", 0x302052, ItemClassification.progression | ItemClassification.useful),
    "Beanstalk": ItemData("Items", 0x302053, ItemClassification.progression_deprioritized),
    "Helicopter Morph": ItemData("Morphs", 0x302054, ItemClassification.progression | ItemClassification.useful),
    "Spring Ball": ItemData("Items", 0x302055, ItemClassification.progression),
    "Large Spring Ball": ItemData("Items", 0x302056, ItemClassification.progression | ItemClassification.useful),
    "Arrow Wheel": ItemData("Items", 0x302057, ItemClassification.progression),
    "Vanishing Arrow Wheel": ItemData("Items", 0x302058, ItemClassification.progression),
    "Mole Tank Morph": ItemData("Morphs", 0x302059, ItemClassification.progression),
    "Watermelon": ItemData("Items", 0x30205A, ItemClassification.progression_deprioritized),
    "Ice Melon": ItemData("Items", 0x30205B, ItemClassification.progression_deprioritized),
    "Fire Melon": ItemData("Items", 0x30205C, ItemClassification.progression_deprioritized),
    "Super Star": ItemData("Items", 0x30205D, ItemClassification.progression),
    "Car Morph": ItemData("Morphs", 0x30205E, ItemClassification.progression),
    "Flashing Eggs": ItemData("Items", 0x30205F, ItemClassification.progression),
    "Giant Eggs": ItemData("Items", 0x302060, ItemClassification.progression),
    "Egg Launcher": ItemData("Items", 0x302061, ItemClassification.progression),
    "Egg Plant": ItemData("Items", 0x302062, ItemClassification.progression | ItemClassification.useful),
    "Submarine Morph": ItemData("Morphs", 0x302063, ItemClassification.progression),
    "Chomp Rock": ItemData("Items", 0x302064, ItemClassification.progression_deprioritized),
    "Poochy": ItemData("Items", 0x302065, ItemClassification.progression),
    "Platform Ghost": ItemData("Items", 0x302066, ItemClassification.progression),
    "Skis": ItemData("Items", 0x302067, ItemClassification.progression_deprioritized),
    "Train Morph": ItemData("Morphs", 0x302068, ItemClassification.progression),
    "Key": ItemData("Items", 0x302069, ItemClassification.progression | ItemClassification.useful),
    "Middle Ring": ItemData("Items", 0x30206A, ItemClassification.progression | ItemClassification.useful),
    "Bucket": ItemData("Items", 0x30206B, ItemClassification.progression_deprioritized),
    "Tulip": ItemData("Items", 0x30206C, ItemClassification.progression),
    "Egg Capacity Upgrade": ItemData("Items", 0x30206D, ItemClassification.progression | ItemClassification.useful, 5),
    "Secret Lens": ItemData("Items", 0x302081, ItemClassification.progression_deprioritized),

    "World 1 Gate": ItemData("Gates", 0x30206E, ItemClassification.progression | ItemClassification.useful),
    "World 2 Gate": ItemData("Gates", 0x30206F, ItemClassification.progression | ItemClassification.useful),
    "World 3 Gate": ItemData("Gates", 0x302070, ItemClassification.progression | ItemClassification.useful),
    "World 4 Gate": ItemData("Gates", 0x302071, ItemClassification.progression | ItemClassification.useful),
    "World 5 Gate": ItemData("Gates", 0x302072, ItemClassification.progression | ItemClassification.useful),
    "World 6 Gate": ItemData("Gates", 0x302073, ItemClassification.progression | ItemClassification.useful),

    "Extra 1": ItemData("Panels", 0x302074, ItemClassification.progression | ItemClassification.useful),
    "Extra 2": ItemData("Panels", 0x302075, ItemClassification.progression | ItemClassification.useful),
    "Extra 3": ItemData("Panels", 0x302076, ItemClassification.progression | ItemClassification.useful),
    "Extra 4": ItemData("Panels", 0x302077, ItemClassification.progression | ItemClassification.useful),
    "Extra 5": ItemData("Panels", 0x302078, ItemClassification.progression | ItemClassification.useful),
    "Extra 6": ItemData("Panels", 0x302079, ItemClassification.progression | ItemClassification.useful),
    "Extra Panels": ItemData("Panels", 0x30207A, ItemClassification.progression | ItemClassification.useful),

    "Bonus 1": ItemData("Panels", 0x30207B, ItemClassification.progression | ItemClassification.useful),
    "Bonus 2": ItemData("Panels", 0x30207C, ItemClassification.progression | ItemClassification.useful),
    "Bonus 3": ItemData("Panels", 0x30207D, ItemClassification.progression | ItemClassification.useful),
    "Bonus 4": ItemData("Panels", 0x30207E, ItemClassification.progression | ItemClassification.useful),
    "Bonus 5": ItemData("Panels", 0x30207F, ItemClassification.progression | ItemClassification.useful),
    "Bonus 6": ItemData("Panels", 0x302080, ItemClassification.progression | ItemClassification.useful),
    "Bonus Panels": ItemData("Panels", 0x302082, ItemClassification.progression | ItemClassification.useful),

    "Anytime Egg": ItemData("Consumable", 0x302083, ItemClassification.useful, 0),
    "Anywhere Pow": ItemData("Consumable", 0x302084, ItemClassification.filler, 0),
    "Winged Cloud Maker": ItemData("Consumable", 0x302085, ItemClassification.filler, 0),
    "Pocket Melon": ItemData("Consumable", 0x302086, ItemClassification.filler, 0),
    "Pocket Fire Melon": ItemData("Consumable", 0x302087, ItemClassification.filler, 0),
    "Pocket Ice Melon": ItemData("Consumable", 0x302088, ItemClassification.filler, 0),
    "Magnifying Glass": ItemData("Consumable", 0x302089, ItemClassification.filler, 0),
    "+10 Stars": ItemData("Consumable", 0x30208A, ItemClassification.useful, 0),
    "+20 Stars": ItemData("Consumable", 0x30208B, ItemClassification.useful, 0),
    "1-Up": ItemData("Lives", 0x30208C, ItemClassification.filler, 0),
    "2-Up": ItemData("Lives", 0x30208D, ItemClassification.filler, 0),
    "3-Up": ItemData("Lives", 0x30208E, ItemClassification.filler, 0),
    "10-Up": ItemData("Lives", 0x30208F, ItemClassification.useful, 5),
    "Bonus Consumables": ItemData("Events", None, ItemClassification.progression, 0),
    "Bandit Consumables": ItemData("Events", None, ItemClassification.progression, 0),
    "Bandit Watermelons": ItemData("Events", None, ItemClassification.progression, 0),

    "Fuzzy Trap": ItemData("Traps", 0x302090, ItemClassification.trap, 0),
    "Reversal Trap": ItemData("Traps", 0x302091, ItemClassification.trap, 0),
    "Darkness Trap": ItemData("Traps", 0x302092, ItemClassification.trap, 0),
    "Freeze Trap": ItemData("Traps", 0x302093, ItemClassification.trap, 0),

    "Boss Clear": ItemData("Events", None, ItemClassification.progression, 0),
    "Piece of Luigi": ItemData("Items", 0x302095, ItemClassification.progression_deprioritized | ItemClassification.useful, 0),
    "Saved Baby Luigi": ItemData("Events", None, ItemClassification.progression, 0),
    "glitched": ItemData("Events", None, ItemClassification.progression, 0),
}

filler_items: Tuple[str, ...] = (
    "Anytime Egg",
    "Anywhere Pow",
    "Winged Cloud Maker",
    "Pocket Melon",
    "Pocket Fire Melon",
    "Pocket Ice Melon",
    "Magnifying Glass",
    "+10 Stars",
    "+20 Stars",
    "1-Up",
    "2-Up",
    "3-Up"
)

trap_items: Tuple[str, ...] = (
    "Fuzzy Trap",
    "Reversal Trap",
    "Darkness Trap",
    "Freeze Trap"
)

trap_value_to_name: Dict[int, str] = {
    0x302090: "Fuzzy Trap",
    0x302091: "Reversal Trap",
    0x302092: "Darkness Trap",
    0x302093: "Freeze Trap",
}

trap_name_to_value: Dict[str, int] = {
    # Our native Traps
    "Fuzzy Trap":           0x302090,
    "Reversal Trap":        0x302091,
    "Darkness Trap":        0x302092,
    "Freeze Trap":          0x302093,

    # Common other trap names
    "Confuse Trap":         0x302090, # Fuzzy Trap
    "Gravity Trap":         0x302090, # Fuzzy Trap
    "Confound Trap":        0x302090, # Fuzzy Trap
    "Confusion Trap":       0x302090, # Fuzzy Trap
    "Chaos Control Trap":   0x302091, # Reversal Trap
    "Reverse Trap":         0x302091, # Reversal Trap
    "Stun Trap":            0x302093, # Freeze Trap
    "Frozen Trap":          0x302093, # Freeze Trap
    "Honey Trap":           0x302093, # Freeze Trap
    "Eject Ability":        0x302092, # Darkness Trap
    "Gooey Bag":            0x302092, # Darkness Trap
}

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories
