from typing import Mapping, Iterator, List, Dict, Any
from dataclasses import dataclass
from worlds.AutoWorld import PerGameCommonOptions
from Options import Choice, OptionGroup, Toggle, Range, StartInventoryPool, ItemDict, DeathLink, DefaultOnToggle

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list

class Character(Choice):
    """
    Choose which character you'd like to play as during your seed
    NOTE: If Zero, certain locations are excluded to prevent unbeatable seeds.
    """
    display_name = "Character"
    option_x = 0
    option_zero = 1
    default = 0


class EnergyLink(DefaultOnToggle):
    """
    Enable EnergyLink support. When enabled, the client can spend EnergyLink to restore current HP.
    """
    display_name = "Energy Link"


class DamageLink(Toggle):
    """
    Share damage with other players through DamageLink.
    """
    display_name = "Damage Link"


class EnergyLinkAutoHeal(DefaultOnToggle):
    """
    Automatically spend EnergyLink to heal missing HP during gameplay.
    """
    display_name = "Energy Link Auto Heal"


class EnergyLinkCostPerHP(Range):
    """
    EnergyLink cost for each HP point restored by auto heal.
    """
    display_name = "Energy Link Cost Per HP"
    range_start = 1
    range_end = 100
    default = 5

class PickupSanity(Toggle):
    """
    Whether collecting freestanding 1ups, HP and Weapon Energy capsules will grant a check.
    """
    display_name = "Pickupsanity"

class EnableBossItemRequirements(Toggle):
    """
    Whether to enable item requirements for bosses
    """
    display_name = "Enable Boss Item Requirements"


class WebSpiderRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Web Spider
    for example: { Twin Slasher: 1, Heart Tank: 2 }
    """

    display_name = "Web Spider Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class CyberPeacockRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Cyber Peacock
    for example: { Soul Body: 1, Heart Tank: 2 }
    """

    display_name = "Cyber Peacock Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class StormOwlRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Storm Owl
    for example: { Aiming Laser: 1, Heart Tank: 2 }
    """

    display_name = "Storm Owl Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class MagmaDragoonRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Magma Dragoon
    for example: { Double Cyclone: 1, Heart Tank: 2 }
    """

    display_name = "Magma Dragoon Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class JetStingrayRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Jet Stingray
    for example: { Frost Tower: 1, Heart Tank: 2 }
    """

    display_name = "Jet Stingray Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class SplitMushroomRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Split Mushroom
    for example: { Lightning Web: 1, Heart Tank: 2 }
    """

    display_name = "Split Mushroom Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class SlashBeastRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Slash Beast
    for example: { Ground Hunter: 1, Heart Tank: 2 }
    """

    display_name = "Slash Beast Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class FrostWalrusRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Frost Walrus
    for example: { Rising Fire: 1, Heart Tank: 2 }
    """

    display_name = "Frost Walrus Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class DoubleIrisRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Double/Iris
    for example: { Rising Fire: 1, Heart Tank: 4 }
    """

    display_name = "Double/Iris Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class GeneralRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat General
    for example: { Soul Body: 1, Heart Tank: 4 }
    """

    display_name = "General Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

class SigmaRequirement(ItemDict, Mapping[str, int]):
    """
    A list of items required in logic to beat Sigma
    Rising Fire is already required by default
    for example: { Ground Hunter: 1, Soul Body: 1, Lightning Web: 1, Heart Tank: 8 }
    """

    display_name = "Sigma Requirement"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()

# making this mixin so we can keep actual game options separate from AP core options that we want enabled
# not sure why this isn't a mixin in core atm, anyways
@dataclass
class StartInventoryFromPoolMixin:
    start_inventory_from_pool: StartInventoryPool

@dataclass
class MMX4Options(StartInventoryFromPoolMixin, PerGameCommonOptions):
    pickupsanity: PickupSanity
    character: Character
    death_link: DeathLink
    damage_link: DamageLink
    energy_link: EnergyLink
    energy_link_auto_heal: EnergyLinkAutoHeal
    energy_link_cost_per_hp: EnergyLinkCostPerHP

    enable_boss_item_requirements: EnableBossItemRequirements
    web_spider_requirement: WebSpiderRequirement
    cyber_peacock_requirement: CyberPeacockRequirement
    storm_owl_requirement: StormOwlRequirement
    magma_dragoon_requirement: MagmaDragoonRequirement
    jet_stingray_requirement: JetStingrayRequirement
    split_mushroom_requirement: SplitMushroomRequirement
    slash_beast_requirement: SlashBeastRequirement
    frost_walrus_requirement: FrostWalrusRequirement

    double_iris_requirement: DoubleIrisRequirement
    general_requirement: GeneralRequirement
    sigma_requirement: SigmaRequirement

option_groups: Dict[str, List[Any]] = {
    "General Options": [PickupSanity, Character],
    "Link Options": [DeathLink, DamageLink, EnergyLink, EnergyLinkAutoHeal, EnergyLinkCostPerHP],
    #"Trap Options": [TrapChance, ForcefemTrapWeight, SpeedChangeTrapWeight]
}