from dataclasses import dataclass

from Options import Choice, Range, Toggle, DefaultOnToggle, OptionDict, OptionSet, OptionGroup, PerGameCommonOptions, StartInventoryPool
from .enums import Items

class Medals(Range):
    """
    How many medals are placed in the item pool
    """
    display_name = "Medals"
    range_start = 1
    range_end = 40
    default = 40

class MedalsRequired(Range):
    """
    Percentage of medals required to finish the game. Result is floored with a minimum of 1.
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

rha_option_groups = [
]

@dataclass
class RHAOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    medals: Medals
    medals_required: MedalsRequired
    superbs: Superbs
    perfects: Perfects
