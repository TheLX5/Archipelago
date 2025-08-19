from typing import Dict, TYPE_CHECKING
import logging

from .Types import LocData

if TYPE_CHECKING:
    from . import MMX4World

def did_include_pickup_locations(world: "MMX4World") -> bool:
    return bool(world.options.pickupsanity)

def get_total_locations(world: "MMX4World") -> int:
    total = 0
    for name in location_table:
        if not did_include_pickup_locations(world) and name in pickup_locations:
            continue

        if is_valid_location(world, name):
            total += 1

    return total

def get_location_names() -> Dict[str, int]:
    names = {name: data.ap_code for name, data in location_table.items()}
    return names

def is_valid_location(world: "MMX4World", name) -> bool:
    if not did_include_pickup_locations(world) and name in pickup_locations:
        return False
    return True

mmx4_locations = {
    # Intro
    "Intro Boss Defeated": LocData(14574100, "Intro Stage"),   
    "Intro Stage Completed": LocData(14574101, "Intro Stage"),   
    # Web Spider
    "Legs Upgrade": LocData(14574102, "Web Spider"),   
    "Web Spider Heart Tank": LocData(14574103, "Web Spider"),   
    "Web Spider Defeated": LocData(14574104, "Web Spider"),   
    "Web Spider Weapon": LocData(14574105, "Web Spider"),   
    # Cyber Peacock
    "Cyber Peacock Heart Tank": LocData(14574106, "Cyber Peacock"),   
    "Cyber Peacock Sub Tank": LocData(14574107, "Cyber Peacock"),   
    "Helmet Upgrade": LocData(14574108, "Cyber Peacock"),   
    "Cyber Peacock Defeated": LocData(14574109, "Cyber Peacock"),   
    "Cyber Peacock Weapon": LocData(14574110, "Cyber Peacock"),  
    # Storm Owl
    "Storm Owl Heart Tank": LocData(14574111, "Storm Owl"),  
    "Arms Upgrade 1": LocData(14574112, "Storm Owl"),  
    "Arms Upgrade 2": LocData(14574113, "Storm Owl"),  
    "Storm Owl Defeated": LocData(14574114, "Storm Owl"),  
    "Storm Owl Weapon": LocData(14574115, "Storm Owl"),  
    # Magma Dragoon
    "Magma Dragoon Heart Tank": LocData(14574116, "Magma Dragoon"),  
    "Body Upgrade": LocData(14574117, "Magma Dragoon"),  
    "Magma Dragoon Defeated": LocData(14574118, "Magma Dragoon"),  
    "Magma Dragoon Weapon": LocData(14574119, "Magma Dragoon"),  
    # Jet Stingray
    "Jet Stingray Heart Tank": LocData(14574120, "Jet Stingray"),  
    "Jet Stingray Sub Tank": LocData(14574121, "Jet Stingray"),  
    "Jet Stingray Defeated": LocData(14574122, "Jet Stingray"),  
    "Jet Stingray Weapon": LocData(14574123, "Jet Stingray"),  
    # Split Mushroom
    "Split Mushroom Heart Tank": LocData(14574124, "Split Mushroom"),  
    "Split Mushroom Defeated": LocData(14574125, "Split Mushroom"),  
    "Split Mushroom Weapon": LocData(14574126, "Split Mushroom"),  
    # Slash Beast
    "Slash Beast Heart Tank": LocData(14574127, "Slash Beast"),  
    "Slash Beast Defeated": LocData(14574128, "Slash Beast"),  
    "Slash Beast Weapon": LocData(14574129, "Slash Beast"),  
    # Frost Walrus
    "Frost Walrus Heart Tank": LocData(14574130, "Frost Walrus"),  
    "Frost Walrus Extra Lives Tank": LocData(14574131, "Frost Walrus"),  
    "Frost Walrus Weapon Tank": LocData(14574132, "Frost Walrus"),  
    "Frost Walrus Defeated": LocData(14574133, "Frost Walrus"),  
    "Frost Walrus Weapon": LocData(14574134, "Frost Walrus"), 
    # Special / End Stages
    "Memorial Hall Colonel Defeated": LocData(14574135, "Memorial Hall"),  
    "Space Port Colonel Defeated": LocData(14574136, "Space Port"),  
    "Double / Iris Defeated": LocData(14574137, "Final Weapon 1"),  
    "General Defeated": LocData(14574138, "Final Weapon 1"),  
    "Web Spider Rematch Defeated": LocData(14574139, "Final Weapon 2"),  
    "Cyber Peacock Rematch Defeated": LocData(14574140, "Final Weapon 2"),  
    "Storm Owl Rematch Defeated": LocData(14574141, "Final Weapon 2"),  
    "Magma Dragoon Rematch Defeated": LocData(14574142, "Final Weapon 2"),  
    "Jet Stingray Rematch Defeated": LocData(14574143, "Final Weapon 2"),  
    "Split Mushroom Rematch Defeated": LocData(14574144, "Final Weapon 2"),  
    "Slash Beast Rematch Defeated": LocData(14574145, "Final Weapon 2"),  
    "Frost Walrus Rematch Defeated": LocData(14574146, "Final Weapon 2"),  
}

