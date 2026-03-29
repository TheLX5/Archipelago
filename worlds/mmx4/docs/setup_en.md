# Mega Man X4

## Required Software

* A legally acquired US ROM of Mega Man X4 for the Playstation
* A legally acquired Playstation BIOS
* [Bizhawk](https://github.com/TASEmulators/BizHawk/releases)
* The patch file which can be found on the releases page - "MMX4_Archipelago.xdelta"

* The built-in Archipelago client, which can be installed [here](https://github.com/ArchipelagoMW/Archipelago/releases)

## Configuring your YAML file

### What is a YAML file and why do I need one?

Your YAML file contains a set of configuration options which provide the generator with information about how it should
generate your game. Each player of a multiworld will provide their own YAML file. This setup allows each player to enjoy
an experience customized for their taste, and different players in the same multiworld can all have different options.

### Where do I get a YAML file?

Check the releases page for the latest version of the YAML. Alternatively you can generate your own using the Archipelago Launcher.

## Connect to the MultiServer

1. Install the APWorld
2. Through the launcher run the Bizhawk Client tool
3. Apply the XDelta patch to the ROM
   * You can use this tool - https://kotcrab.github.io/xdelta-wasm/
4. Run your Patched ROM in Bizhawk
5. In Bizhawk open Tools/Lua Console
6. In the Lua Console open connector_bizhawk_generic.lua which should be in:
   * (Your Archipelago Installation Folder)/Data/Lua
7. Connect to your created room through the Bizhawk Client Tool in the Archipelago Launcher