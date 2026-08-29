from enum import StrEnum

class Items(StrEnum):
    # Stages
    stage_wheel_gator = "Wheel Gator Access Codes"
    stage_bubble_crab = "Bubble Crab Access Codes"
    stage_flame_stag = "Flame Stag Access Codes"
    stage_morph_moth = "Morph Moth Access Codes"
    stage_magna_centipede = "Magna Centipede Access Codes"
    stage_crystal_snail = "Crystal Snail Access Codes"
    stage_overdrive_ostrich = "Overdrive Ostrich Access Codes"
    stage_wire_sponge = "Wire Sponge Access Codes"
    stage_x_hunter = "X-Hunter Base Access Codes"
    stage_x_hunter_1 = "X-Hunter Base #1 Access Codes"
    stage_x_hunter_2 = "X-Hunter Base #2 Access Codes"
    stage_x_hunter_3 = "X-Hunter Base #3 Access Codes"
    stage_x_hunter_4 = "X-Hunter Base #4 Access Codes"
    stage_sigma = "Sigma Access Codes"

    # Second Armor
    helmet = "Helmet Upgrade"
    body = "Body Upgrade"
    arms = "Arms Upgrade"
    legs = "Legs Upgrade"

    # Weapons 
    spin_wheel = "Spin Wheel"
    bubble_splash = "Bubble Splash"
    speed_burner = "Speed Burner"
    silk_shot = "Silk Shot"
    magnet_mine = "Magnet Mine"
    crystal_hunter = "Crystal Hunter"
    sonic_slicer = "Sonic Slicer"
    strike_chain = "Strike Chain"
    shoryuken = "Shoryuken"

    # Ride Armor
    ride_armor = "Ride Armor"

    # Tanks
    heart_tank = "Heart Tank"
    sub_tank = "Sub Tank"

    # Enhancements
    chip_quick_charge = "Quick Charge Chip"
    chip_speedster = "Speedster Chip"
    chip_super_recover = "Super Recover Chip"
    chip_rapid_five = "Rapid Five Chip"
    chip_speed_shot = "Speed Shot Chip"
    chip_buster_plus = "Buster Plus Chip"
    chip_weapon_plus = "Weapon Plus Chip"
    chip_d_converter = "D-Converter Chip"
    chip_d_barrier = "D-Barrier Chip"
    chip_item_plus = "Item Plus Chip"
    chip_spike_walker = "Spike Walker Chip"

    # Medals
    maverick_medal = "Maverick Medal"
    victory = "Sigma Virus Destroyed"

    # Junk
    small_hp = "Small HP Refill"
    large_hp = "Large HP Refill"

    glitched = "Skill"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

class Events(StrEnum):
    x_hunter_stage_1_clear = "X-Hunter Base Stage 1 Clear"
    x_hunter_stage_2_clear = "X-Hunter Base Stage 2 Clear"
    x_hunter_stage_3_clear = "X-Hunter Base Stage 3 Clear"
    x_hunter_stage_4_clear = "X-Hunter Base Stage 4 Clear"
    boss_rematch_clear = "Boss Rematch Defeated"

    wheel_gator_rematch = "Event Defeated Wheel Gator (Rematch)"
    bubble_crab_rematch = "Event Defeated Bubble Crab (Rematch)"
    flame_stag_rematch = "Event Defeated Flame Stag (Rematch)"
    morph_moth_rematch = "Event Defeated Morph Moth (Rematch)"
    magna_centipede_rematch = "Event Defeated Magna Centipede (Rematch)"
    crystal_snail_rematch = "Event Defeated Crystal Snail (Rematch)"
    overdrive_ostrich_rematch = "Event Defeated Overdrive Ostrich (Rematch)"
    wire_sponge_rematch = "Event Defeated Wire Sponge (Rematch)"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)


