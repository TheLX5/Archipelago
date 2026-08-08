import typing

from BaseClasses import Item, ItemClassification
from .enums import Items
from .constants import *
from .stage_data import level_data

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

class TengokuItem(Item):
    game = GAME_NAME

# Item tables
all_items = {
    Items.medal:                    ItemData(PAD | 0xC0, ItemClassification.progression_deprioritized_skip_balancing),

    Items.remix_1_column:           ItemData(PAD | 0x100, ItemClassification.progression | ItemClassification.useful),
    Items.remix_2_column:           ItemData(PAD | 0x101, ItemClassification.progression | ItemClassification.useful),
    Items.remix_3_column:           ItemData(PAD | 0x102, ItemClassification.progression | ItemClassification.useful),
    Items.remix_4_column:           ItemData(PAD | 0x103, ItemClassification.progression | ItemClassification.useful),
    Items.remix_5_column:           ItemData(PAD | 0x104, ItemClassification.progression | ItemClassification.useful),
    Items.remix_6_column:           ItemData(PAD | 0x105, ItemClassification.progression | ItemClassification.useful),
    Items.remix_7_column:           ItemData(PAD | 0x106, ItemClassification.progression | ItemClassification.useful),
    Items.remix_8_column:           ItemData(PAD | 0x107, ItemClassification.progression | ItemClassification.useful),

    Items.karate_man_stage:         ItemData(PAD | 0x00, ItemClassification.progression_deprioritized),
    Items.karate_man_2_stage:       ItemData(PAD | 0x01, ItemClassification.progression_deprioritized),
    Items.the_clappy_trio_stage:    ItemData(PAD | 0x02, ItemClassification.progression_deprioritized),
    Items.the_snappy_trio_stage:    ItemData(PAD | 0x03, ItemClassification.progression_deprioritized),
    Items.polyrhythm_stage:         ItemData(PAD | 0x04, ItemClassification.progression_deprioritized),
    Items.polyrhythm_2_stage:       ItemData(PAD | 0x05, ItemClassification.progression_deprioritized),
    Items.night_walk_stage:         ItemData(PAD | 0x06, ItemClassification.progression_deprioritized),
    Items.night_walk_2_stage:       ItemData(PAD | 0x07, ItemClassification.progression_deprioritized),
    Items.rhythm_tweezers_stage:    ItemData(PAD | 0x08, ItemClassification.progression_deprioritized),
    Items.rhythm_tweezers_2_stage:  ItemData(PAD | 0x09, ItemClassification.progression_deprioritized),
    Items.sick_beats_stage:         ItemData(PAD | 0x0A, ItemClassification.progression_deprioritized),
    Items.bouncy_road_stage:        ItemData(PAD | 0x0B, ItemClassification.progression_deprioritized),
    Items.bouncy_road_2_stage:      ItemData(PAD | 0x0C, ItemClassification.progression_deprioritized),
    Items.ninja_bodyguard_stage:    ItemData(PAD | 0x0D, ItemClassification.progression_deprioritized),
    Items.ninja_descendant_stage:   ItemData(PAD | 0x0E, ItemClassification.progression_deprioritized),
    Items.sneaky_spirits_stage:     ItemData(PAD | 0x0F, ItemClassification.progression_deprioritized),
    Items.sneaky_spirits_2_stage:   ItemData(PAD | 0x10, ItemClassification.progression_deprioritized),
    Items.samurai_slice_stage:      ItemData(PAD | 0x11, ItemClassification.progression_deprioritized),
    Items.spaceball_stage:          ItemData(PAD | 0x12, ItemClassification.progression_deprioritized),
    Items.spaceball_2_stage:        ItemData(PAD | 0x13, ItemClassification.progression_deprioritized),
    Items.tap_trial_stage:          ItemData(PAD | 0x14, ItemClassification.progression_deprioritized),
    Items.tap_trial_2_stage:        ItemData(PAD | 0x15, ItemClassification.progression_deprioritized),
    Items.marching_orders_stage:    ItemData(PAD | 0x16, ItemClassification.progression_deprioritized),
    Items.marching_orders_2_stage:  ItemData(PAD | 0x17, ItemClassification.progression_deprioritized),
    Items.wizards_waltz_stage:      ItemData(PAD | 0x18, ItemClassification.progression_deprioritized),
    Items.bunny_hop_stage:          ItemData(PAD | 0x19, ItemClassification.progression_deprioritized),
    Items.fireworks_stage:          ItemData(PAD | 0x1A, ItemClassification.progression_deprioritized),
    Items.power_calligraphy_stage:  ItemData(PAD | 0x1B, ItemClassification.progression_deprioritized),
    Items.toss_team_stage:          ItemData(PAD | 0x1D, ItemClassification.progression_deprioritized),
    Items.toss_team_2_stage:        ItemData(PAD | 0x1E, ItemClassification.progression_deprioritized),
    Items.rat_race_stage:           ItemData(PAD | 0x1F, ItemClassification.progression_deprioritized),
    Items.tram_and_pauline_stage:   ItemData(PAD | 0x20, ItemClassification.progression_deprioritized),
    Items.showtime_stage:           ItemData(PAD | 0x21, ItemClassification.progression_deprioritized),
    Items.space_dance_stage:        ItemData(PAD | 0x22, ItemClassification.progression_deprioritized),
    Items.cosmic_dance_stage:       ItemData(PAD | 0x23, ItemClassification.progression_deprioritized),
    Items.rapmen_stage:             ItemData(PAD | 0x24, ItemClassification.progression_deprioritized),
    Items.rapwomen_stage:           ItemData(PAD | 0x25, ItemClassification.progression_deprioritized),
    Items.quiz_show_stage:          ItemData(PAD | 0x26, ItemClassification.progression_deprioritized),
    Items.the_bon_odori_stage:      ItemData(PAD | 0x27, ItemClassification.progression_deprioritized),
    Items.the_bon_dance_stage:      ItemData(PAD | 0x28, ItemClassification.progression_deprioritized),
    Items.remix_1_stage:            ItemData(PAD | 0x29, ItemClassification.progression_deprioritized),
    Items.remix_2_stage:            ItemData(PAD | 0x2A, ItemClassification.progression_deprioritized),
    Items.remix_3_stage:            ItemData(PAD | 0x2B, ItemClassification.progression_deprioritized),
    Items.remix_4_stage:            ItemData(PAD | 0x2C, ItemClassification.progression_deprioritized),
    Items.remix_5_stage:            ItemData(PAD | 0x2D, ItemClassification.progression_deprioritized),
    Items.remix_6_stage:            ItemData(PAD | 0x2E, ItemClassification.progression_deprioritized),
    Items.remix_7_stage:            ItemData(PAD | 0x2F, ItemClassification.progression_deprioritized),
    Items.remix_8_stage:            ItemData(PAD | 0x30, ItemClassification.progression_deprioritized),

    Items.beep:                     ItemData(PAD | 0x80, ItemClassification.filler),

    Items.glitched:                 ItemData(None, ItemClassification.progression_deprioritized_skip_balancing),
}

item_groups = {
    "Stage Bundle": {
        Items.remix_1_column.value,
        Items.remix_2_column.value,
        Items.remix_3_column.value,
        Items.remix_4_column.value,
        Items.remix_5_column.value,
        Items.remix_6_column.value,
        Items.remix_7_column.value,
        Items.remix_8_column.value,
    },
    "Stages": {f"{stage_name} Stage" for stage_name in list(level_data.keys())}
}
