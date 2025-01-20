from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, Toggle, DefaultOnToggle, OptionSet, OptionList, OptionDict, PerGameCommonOptions, StartInventoryPool, DeathLink, Visibility
from schema import Schema, Optional


@dataclass
class PerfectDarkOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool