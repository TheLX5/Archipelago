from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import MMX4World

def stage_access_count(state: CollectionState, player: int) -> int:
    count = 0;
    if state.has("Web Spider Stage Access", player):
        count = count + 1
    if state.has("Cyber Peacock Stage Access", player):
        count = count + 1    
    if state.has("Storm Owl Stage Access", player):
        count = count + 1
    if state.has("Magma Dragoon Stage Access", player):
        count = count + 1
    if state.has("Jet Stingray Stage Access", player):
        count = count + 1
    if state.has("Split Mushroom Stage Access", player):
        count = count + 1
    if state.has("Slash Beast Stage Access", player):
        count = count + 1
    if state.has("Frost Walrus Stage Access", player):
        count = count + 1
    return count

def set_rules(world: "MMX4World"):
    player = world.player
    options = world.options

    # Stage Access
    add_rule(world.multiworld.get_entrance("Stage Select -> Web Spider", player),
             lambda state: state.has("Web Spider Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Cyber Peacock", player),
             lambda state: state.has("Cyber Peacock Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Storm Owl", player),
             lambda state: state.has("Storm Owl Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Magma Dragoon", player),
             lambda state: state.has("Magma Dragoon Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Jet Stingray", player),
             lambda state: state.has("Jet Stingray Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Split Mushroom", player),
             lambda state: state.has("Split Mushroom Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Slash Beast", player),
             lambda state: state.has("Slash Beast Stage Access", player))
    add_rule(world.multiworld.get_entrance("Stage Select -> Frost Walrus", player),
             lambda state: state.has("Frost Walrus Stage Access", player))

    # Web Spider Locations
    add_rule(world.multiworld.get_location("Web Spider Heart Tank", player),
             lambda state: state.has("Rising Fire", player))

    # Cyber Peacock Locations
    add_rule(world.multiworld.get_location("Cyber Peacock Heart Tank", player),
             lambda state: state.has("Soul Body", player))
    add_rule(world.multiworld.get_location("Cyber Peacock Sub Tank", player),
             lambda state: state.has("Soul Body", player))
    add_rule(world.multiworld.get_location("Helmet Upgrade", player),
             lambda state: state.has("Soul Body", player))

    # Storm Owl Locations
    add_rule(world.multiworld.get_location("Arms Upgrade 1", player),
             lambda state: state.has("Lightning Web", player))
    add_rule(world.multiworld.get_location("Arms Upgrade 2", player),
             lambda state: state.has("Lightning Web", player))

    # Magma Dragoon
    add_rule(world.multiworld.get_location("Magma Dragoon Heart Tank", player),
             lambda state: state.has("Legs Upgrade", player) or state.has("Lightning Web", player))
    add_rule(world.multiworld.get_location("Body Upgrade", player),
             lambda state: state.has("Lightning Web", player) and state.has("Twin Slasher", player) and 
             (state.has("Plasma Shot Upgrade", player) or state.has("Stock Charge Upgrade", player)))

    # Split Mushroom
    add_rule(world.multiworld.get_location("Split Mushroom Heart Tank", player),
             lambda state: state.has("Lightning Web", player))

    # Frost Walrus
    add_rule(world.multiworld.get_location("Frost Walrus Heart Tank", player),
             lambda state: state.has("Rising Fire", player))
    add_rule(world.multiworld.get_location("Frost Walrus Extra Lives Tank", player),
             lambda state: state.has("Lightning Web", player))

    # Colonel Access
    add_rule(world.multiworld.get_location("Memorial Hall Colonel Defeated", player),
             lambda state: stage_access_count(state, player) >= 4)

    # Sigma Access
    add_rule(world.multiworld.get_entrance("Stage Select -> Space Port", player),
             lambda state: stage_access_count(state, player) >= 8)
    
    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)