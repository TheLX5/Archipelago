from typing import Tuple, Dict, Any
import traceback
from worlds.LauncherComponents import SuffixIdentifier, components, Component, Type, launch_subprocess
from worlds.AutoSNIClient import AutoSNIClientRegister


def my_launch_client(*args) -> None:
    from .sni_ut_client import my_launch
    launch_subprocess(my_launch, name="SNI Client + Universal Tracker", args=args)


for sni_component in components:
    if sni_component.script_name == "SNIClient":
        break

component = Component("SNI Client + Universal Tracker",
                      component_type=Type.CLIENT, func=my_launch_client,
                      file_identifier=sni_component.file_identifier)
components.append(component)


old_new = AutoSNIClientRegister.__new__


def newUT(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any]) -> AutoSNIClientRegister:

    temp = namespace["game_watcher"]

    async def my_game_watcher(self, ctx) -> None:
        if getattr(ctx, "tracker_enabled", False):
            from worlds.tracker.TrackerClient import updateTracker
            try:
                if ctx.tracker_core.player_id is not None and ctx.tracker_core.multiworld is not None:
                    updateTracker(ctx)
            except Exception:
                tb = traceback.format_exc()
                print(tb)
        await temp(self, ctx)
    namespace["game_watcher"] = my_game_watcher

    new_class = old_new(cls, name, bases, namespace)

    if "patch_suffix" in namespace:
        new_suffixes = [*component.file_identifier.suffixes]
        if type(namespace["patch_suffix"]) is str:
            new_suffixes.append(namespace["patch_suffix"])
        else:
            new_suffixes.extend(namespace["patch_suffix"])
        component.file_identifier = SuffixIdentifier(*new_suffixes)
        sni_component.file_identifier = SuffixIdentifier()

    return new_class


AutoSNIClientRegister.__new__ = newUT
