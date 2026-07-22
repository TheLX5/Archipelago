from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MMX2World

from rule_builder.rules import True_, Rule

from .enums import Events, Locations, Regions
from .options import BossWeaknessRando, BossRandomizedHP, BossWeaknessStrictness
from .base_rules import (LEMON,
                         DASH_LEMON,
                         LEVEL_1_CHARGE,
                         LEVEL_2_CHARGE,
                         LEVEL_3_CHARGE,
                         SHORYUKEN, 
                         GIGA_CRUSH, 
                         BUBBLE_SPLASH, 
                         SILK_SHOT, 
                         SPIN_WHEEL, 
                         SONIC_SLICER,
                         STRIKE_CHAIN, 
                         MAGNET_MINE, 
                         SPEED_BURNER,
                         CHARGED_BUBBLE_SPLASH, 
                         CHARGED_SILK_SHOT, 
                         CHARGED_SPIN_WHEEL, 
                         CHARGED_SONIC_SLICER,
                         CHARGED_STRIKE_CHAIN, 
                         CHARGED_MAGNET_MINE, 
                         CHARGED_SPEED_BURNER)

class Weapon():
    id: int
    name: str
    damage: int
    rule: dict

    def __init__(self, id: int, name: str, damage: int, rule: Rule):
        self.id = id
        self.name = name
        self.damage = damage
        self.rule = rule


class Boss():
    name: str
    weakness: list[str]
    sub_weakness: list[str]
    excluded_weaknesses: list[str]
    entrances: list[str]
    locations: list[str]
    weakness_addr: int
    hp: int
    hp_address: int
    required_player_hp: dict[str, int]

    def __init__(self, 
                 name: str, 
                 weakness: list[str], 
                 sub_weakness: list[str],
                 excluded_weaknesses: list[str],
                 entrances: list[str],
                 locations: list[str],
                 weakness_addr: int,
                 hp: int, 
                 hp_address: int,
                 required_player_hp: dict[str, int] = {"No Logic": 1}):
        self.name = name
        self.weakness = weakness.copy()
        self.sub_weakness = sub_weakness.copy()
        self.excluded_weaknesses = excluded_weaknesses.copy()
        self.entrances = entrances.copy()
        self.locations = locations.copy()
        self.weakness_addr = weakness_addr
        self.hp = hp
        self.hp_address = hp_address
        self.required_player_hp = required_player_hp.copy()

    def dump_rom_data(self):
        data = {}
        data["name"] = self.name
        data["weakness"] = self.weakness
        data["sub_weakness"] = self.sub_weakness
        data["weakness_addr"] = self.weakness_addr
        data["hp"] = self.hp
        data["hp_address"] = self.hp_address
        return data

    def dump_slot_data(self):
        data = {}
        data["weakness"] = self.weakness
        data["sub_weakness"] = self.sub_weakness
        data["hp"] = self.hp
        return data