pickup_locations = {
    "Intro Stage Life Energy (1)": LocData(14574200, "Intro Stage"),
    "Intro Stage Max Life Energy (1)": LocData(14574201, "Intro Stage"),
    "Intro Stage 1 Up (1)": LocData(14574202, "Intro Stage"),
    "Web Spider Life Energy (1)": LocData(14574203, "Web Spider"),
    "Web Spider Max Life Energy (1)": LocData(14574204, "Web Spider"),
    "Storm Owl Life Energy (1)": LocData(14574205, "Storm Owl"),
    "Storm Owl Max Life Energy (1)": LocData(14574206, "Storm Owl"),
    "Magma Dragoon Life Energy (1)": LocData(14574207, "Magma Dragoon"),
    "Magma Dragoon Life Energy (2)": LocData(14574208, "Magma Dragoon"),
    "Magma Dragoon Life Energy (3)": LocData(14574209, "Magma Dragoon"),
    "Jet Stingray Max Life Energy (1)": LocData(14574210, "Jet Stingray"),
    "Split Mushroom Life Energy (1)": LocData(14574211, "Split Mushroom"),
    "Split Mushroom Weapon Energy (1)": LocData(14574212, "Split Mushroom"),
    "Slash Beast Max Life Energy (1)": LocData(14574213, "Slash Beast"),
    "Frost Walrus Weapon Energy (1)": LocData(14574214, "Frost Walrus"),
    "Frost Walrus Weapon Energy (2)": LocData(14574215, "Frost Walrus"),
    "Frost Walrus Life Energy (1)": LocData(14574216, "Frost Walrus"),
    "Frost Walrus Life Energy (2)": LocData(14574217, "Frost Walrus"),
    "Frost Walrus 1 Up (1)": LocData(14574218, "Frost Walrus"),
    "Frost Walrus Life Energy (3)": LocData(14574219, "Frost Walrus"),
    "Frost Walrus Life Energy (4)": LocData(14574220, "Frost Walrus"),
    "Frost Walrus Life Energy (5)": LocData(14574221, "Frost Walrus"),
    "Frost Walrus Life Energy (6)": LocData(14574222, "Frost Walrus"),
    "Frost Walrus Life Energy (7)": LocData(14574223, "Frost Walrus"),
    "Frost Walrus Life Energy (8)": LocData(14574224, "Frost Walrus"),
    "Frost Walrus 1 Up (2)": LocData(14574225, "Frost Walrus"),
    "Frost Walrus Max Life Energy (1)": LocData(14574226, "Frost Walrus"),
    "Frost Walrus Max Weapon Energy (1)": LocData(14574227, "Frost Walrus"),
    "Final Weapon Life Energy (1)": LocData(14574228, "Final Weapon 1"),
    "Final Weapon Max Life Energy (1)": LocData(14574229, "Final Weapon 1"),
    "Final Weapon Max Life Energy (2)": LocData(14574230, "Final Weapon 1"),
    "Final Weapon Max Life Energy (3)": LocData(14574231, "Final Weapon 2"),
    "Final Weapon Life Energy (2)": LocData(14574232, "Final Weapon 2"),
    "Final Weapon Life Energy (Boss Rush)": LocData(14574233, "Final Weapon 2"),
    "Final Weapon Weapon Energy (Boss Rush)": LocData(14574234, "Final Weapon 2"),
    "Final Weapon Max Life Energy (4)": LocData(14574235, "Final Weapon 2"),
    "Final Weapon Max Weapon Energy (1)": LocData(14574236, "Final Weapon 2"),
    "Final Weapon Life Energy (3)": LocData(14574237, "Final Weapon 2"),
}

event_locations = {
    "Sigma Defeated": LocData(14574300, "Final Weapon 2"),
}

location_table = {
    **mmx4_locations,
    **pickup_locations,
    **event_locations
}