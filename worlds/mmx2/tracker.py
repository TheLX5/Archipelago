from functools import cached_property
from typing import TYPE_CHECKING, Any, ClassVar
from typing_extensions import override
from worlds.mmx2.options import MMX2Options

from BaseClasses import CollectionState, Entrance, Location, Region, CollectionRule
from rule_builder.rules import Rule
from NetUtils import JSONMessagePart
from Utils import get_fuzzy_results, get_intended_text

from .enums import Items
from .constants import *
from .locations import all_locations

if TYPE_CHECKING:
    from . import MMX2World
    from .boss_data import Boss
    from worlds.AutoWorld import World
else:
    World = object

def rule_to_json(
    rule: CollectionRule | Rule.Resolved | None,
    state: CollectionState,
    indent: str = "",
) -> list[JSONMessagePart]:
    messages: list[JSONMessagePart] = []
    if isinstance(rule, Rule.Resolved) and not rule.always_true:
        if indent:
            messages.append({"type": "text", "text": indent})
        messages.extend(rule.explain_json(state))
    else:
        messages.append({"type": "color", "color": "green", "text": f"{indent}True"})
    return messages

class UTMxin(World):
    using_ut: bool = False
    ut_can_gen_without_yaml: ClassVar = True
    glitches_item_name: str = Items.glitched.value
    #tracker_world = {  # map tracker data for UT
    #    "map_page_maps": ["maps/maps.json"],
    #    "map_page_locations": Tracker.map_locations,
    #    "map_page_setting_key": r"dkc2_current_map_{team}_{player}",
    #    "map_page_index": Tracker.map_page_index,
    #    "external_pack_key": "ut_poptracker_path",
    #    "poptracker_name_mapping": Tracker.poptracker_data,
    #}

    if TYPE_CHECKING:
        options: MMX2Options
        boss_data: dict[str, Boss]

    @cached_property
    def is_ut(self) -> bool:
        return getattr(self.multiworld, "generation_is_fake", False)

    @override
    def generate_early(self) -> None:
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str,Any] = self.multiworld.re_gen_passthrough[GAME_NAME]
            self.options.starting_hp.value = slot_data["starting_hp"]
            self.options.heart_tank_effectiveness.value = slot_data["heart_tank_effectiveness"]
            self.options.boss_weakness_strictness.value = slot_data["boss_weakness_strictness"]
            self.options.pickup_locations.value = slot_data["pickup_locations"]
            self.options.chips.value = slot_data["chips"]
            self.options.jammed_buster.value = slot_data["jammed_buster"]
            self.options.x_hunter_base_boss_rematch_count.value = slot_data["x_hunter_base_boss_rematch_count"]
            self.options.x_hunter_base_level_unlock.value = slot_data["x_hunter_base_level_unlock"]
            self.options.x_hunter_base_open.value = slot_data["x_hunter_base_open"]
            self.options.x_hunter_base_medal_count.value = slot_data["x_hunter_base_medal_count"]
            self.options.x_hunters_arena_medal_count.value = slot_data["x_hunters_arena_medal_count"]

            for enemy_name in self.boss_data.keys():
                enemy_data: dict[str, list | str] = slot_data["boss_data"][enemy_name]
                self.boss_data[enemy_name].weakness = enemy_data["weakness"].copy()
                self.boss_data[enemy_name].sub_weakness = enemy_data["sub_weakness"].copy()
                self.boss_data[enemy_name].hp = enemy_data["hp"]


    def get_logical_path(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart]:
        # Stolen from DrTChops XD
        if not dest_name:
            return [{"type": "text", "text": "Provide a location or region to route to using /get_logical_path [name]"}]

        goal_location: Location | None = None
        goal_region: Region | None = None
        region_name = ""
        location_name, usable, response = get_intended_text(dest_name, [loc.name for loc in self.get_locations()])
        if usable:
            try:
                goal_location = self.get_location(location_name)
            except KeyError:
                return [{"type": "text", "text": f"Location {location_name} not found in this multiworld"}]
            goal_region = goal_location.parent_region
            if not goal_region:
                return [{"type": "text", "text": f"Location {location_name} has no parent region"}]
        else:
            region_name, usable, _resp = get_intended_text(
                dest_name,
                [reg.name for reg in self.get_regions()],
            )
            if usable:
                goal_region = self.get_region(region_name)
            else:
                return [{"type": "text", "text": response}]

        glitched_state = state.copy()
        glitched_state.collect(self.create_item(Items.glitched))

        if goal_location and not goal_location.can_reach(state) and not goal_location.can_reach(glitched_state):
            return [{"type": "text", "text": f"Location {goal_location.name} cannot be reached"}]
        if goal_region not in state.path and goal_region.name != self.origin_region_name:
            return [{"type": "text", "text": f"Region {goal_region.name} cannot be reached"}]

        if not goal_location.can_reach(state) and goal_location.can_reach(glitched_state):
            common_state = glitched_state.copy()
        else:
            common_state = state.copy()

        messages: list[JSONMessagePart] = []
        if goal_region.name != self.origin_region_name:
            path: list[Entrance] = []
            name, connection = common_state.path[goal_region]
            while connection is not None:
                name, connection = connection
                if "->" in name:
                    path.append(self.get_entrance(name))

            path.reverse()
            last = path[-1]
            for p in path:
                messages.extend(
                    [
                        {"type": "entrance_name", "text": p.name, "player": self.player},
                        {"type": "text", "text": "\n"},
                        *rule_to_json(p.access_rule, common_state, indent="    "),
                        {"type": "text", "text": "\n"},
                    ]
                )
                # Remove lone Trues from logic
                if messages[-1]["text"] == "\n" and messages[-2]["text"] == "    True":
                    messages.pop()
                    messages.pop()

        if goal_location:
            messages.extend(
                [
                    {"type": "text", "text": "-> "},
                    {
                        "type": "location_name",
                        "text": goal_location.name,
                        "player": self.player,
                    },
                    {"type": "text", "text": "\n"},
                    *rule_to_json(goal_location.access_rule, common_state, indent="    "),
                ]
            )

        return messages

    def explain_rule(self, dest_name: str, state: CollectionState, *_: Any, **__: Any) -> list[JSONMessagePart]:
        if not dest_name:
            return [{"type": "text", "text": "Enter a location, region, item, or acronym to get an explanation"}]

        types_to_try = {
            "location": self._explain_location,
        }
        attempts = list(types_to_try.keys())
        parts = dest_name.split(maxsplit=1)
        if len(parts) == 2:
            first_word = parts[0].lower()
            for label in types_to_try.keys():
                if first_word == label:
                    attempts = [label]
                    break

        result = []
        usable = False
        best_guess = []
        max_confidence = 0
        confidence = 0
        for classification in attempts:
            result, usable, confidence = types_to_try[classification](dest_name, state)
            if usable:
                return result
            if confidence > max_confidence:
                best_guess = result
                max_confidence = confidence

        return best_guess

    def _explain_location(self, location_name: str, state: CollectionState) -> tuple[list[JSONMessagePart], bool, int]:
        all_location_names = set(self.multiworld.regions.location_cache[self.player])
        guess, usable, response = get_intended_text(location_name, all_location_names)
        if not usable:
            picks = get_fuzzy_results(location_name, all_location_names, limit=1)
            confidence = picks[0][1]
            return [{"type": "text", "text": response}], False, confidence

        location_name = guess
        location = self.get_location(location_name)
        glitched_state = state.copy()
        glitched_state.collect(self.create_item(Items.glitched))

        if location.can_reach(glitched_state) and not location.can_reach(state):
            messages: list[JSONMessagePart] = [
                {"type": "text", "text": "Location: "},
                {"type": "color", "color": "slateblue" if location.can_reach(glitched_state) else "salmon", "text": location_name},
                {"type": "text", "text": " (Can be obtained out of logic)"},
            ]
            messages.extend(
                [
                    {"type": "text", "text": "\nLogic: "},
                    *rule_to_json(location.access_rule, glitched_state),
                ]
            )
        else:
            messages: list[JSONMessagePart] = [
                {"type": "text", "text": "Location: "},
                {"type": "color", "color": "green" if location.can_reach(state) else "salmon", "text": location_name},
            ]
            messages.extend(
                [
                    {"type": "text", "text": "\nLogic: "},
                    *rule_to_json(location.access_rule, state),
                ]
            )
        return messages, True, 100
