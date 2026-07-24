from enum import StrEnum

class Items(StrEnum):
    # Mc Muffin
    medal = "Medal"
    
    # Stages
    remix_1_column = "Remix 1 Column"
    remix_2_column = "Remix 2 Column"
    remix_3_column = "Remix 3 Column"
    remix_4_column = "Remix 4 Column"
    remix_5_column = "Remix 5 Column"
    remix_6_column = "Remix 6 Column"
    remix_7_column = "Remix 7 Column"
    remix_8_column = "Remix 8 Column"
    
    karate_man_stage = "Karate Man Stage"
    rhythm_tweezers_stage = "Rhythm Tweezers Stage"
    marching_orders_stage = "Marching Orders Stage"
    spaceball_stage = "Spaceball Stage"
    the_clappy_trio_stage = "The Clappy Trio Stage"
    remix_1_stage = "Remix 1 Stage"
    sneaky_spirits_stage = "Sneaky Spirits Stage"
    samurai_slice_stage = "Samurai Slice Stage"
    rat_race_stage = "Rat Race Stage"
    sick_beats_stage = "Sick Beats Stage"
    the_bon_odori_stage = "The Bon Odori Stage"
    remix_2_stage = "Remix 2 Stage"
    wizards_waltz_stage = "Wizard's Waltz Stage"
    showtime_stage = "Showtime Stage"
    bunny_hop_stage = "Bunny Hop Stage"
    tram_and_pauline_stage = "Tram & Pauline Stage"
    space_dance_stage = "Space Dance Stage"
    remix_3_stage = "Remix 3 Stage"
    quiz_show_stage = "Quiz Show Stage"
    night_walk_stage = "Night Walk Stage"
    power_calligraphy_stage = "Power Calligraphy Stage"
    polyrhythm_stage = "Polyrhythm Stage"
    rapmen_stage = "RAPMEN Stage"
    remix_4_stage = "Remix 4 Stage"
    bouncy_road_stage = "Bouncy Road Stage"
    ninja_bodyguard_stage = "Ninja Bodyguard Stage"
    toss_team_stage = "Toss Team Stage"
    fireworks_stage = "Fireworks Stage"
    tap_trial_stage = "Tap Trial Stage"
    remix_5_stage = "Remix 5 Stage"
    the_snappy_trio_stage = "The Snappy Trio Stage"
    the_bon_dance_stage = "The Bon Dance Stage"
    cosmic_dance_stage = "Cosmic Dance Stage"
    rapwomen_stage = "RAPWOMEN Stage"
    tap_trial_2_stage = "Tap Trial 2 Stage"
    remix_6_stage = "Remix 6 Stage"
    karate_man_2_stage = "Karate Man 2 Stage"
    rhythm_tweezers_2_stage = "Rhythm Tweezers 2 Stage"
    ninja_descendant_stage = "Ninja Descendant Stage"
    night_walk_2_stage = "Night Walk 2 Stage"
    marching_orders_2_stage = "Marching Orders 2 Stage"
    remix_7_stage = "Remix 7 Stage"
    bouncy_road_2_stage = "Bouncy Road 2 Stage"
    toss_team_2_stage = "Toss Team 2 Stage"
    polyrhythm_2_stage = "Polyrhythm 2 Stage"
    spaceball_2_stage = "Spaceball 2 Stage"
    sneaky_spirits_2_stage = "Sneaky Spirits 2 Stage"
    remix_8_stage = "Remix 8 Stage"

    nothing = "Beep"
    victory = "Victory!"

    glitched = "Skill"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)