weapons = {
    "Lemon": Weapon(0x00, "Lemon", 0x02, LEMON),
    "Dash Lemon": Weapon(0x06, "Dash Lemon", 0x03, DASH_LEMON),
    "Level 1 Charge Shot": Weapon(0x01, "Level 1 Charge Shot", 0x02, LEVEL_1_CHARGE),
    "Level 2 Charge Shot": Weapon(0x03, "Level 2 Charge Shot", 0x03, LEVEL_2_CHARGE),
    "Level 3 Charge Shot": Weapon(0x1D, "Level 3 Charge Shot", 0x03, LEVEL_3_CHARGE),
    "Shoryuken": Weapon(0x04, "Shoryuken", 0x20, SHORYUKEN),
    "Giga Crush": Weapon(0x0F, "Giga Crush", 0x01, GIGA_CRUSH),
    "Bubble Splash": Weapon(0x08, "Bubble Splash", 0x03, BUBBLE_SPLASH),
    "Charged Bubble Splash": Weapon(0x11, "Charged Bubble Splash", 0x05, CHARGED_BUBBLE_SPLASH),
    "Spin Wheel": Weapon(0x0A, "Spin Wheel", 0x03, SPIN_WHEEL),
    "Charged Spin Wheel": Weapon(0x13, "Charged Spin Wheel", 0x05, CHARGED_SPIN_WHEEL),
    "Sonic Slicer": Weapon(0x0B, "Sonic Slicer", 0x03, SONIC_SLICER),
    "Charged Sonic Slicer": Weapon(0x14, "Charged Sonic Slicer", 0x05, CHARGED_SONIC_SLICER),
    "Strike Chain": Weapon(0x0C, "Strike Chain", 0x03, STRIKE_CHAIN),
    "Charged Strike Chain": Weapon(0x15, "Charged Strike Chain", 0x05, CHARGED_STRIKE_CHAIN),
    "Magnet Mine": Weapon(0x0D, "Magnet Mine", 0x03, MAGNET_MINE),
    "Charged Magnet Mine": Weapon(0x16, "Charged Magnet Mine", 0x05, CHARGED_MAGNET_MINE),
    "Speed Burner": Weapon(0x0E, "Speed Burner", 0x03, SPEED_BURNER),
    "Speed Burner (Underwater)": Weapon(0x23, "Speed Burner (Underwater)", 0x03, CHARGED_SILK_SHOT),
    "Charged Speed Burner": Weapon(0x17, "Charged Speed Burner", 0x03, CHARGED_SPEED_BURNER),
    "Silk Shot (Rocks)": Weapon(0x09, "Silk Shot (Rocks)", 0x03, SILK_SHOT),
    "Silk Shot (Black Rock)": Weapon(0x18, "Silk Shot (Black Rock)", 0x05, SILK_SHOT),
    "Silk Shot (Junk)": Weapon(0x1B, "Silk Shot (Junk)", 0x03, SILK_SHOT),
    "Silk Shot (Leaves)": Weapon(0x1C, "Silk Shot (Leaves)", 0x03, SILK_SHOT),
    "Silk Shot (Crystals)": Weapon(0x1E, "Silk Shot (Crystals)", 0x03, SILK_SHOT),
    "Charged Silk Shot (Rocks)": Weapon(0x12, "Charged Silk Shot (Rocks)", 0x05, CHARGED_SILK_SHOT),
    "Charged Silk Shot (Black Rock)": Weapon(0x1F, "Charged Silk Shot (Black Rock)", 0x05, CHARGED_SILK_SHOT),
    "Charged Silk Shot (Junk)": Weapon(0x20, "Charged Silk Shot (Junk)", 0x05, CHARGED_SILK_SHOT),
    "Charged Silk Shot (Leaves)": Weapon(0x21, "Charged Silk Shot (Leaves)", 0x05, CHARGED_SILK_SHOT),
    "Charged Silk Shot (Crystals)": Weapon(0x22, "Charged Silk Shot (Crystals)", 0x05, CHARGED_SILK_SHOT),
}

weapon_groups = {
    "Lemon": ["Lemon", "Dash Lemon"],
    "Charge Shot": ["Level 1 Charge Shot", "Level 2 Charge Shot", "Level 3 Charge Shot"],
    "Bubble Splash": ["Bubble Splash", "Charged Bubble Splash"],
    "Spin Wheel": ["Spin Wheel", "Charged Spin Wheel"],
    "Sonic Slicer": ["Sonic Slicer", "Charged Sonic Slicer"],
    "Strike Chain": ["Strike Chain", "Charged Strike Chain"],
    "Magnet Mine": ["Magnet Mine", "Charged Magnet Mine"],
    "Speed Burner": ["Speed Burner", "Speed Burner (Underwater)", "Charged Speed Burner"],
    "Silk Shot": [""],
}

silk_shot_groups = {
    "Rocks": ["Silk Shot (Rocks)", "Charged Silk Shot (Rocks)"],
    "Black Rock": ["Silk Shot (Black Rock)", "Charged Silk Shot (Black Rock)"],
    "Junk": ["Silk Shot (Junk)", "Charged Silk Shot (Junk)"],
    "Leaves": ["Silk Shot (Leaves)", "Charged Silk Shot (Leaves)"],
    "Crystals": ["Silk Shot (Crystals)", "Charged Silk Shot (Crystals)"],
}

