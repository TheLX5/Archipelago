import typing
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import PDItem, item_table, weapons, gadgets, missions
from .Locations import setup_locations, all_locations, location_groups
from .Regions import create_regions, connect_regions
from .Names import ItemName, LocationName
from .Options import PerfectDarkOptions
from .Rules import PerfectDarkRules


class PerfectDarkWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Perfect Dark with Archipelago",
        "English",
        "setup_en.md",
        "setup/en",
        ["lx5"]
    )

    tutorials = [setup_en]

    #option_groups = metroid_dread_option_groups


class PerfectDarkWorld(World):
    """
    Perfect Dark WIP
    """
    game = "Perfect Dark"
    web = PerfectDarkWeb()

    options_dataclass = PerfectDarkOptions
    options: PerfectDarkOptions
    
    required_client_version = (0, 5, 1)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations
    #item_name_groups = item_groups
    location_name_groups = location_groups
    hint_blacklist = {}

    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    def create_regions(self) -> None:
        location_table = setup_locations(self)
        create_regions(self, location_table)

        itempool: typing.List[PDItem] = []
        
        connect_regions(self)
        
        total_required_locations = 176

        for weapon in weapons.keys():
            itempool.append(self.create_item(weapon))

        for gadget in gadgets.keys():
            itempool.append(self.create_item(gadget))

        for mission in missions.keys():
            itempool.append(self.create_item(mission))

        itempool += [self.create_item(ItemName.shields) for _ in range(2)]
        itempool += [self.create_item(ItemName.health) for _ in range(2)]
        itempool += [self.create_item(ItemName.secondary_action)]
        itempool += [self.create_item(ItemName.akimbo_weapons)]
        itempool += [self.create_item(ItemName.hurricane_fists)]
        itempool += [self.create_item(ItemName.start_slots) for _ in range(4)]
        itempool += [self.create_item(ItemName.starting_ammo) for _ in range(24)]
        
        junk_count = total_required_locations - len(itempool)

        junk_weights = []
        junk_weights += ([ItemName.hp_refill] * 30)
        junk_weights += ([ItemName.pistol_ammo] * 20)
        junk_weights += ([ItemName.magnum_ammo] * 10)
        junk_weights += ([ItemName.smg_ammo] * 20)
        junk_weights += ([ItemName.rifle_ammo] * 20)
        junk_weights += ([ItemName.shotgun_ammo] * 10)
        junk_weights += ([ItemName.bolt_ammo] * 5)
        junk_weights += ([ItemName.farsight_ammo] * 5)
        junk_weights += ([ItemName.grenade_ammo] * 5)
        junk_weights += ([ItemName.rocket_ammo] * 5)
        junk_weights += ([ItemName.sedative_ammo] * 5)
        junk_weights += ([ItemName.n_bomb_ammo] * 10)

        junk_pool = [self.create_item(self.random.choice(junk_weights)) for _ in range(junk_count)]
        
        itempool += junk_pool

        # Finish
        self.multiworld.itempool += itempool


    def create_item(self, name: str, force_classification=False) -> PDItem:
        data = item_table[name]

        if force_classification:
            classification = force_classification
        else:
            classification = data.classsification
        
        created_item = PDItem(name, classification, data.code, self.player)

        return created_item


    def interpret_slot_data(self, slot_data):
        return slot_data
    

    def set_rules(self):
        PerfectDarkRules(self).set_pd_rules()


    def fill_slot_data(self):
        slot_data = {}
        return slot_data


    def generate_early(self):
        pass


    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        pass


    def get_filler_item_name(self) -> str:
        pass


    def generate_output(self, output_directory: str):
        pass

