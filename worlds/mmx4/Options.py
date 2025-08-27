from dataclasses import dataclass
from Options import Choice, OptionGroup, Toggle, Range, PerGameCommonOptions

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

@dataclass
class MMX4Options(PerGameCommonOptions):
    pickupsanity: PickupSanity


mmx4_option_groups = [
    OptionGroup("General Options", [
        PickupSanity,
    ]),
    #OptionGroup("Trap Options", [
    #    TrapChance,
    #    ForcefemTrapWeight,
    #    SpeedChangeTrapWeight,
    #]),
]