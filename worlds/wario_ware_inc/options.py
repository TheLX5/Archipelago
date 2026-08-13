from dataclasses import dataclass

from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, OptionSet

from .enums import Items

class IncludedStages(OptionSet):
    """
    Which stages will be added in the location pool.
    Introduction stage is unlocked by default and can't be toggled off.

    Valid stages:
        - "Jimmy"
        - "Dribble"
        - "Mona"
        - "9-Volt"
        - "Remix 1"
        - "Orbulon"
        - "Dr. Crygor"
        - "Kat"
        - "Remix 2"
        - "Wario"
        - "Easy"
        - "Thrilling"
        - "Hard"
        - "Total Boss"
        - "Sheriff"
        - "Dr. Wario"
        - "Fly Swatter"
        - "Pyoro"
        - "Pyoro 2"
        - "Jump Forever"
        - "Paper Plane"
        - "Skating Board"
    """
    display_name = "Included Stages"
    valid_keys = [
        Items.jimmy.value,
        Items.dribble.value,
        Items.mona.value,
        Items.nine_volt.value,
        Items.remix_1.value,
        Items.orbulon.value,
        Items.crygor.value,
        Items.kat.value,
        Items.remix_2.value,
        Items.wario.value,
        Items.easy.value,
        Items.thrilling.value,
        Items.hard.value,
        Items.total_boss.value,
        Items.sheriff_stage.value,
        Items.dr_wario.value,
        Items.fly_swatter.value,
        Items.pyoro.value,
        Items.pyoro_2.value,
        Items.jump_forever.value,
        Items.paper_plane_stage.value,
        Items.skating_board.value,
    ]
    default = [
        Items.jimmy.value,
        Items.dribble.value,
        Items.mona.value,
        Items.nine_volt.value,
        Items.remix_1.value,
        Items.orbulon.value,
        Items.crygor.value,
        Items.kat.value,
        Items.remix_2.value,
        Items.wario.value,
        Items.easy.value,
        Items.thrilling.value,
        Items.hard.value,
        Items.total_boss.value,
        Items.sheriff_stage.value,
        Items.dr_wario.value,
        Items.fly_swatter.value,
        Items.pyoro.value,
        Items.pyoro_2.value,
        Items.jump_forever.value,
        Items.paper_plane_stage.value,
        Items.skating_board.value,
    ]


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
    At least 4 microgames will be forced per group and the selection will remain relatively equal across groups.
    """
    display_name = "Microgame Count"
    range_start = 18
    range_end = 213
    default = 36


class Flowers(Range):
    """
    How many medals are placed in the item pool.
    Flowers are used to allow you to goal the game which is done by selecting the credits level.
    """
    display_name = "Flowers"
    range_start = 1
    range_end = 50
    default = 30


class FlowersRequired(Range):
    """
    Percentage of medals required to finish the game.
    Result is floored with a minimum of 1.
    """
    display_name = "Medals"
    range_start = 1
    range_end = 100
    default = 75


class MicrogameFlowers(Toggle):
    """
    Enable getting flowers (Hi-Scores) in microgames as valid locations.
    By default every microgame has a location when getting 5 or more score points.
    """
    display_name = "Microgame Flowers"


class StageHiScores(Toggle):
    """
    Enables additional Hi-Score locations for character games.
    These WILL require playing the game again after beating it! May be a nuisance.
    """
    display_name = "Stage Hi-Scores"


@dataclass
class WarioWareOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    included_stages: IncludedStages
    microgame_unlock: MicrogameUnlock
    flowers: Flowers
    flowers_required: FlowersRequired
    microgame_flowers: MicrogameFlowers
    microgame_count: MicrogameCount
    stage_hi_scores: StageHiScores