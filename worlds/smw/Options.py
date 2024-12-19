from dataclasses import dataclass

from Options import Choice, Range, Toggle, DeathLink, DefaultOnToggle, OptionSet, FreeText, OptionGroup, PerGameCommonOptions


class Goal(Choice):
    """
    Determines the goal of the seed

    Bowser: Defeat Koopalings, reach Bowser's Castle and defeat Bowser

    Yoshi Egg Hunt: Find a certain number of Yoshi Eggs
    """
    display_name = "Goal"
    option_bowser = 0
    option_yoshi_egg_hunt = 1
    default = 0


class BossesRequired(Range):
    """
    How many Bosses (Koopalings or Reznor) must be defeated in order to defeat Bowser
    """
    display_name = "Bosses Required"
    range_start = 0
    range_end = 11
    default = 7


class NumberOfYoshiEggs(Range):
    """
    Maximum possible number of Yoshi Eggs that will be in the item pool

    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.
    
    Required Percentage of Yoshi Eggs will be calculated based off of that number.
    """
    display_name = "Max Number of Yoshi Eggs"
    range_start = 1
    range_end = 255
    default = 50


class PercentageOfYoshiEggs(Range):
    """
    What Percentage of Yoshi Eggs are required to finish Yoshi Egg Hunt
    """
    display_name = "Required Percentage of Yoshi Eggs"
    range_start = 1
    range_end = 100
    default = 100


class DragonCoinChecks(Toggle):
    """
    Whether collecting 5 Dragon Coins in each level will grant a check
    """
    display_name = "Dragon Coin Checks"


class MoonChecks(Toggle):
    """
    Whether collecting a 3-Up Moon in a level will grant a check
    """
    display_name = "3up Moon Checks"


class Hidden1UpChecks(Toggle):
    """
    Whether collecting a hidden 1-Up mushroom in a level will grant a check

    These checks are considered cryptic as there's no actual indicator that they're in their respective places
    
    Enable this option at your own risk
    """
    display_name = "Hidden 1-Up Checks"


class BonusBlockChecks(Toggle):
    """
    Whether collecting a 1-Up mushroom from a Bonus Block in a level will grant a check
    """
    display_name = "Bonus Block Checks"


class Blocksanity(Toggle):
    """
    Whether hitting a block with an item or coin inside will grant a check
    
    Note that some blocks are excluded due to how the option and the game works!
    
    Exclusion list:
      * Blocks in Top Secret Area & Front Door/Bowser Castle
      * Blocks that are unreachable unless you glitch your way in
    """
    display_name = "Blocksanity"


class BlockCollectBehavior(Choice):
    """
    How blocks react when they are collected and blocksanity is enabled

    vanilla: Blocks retain their original behavior (always have their original items inside)

    exclude_powerups: Blocks with a single coin and 1-Ups inside will remain collected

    everything: Blocks with a single coin, 1-Ups, powerups and Yoshis will remain collected
    """
    display_name = "Block Collect Behavior"
    option_vanilla = 0
    option_exclude_powerups = 1
    option_everything = 3
    default = 0


class LocationVisualIndicator(OptionSet):
    """
    Locations will have a visual indicator whether the item they have inside is important or not.

    Exits: Goal posts, keys and orbs will have a visual indicator

    Dragon Coins: Dragon Coins will have an AP icon inside

    Moons: 3-Up Moons will be swapped for an AP icon

    Bonus Blocks: Bonus Blocks will have an AP icon inside
    
    Blocksanity: All Blocksanity blocks will have a visual indicator
    """
    display_name = "Location Visual Indicator"
    default = {}
    valid_keys = {
        "Exits",
        "Dragon Coins",
        "Moons",
        "Bonus Blocks",
        "Blocksanity",
    }


class BowserCastleDoors(Choice):
    """
    How the doors of Bowser's Castle behave

    Vanilla: Front and Back Doors behave as vanilla

    Fast: Both doors behave as the Back Door

    Slow: Both doors behave as the Front Door

    "Front Door" rooms depend on the `bowser_castle_rooms` option

    "Back Door" only requires going through the dark hallway to Bowser
    """
    display_name = "Bowser Castle Doors"
    option_vanilla = 0
    option_fast = 1
    option_slow = 2
    default = 0


class BowserCastleRooms(Choice):
    """
    How the rooms of Bowser's Castle Front Door behave

    Vanilla: You can choose which rooms to enter, as in vanilla

    Random Two Room: Two random rooms are chosen

    Random Five Room: Five random rooms are chosen

    Gauntlet: All eight rooms must be cleared

    Labyrinth: Which room leads to Bowser?
    """
    display_name = "Bowser Castle Rooms"
    option_vanilla = 0
    option_random_two_room = 1
    option_random_five_room = 2
    option_gauntlet = 3
    option_labyrinth = 4
    default = 1


