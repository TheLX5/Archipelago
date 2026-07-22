import io
import zipfile
import json
import textwrap
import argparse
import tkinter as tk
from argparse import Namespace
from tkinter import Tk, Frame, Label, StringVar, Entry, filedialog, messagebox, Button, LEFT, X, Y, BOTH, TOP, LabelFrame, \
    Checkbutton, E, W, BOTTOM, RIGHT, font as font, BooleanVar, OptionMenu
from Utils import  persistent_store, persistent_load, get_adjuster_settings_no_defaults, tkinter_center_window

import ModuleUpdate
ModuleUpdate.update()

from .constants import *

WINDOW_MIN_HEIGHT = 540
WINDOW_MIN_WIDTH = 640

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)
    

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    return parser


def main(launcher_args):
    parser = get_argparser()
    args = parser.parse_args(launcher_args, namespace=get_adjuster_settings_no_defaults(GAME_NAME))

    manager_gui()


def manager_gui():    
    manager_window = Tk()
    manager_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.maxsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.resizable(True, False)
    manager_window.wm_title(f"{GAME_NAME} Manager")

    left_frame = Frame(manager_window)
    right_frame = Frame(manager_window)

    linked_frame, linked_vars = create_linked_frame(left_frame)
    global_frame, global_vars = create_global_frame(left_frame)
    file_frame, vars_ns = create_file_frame(left_frame, [linked_vars])
    palette_frame, palette_vars = create_palette_frame(right_frame)

    file_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    linked_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    global_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    palette_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)

    left_frame.pack(side=LEFT, fill=BOTH, expand=True)
    right_frame.pack(side=LEFT, fill=BOTH, expand=True)

    tkinter_center_window(manager_window)
    manager_window.mainloop()


def create_file_frame(parent=None, external_vars=None):
    vars_ns = Namespace()
    if external_vars:
        for var_group in external_vars:
            for key, value in vars(var_group).items():
                setattr(vars_ns, key, value)

    frame = LabelFrame(parent, text="File Manager", padx=4, pady=4, name="file_manager")

    vars_ns.patch_path = StringVar()
    load_frame = Frame(frame)
    file_label = Label(load_frame, text="Patch file: ")
    file_label.pack(side=LEFT, fill=X)
    file_value = Entry(load_frame, textvariable=vars_ns.patch_path, state="readonly")
    file_value.pack(side=RIGHT, fill=X, expand=True)

    def load_patch_window():
        nonlocal vars_ns

        file_path = filedialog.askopenfilename(
            filetypes=[("MMX2 Patch Files", ".apmmx2")])
        try:
            vars_ns.patch_path.set(file_path)
            load_data_from_patch(file_path, vars_ns)
        except Exception as e:
            messagebox.showerror(title="Error while reading MMX2 Patch file", message=str(e))

    def save_patch_window():
        nonlocal vars_ns
        if "" == vars_ns.patch_path.get():
            return
        save_adjusted_data(vars_ns)
        messagebox.showinfo(title="Success", message="Saved changes to MMX2 Patch file!")

    load_button = Button(frame, text="Load MMX2 Patch", command=load_patch_window)
    save_button = Button(frame, text="Save changes to MMX2 Patch", command=save_patch_window)

    load_frame.pack(side=TOP, fill=X)
    load_button.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)

    return frame, vars_ns


def load_data_from_patch(patch_path, vars_ns):
    file = zipfile.ZipFile(patch_path)
    options_file = json.loads(file.read("data.json").decode("UTF-8"))

    if "death_link" in options_file.keys():
        vars_ns.death_link_active.set(options_file["death_link"])
    if "damage_link" in options_file.keys():
        vars_ns.damage_link_active.set(options_file["damage_link"])
    if "energy_link" in options_file.keys():
        vars_ns.energy_link_active.set(options_file["energy_link"])