class Regions(StrEnum):
    intro_stage = "Intro Stage"

    wheel_gator = "Wheel Gator"
    wheel_gator_start = "Wheel Gator - Start"
    wheel_gator_mid = "Wheel Gator - Mid"
    wheel_gator_end = "Wheel Gator - End"
    wheel_gator_boss = "Wheel Gator - Boss"

    bubble_crab = "Bubble Crab"
    bubble_crab_start = "Bubble Crab - Start"
    bubble_crab_open = "Bubble Crab - Open Area"
    bubble_crab_inside = "Bubble Crab - Inside"
    bubble_crab_boss = "Bubble Crab - Boss"

    flame_stag = "Flame Stag"
    flame_stag_start = "Flame Stag - Start"
    flame_stag_volcano = "Flame Stag - Volcano"
    flame_stag_gas = "Flame Stag - Gas"
    flame_stag_boss = "Flame Stag - Boss"

    morph_moth = "Morph Moth"
    morph_moth_start = "Morph Moth - Start"
    morph_moth_parasite_1 = "Morph Moth - Parasite 1"
    morph_moth_parasite_2 = "Morph Moth - Parasite 2"
    morph_moth_after_parasite_1 = "Morph Moth - After Parasite 1"
    morph_moth_after_parasite_2 = "Morph Moth - After Parasite 2"
    morph_moth_boss = "Morph Moth - Boss"

    magna_centipede = "Magna Centipede"
    magna_centipede_start = "Magna Centipede - Start"
    magna_centipede_blade = "Magna Centipede - Blade"
    magna_centipede_security = "Magna Centipede - Security"
    magna_centipede_after_blade = "Magna Centipede - After Blade"
    magna_centipede_after_security = "Magna Centipede - After Security"
    magna_centipede_boss = "Magna Centipede - Boss"

    crystal_snail = "Crystal Snail"
    crystal_snail_start = "Crystal Snail - Start"
    crystal_snail_arena = "Crystal Snail - Arena"
    crystal_snail_after_arena = "Crystal Snail - After Arena"
    crystal_snail_quartz = "Crystal Snail - Quartz"
    crystal_snail_downhill = "Crystal Snail - Downhill"
    crystal_snail_uphill = "Crystal Snail - Uphill"
    crystal_snail_boss = "Crystal Snail - Boss"

    overdrive_ostrich = "Overdrive Ostrich"
    overdrive_ostrich_start = "Overdrive Ostrich - Start"
    overdrive_ostrich_arena = "Overdrive Ostrich - Arena"
    overdrive_ostrich_inside = "Overdrive Ostrich - Inside"
    overdrive_ostrich_boss = "Overdrive Ostrich - Boss"

    wire_sponge = "Wire Sponge"
    wire_sponge_start = "Wire Sponge - Start"
    wire_sponge_elevator = "Wire Sponge - Elevator"
    wire_sponge_outside = "Wire Sponge - Outside"
    wire_sponge_boss = "Wire Sponge - Boss"

    x_hunter_arena = "X-Hunter Arena"

    x_hunter_stage = "X-Hunter Stage"

    x_hunter_stage_1 = "X-Hunter Stage 1"
    x_hunter_stage_1_start = "X-Hunter Stage 1 - Start"
    x_hunter_stage_1_boss = "X-Hunter Stage 1 - Boss"

    x_hunter_stage_2 = "X-Hunter Stage 2"
    x_hunter_stage_2_start = "X-Hunter Stage 2 - Start"
    x_hunter_stage_2_boss = "X-Hunter Stage 2 - Boss"

    x_hunter_stage_3 = "X-Hunter Stage 3"
    x_hunter_stage_3_start = "X-Hunter Stage 3 - Start"
    x_hunter_stage_3_boss = "X-Hunter Stage 3 - Boss"

    x_hunter_stage_4 = "X-Hunter Stage 4"
    x_hunter_stage_4_lobby = "X-Hunter Stage 4 - Lobby"
    x_hunter_stage_4_voice = "X-Hunter Stage 4 - Voice"

    x_hunter_stage_5 = "X-Hunter Stage 5"
    x_hunter_stage_5_zero = "X-Hunter Stage 5 - Zero"
    x_hunter_stage_5_sigma = "X-Hunter Stage 5 - Sigma"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)