class BossShuffle(Choice):
    """
    How bosses are shuffled

    None: Bosses are not shuffled

    Simple: Four Reznors and the seven Koopalings are shuffled around

    Full: Each boss location gets a fully random boss

    Singularity: One or two bosses are chosen and placed at every boss location
    """
    display_name = "Boss Shuffle"
    option_none = 0
    option_simple = 1
    option_full = 2
    option_singularity = 3
    default = 0


class LevelShuffle(Toggle):
    """
    Whether levels are shuffled
    """
    display_name = "Level Shuffle"


class MapTeleportShuffle(Choice):
    """
    Whether map teleports (stars and pipes) are shuffled
    """
    display_name = "Map Teleport Shuffle"
    option_off = 0
    option_on_only_stars = 1
    option_on_only_pipes = 2
    option_on_both_same_type = 3
    option_on_both_mix = 4
    default = 0


class MapTransitionShuffle(Toggle):
    """
    Wheter map transitions are shuffled
    """
    display_name = "Map Transition Shuffle"
    

class ExcludeSpecialZone(Toggle):
    """
    If active, this option will prevent any progression items from being placed in Special Zone levels.

    Additionally, if Level Shuffle is active, Special Zone levels will not be shuffled away from their vanilla tiles.
    """
    display_name = "Exclude Special Zone"


class SwapDonutGhostHouseExits(Toggle):
    """
    If enabled, this option will swap which overworld direction the two exits of the level at the Donut Ghost House overworld tile go:

    False: Normal Exit goes up, Secret Exit goes right.

    True: Normal Exit goes right, Secret Exit goes up.
    """
    display_name = "Swap Donut GH Exits"


class DisplayReceivedItemPopups(Choice):
    """
    What messages to display in-game for items received
    """
    display_name = "Display Received Item Popups"
    option_none = 0
    option_all = 1
    option_progression = 2
    option_progression_minus_yoshi_eggs = 3
    default = 3


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required Yoshi Eggs in the item pool with random junk items (only applicable on Yoshi Egg Hunt goal)
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class InventoryFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random inventory items

    Percentage is calculated after traps
    """
    display_name = "Inventory Fill Percentage"
    range_start = 0
    range_end = 100
    default = 60


class PersistentTrapBehavior(Choice):
    """
    Alters the despawn behavior of Ice, Reverse and Fishing traps.
    """
    display_name = "Persistent Trap Behavior"
    option_gone_after_room_load = 0
    option_gone_after_map_load = 1
    option_gone_after_level_clear = 2
    option_gone_after_dying_once = 3
    option_gone_after_dying_twice = 4
    option_gone_after_dying_thrice = 5
    default = 0


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the level to become slippery
    """
    display_name = "Ice Trap Weight"


class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stuns Mario
    """
    display_name = "Stun Trap Weight"


class LiteratureTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the player to read literature
    """
    display_name = "Literature Trap Weight"


class TimerTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the timer to run low
    """
    display_name = "Timer Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the controls to be reversed in the current level
    """
    display_name = "Reverse Trap Weight"
    
    
class ThwimpTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a Thwimp to spawn above the player
    """
    display_name = "Thwimp Trap Weight"
    

class FishinBooTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes a Fishin' Boo to spawn above the player
    """
    display_name = "Fishin' Boo Trap Weight"


class Autosave(DefaultOnToggle):
    """
    Whether a save prompt will appear after every level
    """
    display_name = "Autosave"


class EarlyClimb(Toggle):
    """
    Force Climb to appear early in the seed as a local item.

    This is particularly useful to prevent BK when Level Shuffle is disabled
    """
    display_name = "Early Climb"


class OverworldSpeed(Choice):
    """
    How fast Mario moves on the overworld
    """
    display_name = "Overworld Speed"
    option_slow = 0
    option_vanilla = 1
    option_fast = 2
    default = 1


class MusicShuffle(Choice):
    """
    Music shuffle type

    None: No Music is shuffled

    Consistent: Each music track is consistently shuffled throughout the game

    Full: Each individual level has a random music track

    Singularity: The entire game uses one song for overworld and one song for levels
    """
    display_name = "Music Shuffle"
    option_none = 0
    option_consistent = 1
    option_full = 2
    option_singularity = 3
    default = 0


class SFXShuffle(Choice):
    """
    Shuffles almost every instance of sound effect playback

    Archipelago elements that play sound effects aren't randomized

    None: No SFX are shuffled

    Full: Each individual SFX call has a random SFX

    Singularity: The entire game uses one SFX for every SFX call
    """
    display_name = "Sound Effect Shuffle"
    option_none = 0
    option_full = 1
    option_singularity = 2
    default = 0