def save_adjusted_data(vars_ns):
    patch_path = vars_ns.patch_path.get()
    file = zipfile.ZipFile(patch_path)

    zip_files = dict()
    for file_name in file.namelist():
        zip_files[file_name] = file.read(file_name)

    options_file = json.loads(file.read("data.json").decode("UTF-8"))
    options_file["death_link"] = vars_ns.death_link_active.get()
    options_file["damage_link"] = vars_ns.damage_link_active.get()
    options_file["energy_link"] = vars_ns.energy_link_active.get()

    zip_files["data.json"] = json.dumps(options_file)

    zip_bytes = create_zipfile(zip_files)    
    if patch_path:
        with open(patch_path, "wb") as f:
            f.write(zip_bytes)


def create_linked_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Linked Options (from Patch File)", padx=4, pady=4)

    vars.death_link_active = BooleanVar()
    death_frame = Frame(frame)
    death_check = Checkbutton(death_frame, variable=vars.death_link_active)
    death_check.pack(side=LEFT, fill=X)
    death_label = Label(death_frame, text="Enable Death Link")
    death_label.pack(side=LEFT, fill=X)

    vars.energy_link_active = BooleanVar()
    energy_frame = Frame(frame)
    energy_check = Checkbutton(energy_frame, variable=vars.energy_link_active)
    energy_check.pack(side=LEFT, fill=X)
    energy_label = Label(energy_frame, text="Enable Energy Link")
    energy_label.pack(side=LEFT, fill=X)

    vars.damage_link_active = BooleanVar()
    damage_frame = Frame(frame)
    damage_check = Checkbutton(damage_frame, variable=vars.damage_link_active)
    damage_check.pack(side=LEFT, fill=X)
    damage_label = Label(damage_frame, text="Enable Damage Link")
    damage_label.pack(side=LEFT, fill=X)

    energy_frame.pack(side=TOP, fill=X)
    death_frame.pack(side=TOP, fill=X)
    damage_frame.pack(side=TOP, fill=X)

    return frame, vars


