from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionDict, OptionSet, OptionGroup, DeathLink, PerGameCommonOptions, StartInventoryPool
from schema import Schema, And, Optional
from .enums import Items


weapons = [
    "Lemon",
    "Dash Lemon",
    "Level 1 Charge Shot",
    "Level 2 Charge Shot",
    "Level 3 Charge Shot",
    #"Shoryuken",
    #"Giga Crush",
    "Bubble Splash",
    "Charged Bubble Splash",
    "Spin Wheel",
    "Charged Spin Wheel",
    "Sonic Slicer",
    "Charged Sonic Slicer",
    "Strike Chain",
    "Charged Strike Chain",
    "Magnet Mine",
    "Charged Magnet Mine",
    "Speed Burner",
    "Speed Burner (Underwater)",
    "Charged Speed Burner",
    "Silk Shot (Rocks)",
    "Silk Shot (Black Rock)",
    "Silk Shot (Junk)",
    "Silk Shot (Leaves)",
    "Silk Shot (Crystals)",
    "Charged Silk Shot (Rocks)",
    "Charged Silk Shot (Black Rock)",
    "Charged Silk Shot (Junk)",
    "Charged Silk Shot (Leaves)",
    "Charged Silk Shot (Crystals)",
]


enemy_names = [
    "Wheel Gator",
    "Bubble Crab",
    "Flame Stag",
    "Morph Moth",
    "Magna Centipede",
    "Crystal Snail",
    "Overdrive Ostrich",
    "Wire Sponge",
    "Magna Quartz",
    "Chop Register",
    "Raider Killer",
    "Pararoid S-38",
    "Gigantic Mechaniloid CF-0",
    "Agile",
    "Serges",
    "Violen",
    "Serges Tank",
    "Agile Flyer",
    "Neo Violen",
    "Zero",
    "Sigma",
    "Sigma Virus",
]

class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support.

    EnergyLink in MMX2 works as a big HP and Weapon Energy pool that the players can use to request HP
    or Weapon Energy whenever they need to.
    
    You make use of this feature by typing /heal <amount> or /refill <amount> in the client.
    """
    display_name = "Energy Link"

class DamageLink(Toggle):
    """
    Enable DamageLink support
    """
    display_name = "Damage Link"

class StartingHP(Range):
    """
    How much HP X will have at the start of the game.

    Notes: Going over 32 HP may cause visual bugs in either gameplay or the pause menu. The max HP is capped at 64.
    """
    display_name = "Starting HP"
    range_start = 1
    range_end = 32
    default = 16

class HeartTankEffectiveness(Range):
    """
    How many units of HP each Heart tank will provide to the user.

    Note: Going over 32 HP may cause visual bugs in either gameplay or the pause menu. The max HP is capped at 64.
    """
    display_name = "Heart Tank Effectiveness"
    range_start = 1
    range_end = 8
    default = 2

class BossWeaknessRando(Choice):
    """
    Every main boss will have its weakness randomized.

    vanilla: Bosses retain their original weaknesses
    swapped: Bosses will swap around their weaknesses with other bosses
    simple: Bosses will have one random weakness
    chaotic_single: Bosses will have one random weakness under the chaotic set
    chaotic_double: Bosses will have two random weaknesses under the chaotic set
    chaotic_triple: Bosses will have three random weakness under the chaotic set

    The chaotic set makes every weapon charge level a separate weakness instead of keeping
    them together, meaning that a boss can be weak to Charged Spin Wheel but not its
    uncharged version.
    """
    display_name = "Boss Weakness Randomization"
    option_vanilla = 0
    option_swapped = 1
    option_simple = 2
    option_chaotic_single = 4
    option_chaotic_double = 5
    option_chaotic_triple = 6
    default = 0

class BossWeaknessStrictness(Choice):
    """
    How strict boss weaknesses will be.

    not_strict: How the original game operates
    weakness_and_buster: Only allow the weakness and buster to deal damage to the bosses
    weakness_and_upgraded_buster: Only allow the weakness and buster charge levels 3 to deal damage to the bosses
    only_weakness: Only the weakness will deal damage to the bosses
    """
    display_name = "Boss Weakness Strictness"
    option_not_strict = 0
    option_weakness_and_buster = 1
    option_weakness_and_upgraded_buster = 2
    option_only_weakness = 3
    default = 0

class BossRandomizedHP(Choice):
    """
    Wheter to randomize the boss' hp or not. Mid bosses aren't supported (yet).

    off: Bosses' HP will not be randomized
    weak: Bosses will have [2,32] HP
    regular: Bosses will have [16,48] HP
    strong: Bosses will have [32,64] HP
    chaotic: Bosses will have [2,64] HP
    """
    display_name = "Boss Randomize HP"
    option_off = 0
    option_weak = 1
    option_regular = 2
    option_strong = 3
    option_chaotic = 4
    default = 0

class PlandoWeaknesses(OptionDict):
    """
    Forces bosses to have a specific weakness. Uses the names that appear on the chaotic weakness set.

    Format: 
      Boss Name: ["Weakness Name"]
    """
    display_name = "Plando Weaknesses"
    schema = Schema({
        Optional(boss_name): 
            [And(str, lambda weapon: weapon in weapons)] for boss_name in enemy_names
    })
    default = {}

class PlandoHP(OptionDict):
    """
    Forces bosses to have a specific HP value. Can't go over 64 or lower than 2.
    Sigma Virus and mid-stage bosses aren't supported here (yet).
    Serges, Violen, Neo Violen and Agile share the same HP value with Agile's data applying to all three.

    Format: 
      Boss Name: HP Value
    """
    display_name = "Plando HP"
    schema = Schema({
        Optional(boss_name): And(int, lambda n: 2 <= n <= 64) for boss_name in enemy_names
    })
    default = {}

class JammedBuster(Toggle):
    """
    Jams X's buster making it only able to shoot lemons.
    Note: This adds another Arms Upgrade into the item pool.
    """
    display_name = "Jammed Buster"

class ShoryukenInPool(DefaultOnToggle):
    """
    Adds Shoryuken to the item pool.
    """
    display_name = "Shoryuken In Pool"

class Chips(OptionSet):
    """
    Which chip items will be included in the game.
    Do note that this feature REQUIRES enabling pickup items as locations!

    Supported enhancement chips:
    * "Quick Charge Chip" [MMX5] Halves charge time for X-Buster and Special Weapon shots
    * "Speedster Chip" [MMX5] Increases walking speed by 50%
    * "Super Recover Chip" [MMX5] Increases recovery from items by 25%
    * "Rapid Five Chip" [MMX5] Increases the amount of buster shots on screen to 5
    * "Speed Shot Chip" [MMX5] Increases default buster shot (lemons) horizontal speed by 50%
    * "Buster Plus Chip" [MMX5] Increases Buster damage by 1
    * "Weapon Plus Chip" [MMX6] Increases Weapon damage by 1
    * "D-Converter Chip" [MMX6] Refills the active weapon when taking damage
    * "D-Barrier Chip" [MMX6] Doubles the I-frames after getting hit
    * "Item Plus Chip" [MMX7] Increases item drop rates by roughly 33%
    * "Spike Walker Chip" [MMX8] Halves speed when sliding down a wall
    """
    display_name = "Enhancement Chips"
    valid_keys = [
        Items.chip_quick_charge.value,
        Items.chip_speedster.value,
        Items.chip_super_recover.value,
        Items.chip_rapid_five.value,
        Items.chip_speed_shot.value,
        Items.chip_buster_plus.value,
        Items.chip_weapon_plus.value,
        Items.chip_d_converter.value,
        Items.chip_d_barrier.value,
        Items.chip_item_plus.value,
        Items.chip_spike_walker.value,
    ]
    default = [
        Items.chip_quick_charge.value,
        Items.chip_speedster.value,
        Items.chip_super_recover.value,
        Items.chip_rapid_five.value,
        Items.chip_speed_shot.value,
        Items.chip_buster_plus.value,
        Items.chip_weapon_plus.value,
        Items.chip_d_converter.value,
        Items.chip_d_barrier.value,
        Items.chip_item_plus.value,
        Items.chip_spike_walker.value,
    ]

class PickupLocations(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will be considered a location.
    """
    display_name = "Pickup Locations"