class Locations(StrEnum):
    intro_stage_boss = "Defeated Gigantic Mechaniloid CF-0"
    intro_stage_clear = "Intro Stage - Clear"
    intro_stage_hp_1 = "Intro Stage - HP Pickup 1 (Before spike pit)"
    intro_stage_hp_2 = "Intro Stage - HP Pickup 2 (Before boss room)"

    wheel_gator_boss = "Defeated Wheel Gator"
    wheel_gator_clear = "Wheel Gator - Clear"
    wheel_gator_heart_tank = "Wheel Gator - Heart Tank"
    wheel_gator_arms = "Wheel Gator - Arms Capsule"
    wheel_gator_hp_1 = "Wheel Gator - HP Pickup 1 (High ledge after spikes section)"
    wheel_gator_hp_2 = "Wheel Gator - HP Pickup 2 (Ledge before Ride Armor)"
    wheel_gator_1up = "Wheel Gator - 1-Up Pickup (Top of elevator)"
    wheel_gator_energy_1 = "Wheel Gator - Weapon Energy Pickup (Ledge in left elevator exit)"
    wheel_gator_hp_3 = "Wheel Gator - HP Pickup 3 (Hidden behind top column after X-Hunter room)"
    wheel_gator_hp_4 = "Wheel Gator - HP Pickup 4 (Ledge before boss room)"
    wheel_gator_hp_5 = "Wheel Gator - HP Pickup 5 (Hidden behind metal slope in exterior section)"
    wheel_gator_hp_6 = "Wheel Gator - HP Pickup 6 (Hidden behind metal slope in exterior section)"
    wheel_gator_hp_7 = "Wheel Gator - HP Pickup 7 (Hidden behind metal slope in exterior section)"

    bubble_crab_boss = "Defeated Bubble Crab"
    bubble_crab_clear = "Bubble Crab - Clear"
    bubble_crab_heart_tank = "Bubble Crab - Heart Tank"
    bubble_crab_sub_tank = "Bubble Crab - Sub Tank"
    bubble_crab_mini_boss = "Defeated Sea Canthller"
    bubble_crab_1up = "Bubble Crab - 1-Up Pickup (Below Spin Wheel blocks before water section)"
    bubble_crab_hp_1 = "Bubble Crab - HP Pickup 1 (Ledge before water section)"
    bubble_crab_hp_2 = "Bubble Crab - HP Pickup 2 (Top-right opening above metal floor)"
    bubble_crab_energy_1 = "Bubble Crab - Weapon Energy Pickup 1 (Top-right ledge in seabed section)"
    bubble_crab_hp_3 = "Bubble Crab - HP Pickup 3 (First pit in seabed section)"
    bubble_crab_hp_4 = "Bubble Crab - HP Pickup 4 (Artificial cave in seabed section)"
    bubble_crab_energy_2 = "Bubble Crab - Weapon Energy Pickup 2 (Artificial cave in seabed section)"
    bubble_crab_hp_5 = "Bubble Crab - HP Pickup 5 (Fake wall below Sub Tank)"
    bubble_crab_hp_6 = "Bubble Crab - HP Pickup 6 (Before boss)"

    flame_stag_boss = "Defeated Flame Stag"
    flame_stag_clear = "Flame Stag - Clear"
    flame_stag_heart_tank = "Flame Stag - Heart Tank"
    flame_stag_sub_tank = "Flame Stag - Sub Tank"
    flame_stag_1up_1 = "Flame Stag - 1-Up Pickup 1 (Top-right of first Beetron section)"
    flame_stag_hp_1 = "Flame Stag - HP Pickup 1 (Cave before first lava section)"
    flame_stag_energy_1 = "Flame Stag - Weapon Energy Pickup 1 (Cave before first lava section)"
    flame_stag_hp_2 = "Flame Stag - HP Pickup 2 (Cave before first lava section)"
    flame_stag_energy_2 = "Flame Stag - Weapon Energy Pickup 2 (Cave before first lava section)"
    flame_stag_hp_3 = "Flame Stag - HP Pickup 3 (Cave before rising lava section)"
    flame_stag_hp_4 = "Flame Stag - HP Pickup 4 (First ledge in rising lava section)"
    flame_stag_1up_2 = "Flame Stag - 1-Up Pickup 2 (Bottom of rising lava section)"
    flame_stag_hp_5 = "Flame Stag - HP Pickup 5 (Second ledge in rising lava section)"
    flame_stag_energy_3 = "Flame Stag - Weapon Energy Pickup 3 (Second ledge in rising lava section)"
    flame_stag_hp_6 = "Flame Stag - HP Pickup 6 (After rising lava section)"
    flame_stag_hp_7 = "Flame Stag - HP Pickup 7 (Bottom-left of lava cave section)"
    flame_stag_energy_4 = "Flame Stag - Weapon Energy Pickup 4 (Bottom-left of lava cave section)"
    flame_stag_hp_8 = "Flame Stag - HP Pickup 8 (Before X-Hunter room)"
    flame_stag_1up_3 = "Flame Stag - 1-Up Pickup 3 (Above third pillar in lava cave section)"
    flame_stag_hp_9 = "Flame Stag - HP Pickup 9 (Ledge in gas pipes section)"

    morph_moth_boss = "Defeated Morph Moth"
    morph_moth_clear = "Morph Moth - Clear"
    morph_moth_heart_tank = "Morph Moth - Heart Tank"
    morph_moth_body = "Morph Moth - Body Capsule"
    morph_moth_mini_boss_1 = "Defeated Pararoid S-38 #1"
    morph_moth_mini_boss_2 = "Defeated Pararoid S-38 #2"
    morph_moth_1up_1 = "Morph Moth - 1-Up Pickup 1 (Left of Heart Tank)"
    morph_moth_1up_2 = "Morph Moth - 1-Up Pickup 2 (Top-left ledge before Pararoid S-38 #1)"
    morph_moth_hp_1 = "Morph Moth - HP Pickup 1 (Before vertical ladder section)"
    morph_moth_hp_2 = "Morph Moth - HP Pickup 2 (Left ledge in vertical ladder section)"
    morph_moth_hp_3 = "Morph Moth - HP Pickup 3 (Right ledge in vertical ladder section)"
    morph_moth_hp_4 = "Morph Moth - HP Pickup 4 (Bottom of magnet ceiling section)"
    morph_moth_hp_5 = "Morph Moth - HP Pickup 5 (Bottom of magnet ceiling section)"

    magna_centipede_boss = "Defeated Magna Centipede"
    magna_centipede_clear = "Magna Centipede - Clear"
    magna_centipede_heart_tank = "Magna Centipede - Heart Tank"
    magna_centipede_sub_tank = "Magna Centipede - Sub Tank"
    magna_centipede_mini_boss_1 = "Defeated Chop Register"
    magna_centipede_mini_boss_2 = "Defeated Raider Killer"
    magna_centipede_hp_1 = "Magna Centipede - HP Pickup 1 (After Chop Register)"
    magna_centipede_hp_2 = "Magna Centipede - HP Pickup 2 (Before X-Hunter room)"

    crystal_snail_boss = "Defeated Crystal Snail"
    crystal_snail_clear = "Crystal Snail - Clear"
    crystal_snail_heart_tank = "Crystal Snail - Heart Tank"
    crystal_snail_helmet = "Crystal Snail - Helmet Capsule"
    crystal_snail_mini_boss_1 = "Defeated Magna Quartz"
    crystal_snail_hp_1 = "Crystal Snail - HP Pickup 1 (Under crystal blocks before X-Hunter room)"
    crystal_snail_energy_1 = "Crystal Snail - Weapon Energy Pickup 1 (Under crystal blocks before X-Hunter room)"
    crystal_snail_hp_2 = "Crystal Snail - HP Pickup 4 (In giant crystal slide section)"
    crystal_snail_hp_3 = "Crystal Snail - HP Pickup 2 (Under crystal blocks before Magna Quartz)"
    crystal_snail_1up_1 = "Crystal Snail - 1-Up Pickup 1 (Under crystal blocks before Magna Quartz)"
    crystal_snail_hp_4 = "Crystal Snail - HP Pickup 3 (After X-Hunter room)"
    crystal_snail_1up_2 = "Crystal Snail - 1-Up Pickup 2 (Fake ceiling next to Helmet Capsule)"

    overdrive_ostrich_boss = "Defeated Overdrive Ostrich"
    overdrive_ostrich_clear = "Overdrive Ostrich - Clear"
    overdrive_ostrich_heart_tank = "Overdrive Ostrich - Heart Tank"
    overdrive_ostrich_leg = "Overdrive Ostrich - Legs Capsule"
    overdrive_ostrich_hp_1 = "Overdrive Ostrich - HP Pickup 1 (Behind Spin Wheel blocks before X-Hunter room)"
    overdrive_ostrich_1up = "Overdrive Ostrich - 1-Up Pickup (Top-right ledge in outdoors bike section)"
    overdrive_ostrich_hp_2 = "Overdrive Ostrich - HP Pickup 2 (On spikes before Legs Capsule)"
    overdrive_ostrich_energy_1 = "Overdrive Ostrich - Weapon Energy Pickup 1 (On spikes before Legs Capsule)"
    overdrive_ostrich_hp_3 = "Overdrive Ostrich - HP Pickup 3 (On spikes before Legs Capsule)"
    overdrive_ostrich_energy_2 = "Overdrive Ostrich - Weapon Energy Pickup 2 (On spikes before Legs Capsule)"

    wire_sponge_boss = "Defeated Wire Sponge"
    wire_sponge_clear = "Wire Sponge - Clear"
    wire_sponge_heart_tank = "Wire Sponge - Heart Tank"
    wire_sponge_sub_tank = "Wire Sponge - Sub Tank"
    wire_sponge_1up_1 = "Wire Sponge - 1-Up Pickup (Above flying platforms in rainy section)"
    wire_sponge_hp_1 = "Wire Sponge - HP Pickup 1 (Before X-Hunter room)"
    wire_sponge_hp_2 = "Wire Sponge - HP Pickup 2 (Before boss room)"

    agile_defeated = "Defeated Agile"
    serges_defeated = "Defeated Serges"
    violen_defeated = "Defeated Violen"

    x_hunter_stage_1_boss = "Defeated Neo Violen"
    x_hunter_stage_1_1up_1 = "X-Hunter Base 1 - 1-Up Pickup 1 (Right ledge after start)"
    x_hunter_stage_1_hp = "X-Hunter Base 1 - HP Pickup (Below flying platforms section)"
    x_hunter_stage_1_1up_2 = "X-Hunter Base 1 - 1-Up Pickup 2 (Below flying platforms section)"

    x_hunter_stage_2_boss = "Defeated Serges Tank"
    x_hunter_stage_2_hp = "X-Hunter Base 2 - HP Pickup (Behind Spin Wheel blocks before boss)"
    x_hunter_stage_2_1up = "X-Hunter Base 2 - 1-Up Pickup (Behind Spin Wheel blocks before boss)"

    x_hunter_stage_3_boss = "Defeated Agile Flyer"
    x_hunter_stage_3_shoryuken = "X-Hunter Base 3 - Shoryuken Capsule"
    x_hunter_stage_3_hp_1 = "X-Hunter Base 3 - HP Pickup 1 (In Strike Chain hole after start)"
    x_hunter_stage_3_1up_1 = "X-Hunter Base 3 - 1-Up Pickup 1 (In Strike Chain hole after start)"
    x_hunter_stage_3_hp_2 = "X-Hunter Base 3 - HP Pickup 2 (Before second moving platform section)"
    x_hunter_stage_3_hp_3 = "X-Hunter Base 3 - HP Pickup 3 (Before second moving platform section)"
    x_hunter_stage_3_hp_4 = "X-Hunter Base 3 - HP Pickup 4 (Before second moving platform section)"
    x_hunter_stage_3_hp_5 = "X-Hunter Base 3 - HP Pickup 5 (Top of second moving platform section)"
    x_hunter_stage_3_hp_6 = "X-Hunter Base 3 - HP Pickup 6 (Top of second moving platform section)"
    x_hunter_stage_3_1up_2 = "X-Hunter Base 3 - 1-Up Pickup 2 (Left of charged Speed Burner + air dash section)"
    x_hunter_stage_3_hp_7 = "X-Hunter Base 3 - HP Pickup 7 (Ledge left of charged Speed Burner + air dash section)"
    x_hunter_stage_3_hp_8 = "X-Hunter Base 3 - HP Pickup 8 (Ledge left of charged Speed Burner + air dash section)"
    x_hunter_stage_3_1up_3 = "X-Hunter Base 3 - 1-Up Pickup 3 (After charged Speed Burner + air dash section)"
    x_hunter_stage_3_1up_4 = "X-Hunter Base 3 - 1-Up Pickup 4 (On spikes after last vertical section)"

    x_hunter_stage_4_wheel_gator = "Defeated Wheel Gator (Rematch)"
    x_hunter_stage_4_bubble_crab = "Defeated Bubble Crab (Rematch)"
    x_hunter_stage_4_flame_stag = "Defeated Flame Stag (Rematch)"
    x_hunter_stage_4_morph_moth = "Defeated Morph Moth (Rematch)"
    x_hunter_stage_4_magna_centipede = "Defeated Magna Centipede (Rematch)"
    x_hunter_stage_4_crystal_snail = "Defeated Crystal Snail (Rematch)"
    x_hunter_stage_4_overdrive_ostrich = "Defeated Overdrive Ostrich (Rematch)"
    x_hunter_stage_4_wire_sponge = "Defeated Wire Sponge (Rematch)"
    x_hunter_stage_4_hp_1 = "X-Hunter Base 4 - HP Pickup 1 (In boss rematch capsules room)"
    x_hunter_stage_4_hp_2 = "X-Hunter Base 4 - HP Pickup 2 (In boss rematch capsules room)"
    x_hunter_stage_4_hp_3 = "X-Hunter Base 4 - HP Pickup 3 (In boss rematch capsules room)"
    x_hunter_stage_4_hp_4 = "X-Hunter Base 4 - HP Pickup 4 (In boss rematch capsules room)"
    x_hunter_stage_4_clear = "X-Hunter Base 4 - Clear"

    x_hunter_stage_5_zero = "Defeated Zero"
    x_hunter_stage_5_sigma = "Defeated Neo Sigma"
    
    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return repr(self.value)