def create_global_frame(parent=None):
    vars_ns = Namespace()
    frame = LabelFrame(parent, text="Global Options (saved automatically)", padx=4, pady=4)
    
    def save_callback(*args):
        nonlocal vars_ns
        save_vars = Namespace()
        save_vars.long_jump = vars_ns.long_jump.get()
        save_vars.shoryuken_input = vars_ns.shoryuken_input.get()
        save_vars.serges_qol = vars_ns.serges_qol.get()
        save_vars.button_dash = vars_ns.button_dash.get()
        save_vars.button_jump = vars_ns.button_jump.get()
        save_vars.button_menu = vars_ns.button_menu.get()
        save_vars.button_shot = vars_ns.button_shot.get()
        save_vars.button_select_l = vars_ns.button_select_l.get()
        save_vars.button_select_r = vars_ns.button_select_r.get()
        persistent_store("global_settings", GAME_NAME, save_vars)

    persistent_settings = persistent_load().get("global_settings", {}).get(GAME_NAME, Namespace())

    vars_ns.long_jump = BooleanVar()
    long_jump_frame = Frame(frame)
    long_jump_check = Checkbutton(long_jump_frame, variable=vars_ns.long_jump, command=save_callback)
    long_jump_check.pack(side=LEFT, fill=X)
    long_jump_label = Label(long_jump_frame, text="Enable X4 styled dash jumps")
    long_jump_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "long_jump"):
            vars_ns.long_jump.set(persistent_settings.long_jump)
    else:
        vars_ns.long_jump.set(False)

    vars_ns.shoryuken_input = BooleanVar()
    shoryuken_input_frame = Frame(frame)
    shoryuken_input_check = Checkbutton(shoryuken_input_frame, variable=vars_ns.shoryuken_input, command=save_callback)
    shoryuken_input_check.pack(side=LEFT, fill=X)
    shoryuken_input_label = Label(shoryuken_input_frame, text="Use Hadouken inputs for Shoryuken")
    shoryuken_input_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "shoryuken_input"):
            vars_ns.shoryuken_input.set(persistent_settings.shoryuken_input)
    else:
        vars_ns.shoryuken_input.set(False)

    vars_ns.serges_qol = BooleanVar()
    serges_qol_frame = Frame(frame)
    serges_qol_check = Checkbutton(serges_qol_frame, variable=vars_ns.serges_qol, command=save_callback)
    serges_qol_check.pack(side=LEFT, fill=X)
    serges_qol_label = Label(serges_qol_frame, text="Makes both Serges fights enjoyable")
    serges_qol_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "serges_qol"):
            vars_ns.serges_qol.set(persistent_settings.serges_qol)
    else:
        vars_ns.serges_qol.set(False)

    states = ["A", "B", "X", "Y", "L", "R", "START", "SELECT"]

    vars_ns.button_dash = StringVar()
    button_dash_frame = Frame(frame)
    button_dash_menu = OptionMenu(button_dash_frame, vars_ns.button_dash, *states, command=save_callback)
    button_dash_menu.config(width=8)
    button_dash_menu.pack(side=LEFT, fill=X)
    button_dash_label = Label(button_dash_frame, text="DASH Button")
    button_dash_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_dash"):
            vars_ns.button_dash.set(persistent_settings.button_dash)
    else:
        vars_ns.button_dash.set("A")

    vars_ns.button_jump = StringVar()
    button_jump_frame = Frame(frame)
    button_jump_menu = OptionMenu(button_jump_frame, vars_ns.button_jump, *states, command=save_callback)
    button_jump_menu.config(width=8)
    button_jump_menu.pack(side=LEFT, fill=X)
    button_jump_label = Label(button_jump_frame, text="JUMP Button")
    button_jump_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_jump"):
            vars_ns.button_jump.set(persistent_settings.button_jump)
    else:
        vars_ns.button_jump.set("B")

    vars_ns.button_menu = StringVar()
    button_menu_frame = Frame(frame)
    button_menu_menu = OptionMenu(button_menu_frame, vars_ns.button_menu, *states, command=save_callback)
    button_menu_menu.config(width=8)
    button_menu_menu.pack(side=LEFT, fill=X)
    button_menu_label = Label(button_menu_frame, text="MENU Button")
    button_menu_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_menu"):
            vars_ns.button_menu.set(persistent_settings.button_menu)
    else:
        vars_ns.button_menu.set("START")

    vars_ns.button_shot = StringVar()
    button_shot_frame = Frame(frame)
    button_shot_menu = OptionMenu(button_shot_frame, vars_ns.button_shot, *states, command=save_callback)
    button_shot_menu.config(width=8)
    button_shot_menu.pack(side=LEFT, fill=X)
    button_shot_label = Label(button_shot_frame, text="SHOT Button")
    button_shot_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_shot"):
            vars_ns.button_shot.set(persistent_settings.button_shot)
    else:
        vars_ns.button_shot.set("Y")

    vars_ns.button_select_l = StringVar()
    button_select_l_frame = Frame(frame)
    button_select_l_menu = OptionMenu(button_select_l_frame, vars_ns.button_select_l, *states, command=save_callback)
    button_select_l_menu.config(width=8)
    button_select_l_menu.pack(side=LEFT, fill=X)
    button_select_l_label = Label(button_select_l_frame, text="SELECT L Button")
    button_select_l_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_select_l"):
            vars_ns.button_select_l.set(persistent_settings.button_select_l)
    else:
        vars_ns.button_select_l.set("L")

    vars_ns.button_select_r = StringVar()
    button_select_r_frame = Frame(frame)
    button_select_r_menu = OptionMenu(button_select_r_frame, vars_ns.button_select_r, *states, command=save_callback)
    button_select_r_menu.config(width=8)
    button_select_r_menu.pack(side=LEFT, fill=X)
    button_select_r_label = Label(button_select_r_frame, text="SELECT R Button")
    button_select_r_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "button_select_r"):
            vars_ns.button_select_r.set(persistent_settings.button_select_r)
    else:
        vars_ns.button_select_r.set("R")

    long_jump_frame.pack(side=TOP, fill=X)
    shoryuken_input_frame.pack(side=TOP, fill=X)
    serges_qol_frame.pack(side=TOP, fill=X)
    button_dash_frame.pack(side=TOP, fill=X)
    button_jump_frame.pack(side=TOP, fill=X)
    button_menu_frame.pack(side=TOP, fill=X)
    button_shot_frame.pack(side=TOP, fill=X)
    button_select_l_frame.pack(side=TOP, fill=X)
    button_select_r_frame.pack(side=TOP, fill=X)

    return frame, vars_ns


