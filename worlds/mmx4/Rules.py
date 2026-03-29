import typing
from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, forbid_item
from typing import TYPE_CHECKING

from .Options import MMX4Options
from .Locations import did_include_pickup_locations

if TYPE_CHECKING:
    from . import MMX4World

def stage_access_count(state: CollectionState, options: MMX4Options, player: int) -> int:
    count = 0;
    if can_beat_web_spider(state, options, player):
        count = count + 1
    if can_beat_cyber_peacock(state, options, player):
        count = count + 1
    if can_beat_strom_owl(state, options, player):
        count = count + 1
    if can_beat_magma_dragoon(state, options, player):
        count = count + 1
    if can_beat_jet_stingray(state, options, player):
        count = count + 1
    if can_beat_split_mushroom(state, options, player):
        count = count + 1
    if can_beat_slash_beast(state, options, player):
        count = count + 1
    if can_beat_frost_walrus(state, options, player):
        count = count + 1
    return count

def is_zero(world: "MMX4World") -> bool:
    return getattr(world.options.character, "value", world.options.character) == 1

def can_beat_web_spider(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Web Spider Stage Access", player) and state.has_all_counts(options.web_spider_requirement, player);
    else:
        return state.has("Web Spider Stage Access", player)

def can_beat_cyber_peacock(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Cyber Peacock Stage Access", player) and state.has_all_counts(options.cyber_peacock_requirement, player);
    else:
        return state.has("Cyber Peacock Stage Access", player)

def can_beat_strom_owl(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Storm Owl Stage Access", player) and state.has_all_counts(options.storm_owl_requirement, player);
    else:
        return state.has("Storm Owl Stage Access", player)

def can_beat_magma_dragoon(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Magma Dragoon Stage Access", player) and state.has_all_counts(options.magma_dragoon_requirement, player);
    else:
        return state.has("Magma Dragoon Stage Access", player)

def can_beat_jet_stingray(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Jet Stingray Stage Access", player) and state.has_all_counts(options.jet_stingray_requirement, player);
    else:
        return state.has("Jet Stingray Stage Access", player)

def can_beat_split_mushroom(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Split Mushroom Stage Access", player) and state.has_all_counts(options.split_mushroom_requirement, player);
    else:
        return state.has("Split Mushroom Stage Access", player)

def can_beat_slash_beast(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Slash Beast Stage Access", player) and state.has_all_counts(options.slash_beast_requirement, player);
    else:
        return state.has("Slash Beast Stage Access", player)

def can_beat_frost_walrus(state: CollectionState, options: MMX4Options, player: int) -> bool:
    if(bool(options.enable_boss_item_requirements)):
        return state.has("Frost Walrus Stage Access", player) and state.has_all_counts(options.frost_walrus_requirement, player);
    else:
        return state.has("Frost Walrus Stage Access", player)

def can_beat_double_iris(state: CollectionState, options: MMX4Options, player: int) -> bool:
    return state.has_all_counts(options.double_iris_requirement, player);

def can_beat_general(state: CollectionState, options: MMX4Options, player: int) -> bool:
    return state.has_all_counts(options.general_requirement, player);

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

    # Maverick Requirements
    if(bool(options.enable_boss_item_requirements)):
        add_rule(world.multiworld.get_location("Web Spider Defeated", player),
                 lambda state: can_beat_web_spider(state, options, player))
        add_rule(world.multiworld.get_location("Cyber Peacock Defeated", player),
                 lambda state: can_beat_cyber_peacock(state, options, player))
        add_rule(world.multiworld.get_location("Storm Owl Defeated", player),
                 lambda state: can_beat_strom_owl(state, options, player))
        add_rule(world.multiworld.get_location("Magma Dragoon Defeated", player),
                 lambda state: can_beat_magma_dragoon(state, options, player))
        add_rule(world.multiworld.get_location("Jet Stingray Defeated", player),
                 lambda state: can_beat_jet_stingray(state, options, player))
        add_rule(world.multiworld.get_location("Split Mushroom Defeated", player),
                 lambda state: can_beat_split_mushroom(state, options, player))
        add_rule(world.multiworld.get_location("Slash Beast Defeated", player),
                 lambda state: can_beat_slash_beast(state, options, player))
        add_rule(world.multiworld.get_location("Frost Walrus Defeated", player),
                 lambda state: can_beat_frost_walrus(state, options, player))
        add_rule(world.multiworld.get_location("Web Spider Weapon", player),
                 lambda state: can_beat_web_spider(state, options, player))
        add_rule(world.multiworld.get_location("Cyber Peacock Weapon", player),
                 lambda state: can_beat_cyber_peacock(state, options, player))
        add_rule(world.multiworld.get_location("Storm Owl Weapon", player),
                 lambda state: can_beat_strom_owl(state, options, player))
        add_rule(world.multiworld.get_location("Magma Dragoon Weapon", player),
                 lambda state: can_beat_magma_dragoon(state, options, player))
        add_rule(world.multiworld.get_location("Jet Stingray Weapon", player),
                 lambda state: can_beat_jet_stingray(state, options, player))
        add_rule(world.multiworld.get_location("Split Mushroom Weapon", player),
                 lambda state: can_beat_split_mushroom(state, options, player))
        add_rule(world.multiworld.get_location("Slash Beast Weapon", player),
                 lambda state: can_beat_slash_beast(state, options, player))
        add_rule(world.multiworld.get_location("Frost Walrus Weapon", player),
                 lambda state: can_beat_frost_walrus(state, options, player))

    # Zero Specific Locations that shouldn't exist if chosen as the character to play as, otherwise they get added to the pool
    if not is_zero(world):

        # Cyber Peacock
        add_rule(world.multiworld.get_location("Cyber Peacock Heart Tank", player),
                 lambda state: state.has("Soul Body", player))
        add_rule(world.multiworld.get_location("Cyber Peacock Sub Tank", player),
                 lambda state: state.has("Soul Body", player))

        # Magma Dragoon
        add_rule(world.multiworld.get_location("Body Upgrade", player),
                 lambda state: state.has("Lightning Web", player)
                 and state.has("Twin Slasher", player)
                 and (state.has("Plasma Shot Upgrade", player) or state.has("Stock Charge Upgrade", player)))

    elif did_include_pickup_locations(world):
        # Zero cannot damage the Intro boss if Soul Body is acquired early
        # so we limit Soul Body to local only and restrict from being on the Intro Stage pickups :/ Thanks Capcom
        for location_name in (
            "Intro Stage Life Energy (1)",
            "Intro Stage Max Life Energy (1)",
            "Intro Stage 1 Up (1)",
        ):
            forbid_item(world.multiworld.get_location(location_name, player), "Soul Body", player)

    # Web Spider Locations
    add_rule(world.multiworld.get_location("Web Spider Heart Tank", player),
             lambda state: state.has("Rising Fire", player))

    # Magma Dragoon
    add_rule(world.multiworld.get_location("Magma Dragoon Heart Tank", player),
             lambda state: state.has("Legs Upgrade", player) or state.has("Lightning Web", player))

    # Split Mushroom
    add_rule(world.multiworld.get_location("Split Mushroom Heart Tank", player),
             lambda state: state.has("Lightning Web", player))

    # Frost Walrus
    add_rule(world.multiworld.get_location("Frost Walrus Heart Tank", player),
             lambda state: state.has("Rising Fire", player))
    add_rule(world.multiworld.get_location("Frost Walrus Extra Lives Tank", player),
         (lambda state: state.has("Soul Body", player)) if is_zero(world)
         else (lambda state: state.has("Lightning Web", player)))

    # Storm Owl
    add_rule(world.multiworld.get_location("Arms Upgrade 1", player),
             (lambda state: state.has("Soul Body", player)) if is_zero(world)
             else (lambda state: state.has("Lightning Web", player)))
    add_rule(world.multiworld.get_location("Arms Upgrade 2", player),
             (lambda state: state.has("Soul Body", player)) if is_zero(world)
             else (lambda state: state.has("Lightning Web", player)))

    # Cyber Peacock
    add_rule(world.multiworld.get_location("Helmet Upgrade", player),
             lambda state: state.has("Soul Body", player))

    # Colonel Access
    colonel_rule = (lambda state: stage_access_count(state, options, player) >= 8) if is_zero(world) \
                    else (lambda state: stage_access_count(state, options, player) >= 4)

    if not is_zero(world):  # because Zero excludes Memorial Hall entirely
        add_rule(world.multiworld.get_location("Memorial Hall Colonel Defeated", player), colonel_rule)

    add_rule(world.multiworld.get_location("Space Port Colonel Defeated", player), colonel_rule)

    # Double/Iris and General
    if(bool(options.enable_boss_item_requirements)):
        add_rule(world.multiworld.get_location("Double / Iris Defeated", player),
                 lambda state: can_beat_double_iris(state, options, player))
        add_rule(world.multiworld.get_location("General Defeated", player),
                 lambda state: can_beat_double_iris(state, options, player) and can_beat_general(state, options, player))
        add_rule(world.multiworld.get_entrance("Final Weapon 1 -> Final Weapon 2", player),
                 lambda state: can_beat_double_iris(state, options, player) and can_beat_general(state, options, player))

    # Sigma Access
    # Final Weapon Life Energy (3) requires Rising Fire
    add_rule(world.multiworld.get_entrance("Stage Select -> Space Port", player),
             lambda state: stage_access_count(state, options, player) >= 8)
    if did_include_pickup_locations(world):
        add_rule(world.multiworld.get_location("Final Weapon Life Energy (3)", player),
                 lambda state: state.has("Rising Fire", player))

    # Beating Sigma also requires Rising Fire. Shouldn't change anything for the actual logic since it's the last check, but is helpful to have for Universal Tracker
    add_rule(world.multiworld.get_location("Sigma Defeated", player),
            lambda state: state.has("Rising Fire", player))
    
    # Victory condition rule!
    world.multiworld.completion_condition[player] = lambda state: state.has("Victory", player)