weapon_groups_chaotic = {
    "Lemon": ["Lemon"],
    "Dash Lemon": ["Dash Lemon"],
    "Level 1 Charge Shot": ["Level 1 Charge Shot"],
    "Level 2 Charge Shot": ["Level 2 Charge Shot"],
    "Level 3 Charge Shot": ["Level 3 Charge Shot"],
    "Bubble Splash": ["Bubble Splash"],
    "Charged Bubble Splash": ["Charged Bubble Splash"],
    "Spin Wheel": ["Spin Wheel"],
    "Charged Spin Wheel": ["Charged Spin Wheel"],
    "Sonic Slicer": ["Sonic Slicer"],
    "Charged Sonic Slicer": ["Charged Sonic Slicer"],
    "Strike Chain": ["Strike Chain"],
    "Charged Strike Chain": ["Charged Strike Chain"],
    "Magnet Mine": ["Magnet Mine"],
    "Charged Magnet Mine": ["Charged Magnet Mine"],
    "Speed Burner": ["Speed Burner", "Speed Burner (Underwater)"],
    "Charged Speed Burner": ["Charged Speed Burner"],
    "Silk Shot": [],
    "Charged Silk Shot": [],
}

silk_shot_groups_chaotic = {
    "Rocks": ["Silk Shot (Rocks)"],
    "Charged Rocks": ["Charged Silk Shot (Rocks)"],
    "Black Rock": ["Silk Shot (Black Rock)"],
    "Charged Black Rock": ["Charged Silk Shot (Black Rock)"],
    "Junk": ["Silk Shot (Junk)"],
    "Charged Junk": ["Charged Silk Shot (Junk)"],
    "Leaves": ["Silk Shot (Leaves)"],
    "Charged Leaves": ["Charged Silk Shot (Leaves)"],
    "Crystals": ["Silk Shot (Crystals)"],
    "Charged Crystals": ["Charged Silk Shot (Crystals)"],
}

