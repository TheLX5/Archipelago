import typing

from BaseClasses import Item, ItemClassification
from .enums import Items
from .constants import *

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

class MMX2Item(Item):
    game = GAME_NAME

# Item tables
all_items = {
    Items.victory:                  ItemData(0xFF, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    Items.maverick_medal:           ItemData(0xFE, ItemClassification.progression_skip_balancing | ItemClassification.useful),

    Items.stage_wheel_gator:         ItemData(0x18, ItemClassification.progression | ItemClassification.useful),
    Items.stage_bubble_crab:         ItemData(0x16, ItemClassification.progression | ItemClassification.useful),
    Items.stage_flame_stag:          ItemData(0x13, ItemClassification.progression | ItemClassification.useful),
    Items.stage_morph_moth:          ItemData(0x11, ItemClassification.progression | ItemClassification.useful),
    Items.stage_magna_centipede:     ItemData(0x14, ItemClassification.progression | ItemClassification.useful),
    Items.stage_crystal_snail:       ItemData(0x19, ItemClassification.progression | ItemClassification.useful),
    Items.stage_overdrive_ostrich:   ItemData(0x15, ItemClassification.progression | ItemClassification.useful),
    Items.stage_wire_sponge:         ItemData(0x10, ItemClassification.progression | ItemClassification.useful),
    Items.stage_x_hunter:            ItemData(0x17, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    Items.stage_sigma:               ItemData(0x1A, ItemClassification.progression_skip_balancing | ItemClassification.useful),

    Items.spin_wheel:               ItemData(0x04, ItemClassification.progression),
    Items.bubble_splash:            ItemData(0x02, ItemClassification.progression),
    Items.speed_burner:             ItemData(0x08, ItemClassification.progression),
    Items.silk_shot:                ItemData(0x03, ItemClassification.progression),
    Items.magnet_mine:              ItemData(0x07, ItemClassification.progression),
    Items.crystal_hunter:           ItemData(0x01, ItemClassification.progression),
    Items.sonic_slicer:             ItemData(0x05, ItemClassification.progression),
    Items.strike_chain:             ItemData(0x06, ItemClassification.progression),
    
    Items.shoryuken:                ItemData(0x09, ItemClassification.useful),
    
    Items.heart_tank:               ItemData(0x0E, ItemClassification.progression_deprioritized),
    Items.sub_tank:                 ItemData(0x0F, ItemClassification.useful),
    
    Items.helmet:                   ItemData(0x0A, ItemClassification.progression),
    Items.body:                     ItemData(0x0B, ItemClassification.progression),
    Items.arms:                     ItemData(0x0C, ItemClassification.progression),
    Items.legs:                     ItemData(0x0D, ItemClassification.progression),

    Items.small_hp:                 ItemData(0x1C, ItemClassification.filler),
    Items.large_hp:                 ItemData(0x1D, ItemClassification.filler),

    Items.chip_quick_charge:        ItemData(0x20, ItemClassification.useful),
    Items.chip_speedster:           ItemData(0x21, ItemClassification.useful),
    Items.chip_super_recover:       ItemData(0x22, ItemClassification.useful),
    Items.chip_rapid_five:          ItemData(0x23, ItemClassification.useful),
    Items.chip_speed_shot:          ItemData(0x24, ItemClassification.useful),
    Items.chip_buster_plus:         ItemData(0x25, ItemClassification.useful),
    Items.chip_weapon_plus:         ItemData(0x26, ItemClassification.useful),
    Items.chip_d_converter:         ItemData(0x27, ItemClassification.useful),
    Items.chip_item_plus:           ItemData(0x28, ItemClassification.useful),
    Items.chip_spike_walker:        ItemData(0x29, ItemClassification.useful),
    Items.chip_d_barrier:           ItemData(0x2A, ItemClassification.useful),

    Items.glitched:                 ItemData(None, ItemClassification.progression_deprioritized_skip_balancing),
}

item_groups = {
    "Weapons": {
        Items.spin_wheel.value,
        Items.bubble_splash.value,
        Items.speed_burner.value,
        Items.silk_shot.value,
        Items.magnet_mine.value,
        Items.crystal_hunter.value,
        Items.sonic_slicer.value,
        Items.strike_chain.value,
    },
    "Armor Upgrades": {
        Items.helmet.value,
        Items.body.value,
        Items.arms.value,
        Items.legs.value,
    },
    "Chips": {
        Items.chip_quick_charge.value,
        Items.chip_speedster.value,
        Items.chip_super_recover.value,
        Items.chip_rapid_five.value,
        Items.chip_speed_shot.value,
        Items.chip_buster_plus.value,
        Items.chip_weapon_plus.value,
        Items.chip_d_converter.value,
        Items.chip_item_plus.value,
        Items.chip_spike_walker.value,
        Items.chip_d_barrier.value,
    },
    "Access Codes": {
        Items.stage_wheel_gator.value,
        Items.stage_bubble_crab.value,
        Items.stage_flame_stag.value,
        Items.stage_morph_moth.value,
        Items.stage_magna_centipede.value,
        Items.stage_crystal_snail.value,
        Items.stage_overdrive_ostrich.value,
        Items.stage_wire_sponge.value,
        #Items.stage_x_hunter_1.value,
        #Items.stage_x_hunter_2.value,
        #Items.stage_x_hunter_3.value,
        #Items.stage_x_hunter_4.value,
        Items.stage_x_hunter.value,
    },
    "Stages": {
        Items.stage_wheel_gator.value,
        Items.stage_bubble_crab.value,
        Items.stage_flame_stag.value,
        Items.stage_morph_moth.value,
        Items.stage_magna_centipede.value,
        Items.stage_crystal_snail.value,
        Items.stage_overdrive_ostrich.value,
        Items.stage_wire_sponge.value,
        #Items.stage_x_hunter_1.value,
        #Items.stage_x_hunter_2.value,
        #Items.stage_x_hunter_3.value,
        #Items.stage_x_hunter_4.value,
        Items.stage_x_hunter.value,
    }
}
