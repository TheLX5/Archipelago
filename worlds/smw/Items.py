import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    useful: bool = False
    quantity: int = 1
    event: bool = False


class SMWItem(Item):
    game: str = "Super Mario World"


# Separate tables for each type of item.
junk_table = {
    ItemName.one_coin:        ItemData(0xBC0017, False),
    ItemName.five_coins:      ItemData(0xBC0018, False),
    ItemName.ten_coins:       ItemData(0xBC0019, False),
    ItemName.fifty_coins:     ItemData(0xBC001A, False),
    ItemName.one_up_mushroom: ItemData(0xBC0001, False),
}

inventory_table = {
    ItemName.mushroom_inventory:        ItemData(0xBC0040, False, False, True),
    ItemName.fire_flower_inventory:     ItemData(0xBC0041, False, False, True),
    ItemName.feather_inventory:         ItemData(0xBC0042, False, False, True),
    ItemName.star_inventory:            ItemData(0xBC0043, False, False, True),
    ItemName.green_yoshi_inventory:     ItemData(0xBC0044, False, False, True),
    ItemName.red_yoshi_inventory:       ItemData(0xBC0045, False, False, True),
    ItemName.blue_yoshi_inventory:      ItemData(0xBC0046, False, False, True),
    ItemName.yellow_yoshi_inventory:    ItemData(0xBC0047, False, False, True),
}

collectable_table = {
    ItemName.yoshi_egg:       ItemData(0xBC0002, True),
}

upgrade_table = {
    ItemName.mario_run:           ItemData(0xBC0003, True),
    ItemName.mario_carry:         ItemData(0xBC0004, True),
    ItemName.mario_swim:          ItemData(0xBC0005, True),
    ItemName.mario_spin_jump:     ItemData(0xBC0006, True),
    ItemName.mario_climb:         ItemData(0xBC0007, True),
    ItemName.yoshi_activate:      ItemData(0xBC0008, True),
    ItemName.p_switch:            ItemData(0xBC0009, True),
    ItemName.progressive_powerup: ItemData(0xBC000A, True),
    ItemName.p_balloon:           ItemData(0xBC000B, True),
    ItemName.super_star_active:   ItemData(0xBC000D, True),
    ItemName.special_world_clear: ItemData(0xBC001B, True),
    ItemName.extra_defense:       ItemData(0xBC0020, False, False, True),
}

switch_palace_table = {
    ItemName.yellow_switch_palace: ItemData(0xBC000E, True),
    ItemName.green_switch_palace:  ItemData(0xBC000F, True),
    ItemName.red_switch_palace:    ItemData(0xBC0010, True),
    ItemName.blue_switch_palace:   ItemData(0xBC0011, True),
}

trap_table = {
    ItemName.ice_trap:              ItemData(0xBC0080, False, True),
    ItemName.stun_trap:             ItemData(0xBC0081, False, True),
    ItemName.literature_trap:       ItemData(0xBC0082, False, True),
    ItemName.timer_trap:            ItemData(0xBC0083, False, True),
    ItemName.reverse_controls_trap: ItemData(0xBC0084, False, True),
    ItemName.thwimp_trap:           ItemData(0xBC0085, False, True),
    ItemName.fishin_trap:           ItemData(0xBC0086, False, True),
    ItemName.screen_flip_trap:      ItemData(0xBC0087, False, True),
    ItemName.sticky_floor_trap:     ItemData(0xBC0088, False, True),
    ItemName.sticky_hands_trap:     ItemData(0xBC0089, False, True),
    ItemName.pixelate_trap:         ItemData(0xBC008A, False, True),
    ItemName.spotlight_trap:        ItemData(0xBC008B, False, True),
}

event_table = {
    ItemName.victory:   ItemData(0xBC0000, True),
    ItemName.koopaling: ItemData(0xBC0012, True),
}

# Complete item table.
item_table = {
    **junk_table,
    **inventory_table,
    **collectable_table,
    **upgrade_table,
    **switch_palace_table,
    **trap_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

trap_value_to_name: typing.Dict[int, str] = {
    0xBC0080: ItemName.ice_trap,
    0xBC0081: ItemName.stun_trap,
    0xBC0082: ItemName.literature_trap,
    0xBC0083: ItemName.timer_trap,
    0xBC0084: ItemName.reverse_controls_trap,
    0xBC0085: ItemName.thwimp_trap,
    0xBC0086: ItemName.fishin_trap,
    0xBC0087: ItemName.screen_flip_trap,
    0xBC0088: ItemName.sticky_floor_trap,
    0xBC0089: ItemName.sticky_hands_trap,
    0xBC008A: ItemName.pixelate_trap,
    0xBC008B: ItemName.spotlight_trap,
}

trap_name_to_value: typing.Dict[str, int] = {
    # Our native Traps
    ItemName.ice_trap:              0xBC0080,
    ItemName.stun_trap:             0xBC0081,
    ItemName.literature_trap:       0xBC0082,
    ItemName.timer_trap:            0xBC0083,
    ItemName.reverse_controls_trap: 0xBC0084,
    ItemName.thwimp_trap:           0xBC0085,
    ItemName.fishin_trap:           0xBC0086,
    ItemName.screen_flip_trap:      0xBC0087,
    ItemName.sticky_floor_trap:     0xBC0088,
    ItemName.sticky_hands_trap:     0xBC0089,
    ItemName.pixelate_trap:         0xBC008A,
    ItemName.spotlight_trap:        0xBC008B,

    # Common other trap names
    "Chaos Control Trap": 0xBC0081,  # Stun Trap
    "Confuse Trap":       0xBC0084,  # Reverse Trap
    "Exposition Trap":    0xBC0082,  # Literature Trap
    "Cutscene Trap":      0xBC0082,  # Literature Trap
    "Freeze Trap":        0xBC0081,  # Stun Trap
    "Frozen Trap":        0xBC0081,  # Stun Trap
    "Paralyze Trap":      0xBC0081,  # Stun Trap
    "Reversal Trap":      0xBC0084,  # Reverse Trap
    "Fuzzy Trap":         0xBC0084,  # Reverse Trap
    "Confound Trap":      0xBC0084,  # Reverse Trap
    "Confusion Trap":     0xBC0084,  # Reverse Trap
    "Police Trap":        0xBC0085,  # Thwimp Trap
    "Buyon Trap":         0xBC0085,  # Thwimp Trap
    "Gooey Bag":          0xBC0085,  # Thwimp Trap
    "TNT Barrel Trap":    0xBC0085,  # Thwimp Trap
    "Honey Trap":         0xBC0088,  # Sticky Floor Trap
    "Slowness Trap":      0xBC0088,  # Sticky Floor Trap
    "Darkness Trap":      0xBC008B,  # Spotlight Trap
}