default_boss_data = {
    "Wheel Gator": Boss(
        name="Wheel Gator",
        weakness=["Strike Chain", "Charged Strike Chain"],
        sub_weakness=["Bubble Splash"],
        excluded_weaknesses=[],
        weakness_addr=0x37643,
        hp=32,
        hp_address=0x1B7B0,
        entrances=[f"{Regions.wheel_gator_end} -> {Regions.wheel_gator_boss}"],
        locations=[Locations.wheel_gator_boss, Locations.x_hunter_stage_4_wheel_gator, Events.wheel_gator_rematch],
    ),
    "Bubble Crab": Boss(
        name="Bubble Crab",
        weakness=["Spin Wheel", "Charged Spin Wheel"],
        sub_weakness=[],
        excluded_weaknesses=["Speed Burner", "Charged Speed Burner"],
        weakness_addr=0x3753A,
        hp=32,
        hp_address=0x3C267,
        entrances=[f"{Regions.bubble_crab_inside} -> {Regions.bubble_crab_boss}"],
        locations=[Locations.bubble_crab_boss, Locations.x_hunter_stage_4_bubble_crab, Events.bubble_crab_rematch],
    ),
    "Flame Stag": Boss(
        name="Flame Stag",
        weakness=["Bubble Splash", "Charged Bubble Splash"],
        sub_weakness=["Sonic Slicer", "Charged Sonic Slicer", "Silk Shot (Leaves)", "Charged Silk Shot (Leaves)"],
        excluded_weaknesses=[],
        weakness_addr=0x3761D,
        hp=32,
        hp_address=0x24056,
        entrances=[f"{Regions.flame_stag_gas} -> {Regions.flame_stag_boss}"],
        locations=[Locations.flame_stag_boss, Locations.x_hunter_stage_4_flame_stag, Events.flame_stag_rematch],
    ),
    "Morph Moth": Boss(
        name="Morph Moth",
        weakness=["Speed Burner", "Charged Speed Burner"],
        sub_weakness=["Charged Magnet Mine"],
        excluded_weaknesses=[],
        weakness_addr=0x376DB,
        hp=32,
        hp_address=0x1AB86,
        entrances=[f"{Regions.morph_moth_after_parasite_2} -> {Regions.morph_moth_boss}"],
        locations=[Locations.morph_moth_boss, Locations.x_hunter_stage_4_morph_moth, Events.morph_moth_rematch],
    ),
    "Magna Centipede": Boss(
        name="Magna Centipede",
        weakness=["Silk Shot (Junk)", "Charged Silk Shot (Junk)"],
        sub_weakness=["Strike Chain", "Charged Strike Chain"],
        excluded_weaknesses=[],
        weakness_addr=0x374EE,
        hp=32,
        hp_address=0x22C75,
        entrances=[f"{Regions.magna_centipede_after_security} -> {Regions.magna_centipede_boss}"],
        locations=[Locations.magna_centipede_boss, Locations.x_hunter_stage_4_magna_centipede, Events.magna_centipede_rematch],
    ),
    "Crystal Snail": Boss(
        name="Crystal Snail",
        weakness=["Magnet Mine", "Charged Magnet Mine"],
        sub_weakness=["Charged Spin Wheel", "Charged Silk Shot (Rocks)"],
        excluded_weaknesses=[],
        weakness_addr=0x37514,
        hp=32,
        hp_address=0x3B521,
        entrances=[f"{Regions.crystal_snail_uphill} -> {Regions.crystal_snail_boss}"],
        locations=[Locations.crystal_snail_boss, Locations.x_hunter_stage_4_crystal_snail, Events.crystal_snail_rematch],
    ),
    "Overdrive Ostrich": Boss(
        name="Overdrive Ostrich",
        weakness=["Lemon", "Dash Lemon", "Level 1 Charge Shot", "Level 2 Charge Shot", "Level 3 Charge Shot"],
        sub_weakness=["Silk Shot (Rocks)", "Charged Silk Shot (Rocks)", "Silk Shot (Junk)", "Charged Silk Shot (Junk)"],
        excluded_weaknesses=[],
        weakness_addr=0x375F7,
        hp=32,
        hp_address=0x4690B,
        entrances=[f"{Regions.overdrive_ostrich_inside} -> {Regions.overdrive_ostrich_boss}"],
        locations=[Locations.overdrive_ostrich_boss, Locations.x_hunter_stage_4_overdrive_ostrich, Events.overdrive_ostrich_rematch],
    ),
    "Wire Sponge": Boss(
        name="Wire Sponge",
        weakness=["Sonic Slicer", "Charged Sonic Slicer"],
        sub_weakness=["Speed Burner", "Charged Magnet Mine"],
        excluded_weaknesses=[],
        weakness_addr=0x37560,
        hp=32,
        hp_address=0x21C54,
        entrances=[f"{Regions.wire_sponge_outside} -> {Regions.wire_sponge_boss}"],
        locations=[Locations.wire_sponge_boss, Locations.x_hunter_stage_4_wire_sponge, Events.wire_sponge_rematch],
    ),
    "Magna Quartz": Boss(
        name="Magna Quartz",
        weakness=["Spin Wheel", "Charged Spin Wheel"],
        sub_weakness=[],
        excluded_weaknesses=[],
        weakness_addr=0x37DF8,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.crystal_snail_start} -> {Regions.crystal_snail_quartz}"],
        locations=[Locations.crystal_snail_mini_boss_1],
    ),
    "Chop Register": Boss(
        name="Chop Register",
        weakness=["Silk Shot (Junk)", "Charged Silk Shot (Junk)"],
        sub_weakness=["Strike Chain", "Charged Strike Chain"],
        excluded_weaknesses=[],
        weakness_addr=0x37E20,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.magna_centipede_start} -> {Regions.magna_centipede_blade}"],
        locations=[Locations.magna_centipede_mini_boss_1],
    ),
    "Raider Killer": Boss(
        name="Raider Killer",
        weakness=["Speed Burner", "Charged Speed Burner"],
        sub_weakness=["Charged Magnet Mine"],
        excluded_weaknesses=[],
        weakness_addr=0x37E48,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.magna_centipede_after_blade} -> {Regions.magna_centipede_security}"],
        locations=[Locations.magna_centipede_mini_boss_2],
    ),
    "Pararoid S-38": Boss(
        name="Pararoid S-38",
        weakness=["Sonic Slicer", "Charged Bubble Splash", "Speed Burner"],
        sub_weakness=["Bubble Splash", "Charged Spin Wheel"],
        excluded_weaknesses=[],
        weakness_addr=0x37E70,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.morph_moth_start} -> {Regions.morph_moth_parasite_1}",
                   f"{Regions.morph_moth_after_parasite_1} -> {Regions.morph_moth_parasite_2}"],
        locations=[Locations.morph_moth_mini_boss_1, Locations.morph_moth_mini_boss_2],
    ),
    "Gigantic Mechaniloid CF-0": Boss(
        name="Gigantic Mechaniloid CF-0",
        weakness=["Lemon", "Dash Lemon"],
        sub_weakness=[],
        excluded_weaknesses=[],
        weakness_addr=0x0,
        hp=32,
        hp_address=0x3949F,
        entrances=[],
        locations=[Locations.intro_stage_boss],
    ),
    "Agile": Boss(
        name="Agile",
        weakness=["Magnet Mine", "Charged Magnet Mine"],
        sub_weakness=["Charged Spin Wheel", "Charged Silk Shot (Rocks)"],
        excluded_weaknesses=[],
        weakness_addr=0x37D80,
        hp=32,
        hp_address=0x23E49,
        entrances=[],
        locations=[Locations.agile_defeated],
    ),
    "Serges": Boss(
        name="Serges",
        weakness=["Sonic Slicer", "Charged Sonic Slicer"],
        sub_weakness=["Speed Burner", "Charged Magnet Mine"],
        excluded_weaknesses=["Silk Shot (Leaves)", "Charged Silk Shot (Leaves)",
                             "Charged Speed Burner", "Charged Bubble Splash"],
        weakness_addr=0x37DA8,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.x_hunter_stage_2_start} -> {Regions.x_hunter_stage_2_boss}"],
        locations=[Locations.serges_defeated, Events.x_hunter_stage_2_clear],
    ),
    "Violen": Boss(
        name="Violen",
        weakness=["Bubble Splash", "Charged Bubble Splash"],
        sub_weakness=["Sonic Slicer", "Charged Sonic Slicer", "Silk Shot (Leaves)", "Charged Silk Shot (Leaves)"],
        excluded_weaknesses=[],
        weakness_addr=0x37DD0,
        hp=32,
        hp_address=0x0,
        entrances=[],
        locations=[Locations.violen_defeated],
    ),
    "Serges Tank": Boss(
        name="Serges Tank",
        weakness=["Silk Shot (Junk)", "Charged Silk Shot (Junk)", "Giga Crush"],
        sub_weakness=["Strike Chain", "Charged Bubble Splash", "Charged Magnet Mine"],
        excluded_weaknesses=["Charged Speed Burner"],
        weakness_addr=0x377BF,
        hp=32,
        hp_address=0x14D4F,
        entrances=[f"{Regions.x_hunter_stage_2_start} -> {Regions.x_hunter_stage_2_boss}"],
        locations=[Events.x_hunter_stage_2_clear],
    ),
    "Agile Flyer": Boss(
        name="Agile Flyer",
        weakness=["Magnet Mine", "Charged Magnet Mine"],
        sub_weakness=[],
        excluded_weaknesses=[],
        weakness_addr=0x377E5,
        hp=32,
        hp_address=0xAF148,
        entrances=[f"{Regions.x_hunter_stage_3_start} -> {Regions.x_hunter_stage_3_boss}"],
        locations=[Events.x_hunter_stage_3_clear],
    ),
    "Neo Violen": Boss(
        name="Neo Violen",
        weakness=["Bubble Splash", "Charged Bubble Splash"],
        sub_weakness=["Sonic Slicer", "Charged Sonic Slicer", "Silk Shot (Leaves)", "Charged Silk Shot (Leaves)"],
        excluded_weaknesses=[],
        weakness_addr=0x3780B,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.x_hunter_stage_1_start} -> {Regions.x_hunter_stage_1_boss}"],
        locations=[Events.x_hunter_stage_1_clear],
    ),
    "Zero": Boss(
        name="Zero",
        weakness=["Speed Burner", "Charged Speed Burner"],
        sub_weakness=[],
        excluded_weaknesses=[],
        weakness_addr=0x3774D,
        hp=32,
        hp_address=0x14BCBF,
        entrances=[f"{Regions.x_hunter_stage_5} -> {Regions.x_hunter_stage_5_zero}"],
        locations=[Locations.x_hunter_stage_5_zero],
    ),
    "Neo Sigma": Boss(
        name="Neo Sigma",
        weakness=["Sonic Slicer", "Charged Sonic Slicer"],
        sub_weakness=[],
        excluded_weaknesses=[],
        weakness_addr=0x37773,
        hp=32,
        hp_address=0x15618F,
        entrances=[f"{Regions.x_hunter_stage_5_zero} -> {Regions.x_hunter_stage_5_sigma}"],
        locations=[Locations.x_hunter_stage_5_sigma],
    ),
    "Sigma Virus": Boss(
        name="Sigma Virus",
        weakness=["Strike Chain"],
        sub_weakness=["Charged Strike Chain"],
        excluded_weaknesses=[],
        weakness_addr=0x37799,
        hp=32,
        hp_address=0x0,
        entrances=[f"{Regions.x_hunter_stage_5_zero} -> {Regions.x_hunter_stage_5_sigma}"],
        locations=[Locations.x_hunter_stage_5_sigma],
    ),
}