class Regions(StrEnum):
    karate_man = "Karate Man"
    rhythm_tweezers = "Rhythm Tweezers"
    marching_orders = "Marching Orders"
    spaceball = "Spaceball"
    the_clappy_trio = "The Clappy Trio"
    remix_1 = "Remix 1"
    sneaky_spirits = "Sneaky Spirits"
    samurai_slice = "Samurai Slice"
    rat_race = "Rat Race"
    sick_beats = "Sick Beats"
    the_bon_odori = "The Bon Odori"
    remix_2 = "Remix 2"
    wizards_waltz = "Wizard's Waltz"
    showtime = "Showtime"
    bunny_hop = "Bunny Hop"
    tram_and_pauline = "Tram & Pauline"
    space_dance = "Space Dance"
    remix_3 = "Remix 3"
    quiz_show = "Quiz Show"
    night_walk = "Night Walk"
    power_calligraphy = "Power Calligraphy"
    polyrhythm = "Polyrhythm"
    rapmen = "RAPMEN"
    remix_4 = "Remix 4"
    bouncy_road = "Bouncy Road"
    ninja_bodyguard = "Ninja Bodyguard"
    toss_team = "Toss Team"
    fireworks = "Fireworks"
    tap_trial = "Tap Trial"
    remix_5 = "Remix 5"
    the_snappy_trio = "The Snappy Trio"
    the_bon_dance = "The Bon Dance"
    cosmic_dance = "Cosmic Dance"
    rapwomen = "RAPWOMEN"
    tap_trial_2 = "Tap Trial 2"
    remix_6 = "Remix 6"
    karate_man_2 = "Karate Man 2"
    rhythm_tweezers_2 = "Rhythm Tweezers 2"
    ninja_descendant = "Ninja Descendant"
    night_walk_2 = "Night Walk 2"
    marching_orders_2 = "Marching Orders 2"
    remix_7 = "Remix 7"
    bouncy_road_2 = "Bouncy Road 2"
    toss_team_2 = "Toss Team 2"
    polyrhythm_2 = "Polyrhythm 2"
    spaceball_2 = "Spaceball 2"
    sneaky_spirits_2 = "Sneaky Spirits 2"
    remix_8 = "Remix 8"

    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)