def create_palette_frame(parent=None):
    vars_ns = Namespace()
    frame = LabelFrame(parent, text="Palette Options (saved automatically)", padx=4, pady=4)
    
    def save_callback(*args):
        nonlocal vars_ns
        save_vars = Namespace()
        save_vars.pal_default = vars_ns.pal_default.get()
        save_vars.pal_crystal = vars_ns.pal_crystal.get()
        save_vars.pal_bubble = vars_ns.pal_bubble.get()
        save_vars.pal_silk = vars_ns.pal_silk.get()
        save_vars.pal_wheel = vars_ns.pal_wheel.get()
        save_vars.pal_slicer = vars_ns.pal_slicer.get()
        save_vars.pal_chain = vars_ns.pal_chain.get()
        save_vars.pal_mine = vars_ns.pal_mine.get()
        save_vars.pal_burner = vars_ns.pal_burner.get()
        persistent_store("palette_settings", GAME_NAME, save_vars)

    persistent_settings = persistent_load().get("palette_settings", {}).get(GAME_NAME, Namespace())

    states = [
        "blue",
        "gold_armor",
        "homing_torpedo",
        "chameleon_sting",
        "rolling_shield",
        "fire_wave",
        "storm_tornado",
        "electric_spark",
        "boomerang_cutter",
        "shotgun_ice",
        "crystal_hunter",
        "bubble_splash",
        "silk_shot",
        "spin_wheel",
        "sonic_slicer",
        "strike_chain",
        "magnet_mine",
        "speed_burner",
        "acid_burst",
        "parasitic_bomb",
        "triad_thunder",
        "spinning_blade",
        "ray_splasher",
        "gravity_well",
        "frost_shield",
        "tornado_fang",
    ]

    SIZE = 18

    vars_ns.pal_default = StringVar()
    pal_default_frame = Frame(frame)
    pal_default_menu = OptionMenu(pal_default_frame, vars_ns.pal_default, *states, command=save_callback)
    pal_default_menu.config(width=SIZE)
    pal_default_menu.pack(side=LEFT, fill=X)
    pal_default_label = Label(pal_default_frame, text="Default Palette")
    pal_default_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_default"):
            vars_ns.pal_default.set(persistent_settings.pal_default)
    else:
        vars_ns.pal_default.set("blue")

    vars_ns.pal_crystal = StringVar()
    pal_crystal_frame = Frame(frame)
    pal_crystal_menu = OptionMenu(pal_crystal_frame, vars_ns.pal_crystal, *states, command=save_callback)
    pal_crystal_menu.config(width=SIZE)
    pal_crystal_menu.pack(side=LEFT, fill=X)
    pal_crystal_label = Label(pal_crystal_frame, text="Crystal Hunter Palette")
    pal_crystal_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_crystal"):
            vars_ns.pal_crystal.set(persistent_settings.pal_crystal)
    else:
        vars_ns.pal_crystal.set("crystal_hunter")

    vars_ns.pal_bubble = StringVar()
    pal_bubble_frame = Frame(frame)
    pal_bubble_menu = OptionMenu(pal_bubble_frame, vars_ns.pal_bubble, *states, command=save_callback)
    pal_bubble_menu.config(width=SIZE)
    pal_bubble_menu.pack(side=LEFT, fill=X)
    pal_bubble_label = Label(pal_bubble_frame, text="Bubble Splash Palette")
    pal_bubble_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_bubble"):
            vars_ns.pal_bubble.set(persistent_settings.pal_bubble)
    else:
        vars_ns.pal_bubble.set("bubble_splash")

    vars_ns.pal_silk = StringVar()
    pal_silk_frame = Frame(frame)
    pal_silk_menu = OptionMenu(pal_silk_frame, vars_ns.pal_silk, *states, command=save_callback)
    pal_silk_menu.config(width=SIZE)
    pal_silk_menu.pack(side=LEFT, fill=X)
    pal_silk_label = Label(pal_silk_frame, text="Silk Shot Palette")
    pal_silk_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_silk"):
            vars_ns.pal_silk.set(persistent_settings.pal_silk)
    else:
        vars_ns.pal_silk.set("silk_shot")

    vars_ns.pal_wheel = StringVar()
    pal_wheel_frame = Frame(frame)
    pal_wheel_menu = OptionMenu(pal_wheel_frame, vars_ns.pal_wheel, *states, command=save_callback)
    pal_wheel_menu.config(width=SIZE)
    pal_wheel_menu.pack(side=LEFT, fill=X)
    pal_wheel_label = Label(pal_wheel_frame, text="Spin Wheel Palette")
    pal_wheel_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_wheel"):
            vars_ns.pal_wheel.set(persistent_settings.pal_wheel)
    else:
        vars_ns.pal_wheel.set("spin_wheel")

    vars_ns.pal_slicer = StringVar()
    pal_slicer_frame = Frame(frame)
    pal_slicer_menu = OptionMenu(pal_slicer_frame, vars_ns.pal_slicer, *states, command=save_callback)
    pal_slicer_menu.config(width=SIZE)
    pal_slicer_menu.pack(side=LEFT, fill=X)
    pal_slicer_label = Label(pal_slicer_frame, text="Sonic Slicer Palette")
    pal_slicer_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_slicer"):
            vars_ns.pal_slicer.set(persistent_settings.pal_slicer)
    else:
        vars_ns.pal_slicer.set("sonic_slicer")

    vars_ns.pal_chain = StringVar()
    pal_chain_frame = Frame(frame)
    pal_chain_menu = OptionMenu(pal_chain_frame, vars_ns.pal_chain, *states, command=save_callback)
    pal_chain_menu.config(width=SIZE)
    pal_chain_menu.pack(side=LEFT, fill=X)
    pal_chain_label = Label(pal_chain_frame, text="Strike Chain Palette")
    pal_chain_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_chain"):
            vars_ns.pal_chain.set(persistent_settings.pal_chain)
    else:
        vars_ns.pal_chain.set("strike_chain")

    vars_ns.pal_mine = StringVar()
    pal_mine_frame = Frame(frame)
    pal_mine_menu = OptionMenu(pal_mine_frame, vars_ns.pal_mine, *states, command=save_callback)
    pal_mine_menu.config(width=SIZE)
    pal_mine_menu.pack(side=LEFT, fill=X)
    pal_mine_label = Label(pal_mine_frame, text="Magnet Mine Palette")
    pal_mine_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_mine"):
            vars_ns.pal_mine.set(persistent_settings.pal_mine)
    else:
        vars_ns.pal_mine.set("magnet_mine")

    vars_ns.pal_burner = StringVar()
    pal_burner_frame = Frame(frame)
    pal_burner_menu = OptionMenu(pal_burner_frame, vars_ns.pal_burner, *states, command=save_callback)
    pal_burner_menu.config(width=SIZE)
    pal_burner_menu.pack(side=LEFT, fill=X)
    pal_burner_label = Label(pal_burner_frame, text="Speed Burner Palette")
    pal_burner_label.pack(side=LEFT, fill=X)
    if hasattr(persistent_settings, "pal_burner"):
            vars_ns.pal_burner.set(persistent_settings.pal_burner)
    else:
        vars_ns.pal_burner.set("speed_burner")

    pal_default_frame.pack(side=TOP, fill=X)
    pal_crystal_frame.pack(side=TOP, fill=X)
    pal_bubble_frame.pack(side=TOP, fill=X)
    pal_silk_frame.pack(side=TOP, fill=X)
    pal_wheel_frame.pack(side=TOP, fill=X)
    pal_slicer_frame.pack(side=TOP, fill=X)
    pal_chain_frame.pack(side=TOP, fill=X)
    pal_mine_frame.pack(side=TOP, fill=X)
    pal_burner_frame.pack(side=TOP, fill=X)

    return frame, vars_ns


def create_zipfile(files: dict[str, bytes]) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def launch(*launcher_args):
    main(launcher_args)