def remove_excluded_weaknesses(weapon_list: list[str], exclusion_list: list[str]):
    for weapon in exclusion_list:
        if weapon in weapon_list:
            weapon_list.remove(weapon)
    return weapon_list

def shuffle_weaknesses(world: "MMX2World"):
    if world.options.boss_weakness_rando == BossWeaknessRando.option_vanilla:
        return 
    
    elif world.options.boss_weakness_rando == BossWeaknessRando.option_swapped:
        # Swap around existing weaknesses, skips over the intro boss
        shuffled_boss_names = list(default_boss_data.keys())
        shuffled_boss_names.remove("Gigantic Mechaniloid CF-0")
        world.random.shuffle(shuffled_boss_names)
        for boss_name in default_boss_data.keys():
            if boss_name == "Gigantic Mechaniloid CF-0":
                continue
            selected_boss_name = shuffled_boss_names.pop(0)
            world.boss_data[boss_name].weakness = default_boss_data[selected_boss_name].weakness.copy()
            world.boss_data[boss_name].sub_weakness = default_boss_data[selected_boss_name].sub_weakness.copy()
        
    elif world.options.boss_weakness_rando == BossWeaknessRando.option_simple:
        # Selects a weapon at random. Charged and uncharged versions are kept together.
        # Every time a weapon is rolled, every other weapon is more likely to appear
        # Silk shot can be selected exactly once per boss.
        weapon_list = []
        boss_order = list(world.boss_data.keys())
        boss_order.remove("Gigantic Mechaniloid CF-0")
        world.random.shuffle(boss_order)
        for boss_name in boss_order:
            weapon_list.extend(list(weapon_groups))
            weapon_list = remove_excluded_weaknesses(weapon_list, world.boss_data[boss_name].excluded_weaknesses)
            world.random.shuffle(weapon_list)
            chosen_weapon = weapon_list.pop(0)
            weapon_list = [w for w in weapon_list if w != chosen_weapon]

            if "Silk Shot" in chosen_weapon:
                chosen_weapon = world.random.choice(list(silk_shot_groups.keys()))
                new_weakness_data = silk_shot_groups[chosen_weapon].copy()
            else:
                new_weakness_data = weapon_groups[chosen_weapon].copy()

            world.boss_data[boss_name].weakness = new_weakness_data.copy()

    else:
        # Selects a weapon at random. Charged and uncharged versions are kept separate.
        # Every time a weapon is rolled, every other weapon is more likely to appear
        # Silk shot can be selected exactly once per boss.
        if world.options.boss_weakness_rando == BossWeaknessRando.option_chaotic_single:
            times = 1
        elif world.options.boss_weakness_rando == BossWeaknessRando.option_chaotic_double:
            times = 2
        elif world.options.boss_weakness_rando == BossWeaknessRando.option_chaotic_triple:
            times = 3
        else:
            times = 1

        weapon_list = []
        boss_order = list(world.boss_data.keys())
        boss_order.remove("Gigantic Mechaniloid CF-0")
        world.random.shuffle(boss_order)
        for boss_name in boss_order:
            world.boss_data[boss_name].weakness = []
            weapon_list.extend(list(weapon_groups_chaotic))
            weapon_list = remove_excluded_weaknesses(weapon_list, world.boss_data[boss_name].excluded_weaknesses)
            world.random.shuffle(weapon_list)
            for _ in range(times):
                chosen_weapon = weapon_list.pop(0)
                weapon_list = [w for w in weapon_list if w != chosen_weapon]
                
                if "Silk Shot" in chosen_weapon:
                    chosen_weapon = world.random.choice(list(silk_shot_groups_chaotic.keys()))
                    new_weakness_data = silk_shot_groups_chaotic[chosen_weapon].copy()
                else:
                    new_weakness_data = weapon_groups_chaotic[chosen_weapon].copy()

                world.boss_data[boss_name].weakness.extend(new_weakness_data)

    # Apply plando weaknesses, they disregard everything else rolled before
    if len(world.options.boss_weakness_plando.value.keys()) != 0:
        for boss_name, plando_weaknesses in world.options.boss_weakness_plando.value.items():
            plando_weaknesses: dict[str, list]
            world.boss_data[boss_name].weakness = plando_weaknesses.copy()

    # Apply strictness logic for buster and charged buster settings
    if world.options.boss_weakness_strictness == BossWeaknessStrictness.option_weakness_and_buster:
        for boss_name in world.boss_data.keys():
            world.boss_data[boss_name].weakness.extend(["Lemon", 
                                                        "Dash Lemon", 
                                                        "Level 1 Charge Shot", 
                                                        "Level 2 Charge Shot", 
                                                        "Level 3 Charge Shot"])
    elif world.options.boss_weakness_strictness == BossWeaknessStrictness.option_weakness_and_upgraded_buster:
        for boss_name in world.boss_data.keys():
            world.boss_data[boss_name].weakness.extend(["Level 3 Charge Shot"])

    #for boss_name, boss_data in world.boss_data.items():
    #    print (boss_name)
    #    for weapon in boss_data.weakness:
    #        print (f"    - {weapon}")