class Locations(StrEnum):
    karate_man_clear = "Karate Man - Clear"
    karate_man_ok = "Karate Man - OK"
    karate_man_superb = "Karate Man - Superb"
    karate_man_perfect = "Karate Man - Perfect"

    rhythm_tweezers_clear = "Rhythm Tweezers - Clear"
    rhythm_tweezers_ok = "Rhythm Tweezers - OK"
    rhythm_tweezers_superb = "Rhythm Tweezers - Superb"
    rhythm_tweezers_perfect = "Rhythm Tweezers - Perfect"

    marching_orders_clear = "Marching Orders - Clear"
    marching_orders_ok = "Marching Orders - OK"
    marching_orders_superb = "Marching Orders - Superb"
    marching_orders_perfect = "Marching Orders - Perfect"

    spaceball_clear = "Spaceball - Clear"
    spaceball_ok = "Spaceball - OK"
    spaceball_superb = "Spaceball - Superb"
    spaceball_perfect = "Spaceball - Perfect"

    the_clappy_trio_clear = "The Clappy Trio - Clear"
    the_clappy_trio_ok = "The Clappy Trio - OK"
    the_clappy_trio_superb = "The Clappy Trio - Superb"
    the_clappy_trio_perfect = "The Clappy Trio - Perfect"

    remix_1_clear = "Remix 1 - Clear"
    remix_1_ok = "Remix 1 - OK"
    remix_1_superb = "Remix 1 - Superb"
    remix_1_perfect = "Remix 1 - Perfect"

    sneaky_spirits_clear = "Sneaky Spirits - Clear"
    sneaky_spirits_ok = "Sneaky Spirits - OK"
    sneaky_spirits_superb = "Sneaky Spirits - Superb"
    sneaky_spirits_perfect = "Sneaky Spirits - Perfect"

    samurai_slice_clear = "Samurai Slice - Clear"
    samurai_slice_ok = "Samurai Slice - OK"
    samurai_slice_superb = "Samurai Slice - Superb"
    samurai_slice_perfect = "Samurai Slice - Perfect"

    rat_race_clear = "Rat Race - Clear"
    rat_race_ok = "Rat Race - OK"
    rat_race_superb = "Rat Race - Superb"
    rat_race_perfect = "Rat Race - Perfect"

    sick_beats_clear = "Sick Beats - Clear"
    sick_beats_ok = "Sick Beats - OK"
    sick_beats_superb = "Sick Beats - Superb"
    sick_beats_perfect = "Sick Beats - Perfect"

    the_bon_odori_clear = "The Bon Odori - Clear"
    the_bon_odori_ok = "The Bon Odori - OK"
    the_bon_odori_superb = "The Bon Odori - Superb"
    the_bon_odori_perfect = "The Bon Odori - Perfect"

    remix_2_clear = "Remix 2 - Clear"
    remix_2_ok = "Remix 2 - OK"
    remix_2_superb = "Remix 2 - Superb"
    remix_2_perfect = "Remix 2 - Perfect"

    wizards_waltz_clear = "Wizard's Waltz - Clear"
    wizards_waltz_ok = "Wizard's Waltz - OK"
    wizards_waltz_superb = "Wizard's Waltz - Superb"
    wizards_waltz_perfect = "Wizard's Waltz - Perfect"

    showtime_clear = "Showtime - Clear"
    showtime_ok = "Showtime - OK"
    showtime_superb = "Showtime - Superb"
    showtime_perfect = "Showtime - Perfect"

    bunny_hop_clear = "Bunny Hop - Clear"
    bunny_hop_ok = "Bunny Hop - OK"
    bunny_hop_superb = "Bunny Hop - Superb"
    bunny_hop_perfect = "Bunny Hop - Perfect"

    tram_and_pauline_clear = "Tram & Pauline - Clear"
    tram_and_pauline_ok = "Tram & Pauline - OK"
    tram_and_pauline_superb = "Tram & Pauline - Superb"
    tram_and_pauline_perfect = "Tram & Pauline - Perfect"

    space_dance_clear = "Space Dance - Clear"
    space_dance_ok = "Space Dance - OK"
    space_dance_superb = "Space Dance - Superb"
    space_dance_perfect = "Space Dance - Perfect"

    remix_3_clear = "Remix 3 - Clear"
    remix_3_ok = "Remix 3 - OK"
    remix_3_superb = "Remix 3 - Superb"
    remix_3_perfect = "Remix 3 - Perfect"

    quiz_show_clear = "Quiz Show - Clear"
    quiz_show_ok = "Quiz Show - OK"
    quiz_show_superb = "Quiz Show - Superb"
    quiz_show_perfect = "Quiz Show - Perfect"

    night_walk_clear = "Night Walk - Clear"
    night_walk_ok = "Night Walk - OK"
    night_walk_superb = "Night Walk - Superb"
    night_walk_perfect = "Night Walk - Perfect"

    power_calligraphy_clear = "Power Calligraphy - Clear"
    power_calligraphy_ok = "Power Calligraphy - OK"
    power_calligraphy_superb = "Power Calligraphy - Superb"
    power_calligraphy_perfect = "Power Calligraphy - Perfect"

    polyrhythm_clear = "Polyrhythm - Clear"
    polyrhythm_ok = "Polyrhythm - OK"
    polyrhythm_superb = "Polyrhythm - Superb"
    polyrhythm_perfect = "Polyrhythm - Perfect"

    rapmen_clear = "RAPMEN - Clear"
    rapmen_ok = "RAPMEN - OK"
    rapmen_superb = "RAPMEN - Superb"
    rapmen_perfect = "RAPMEN - Perfect"

    remix_4_clear = "Remix 4 - Clear"
    remix_4_ok = "Remix 4 - OK"
    remix_4_superb = "Remix 4 - Superb"
    remix_4_perfect = "Remix 4 - Perfect"

    bouncy_road_clear = "Bouncy Road - Clear"
    bouncy_road_ok = "Bouncy Road - OK"
    bouncy_road_superb = "Bouncy Road - Superb"
    bouncy_road_perfect = "Bouncy Road - Perfect"

    ninja_bodyguard_clear = "Ninja Bodyguard - Clear"
    ninja_bodyguard_ok = "Ninja Bodyguard - OK"
    ninja_bodyguard_superb = "Ninja Bodyguard - Superb"
    ninja_bodyguard_perfect = "Ninja Bodyguard - Perfect"

    toss_team_clear = "Toss Team - Clear"
    toss_team_ok = "Toss Team - OK"
    toss_team_superb = "Toss Team - Superb"
    toss_team_perfect = "Toss Team - Perfect"

    fireworks_clear = "Fireworks - Clear"
    fireworks_ok = "Fireworks - OK"
    fireworks_superb = "Fireworks - Superb"
    fireworks_perfect = "Fireworks - Perfect"

    tap_trial_clear = "Tap Trial - Clear"
    tap_trial_ok = "Tap Trial - OK"
    tap_trial_superb = "Tap Trial - Superb"
    tap_trial_perfect = "Tap Trial - Perfect"

    remix_5_clear = "Remix 5 - Clear"
    remix_5_ok = "Remix 5 - OK"
    remix_5_superb = "Remix 5 - Superb"
    remix_5_perfect = "Remix 5 - Perfect"

    the_snappy_trio_clear = "The Snappy Trio - Clear"
    the_snappy_trio_ok = "The Snappy Trio - OK"
    the_snappy_trio_superb = "The Snappy Trio - Superb"
    the_snappy_trio_perfect = "The Snappy Trio - Perfect"

    the_bon_dance_clear = "The Bon Dance - Clear"
    the_bon_dance_ok = "The Bon Dance - OK"
    the_bon_dance_superb = "The Bon Dance - Superb"
    the_bon_dance_perfect = "The Bon Dance - Perfect"

    cosmic_dance_clear = "Cosmic Dance - Clear"
    cosmic_dance_ok = "Cosmic Dance - OK"
    cosmic_dance_superb = "Cosmic Dance - Superb"
    cosmic_dance_perfect = "Cosmic Dance - Perfect"

    rapwomen_clear = "RAPWOMEN - Clear"
    rapwomen_ok = "RAPWOMEN - OK"
    rapwomen_superb = "RAPWOMEN - Superb"
    rapwomen_perfect = "RAPWOMEN - Perfect"

    tap_trial_2_clear = "Tap Trial 2 - Clear"
    tap_trial_2_ok = "Tap Trial 2 - OK"
    tap_trial_2_superb = "Tap Trial 2 - Superb"
    tap_trial_2_perfect = "Tap Trial 2 - Perfect"

    remix_6_clear = "Remix 6 - Clear"
    remix_6_ok = "Remix 6 - OK"
    remix_6_superb = "Remix 6 - Superb"
    remix_6_perfect = "Remix 6 - Perfect"

    karate_man_2_clear = "Karate Man 2 - Clear"
    karate_man_2_ok = "Karate Man 2 - OK"
    karate_man_2_superb = "Karate Man 2 - Superb"
    karate_man_2_perfect = "Karate Man 2 - Perfect"

    rhythm_tweezers_2_clear = "Rhythm Tweezers 2 - Clear"
    rhythm_tweezers_2_ok = "Rhythm Tweezers 2 - OK"
    rhythm_tweezers_2_superb = "Rhythm Tweezers 2 - Superb"
    rhythm_tweezers_2_perfect = "Rhythm Tweezers 2 - Perfect"

    ninja_descendant_clear = "Ninja Descendant - Clear"
    ninja_descendant_ok = "Ninja Descendant - OK"
    ninja_descendant_superb = "Ninja Descendant - Superb"
    ninja_descendant_perfect = "Ninja Descendant - Perfect"

    night_walk_2_clear = "Night Walk 2 - Clear"
    night_walk_2_ok = "Night Walk 2 - OK"
    night_walk_2_superb = "Night Walk 2 - Superb"
    night_walk_2_perfect = "Night Walk 2 - Perfect"

    marching_orders_2_clear = "Marching Orders 2 - Clear"
    marching_orders_2_ok = "Marching Orders 2 - OK"
    marching_orders_2_superb = "Marching Orders 2 - Superb"
    marching_orders_2_perfect = "Marching Orders 2 - Perfect"

    remix_7_clear = "Remix 7 - Clear"
    remix_7_ok = "Remix 7 - OK"
    remix_7_superb = "Remix 7 - Superb"
    remix_7_perfect = "Remix 7 - Perfect"

    bouncy_road_2_clear = "Bouncy Road 2 - Clear"
    bouncy_road_2_ok = "Bouncy Road 2 - OK"
    bouncy_road_2_superb = "Bouncy Road 2 - Superb"
    bouncy_road_2_perfect = "Bouncy Road 2 - Perfect"

    toss_team_2_clear = "Toss Team 2 - Clear"
    toss_team_2_ok = "Toss Team 2 - OK"
    toss_team_2_superb = "Toss Team 2 - Superb"
    toss_team_2_perfect = "Toss Team 2 - Perfect"

    polyrhythm_2_clear = "Polyrhythm 2 - Clear"
    polyrhythm_2_ok = "Polyrhythm 2 - OK"
    polyrhythm_2_superb = "Polyrhythm 2 - Superb"
    polyrhythm_2_perfect = "Polyrhythm 2 - Perfect"

    spaceball_2_clear = "Spaceball 2 - Clear"
    spaceball_2_ok = "Spaceball 2 - OK"
    spaceball_2_superb = "Spaceball 2 - Superb"
    spaceball_2_perfect = "Spaceball 2 - Perfect"

    sneaky_spirits_2_clear = "Sneaky Spirits 2 - Clear"
    sneaky_spirits_2_ok = "Sneaky Spirits 2 - OK"
    sneaky_spirits_2_superb = "Sneaky Spirits 2 - Superb"
    sneaky_spirits_2_perfect = "Sneaky Spirits 2 - Perfect"

    remix_8_clear = "Remix 8 - Clear"
    remix_8_ok = "Remix 8 - OK"
    remix_8_superb = "Remix 8 - Superb"
    remix_8_perfect = "Remix 8 - Perfect"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)