class XHunterBaseBossRematchCount(Range):
    """
    How many boss rematches are needed in the fourth X-Hunter's Base stage.
    """
    display_name = "X-Hunter Base 4 Rematch count"
    range_start = 0
    range_end = 8
    default = 8

class XHunterBaseLevelUnlock(Choice):
    """
    How are X-Hunter Base levels unlocked once you have access to the X-Hunter Base.
      - **Vanilla**: Each level is unlocked as soon the previous one is beaten.
      - **All Open**: All levels are unlocked.
    """
    display_name = "X-Hunter Level Unlock"
    option_vanilla = 0
    option_all_open = 1
    #option_item_per_level = 2

class XHunterBaseOpen(Choice):
    """
    Under which condition will X-Hunter's Base open.
    """
    display_name = "X-Hunter Base Open"
    option_item = 0
    option_medals = 1
    default = 1

class XHunterBaseMedalCount(Range):
    """
    How many Maverick Medals are required to access X-Hunter's Stage.
    """
    display_name = "X-Hunter Base Medal Count"
    range_start = 0
    range_end = 8
    default = 6

class XHuntersArenaMedalCount(Range):
    """
    How many Maverick Medals are required to allow X-Hunters to spawn on their Arena areas in the main levels.

    You have to press SELECT on the map to swap which X-Hunter will be available.
    """
    display_name = "X-Hunters Medal Count"
    range_start = 0
    range_end = 5
    default = 2


mmx2_option_groups = [
    OptionGroup("Gameplay Options", [
        StartingHP,
        HeartTankEffectiveness,
        JammedBuster,
        Chips,
        ShoryukenInPool,
        XHuntersArenaMedalCount,
    ]),
    OptionGroup("Boss Weakness Options", [
        BossWeaknessRando,
        PlandoWeaknesses,
        BossWeaknessStrictness,
        BossRandomizedHP,
        PlandoHP,
    ]),
    OptionGroup("X-Hunter's Base Options", [
        XHunterBaseOpen,
        XHunterBaseMedalCount,
        XHunterBaseBossRematchCount,
        XHunterBaseLevelUnlock,
    ]),
]

@dataclass
class MMX2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    energy_link: EnergyLink
    death_link: DeathLink
    damage_link: DamageLink
    starting_hp: StartingHP
    heart_tank_effectiveness: HeartTankEffectiveness
    boss_weakness_rando: BossWeaknessRando
    boss_weakness_strictness: BossWeaknessStrictness
    boss_weakness_plando: PlandoWeaknesses
    boss_randomize_hp: BossRandomizedHP
    boss_hp_plando: PlandoHP
    pickup_locations: PickupLocations
    jammed_buster: JammedBuster
    chips: Chips
    shoryuken_in_pool: ShoryukenInPool
    x_hunter_base_open: XHunterBaseOpen
    x_hunter_base_medal_count: XHunterBaseMedalCount
    x_hunter_base_boss_rematch_count: XHunterBaseBossRematchCount
    x_hunter_base_level_unlock: XHunterBaseLevelUnlock
    x_hunters_arena_medal_count: XHuntersArenaMedalCount