def shuffle_hp(world: "MMX2World"):
    if world.options.boss_randomize_hp == BossRandomizedHP.option_off:
        return
    elif world.options.boss_randomize_hp == BossRandomizedHP.option_weak:
        ranges = (2, 32)
    elif world.options.boss_randomize_hp == BossRandomizedHP.option_regular:
        ranges = (12, 48)
    elif world.options.boss_randomize_hp == BossRandomizedHP.option_strong:
        ranges = (32, 64)
    elif world.options.boss_randomize_hp == BossRandomizedHP.option_chaotic:
        ranges = (2, 64)

    for boss_name in world.boss_data.keys():
        world.boss_data[boss_name].hp = world.random.randint(ranges[0], ranges[1])

    # Apply plando HP settings, they disregard everything else rolled before
    if len(world.options.boss_hp_plando.value.keys()) != 0:
        for boss_name, plando_hp in world.options.boss_hp_plando.value.items():
            world.boss_data[boss_name].hp = plando_hp

    # TODO: Make Serges and Violen not use Agile's HP value
    world.boss_data["Serges"].hp = world.boss_data["Agile"].hp
    world.boss_data["Violen"].hp = world.boss_data["Agile"].hp
    world.boss_data["Neo Violen"].hp = world.boss_data["Agile"].hp

    # TODO: Randomize Sigma Virus' HP
    world.boss_data["Sigma Virus"].hp = 32
