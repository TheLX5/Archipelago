from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, Visibility, PerGameCommonOptions, StartInventoryPool

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


class TempoUp(Toggle):
    """
    Enables Tempo Up! songs from the arcade version of Tengoku.
    """
    display_name = "Tempo Up Songs"
    visibility = Visibility.spoiler


class PatchPlus(DefaultOnToggle):
    """
    Enables several quality of life changes.

    List of Quality of Life changes: https://thelx5.github.io/rha/index.html#versions-plus
    """
    display_name = "PLUS Patch"


class DefaultVoices(Choice):
    """
    Which language will be used for voice clips. Can be toggled in-game.
    """
    display_name = "Voice Language"
    option_japanese = 0x00
    option_english = 0x01
    default = option_english


class DefaultMusic(Choice):
    """
    Which language will be used for songs with lyrics. Can be toggled in-game.
    """
    display_name = "Music Language"
    option_japanese = 0x00
    option_english = 0x02
    default = option_english


@dataclass
class RHAOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    level_unlock: LevelUnlock
    medals: Medals
    medals_required: MedalsRequired
    superbs: Superbs
    perfects: Perfects
    tempo_up: TempoUp
    patch_plus: PatchPlus
    default_voices: DefaultVoices
    default_music: DefaultMusic
