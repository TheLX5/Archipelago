from typing import List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

@dataclass
class MMX4Options(PerGameCommonOptions):
    pickupsanity: PickupSanity

option_groups: Dict[str, List[Any]] = {
    "General Options": [PickupSanity],
    #"Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
}