class MarioPalette(Choice):
    """
    Mario palette color
    """
    display_name = "Mario Palette"
    option_mario = 0
    option_luigi = 1
    option_wario = 2
    option_waluigi = 3
    option_geno = 4
    option_princess = 5
    option_dark = 6
    option_sponge = 7
    default = 0


class LevelPaletteShuffle(Choice):
    """
    Whether to shuffle level palettes

    Off: Do not shuffle palettes

    On Legacy: Uses only the palette sets from the original game

    On Curated: Uses custom, hand-crafted palette sets
    """
    display_name = "Level Palette Shuffle"
    option_off = 0
    option_on_legacy = 1
    option_on_curated = 2
    default = 0


class OverworldPaletteShuffle(Choice):
    """
    Whether to shuffle overworld palettes

    Off: Do not shuffle palettes

    On Legacy: Uses only the palette sets from the original game

    On Curated: Uses custom, hand-crafted palette sets
    """
    display_name = "Overworld Palette Shuffle"
    option_off = 0
    option_on_legacy = 1
    option_on_curated = 2
    default = 0


class StartingLifeCount(Range):
    """
    How many extra lives to start the game with
    """
    display_name = "Starting Life Count"
    range_start = 1
    range_end = 99
    default = 5


class EnergyLink(DefaultOnToggle):
    """
    Allows players to contribute to the EnergyLink pool by collecting coins

    Players can exchange EnergyLink coins for consumable items
    """
    display_name = "Energy Link"


smw_option_groups = [
    OptionGroup("Goal Options", [
        Goal,
        BossesRequired,
        NumberOfYoshiEggs,
        PercentageOfYoshiEggs,
    ]),
    OptionGroup("Sanity Options", [
        DragonCoinChecks,
        MoonChecks,
        Hidden1UpChecks,
        BonusBlockChecks,
        Blocksanity,
    ]),
    OptionGroup("Level Shuffling", [
        LevelShuffle,
        MapTeleportShuffle,
        MapTransitionShuffle,
        ExcludeSpecialZone,
        BowserCastleDoors,
        BowserCastleRooms,
        BossShuffle,
        SwapDonutGhostHouseExits,
    ]),
    OptionGroup("Junk and Traps", [
        InventoryFillPercentage,
        PersistentTrapBehavior,
        JunkFillPercentage,
        TrapFillPercentage,
        IceTrapWeight,
        StunTrapWeight,
        LiteratureTrapWeight,
        TimerTrapWeight,
        ReverseTrapWeight,
        ThwimpTrapWeight,
        FishinBooTrapWeight,
    ]),
    OptionGroup("Aesthetics", [
        DisplayReceivedItemPopups,
        BlockCollectBehavior,
        LocationVisualIndicator,
        Autosave,
        OverworldSpeed,
        MusicShuffle,
        SFXShuffle,
        MarioPalette,
        LevelPaletteShuffle,
        OverworldPaletteShuffle,
        StartingLifeCount,
    ]),
]


@dataclass
class SMWOptions(PerGameCommonOptions):
    death_link: DeathLink
    goal: Goal
    bosses_required: BossesRequired
    max_yoshi_egg_cap: NumberOfYoshiEggs
    percentage_of_yoshi_eggs: PercentageOfYoshiEggs
    dragon_coin_checks: DragonCoinChecks
    moon_checks: MoonChecks
    hidden_1up_checks: Hidden1UpChecks
    bonus_block_checks: BonusBlockChecks
    blocksanity: Blocksanity
    bowser_castle_doors: BowserCastleDoors
    bowser_castle_rooms: BowserCastleRooms
    level_shuffle: LevelShuffle
    map_teleport_shuffle: MapTeleportShuffle
    map_transition_shuffle: MapTransitionShuffle
    exclude_special_zone: ExcludeSpecialZone
    boss_shuffle: BossShuffle
    swap_donut_gh_exits: SwapDonutGhostHouseExits
    display_received_item_popups: DisplayReceivedItemPopups
    block_collect_behavior: BlockCollectBehavior
    location_visual_indicator: LocationVisualIndicator
    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    inventory_fill_percentage: InventoryFillPercentage
    persistent_trap_behavior: PersistentTrapBehavior
    ice_trap_weight: IceTrapWeight
    stun_trap_weight: StunTrapWeight
    literature_trap_weight: LiteratureTrapWeight
    timer_trap_weight: TimerTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    thwimp_trap_weight: ThwimpTrapWeight
    fishin_trap_weight: FishinBooTrapWeight
    autosave: Autosave
    early_climb: EarlyClimb
    overworld_speed: OverworldSpeed
    music_shuffle: MusicShuffle
    sfx_shuffle: SFXShuffle
    mario_palette: MarioPalette
    level_palette_shuffle: LevelPaletteShuffle
    overworld_palette_shuffle: OverworldPaletteShuffle
    starting_life_count: StartingLifeCount
    energy_link: EnergyLink
