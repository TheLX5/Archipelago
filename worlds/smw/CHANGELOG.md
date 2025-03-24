# Super Mario World - Changelog


## v3.0

### Features:

- Map teleport and transition shuffle
	- Shuffle pipe and star destinations
	- Shuffle map transitions
- New inventory system that allows you to use a powerup before entering a level
	- You can gain those items from the multiworld or from the level goals
- New Items
	- Progressive Swim
	- Progressive Super Star
	- Extra Defense
	- Inventory Mushroom
	- Inventory Fire Flower
	- Inventory Feather
	- Inventory Super Star
	- Inventory Green Yoshi
	- Inventory Red Yoshi
	- Inventory Yellow Yoshi
	- Inventory Blue Yoshi
- New traps
	- Fishin' Boo Trap
	- Screen Flip Trap
	- Sticky Hands Trap
	- Sticky Floor Trap
	- Pixelate Trap
	- Spotlight Trap
- EnergyLink support
	- Deposit energy by collecting coins in levels
	- Use energy to purchase inventory items
- Blocks with coins and powerups can be kept collected after hitting them once
	- Makes the game harder on subsequent visits to any level
- Persisting traps can be altered to despawn on certain events
	- Gone on room load
	- Gone on map load
	- Gone after dying
	- Gone after being hurt
- New options: 
	- `energy_link`
	- `location_visual_indicator`
	- `block_collect_behavior`
	- `inventory_fill_percentage`
	- `persistent_trap_behavior`
	- `map_teleport_shuffle`
	- `map_transition_shuffle`


### Quality of Life

- New appareances for blocks, 3-Up Moons and Dragon Coins when they're enabled as valid locations
- Current item box contents are displayed during the map gameplay
- Made Swim a progressive item; the second upgrade allows for faster horizontal swimming
- Added location groups

### Bug Fixes:

- Several logic tweaks/fixes
- Some levels received adjustments to their vertical scroll setting
- Ice Trap is now more slippery



## v2.0

### Features:

- New optional Location Checks
	- 3-Up Moons
	- Hidden 1-Ups
	- Bonus Blocks
	- Blocksanity
		- All blocks that contain coins or items are included, with the exception of:
			- Blocks in Top Secret Area & Front Door/Bowser Castle
			- Blocks that are unreachable without glitches/unreasonable movement
- New Items
	- Special Zone Clear
	- New Filler Items
		- 1 Coin
		- 5 Coins
		- 10 Coins
		- 50 Coins
	- New Trap Items
		- Reverse Trap
		- Thwimp Trap
- SFX Shuffle
- Palette Shuffle Overhaul
	- New Curated Palette can now be used for the Overworld and Level Palette Shuffle options
	- Foreground and Background Shuffle options have been merged into a single option
- Max possible Yoshi Egg value is 255
	- UI in-game is updated to handle 3-digits
	- New `Display Received Item Popups` option: `progression_minus_yoshi_eggs`

### Quality of Life:

- In-Game Indicators are now displayed on the map screen for location checks and received items
- In-level sprites are displayed upon receiving certain items
- The Camera Scroll unlocking is now only enabled on levels where it needs to be
- SMW can now handle receiving more than 255 items
- Significant World Code cleanup
	- New Options API
	- Removal of `world: MultiWorld` across the world
- The PopTracker pack now has tabs for every level/sublevel, and can automatically swap tabs while playing if connected to the server

### Bug Fixes:

- Several logic tweaks/fixes


## v1.1

### Features:

- New Item
	- Timer Trap
- `Bowser Castle Rooms` option which changes the behavior of the Front Door
- `Boss Shuffle` option
- `Overworld Palette Shuffle` option

### Quality of Life:

- `Overworld Speed` option which allows the player to move faster or slower on the map
- `Early Climb` option which guarantees that `Climb` will be found locally in an early location
- `Exclude Special Zone` option which fully excludes Special Zone levels from the seed
	- Note: this option is ignored if the player chooses to fill their entire item pool with Yoshi Eggs, which are Progression Items
- Ice and Stun Traps are now queued if received while another of its type is already active, and are then activated at the next opportunity

### Bug Fixes:

- Fixed `Chocolate Island 4 - Dragon Coins` requiring `Run` instead of `P-Switch`
- Fixed a Literature Trap typo


## v1.0 - First Stable Release

### Features:

- Goal
	- Bowser
		- Defeat bosses, reach Bowser's Castle, and defeat Bowser
	- Yoshi Egg Hunt
		- Find a certain number of Yoshi Eggs spread across the MultiWorld`
- Locations included:
	- Level exits (Normal and Secret)
	- Dragon Coins
		- Collect at least five Dragon Coins in a level to send a location check
- Items included:
	- Run
	- Carry
	- Swim
	- Spin Jump
	- Climb
	- Yoshi
	- P-Switch
	- P-Balloon
	- Progressive Powerup
		- Unlocks the ability to use Mushrooms, Fire Flowers, and Capes, progressively
	- Super Star Activate
	- Yellow Switch Palace
	- Green Switch Palace
	- Red Switch Palace
	- Blue Switch Palace
	- 1-Up Mushroom
	- Yoshi Egg
		- Only on `Yoshi Egg Hunt` goal
	- Traps
		- Ice Trap
		- Stun Trap
		- Literature Trap
- `Bowser Castle Doors` option
	- Whether the Front Door and Back Door map tiles lead to the Front Door or Back Door levels
- DeathLink is supported
- Level Shuffle is supported
- Autosave is supported
- Music Shuffle is supported
- Mario's palette can be selected
- Level Palettes can be shuffled
- Starting life count can be set
