from dataclasses import dataclass

from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, OptionSet, Visibility

from .stage_data import microgame_data, game_data

class IncludedStages(OptionSet):
    """
    Which stages will be added in the location pool.
    Can be left empty.

    Valid stages:
        - "Wario"
        - "Mona"
        - "Jimmy"
        - "Kat & Ana"
        - "Dribble & Spitz"
        - "Dr. Crygor"
        - "Orbulon"
        - "9-Volt"
        - "Wario-Man"
        - "Jimmy's Folks"
        - "WarioWatch"
        - "WarioWatch 2"
        - "Skyscraper"
        - "Tower"
        - "Mansion"
    """
    display_name = "Included Stages"
    valid_keys = [game.value for game in game_data.keys()]
    default = [game.value for game in game_data.keys()]


class StartingStage(OptionSet):
    """
    Which of the following stages will be chosen as a potential initial stage.
    The stage has to be in the pool in order to be chosen.
    Can be left empty.

    Valid stages:
        - "Wario"
        - "Mona"
        - "Jimmy"
        - "Kat & Ana"
        - "Dribble & Spitz"
        - "Dr. Crygor"
        - "Orbulon"
        - "9-Volt"
        - "Wario-Man"
        - "Jimmy's Folks"
        - "WarioWatch"
        - "WarioWatch 2"
        - "Skyscraper"
        - "Tower"
        - "Mansion"
    """
    display_name = "Starting Stage Pool"
    valid_keys = [game.value for game in game_data.keys()]
    default = [game.value for game in game_data.keys()]


class StartingMicrogames(Range):
    """
    How many individual microgames will be unlocked by default at the start.
    """
    display_name = "Starting Microgames Count"
    range_start = 4
    range_end = 20
    default = 4


class MicrogameUnlock(Choice):
    """
    How are microgames unlocked.
    * Bundles: Character bundles are added into the pool which unlocks the corresponding set of games
    * Individual: Unlocks for individual microgames are added into the pool
    """
    display_name = "Microgame Unlock"
    option_bundles = 0
    option_individual = 1
    default = 0


class MicrogameCount(Range):
    """
    How many microgames will be considered locations. Selected at random.
    Unselected microgames will not be unlocked.
    At least 2 microgames will be forced per stage and the selection will remain relatively equal across stages.
    """
    display_name = "Microgame Count"
    range_start = 20
    range_end = 223
    default = 40


class ExcludedMicrogames(OptionSet):
    """
    Which microgames will not be considered in the random selection of microgames for the current session.
    """
    display_name = "Excluded Microgames"
    default = []
    valid_keys = [microgame.value for microgame in microgame_data.keys()]


class Crowns(Range):
    """
    How many crowns are placed in the item pool.
    Crowns are used to allow you to goal the game which is done by selecting the credits level.
    """
    display_name = "Crowns"
    range_start = 1
    range_end = 50
    default = 30


class CrownsRequired(Range):
    """
    Percentage of crowns required to finish the game.
    Result is floored with a minimum of 1.
    """
    display_name = "Crowns Required"
    range_start = 1
    range_end = 100
    default = 75


class MicrogameCrowns(Toggle):
    """
    Enable getting crowns (Hi-Scores) in microgames as valid locations.
    By default every microgame has a location when getting 3 or more score points.
    """
    display_name = "Microgame Crowns"


class StageHiScores(Toggle):
    """
    Enables additional Hi-Score locations for character games.
    These WILL require playing the game again after beating it! May be a nuisance.
    """
    display_name = "Stage Hi-Scores"


@dataclass
class WarioTwistedOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    included_stages: IncludedStages
    starting_stage: StartingStage
    microgame_unlock: MicrogameUnlock
    crowns: Crowns
    crowns_required: CrownsRequired
    starting_microgames: StartingMicrogames
    excluded_microgames: ExcludedMicrogames
    microgame_crowns: MicrogameCrowns
    microgame_count: MicrogameCount
    stage_hi_scores: StageHiScores