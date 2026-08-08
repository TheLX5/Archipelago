from .constants import *
from .enums import Locations, Regions, Items


level_data = {
    Regions.karate_man: 0x00,
    Regions.karate_man_2: 0x01,
    Regions.the_clappy_trio: 0x02,
    Regions.the_snappy_trio: 0x03,
    Regions.polyrhythm: 0x04,
    Regions.polyrhythm_2: 0x05,
    Regions.night_walk: 0x06,
    Regions.night_walk_2: 0x07,
    Regions.rhythm_tweezers: 0x08,
    Regions.rhythm_tweezers_2: 0x09,
    Regions.sick_beats: 0x0A,
    Regions.bouncy_road: 0x0B,
    Regions.bouncy_road_2: 0x0C,
    Regions.ninja_bodyguard: 0x0D,
    Regions.ninja_descendant: 0x0E,
    Regions.sneaky_spirits: 0x0F,
    Regions.sneaky_spirits_2: 0x10,
    Regions.samurai_slice: 0x11,
    Regions.spaceball: 0x12,
    Regions.spaceball_2: 0x13,
    Regions.tap_trial: 0x14,
    Regions.tap_trial_2: 0x15,
    Regions.marching_orders: 0x16,
    Regions.marching_orders_2: 0x17,
    Regions.wizards_waltz: 0x18,
    Regions.bunny_hop: 0x19,
    Regions.fireworks: 0x1A,
    Regions.power_calligraphy: 0x1B,
    Regions.toss_team: 0x1D,
    Regions.toss_team_2: 0x1E,
    Regions.rat_race: 0x1F,
    Regions.tram_and_pauline: 0x20,
    Regions.showtime: 0x21,
    Regions.space_dance: 0x22,
    Regions.cosmic_dance: 0x23,
    Regions.rapmen: 0x24,
    Regions.rapwomen: 0x25,
    Regions.quiz_show: 0x26,
    Regions.the_bon_odori: 0x27,
    Regions.the_bon_dance: 0x28,
    Regions.remix_1: 0x29,
    Regions.remix_2: 0x2A,
    Regions.remix_3: 0x2B,
    Regions.remix_4: 0x2C,
    Regions.remix_5: 0x2D,
    Regions.remix_6: 0x2E,
    Regions.remix_7: 0x2F,
    Regions.remix_8: 0x30,
}

perfect_data = {
    0x00: 0x28,  # Karate Man
    0x01: 0x2E,  # Karate Man 2
    0x02: 0x08,  # The Clappy Trio
    0x03: 0x2D,  # The Snappy Trio
    0x04: 0x13,  # Polyrhythm
    0x05: 0x1F,  # Polyrhythm 2
    0x06: 0x23,  # Night Walk
    0x07: 0x16,  # Night Walk 2
    0x08: 0x20,  # Rhythm Tweezers
    0x09: 0x26,  # Rhythm Tweezers 2
    0x0A: 0x11,  # Sick Beats
    0x0B: 0x2C,  # Bouncy Road
    0x0C: 0x2F,  # Bouncy Road 2
    0x0D: 0x24,  # Ninja Bodyguard
    0x0E: 0x1E,  # Ninja Reincarnate
    0x0F: 0x29,  # Sneaky Spirits
    0x10: 0x0F,  # Sneaky Spirits 2
    0x11: 0x21,  # Samurai Slice
    0x12: 0x10,  # Spaceball
    0x13: 0x17,  # Spaceball 2
    0x14: 0x0C,  # Tap Trial
    0x15: 0x0D,  # Tap Trial 2
    0x16: 0x18,  # Marching Orders
    0x17: 0x0E,  # Marching Orders 2
    0x18: 0x2A,  # Wizard's Waltz
    0x19: 0x1A,  # Bunny Hop
    0x1A: 0x14,  # Fireworks
    0x1B: 0x1B,  # Power Calligraphy
    0x1D: 0x1C,  # Toss Boys
    0x1E: 0x27,  # Toss Boys 2
    0x1F: 0x19,  # Rat Race
    0x20: 0x12,  # Tram & Pauline
    0x21: 0x22,  # Showtime
    0x22: 0x0A,  # Space Dance
    0x23: 0x1D,  # Cosmic Dance
    0x24: 0x0B,  # Rap Men
    0x25: 0x15,  # Rap Women
    0x26: 0x2B,  # Quiz Show
    0x27: 0x09,  # The Bon Odori
    0x28: 0x25,  # The Bon Dance
    0x29: 0x00,  # Remix 1
    0x2A: 0x01,  # Remix 2
    0x2B: 0x02,  # Remix 3
    0x2C: 0x03,  # Remix 4
    0x2D: 0x04,  # Remix 5
    0x2E: 0x05,  # Remix 6
    0x2F: 0x06,  # Remix 7
    0x30: 0x07,  # Remix 8
}

remix_groups = {
    Items.remix_1_column: [
        Regions.karate_man.value,
        Regions.rhythm_tweezers.value,
        Regions.marching_orders.value,
        Regions.spaceball.value,
        Regions.the_clappy_trio.value,
        Regions.remix_1.value,
    ],
    Items.remix_2_column: [
        Regions.sneaky_spirits.value,
        Regions.samurai_slice.value,
        Regions.rat_race.value,
        Regions.sick_beats.value,
        Regions.the_bon_odori.value,
        Regions.remix_2.value,
    ],
    Items.remix_3_column: [
        Regions.wizards_waltz.value,
        Regions.showtime.value,
        Regions.bunny_hop.value,
        Regions.tram_and_pauline.value,
        Regions.space_dance.value,
        Regions.remix_3.value,
    ],
    Items.remix_4_column: [
        Regions.quiz_show.value,
        Regions.night_walk.value,
        Regions.power_calligraphy.value,
        Regions.polyrhythm.value,
        Regions.rapmen.value,
        Regions.remix_4.value,
    ],
    Items.remix_5_column: [
        Regions.bouncy_road.value,
        Regions.ninja_bodyguard.value,
        Regions.toss_team.value,
        Regions.fireworks.value,
        Regions.tap_trial.value,
        Regions.remix_5.value,
    ],
    Items.remix_6_column: [
        Regions.the_snappy_trio.value,
        Regions.the_bon_dance.value,
        Regions.cosmic_dance.value,
        Regions.rapwomen.value,
        Regions.tap_trial_2.value,
        Regions.remix_6.value,
    ],
    Items.remix_7_column: [
        Regions.karate_man_2.value,
        Regions.rhythm_tweezers_2.value,
        Regions.ninja_descendant.value,
        Regions.night_walk_2.value,
        Regions.marching_orders_2.value,
        Regions.remix_7.value,
    ],
    Items.remix_8_column: [
        Regions.bouncy_road_2.value,
        Regions.toss_team_2.value,
        Regions.polyrhythm_2.value,
        Regions.spaceball_2.value,
        Regions.sneaky_spirits_2.value,
        Regions.remix_8.value,
    ],
}