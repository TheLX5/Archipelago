from dataclasses import dataclass
from typing_extensions import override
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import MMX2World

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAnyCount, HasAll, Rule, WrapperRule, False_, True_
from rule_builder.field_resolvers import FromOption, FromWorldAttr
from BaseClasses import CollectionState, MultiWorld
from NetUtils import JSONMessagePart

from .options import JammedBuster, XHunterBaseOpen, XHunterBaseMedalCount

from .enums import Items
from .constants import *

@dataclass()
class Macro(WrapperRule["MMX2World"], game=GAME_NAME):
    name: str
    description: str = ""

    @override
    def _instantiate(self, world: "MMX2World") -> Rule.Resolved:
        if rule := world.rule_macros.get(self.name):
            return rule
        rule = self.Resolved(
            self.child.resolve(world),
            self.name,
            self.description,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        world.rule_macros[self.name] = rule
        return rule

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str
        description: str = ""

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [{"type": "color", "color": "green" if self(state) else "salmon", "text": str(self)}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name

@dataclass()
class HasHP(Rule["MMX2World"], game=GAME_NAME):
    hp_required: int

    @override
    def _instantiate(self, world: "MMX2World") -> Rule.Resolved:
        return self.Resolved(self.hp_required, player=world.player)#, caching_enabled=True)

    class Resolved(Rule.Resolved):
        hp_required: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.current_hp[self.player] >= self.hp_required

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {Items.heart_tank.value(): {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [
                {"type": "color", "color": "green" if state and self(state) else "salmon", "text": f"{self.hp_required} HP"},
            ]

CAN_USE_CHECKPOINTS = Has(Items.helmet)
CAN_AIR_DASH = Has(Items.legs)
CAN_CHARGE_UNJAMMED_BUSTER = Has(Items.arms, 1, options=[OptionFilter(JammedBuster, 0)])
CAN_CHARGE_JAMMED_BUSTER = Has(Items.arms, 2, options=[OptionFilter(JammedBuster, 0, operator="ne")])
UNJAMMED_BUSTER = Has(Items.arms, options=[OptionFilter(JammedBuster, 0, operator="ne")], filtered_resolution=True)

CAN_CHARGE = Macro(
    CAN_CHARGE_UNJAMMED_BUSTER | CAN_CHARGE_JAMMED_BUSTER,
    "Can charge buster",
    "Able to charge shots"
)

LEMON = Macro(
    True_(),
    "Lemons",
    "Can deal damage with lemons"
)

DASH_LEMON = Macro(
    True_(),
    "Dash Lemons",
    "Can deal damage with lemons while performing a dash"
)

LEVEL_1_CHARGE = Macro(
    UNJAMMED_BUSTER,
    "Level 1 Charge Shot",
    "Can deal damage with level 1 charge buster"
)

LEVEL_2_CHARGE = Macro(
    UNJAMMED_BUSTER,
    "Level 2 Charge Shot",
    "Can deal damage with level 1 charge buster"
)

LEVEL_3_CHARGE = Macro(
    CAN_CHARGE,
    "Level 3 Charge Shot",
    "Can deal damage with level 1 charge buster"
)

SPIN_WHEEL = Macro(
    Has(Items.spin_wheel),
    "Spin Wheel",
    "Can deal damage with Spin Wheel"
)
BUBBLE_SPLASH = Macro(
    Has(Items.bubble_splash),
    "Bubble Splash",
    "Can deal damage with Bubble Splash"
)
SPEED_BURNER = Macro(
    Has(Items.speed_burner),
    "Speed Burner",
    "Can deal damage with Speed Burner"
)
SILK_SHOT = Macro(
    Has(Items.silk_shot),
    "Silk Shot",
    "Can deal damage with Silk Shot"
)
MAGNET_MINE = Macro(
    Has(Items.magnet_mine),
    "Magnet Mine",
    "Can deal damage with Magnet Mine"
)
SONIC_SLICER = Macro(
    Has(Items.sonic_slicer),
    "Sonic Slicer",
    "Can deal damage with Sonic Slicer"
)
STRIKE_CHAIN = Macro(
    Has(Items.strike_chain),
    "Strike Chain",
    "Can deal damage with Strike Chain"
)

CHARGED_SPIN_WHEEL = Macro(
    CAN_CHARGE & SPIN_WHEEL,
    "Charged Spin Wheel",
    "Can deal damage with Spin Wheel"
)
CHARGED_BUBBLE_SPLASH = Macro(
    CAN_CHARGE & BUBBLE_SPLASH,
    "Charged Bubble Splash",
    "Can deal damage with Bubble Splash"
)
CHARGED_SPEED_BURNER = Macro(
    CAN_CHARGE & SPEED_BURNER,
    "Charged Speed Burner",
    "Can deal damage with Speed Burner"
)
CHARGED_SILK_SHOT = Macro(
    CAN_CHARGE & SILK_SHOT,
    "Charged Silk Shot",
    "Can deal damage with Silk Shot"
)
CHARGED_MAGNET_MINE = Macro(
    CAN_CHARGE & MAGNET_MINE,
    "Charged Magnet Mine",
    "Can deal damage with Magnet Mine"
)
CHARGED_SONIC_SLICER = Macro(
    CAN_CHARGE & SONIC_SLICER,
    "Charged Sonic Slicer",
    "Can deal damage with Sonic Slicer"
)
CHARGED_STRIKE_CHAIN = Macro(
    CAN_CHARGE & STRIKE_CHAIN,
    "Charged Strike Chain",
    "Can deal damage with Strike Chain"
)

SHORYUKEN = Macro(
    Has(Items.shoryuken),
    "Shoryuken",
    "Can deal damage with Shoryuken"
)
GIGA_CRUSH = Macro(
    Has(Items.body),
    "Giga Crush",
    "Can deal damage with Giga Crush"
)

CRYSTAL_HUNTER = Has(Items.crystal_hunter)

CAN_ENTER_BASE_KEYS = Has(Items.maverick_medal, count=FromOption(XHunterBaseMedalCount), options=[OptionFilter(XHunterBaseOpen, XHunterBaseOpen.option_medals)])
CAN_ENTER_BASE_ITEM = Has(Items.stage_x_hunter, options=[OptionFilter(XHunterBaseOpen, XHunterBaseOpen.option_item)])
CAN_ENTER_BASE = CAN_ENTER_BASE_KEYS | CAN_ENTER_BASE_ITEM
