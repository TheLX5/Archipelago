from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionSet, PerGameCommonOptions, StartInventoryPool

class Patches(OptionSet):
    """
    Which sets of patches you'd like to see applied:
    * Plus: Adds a lot of changes to "modernize" the game
    * SFX: Enables english localization to various audio files in the game
    """
    display_name = "Patches"
    valid_keys = [
        "Plus",
        "SFX",
    ]
    default = [
        "Plus",
        "SFX",
    ]


class LevelUnlock(Choice):
    """
    How are levels unlocked.
    * Bundles: Remix bundles are added into the pool which unlocks the corresponding column
    * Individual: Unlocks for individual levels are added into the pool
    """
    display_name = "Level Unlock"
    option_bundles = 0
    option_individual = 1
    default = 0


class Medals(Range):
    """
    How many medals are placed in the item pool.
    Medals are used to allow you to goal the game which is done by selecting the credits level.
    """
    display_name = "Medals"
    range_start = 1
    range_end = 40
    default = 40


class MedalsRequired(Range):
    """
    Percentage of medals required to finish the game.
    Result is floored with a minimum of 1.
    """
    display_name = "Medals"
    range_start = 1
    range_end = 100
    default = 75


class Superbs(DefaultOnToggle):
    """
    Enable getting Superb as locations.
    """
    display_name = "Superbs"


class Perfects(Toggle):
    """
    Enable getting Perfect as locations.
    """
    display_name = "Perfects"


@dataclass
class RHAOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    patches: Patches
    level_unlock: LevelUnlock
    medals: Medals
    medals_required: MedalsRequired
    superbs: Superbs
    perfects: Perfects
