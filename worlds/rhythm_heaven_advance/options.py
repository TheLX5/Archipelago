from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionDict, OptionSet, OptionGroup, PerGameCommonOptions, StartInventoryPool
from .enums import Items

class Medals(Range):
    """
    How many medals are needed to activete the credits level and finish the game
    """
    display_name = "Medals"
    range_start = 1
    range_end = 50
    default = 30

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

rha_option_groups = [
]

@dataclass
class RHAOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    medals: Medals
    superbs: Superbs
    perfects: Perfects
