from dataclasses import dataclass
import copy
import random

@dataclass
class EnemyData():
    id: int
    name: str
    weight: int
    disp: tuple[int,int]
    tags: list[str]
    replaces: list[str]

enemy_list = {
    0x00: EnemyData(0x00, "Green Koopa, no shell", 10, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe"]),
    0x01: EnemyData(0x01, "Red Koopa, no shell", 10, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x02: EnemyData(0x02, "Blue Koopa, no shell", 5, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x03: EnemyData(0x03, "Yellow Koopa, no shell", 5, (0,0), ["ground"], ["ground", "bounceable", "upsidedown pipe"]),
    0x04: EnemyData(0x04, "Green Koopa", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe"]),
    0x05: EnemyData(0x05, "Red Koopa", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe", "stay on ledge"]),
    0x07: EnemyData(0x07, "Yellow Koopa", 10, (0,0), ["ground"], ["ground", "kickable", "bounceable", "upsidedown pipe"]),
    0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying"]),
    0x09: EnemyData(0x09, "Green bouncing Koopa (Y&1)", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable", "ambush small", "bouncing koopa"]),
    0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating"]),
    0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating"]),
    0x0C: EnemyData(0x0C, "Yellow Koopa with wings", 20, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x0E: EnemyData(0x0E, "Keyhole", 20, (0,0), ["skip"], ["skip"]),
    0x0F: EnemyData(0x0F, "Goomba", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x10: EnemyData(0x10, "Bouncing Goomba with wings", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x1A: EnemyData(0x1A, "Classic Pirhana Plant (use ExGFX)", 20, (0,0), ["skip"], ["pipe"]),
    0x1C: EnemyData(0x1C, "Bullet Bill", 10, (0,0), ["floating"], ["flying", "floating", "water", "ground"]),
    0x21: EnemyData(0x21, "Moving coin", 20, (0,0), ["skip"], ["skip"]),
    0x2D: EnemyData(0x2D, "Baby green Yoshi", 20, (0,0), ["skip"], ["skip"]),
    0x2F: EnemyData(0x2F, "Portable spring board", 20, (0,0), ["skip"], ["skip"]),
    0x35: EnemyData(0x35, "Green Yoshi", 20, (0,0), ["skip"], ["skip"]),
    0x3E: EnemyData(0x3E, "POW, blue/silver (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x45: EnemyData(0x45, "Directional coins, no time limit", 20, (0,0), ["skip"], ["skip"]),
    0x4F: EnemyData(0x4F, "Jumping Pirhana Plant", 20, (0,0), ["pipe"], ["pipe"]),
    0x50: EnemyData(0x50, "Jumping Pirhana Plant, spit fire", 20, (0,0), ["pipe"], ["pipe"]),
    0x59: EnemyData(0x59, "Turn block bridge, horizontal and vertical", 20, (0,0), ["skip"], ["skip"]),
    0x5A: EnemyData(0x5A, "Turn block bridge, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x6B: EnemyData(0x6B, "Spring board, left wall", 20, (0,0), ["skip"], ["skip"]),
    0x6C: EnemyData(0x6C, "Spring board, right wall", 20, (0,0), ["skip"], ["skip"]),
    0x6D: EnemyData(0x6D, "Invisible solid block", 20, (0,0), ["skip"], ["skip"]),
    0x74: EnemyData(0x74, "Mushroom", 20, (0,0), ["skip"], ["skip"]),
    0x75: EnemyData(0x75, "Flower", 20, (0,0), ["skip"], ["skip"]),
    0x77: EnemyData(0x77, "Feather", 20, (0,0), ["skip"], ["skip"]),
    0x79: EnemyData(0x79, "Growing Vine", 20, (0,0), ["skip"], ["skip"]),
    0x7B: EnemyData(0x7B, "Standard Goal Point", 20, (0,0), ["skip"], ["skip"]),
    0x7E: EnemyData(0x7E, "Flying Red coin, worth 5 coins", 20, (0,0), ["skip"], ["skip"]),
    0x7F: EnemyData(0x7F, "Flying Yellow 1-UP", 20, (0,0), ["skip"], ["skip"]),
    0x81: EnemyData(0x81, "Changing item from a translucent block", 20, (0,0), ["skip"], ["skip"]),
    0x83: EnemyData(0x83, "Left flying question block, coin/flower/feather/1-UP (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0x84: EnemyData(0x84, "Flying question block, coin/flower/feather/1-UP (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0xB1: EnemyData(0xB1, "Creating/Eating block (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xB9: EnemyData(0xB9, "Info Box, message 1/2 (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xBD: EnemyData(0xBD, "Sliding Koopa without a shell", 20, (0,0), ["ground"], ["floating", "ground"]),
    0xC1: EnemyData(0xC1, "Flying grey turnblocks, first up/down (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xC7: EnemyData(0xC7, "Invisible mushroom", 20, (0,0), ["skip"], ["skip"]),
    0xC8: EnemyData(0xC8, "Light switch block for dark room", 20, (0,0), ["skip"], ["skip"]),
    0xDA: EnemyData(0xDA, "Green Koopa shell", 4, (0,0), ["ground"], ["ground"]),
    0xDB: EnemyData(0xDB, "Red Koopa shell", 2, (0,0), ["ground"], ["ground"]),
    0xDC: EnemyData(0xDC, "Blue Koopa shell", 1, (0,0), ["ground"], ["ground"]),
    0xDD: EnemyData(0xDD, "Yellow Koopa shell", 1, (0,0), ["ground"], ["ground"]),
    0xDF: EnemyData(0xDF, "Green shell, won't use Special World color", 1, (0,0), ["ground"], ["ground"]),
    0x0D: EnemyData(0x0D, "Bob-omb", 20, (0,0), ["ground"], ["ground", "shooter", "ambush small", "bounceable"]),
    0x11: EnemyData(0x11, "Buzzy Beetle", 15, (0,0), ["ground"], ["ground", "kickable", "bounceable"]),
    0x13: EnemyData(0x13, "Spiny", 20, (0,0), ["ground"], ["ground"]),
    0x14: EnemyData(0x14, "Spiny falling", 20, (0,0), ["floating"], ["ground", "ambush small", "ambush"]),
    0x15: EnemyData(0x15, "Fish, horizontal", 20, (0,0), ["water"], ["water"]),
    0x16: EnemyData(0x16, "Fish, vertical", 20, (0,0), ["water"], ["water"]),
    0x18: EnemyData(0x18, "Surface jumping fish", 20, (0,0), ["surface"], ["surface"]),
    0x1B: EnemyData(0x1B, "Bouncing football in place", 15, (0,0), ["ground"], ["ground", "ambush"]),
    0x1D: EnemyData(0x1D, "Hopping flame", 15, (0,0), ["ground"], ["ground", "shooter", "pipe", "upsidedown pipe"]),
    0x1E: EnemyData(0x1E, "Lakitu Normal/Fish (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x1F: EnemyData(0x1F, "Magikoopa", 20, (0,0), ["skip"], ["skip"]),
    0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["floating", "ground", "line", "rotating", "water"]),
    0x22: EnemyData(0x22, "Green vertical net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x23: EnemyData(0x23, "Red fast vertical net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x24: EnemyData(0x24, "Green horizontal net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x25: EnemyData(0x25, "Red fast horizontal net Koopa, below/above (X&1)", 20, (0,0), ["net"], ["net"]),
    0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["ambush"], ["floating", "water", "ambush"]),
    0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["ground"], ["ground", "water", "ambush small"]),
    0x28: EnemyData(0x28, "Big Boo", 3, (0,3), ["floating"], ["floating", "flying", "ground", "water", "lava", "rotating", "buried", "shooter", "pipe", "upsidedown pipe"]),
    0x29: EnemyData(0x29, "Koopa Kid (place at X=12, Y=0 to 6)", 20, (0,0), ["skip"], ["skip"]),
    0x2A: EnemyData(0x2A, "Upside down Piranha Plant", 20, (0,1), ["upsidedown pipe"], ["upsidedown pipe"]),
    0x2B: EnemyData(0x2B, "Sumo Brother's fire lightning", 15, (0,0), ["floating"], ["floating", "flying", "ambush"]),
    0x2C: EnemyData(0x2C, "Yoshi egg Red/Blue/Yellow/Blue (X&3)", 20, (0,0), ["skip"], ["skip"]),
    0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["ground", "wall"], ["ground", "wall", "floating", "upsidedown pipe"]),
    0x30: EnemyData(0x30, "Dry Bones, throws bones", 18, (0,0), ["ground"], ["ground", "bounceable"]),
    0x31: EnemyData(0x31, "Bony Beetle", 18, (0,0), ["ground"], ["ground", "bounceable"]),
    0x32: EnemyData(0x32, "Dry Bones, stay on ledge", 20, (0,0), ["ground"], ["ground", "bounceable", "stay on ledge"]),
    0x33: EnemyData(0x33, "Fireball, vertical", 20, (0,0), ["lava"], ["lava"]),
    0x34: EnemyData(0x34, "Boss fireball, stationary", 20, (0,0), ["skip"], ["skip"]),
    0x37: EnemyData(0x37, "Boo", 17, (0,0), ["floating"], ["floating", "flying", "ground", "water", "lava", "rotating", "buried", "shooter", "ambush small", "pipe", "upsidedown pipe"]),
    0x38: EnemyData(0x38, "Eerie", 15, (0,0), ["flying"], ["floating", "flying", "lava", "line", "shooter", "upsidedown pipe"]),
    0x39: EnemyData(0x39, "Eerie, wave motion", 15, (0,0), ["flying"], ["flying", "ground", "lava", "water", "line", "shooter", "upsidedown pipe"]),
    0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["floating", "water"]),
    0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["wall", "flying", "floating"]),
    0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["wall", "floating"]),
    0x3D: EnemyData(0x3D, "Rip Van Fish", 15, (0,0), ["water"], ["water", "ground"]),
    0x3F: EnemyData(0x3F, "Para-Goomba", 15, (0,0), ["floating"], ["floating", "flying", "ambush", "ambush small"]),
    0x40: EnemyData(0x40, "Para-Bomb", 15, (0,0), ["floating"], ["floating", "flying", "ambush", "ambush small"]),
    0x41: EnemyData(0x41, "Dolphin, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x42: EnemyData(0x42, "Dolphin2, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x43: EnemyData(0x43, "Dolphin, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x44: EnemyData(0x44, "Torpedo Ted", 20, (0,0), ["water"], ["skip"]),
    0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x47: EnemyData(0x47, "Swimming/Jumping fish, doesn't need water", 15, (0,0), ["surface", "floating"], ["ground", "floating", "surface", "shooter"]),
    0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["ground", "ambush", "ambush small"]),
    0x49: EnemyData(0x49, "Growing/shrinking pipe end", 20, (0,0), ["skip"], ["skip"]),
    0x4A: EnemyData(0x4A, "Goal Point Question Sphere", 20, (0,0), ["skip"], ["skip"]),
    0x4B: EnemyData(0x4B, "Pipe dwelling Lakitu", 20, (0,0), ["pipe"], ["pipe"]),
    0x4C: EnemyData(0x4C, "Exploding Block, fish/goomba/Koopa/Koopa with shell (X&3)", 15, (0,0), ["floating"], ["floating", "water", "shooter"]),
    0x4D: EnemyData(0x4D, "Ground dwelling Monty Mole, follow/hop (X&1)", 15, (0,0), ["floating", "buried", "ground"], ["floating", "buried"]),
    0x4E: EnemyData(0x4E, "Ledge dwelling Monty Mole, follow/hop (X&1)", 15, (0,0), ["floating"], ["skip"]),
    0x51: EnemyData(0x51, "Ninji", 20, (0,0), ["ground"], ["ground", "bounceable"]),
    0x52: EnemyData(0x52, "Moving ledge hole in ghost house", 20, (0,0), ["skip"], ["skip"]),
    0x54: EnemyData(0x54, "Climbing net door, use with object 0x4A-E", 20, (0,0), ["skip"], ["skip"]),
    0x55: EnemyData(0x55, "Checkerboard platform, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x56: EnemyData(0x56, "Flying rock platform, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0x57: EnemyData(0x57, "Checkerboard platform, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x58: EnemyData(0x58, "Flying rock platform, vertical", 20, (0,0), ["skip"], ["skip"]),
    0x5B: EnemyData(0x5B, "Brown platform floating in water", 20, (0,0), ["skip"], ["skip"]),
    0x5C: EnemyData(0x5C, "Checkerboard platform that falls", 20, (0,0), ["skip"], ["skip"]),
    0x5D: EnemyData(0x5D, "Orange platform floating in water", 20, (0,0), ["skip"], ["skip"]),
    0x5E: EnemyData(0x5E, "Orange platform, goes on forever", 20, (0,0), ["skip"], ["skip"]),
    0x5F: EnemyData(0x5F, "Brown platform on a chain", 20, (0,0), ["skip"], ["skip"]),
    0x60: EnemyData(0x60, "Flat green switch palace switch", 20, (0,0), ["skip"], ["skip"]),
    0x61: EnemyData(0x61, "Floating skulls", 20, (0,0), ["skip"], ["skip"]),
    0x62: EnemyData(0x62, "Brown platform, line-guided", 20, (0,0), ["skip"], ["skip"]),
    0x63: EnemyData(0x63, "Checker/brown platform, line-guided (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x64: EnemyData(0x64, "Rope mechanism, line-guided (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x65: EnemyData(0x65, "Chainsaw, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x66: EnemyData(0x66, "Upside down chainsaw, line-guided, null/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x67: EnemyData(0x67, "Grinder, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x68: EnemyData(0x68, "Fuzz Ball, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line"]),
    0x6A: EnemyData(0x6A, "Coin game cloud", 20, (0,0), ["skip"], ["skip"]),
    0x6E: EnemyData(0x6E, "Dino Rhino", 10, (0,0), ["ground"], ["ground", "bounceable"]),
    0x6F: EnemyData(0x6F, "Dino Torch", 12, (0,0), ["ground"], ["ground", "bounceable"]),
    0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["ground"], ["ground"]),
    0x71: EnemyData(0x71, "Super Koopa, red cape, swoop", 18, (0,0), ["floating", "ambush"], ["floating", "ambush", "ambush small"]),
    0x72: EnemyData(0x72, "Super Koopa, yellow cape, swoop", 18, (0,0), ["floating", "ambush"], ["floating", "ambush", "ambush small"]),
    0x73: EnemyData(0x73, "Super Koopa, feather/yellow cape (X&1)", 18, (0,0), ["ground"], ["ground"]),
    0x7A: EnemyData(0x7A, "Firework, makes Mario temporarily invisible", 20, (0,0), ["skip"], ["skip"]),
    0x7D: EnemyData(0x7D, "Balloon", 20, (0,0), ["skip"], ["skip"]),
    0x86: EnemyData(0x86, "Wiggler", 5, (0,0), ["ground"], ["ground", "stay on ledge"]),
    0x87: EnemyData(0x87, "Lakitu's cloud, no time limit", 20, (0,0), ["skip"], ["skip"]),
    0x8A: EnemyData(0x8A, "Bird from Yoshi's house, max of 4", 20, (0,0), ["skip"], ["skip"]),
    0x8B: EnemyData(0x8B, "Puff of smoke from Yoshi's house", 20, (0,0), ["skip"], ["skip"]),
    0x8D: EnemyData(0x8D, "Ghost house exit sign and door", 20, (0,0), ["skip"], ["skip"]),
    0x8E: EnemyData(0x8E, "Invisible 'Warp Hole' blocks", 20, (0,0), ["skip"], ["skip"]),
    0x8F: EnemyData(0x8F, "Scale platforms, long/short between (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["flying"], ["ground", "floating", "flying", "line", "ambush", "shooter"]),
    0x91: EnemyData(0x91, "Chargin' Chuck", 15, (0,0), ["ground"], ["ground", "bounceable", "pipe", "upsidedown pipe"]),
    0x92: EnemyData(0x92, "Splitin' Chuck", 12, (0,0), ["ground"], ["ground", "upsidedown pipe"]),
    0x93: EnemyData(0x93, "Bouncin' Chuck", 15, (0,0), ["ground"], ["ground", "pipe", "upsidedown pipe"]),
    0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["ground"], ["ground"]),
    0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["ground"], ["ground", "bounceable", "stay on ledge"]),
    0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["ground"], ["ground"]),
    0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["ground"], ["ground"]),
    0x9A: EnemyData(0x9A, "Sumo Brother", 20, (0,0), ["skip"], ["skip"]),
    0x9B: EnemyData(0x9B, "Hammer Brother (requires sprite 9C)", 20, (0,0), ["skip"], ["skip"]),
    0x9C: EnemyData(0x9C, "Flying blocks for Hammer Brother", 20, (0,0), ["skip"], ["skip"]),
    0x9D: EnemyData(0x9D, "Bubble with Goomba/bomb/fish/mushroom (X&3)", 10, (0,0), ["flying"], ["flying"]),
    0x9E: EnemyData(0x9E, "Ball and Chain, clockwise/counter (X&1)", 15, (0,0), ["rotating"], ["floating", "rotating", "line", "buried", "water", "shooter", "pipe", "upsidedown pipe"]),
    0x9F: EnemyData(0x9F, "Banzai Bill", 10, (0,0), ["flying"], ["flying", "line", "shooter"]),
    0xA2: EnemyData(0xA2, "MechaKoopa", 12, (0,0), ["ground"], ["ground"]),
    0xA3: EnemyData(0xA3, "Grey platform on chain, clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xA4: EnemyData(0xA4, "Floating Spike ball, slow/fast (X&1)", 20, (0,0), ["surface"], ["surface"]),
    0xA5: EnemyData(0xA5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 20, (0,0), ["wall"], ["wall"]),
    0xA6: EnemyData(0xA6, "HotHead, ground-guided, left/right (X&1)", 20, (0,0), ["wall"], ["wall"]),
    0xA8: EnemyData(0xA8, "Blargg", 20, (0,0), ["skip"], ["pipe"]),
    0xAA: EnemyData(0xAA, "Fishbone", 20, (0,0), ["flying", "floating", "water"], ["flying", "floating", "water", "line", "shooter"]),
    0xAB: EnemyData(0xAB, "Rex", 20, (0,0), ["ground"], ["ground", "bounceable"]),
    0xAC: EnemyData(0xAC, "Wooden Spike, moving down and up", 20, (0,0), ["skip"], ["skip"]),
    0xAD: EnemyData(0xAD, "Wooden Spike, moving up/down first (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xAE: EnemyData(0xAE, "Fishin' Boo", 20, (0,0), ["skip"], ["skip"]),
    0xAF: EnemyData(0xAF, "Boo Block", 20, (0,0), ["skip"], ["skip"]),
    0xB0: EnemyData(0xB0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["flying", "water"]),
    0xB2: EnemyData(0xB2, "Falling Spike", 15, (0,0), ["floating"], ["floating", "water", "flying", "ambush", "ambush small"]),
    0xB3: EnemyData(0xB3, "Bowser statue fireball", 15, (0,0), ["flying"], ["flying", "floating"]),
    0xB4: EnemyData(0xB4, "Grinder, non-line-guided", 17, (0,0), ["ground"], ["ground"]),
    0xB6: EnemyData(0xB6, "Reflecting fireball", 20, (0,0), ["flying"], ["flying"]),
    0xB7: EnemyData(0xB7, "Carrot Top lift, upper right", 20, (0,0), ["skip"], ["skip"]),
    0xB8: EnemyData(0xB8, "Carrot Top lift, upper left", 20, (0,0), ["skip"], ["skip"]),
    0xBA: EnemyData(0xBA, "Timed lift, 4 sec/1 sec (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xBB: EnemyData(0xBB, "Grey moving castle block, horizontal", 20, (0,0), ["skip"], ["skip"]),
    0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["ground"], ["ground"]),
    0xBE: EnemyData(0xBE, "Swooper Bat, hang/fly/fly/fly (X&3)", 20, (0,0), ["floating", "ambush"], ["floating", "rotating", "ambush", "ambush small"]),
    0xBF: EnemyData(0xBF, "Mega Mole", 15, (0,0), ["ground"], ["ground"]),
    0xC0: EnemyData(0xC0, "Grey platform on lava, sinks", 20, (0,0), ["skip"], ["skip"]),
    0xC2: EnemyData(0xC2, "Blurp fish", 20, (0,0), ["water"], ["water", "floating", "flying"]),
    0xC3: EnemyData(0xC3, "A Porcu-Puffer fish", 20, (0,0), ["skip"], ["skip"]),
    0xC4: EnemyData(0xC4, "Grey platform that falls", 20, (0,0), ["skip"], ["skip"]),
    0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["skip"], ["skip"]),
    0xC6: EnemyData(0xC6, "Dark room with spot light (disco ball)", 20, (0,0), ["skip"], ["skip"]),
    0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 3, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    0xE0: EnemyData(0xE0, "3 platforms on chains, clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
    0xE2: EnemyData(0xE2, "Boo Buddies, counter-clockwise", 20, (0,0), ["skip"], ["skip"]),
    0xE3: EnemyData(0xE3, "Boo Buddies, clockwise", 20, (0,0), ["skip"], ["skip"]),
    0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["skip"], ["skip"]),

    0xC9: EnemyData(0xC9, "Bullet Bill shooter", 35, (0,0), ["shooter"], ["shooter"]),
    0xCA: EnemyData(0xCA, "Torpedo Launcher", 35, (0,0), ["shooter"], ["shooter"]),

    0xCB: EnemyData(0xCB, "Eerie, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD1: EnemyData(0xD1, "Jumping fish, generator", 20, (0,0), ["generator"], ["generator"]),
    0xCC: EnemyData(0xCC, "Para-Goomba, generator", 20, (0,0), ["generator"], ["generator"]),
    0xCD: EnemyData(0xCD, "Para-Bomb, generator", 20, (0,0), ["generator"], ["generator"]),
    0xCE: EnemyData(0xCE, "Para-Bomb and Para-Goomba, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD3: EnemyData(0xD3, "Super Koopa, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD4: EnemyData(0xD4, "Bubble with Goomba and Bob-omb, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD5: EnemyData(0xD5, "Bullet Bill, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD6: EnemyData(0xD6, "Bullet Bill surrounded, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD7: EnemyData(0xD7, "Bullet Bill diagonal, generator", 20, (0,0), ["generator"], ["generator"]),
    0xD8: EnemyData(0xD8, "Bowser statue fire breath, generator", 20, (0,0), ["generator"], ["generator"]),
}

tag_list = {
    "ground": [],
    "flying": [],
    "floating": [],
    "rotating": [],
    "water": [],
    "lava": [],
    "wall": [],
    "buried": [],
    "net": [],
    "surface": [],
    "line": [],
    "pipe": [],
    "upsidedown pipe": [],
    "ambush": [],
    "generator": [],
    "shooter": [],
    "kickable": [],
    "ambush small": [],
    "flying koopa": [],
    "blue koopa": [],
    "bouncing koopa": [],
    "rotating platforms": [],
    "boss enemy": [],
    "mode 7": [],
    "bounceable": [],
    "force line spin": [],
    "mega mole": [],
    "stay on ledge": [],
}

SPRITE_POINTERS_ADDR = 0x2EC00

# Per level special properties for sprites, these replace the default settings.
# Default settings are restored per level
# Remember to add new/special tags to tag_list
enemy_list_special_cases = {
    #0x00C: {
    #    0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["skip"], ["skip"]),
    #},
    0x00D: {
        0x71: EnemyData(0x71, "Super Koopa, red cape, swoop", 20, (0,0), ["skip"], ["skip"]),
    },
    0x10B: {
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["flying koopa"], ["skip"]),
        0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
    },
    0x134: {
        0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x135: {
        0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x023: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x103: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x015: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x016: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x017: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["ground"], ["ground", "blue koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["blue koopa"], ["skip"]),
    },
    0x005: {
        0x09: EnemyData(0x09, "Green bouncing Koopa (Y&1)", 15, (0,0), ["ground"], ["ground", "bouncing koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["bouncing koopa"], ["skip"]),
        0xA3: EnemyData(0xA3, "Grey platform on chain, clockwise/counter (X&1)", 20, (0,0), ["rotating platforms"], ["rotating platforms"]),
        0xE0: EnemyData(0xE0, "3 platforms on chains, clockwise/counter (X&1)", 20, (0,0), ["rotating platforms"], ["rotating platforms"]),
    },
    0x120: {
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x28: EnemyData(0x28, "Big Boo", 4, (0,3), ["floating"], ["skip"]),
        0xB0: EnemyData(0xB0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
        0xB6: EnemyData(0xB6, "Reflecting fireball", 20, (0,0), ["flying"], ["skip"]),
    },
    0x12A: {
        0x06: EnemyData(0x06, "Blue Koopa", 10, (0,0), ["skip"], ["skip"]),
    },
    0x128: {
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
    },
    0x0E9: {
        0xDC: EnemyData(0xDC, "Blue Koopa shell", 1, (0,0), ["skip"], ["skip"]),
    },
    0x009: {
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["ambush small"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
    },
    0x001: {
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["kickable"], ["skip"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["bouncing koopa"], ["skip"]),
    },
    0x11A: {
        0xB4: EnemyData(0xB4, "Grinder, non-line-guided", 17, (0,0), ["ground"], ["skip"]),
        0x4F: EnemyData(0x4F, "Jumping Pirhana Plant", 20, (0,0), ["buried"], ["skip"]),
        0x50: EnemyData(0x50, "Jumping Pirhana Plant, spit fire", 20, (0,0), ["buried"], ["skip"]),
        0xDA: EnemyData(0xDA, "Green Koopa shell", 4, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0xDB: EnemyData(0xDB, "Red Koopa shell", 2, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0xDC: EnemyData(0xDC, "Blue Koopa shell", 1, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0xDD: EnemyData(0xDD, "Yellow Koopa shell", 1, (0,0), ["kickable"], ["ground", "kickable", "bounceable"]),
        0xDF: EnemyData(0xDF, "Green shell, won't use Special World color", 1, (0,0), ["bounceable"], ["ground"]),
        0x11: EnemyData(0x11, "Buzzy Beetle", 15, (0,0), ["bounceable"], ["ground", "kickable", "bounceable"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
    },
    0x10A: {
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
    },
    0x136: {
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["ambush"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["ground"], ["skip"]),
        0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x28: EnemyData(0x28, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
        0x08: EnemyData(0x08, "Green Koopa, flying left", 20, (0,0), ["flying"], ["floating", "flying", "flying koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x1F2: {
        0xB6: EnemyData(0xB6, "Reflecting fireball", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x28: EnemyData(0x28, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0x1D: EnemyData(0x1D, "Hopping flame", 12, (0,0), ["ground"], ["boss enemy"]),
        0x13: EnemyData(0x13, "Spiny", 15, (0,0), ["ground"], ["boss enemy"]),
        0x14: EnemyData(0x14, "Spiny falling", 15, (0,0), ["floating"], ["boss enemy"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["boss enemy"]),
        0x91: EnemyData(0x91, "Chargin' Chuck", 10, (0,0), ["ground"], ["boss enemy"]),
        0x92: EnemyData(0x92, "Splitin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x93: EnemyData(0x93, "Bouncin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 7, (0,0), ["ground"], ["boss enemy"]),
        0xA5: EnemyData(0xA5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 12, (0,0), ["wall"], ["boss enemy"]),
        0xA6: EnemyData(0xA6, "HotHead, ground-guided, left/right (X&1)", 10, (0,0), ["wall"], ["boss enemy"]),
        0xAE: EnemyData(0xAE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0xB4: EnemyData(0xB4, "Grinder, non-line-guided", 8, (0,0), ["ground"], ["boss enemy"]),
        0xBF: EnemyData(0xBF, "Mega Mole", 10, (0,0), ["ground"], ["boss enemy"]),
        0xCB: EnemyData(0xCB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD5: EnemyData(0xD5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD6: EnemyData(0xD6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD7: EnemyData(0xD7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
    },
    0x0D3: {
        0xB6: EnemyData(0xB6, "Reflecting fireball", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x28: EnemyData(0x28, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0x1D: EnemyData(0x1D, "Hopping flame", 12, (0,0), ["ground"], ["boss enemy"]),
        0x13: EnemyData(0x13, "Spiny", 15, (0,0), ["ground"], ["boss enemy"]),
        0x14: EnemyData(0x14, "Spiny falling", 15, (0,0), ["floating"], ["boss enemy"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["boss enemy"]),
        0x91: EnemyData(0x91, "Chargin' Chuck", 10, (0,0), ["ground"], ["boss enemy"]),
        0x92: EnemyData(0x92, "Splitin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x93: EnemyData(0x93, "Bouncin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 5, (0,0), ["ground"], ["boss enemy"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 7, (0,0), ["ground"], ["boss enemy"]),
        0xA5: EnemyData(0xA5, "Fuzzball/Sparky, ground-guided, left/right (X&1)", 12, (0,0), ["wall"], ["boss enemy"]),
        0xA6: EnemyData(0xA6, "HotHead, ground-guided, left/right (X&1)", 10, (0,0), ["wall"], ["boss enemy"]),
        0xAE: EnemyData(0xAE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0xB4: EnemyData(0xB4, "Grinder, non-line-guided", 8, (0,0), ["ground"], ["boss enemy"]),
        0xBF: EnemyData(0xBF, "Mega Mole", 10, (0,0), ["ground"], ["boss enemy"]),
        0xCB: EnemyData(0xCB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD5: EnemyData(0xD5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD6: EnemyData(0xD6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD7: EnemyData(0xD7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xAF: EnemyData(0xAF, "Boo Block", 12, (0,0), ["skip"], ["boss enemy"]),
        0x37: EnemyData(0x37, "Boo", 17, (0,0), ["floating"], ["boss enemy"]),
    },
    0x1EB: {
        0x33: EnemyData(0x33, "Fireball, vertical", 20, (0,0), ["boss enemy"], ["boss enemy"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 15, (0,0), ["skip"], ["boss enemy"]),
        0x28: EnemyData(0x28, "Big Boo", 1, (0,3), ["floating"], ["boss enemy"]),
        0xAE: EnemyData(0xAE, "Fishin' Boo", 1, (0,0), ["skip"], ["boss enemy"]),
        0xCB: EnemyData(0xCB, "Eerie, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD5: EnemyData(0xD5, "Bullet Bill, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD6: EnemyData(0xD6, "Bullet Bill surrounded, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD7: EnemyData(0xD7, "Bullet Bill diagonal, generator", 4, (0,0), ["generator"], ["boss enemy"]),
        0xD1: EnemyData(0xD1, "Jumping fish, generator", 3, (0,0), ["generator"], ["boss enemy"]),
        0xD3: EnemyData(0xD3, "Super Koopa, generator", 20, (0,0), ["generator"], ["boss enemy"]),
        0xAF: EnemyData(0xAF, "Boo Block", 12, (0,0), ["skip"], ["boss enemy"]),
        0xB0: EnemyData(0xB0, "Reflecting stream of Boo Buddies", 10, (0,0), ["flying"], ["boss enemy"]),
        0x37: EnemyData(0x37, "Boo", 17, (0,0), ["floating"], ["boss enemy"]),
    },
    0x118: {
        0x91: EnemyData(0x91, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
    },
    0x11C: {
        0x28: EnemyData(0x28, "Big Boo", 1, (0,3), ["floating"], ["skip"]),
        0x37: EnemyData(0x37, "Boo", 17, (0,0), ["floating"], ["skip"]),
        0xB0: EnemyData(0xB0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
    },
    0x1FE: {
        0x28: EnemyData(0x28, "Big Boo", 1, (0,3), ["floating"], ["skip"]),
        0x37: EnemyData(0x37, "Boo", 17, (0,0), ["floating"], ["skip"]),
        0xB0: EnemyData(0xB0, "Reflecting stream of Boo Buddies", 15, (0,0), ["flying"], ["skip"]),
    },
    0x1C2: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        0xAF: EnemyData(0xAF, "Boo Block", 12, (0,0), ["skip"],  ["flying koopa"]),
    },
    0x115: {
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["ground"], ["skip"]),
        0x1B: EnemyData(0x1B, "Bouncing football in place", 15, (0,0), ["ground"], ["skip"]),
    },
    0x10F: {
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying koopa"], ["flying", "floating", "flying koopa"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x116: {
        0x91: EnemyData(0x91, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        #0xBF: EnemyData(0xBF, "Mega Mole", 15, (0,0), ["skip"], ["skip"]),
    },
    0x00B: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x1C: EnemyData(0x1C, "Bullet Bill", 10, (0,0), ["skip"], ["skip"]),
    },
    0x0E1: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0E0: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["ground", "wall"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),

        0x28: EnemyData(0x28, "Big Boo", 4, (0,3), ["floating"], ["skip"]),
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["floating", "water"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["water", "wall", "floating"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["flying"], ["skip"]),
        0x30: EnemyData(0x30, "Dry Bones, throws bones", 18, (0,0), ["water", "wall", "floating"], ["wall"]),
        0x31: EnemyData(0x31, "Bony Beetle", 18, (0,0), ["water", "wall", "floating"], ["wall"]),

    },
    0x00F: {
        0x65: EnemyData(0x65, "Chainsaw, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x66: EnemyData(0x66, "Upside down chainsaw, line-guided, null/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x67: EnemyData(0x67, "Grinder, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0x68: EnemyData(0x68, "Fuzz Ball, line-guided, right/left (X&1)", 20, (0,0), ["line"], ["line", "force line spin"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["force line spin"], ["skip"]),
    },
    0x11D: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x1E8: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x1E9: {
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 2, (0,0), ["floating", "flying"], ["floating", "flying", "water", "shooter"]),
    },
    0x01D: {
        0x97: EnemyData(0x97, "Puntin' Chuck", 5, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 5, (0,0), ["skip"], ["skip"]),
        0x2E: EnemyData(0x2E, "Spike Top", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
    },
    0x022: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0F5: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0F6: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D0: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D1: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["skip"], ["skip"]),
    },
    0x0D2: {
        0x0A: EnemyData(0x0A, "Red vertical flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0x0B: EnemyData(0x0B, "Red horizontal flying Koopa", 20, (0,0), ["flying"], ["flying", "floating", "flying koopa"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["flying koopa"], ["skip"]),
    },
    0x10E: {
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x6E: EnemyData(0x6E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x6F: EnemyData(0x6F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x91: EnemyData(0x91, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x92: EnemyData(0x92, "Splitin' Chuck", 12, (0,0), ["skip"], ["skip"]),
        0x93: EnemyData(0x93, "Bouncin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x28: EnemyData(0x28, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x1BD: {
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x6E: EnemyData(0x6E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x6F: EnemyData(0x6F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x91: EnemyData(0x91, "Chargin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x92: EnemyData(0x92, "Splitin' Chuck", 12, (0,0), ["skip"], ["skip"]),
        0x93: EnemyData(0x93, "Bouncin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x94: EnemyData(0x94, "Whistlin' Chuck, fish/Koopa (X&1)", 5, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x28: EnemyData(0x28, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x00E: {
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x6E: EnemyData(0x6E, "Dino Rhino", 10, (0,0), ["skip"], ["skip"]),
        0x6F: EnemyData(0x6F, "Dino Torch", 12, (0,0), ["skip"], ["skip"]),
        0x95: EnemyData(0x95, "Clapin' Chuck", 15, (0,0), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x99: EnemyData(0x99, "Volcano Lotus", 15, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0xBF: EnemyData(0xBF, "Mega Mole", 10, (0,0), ["skip"], ["skip"]),
    },
    0x020: {
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x9F: EnemyData(0x9F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x28: EnemyData(0x28, "Big Boo", 3, (0,3), ["skip"], ["skip"]),
    },
    0x127: {
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
    },
    0x116: {
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x9F: EnemyData(0x9F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["mega mole"], ["skip"]),
        0xBF: EnemyData(0xBF, "Mega Mole", 20, (0,0), ["ground"], ["ground", "mega mole"]),
    },
    0x1F3: {
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x9F: EnemyData(0x9F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
    },
    0x1E2: {
        0x3A: EnemyData(0x3A, "Urchin, fixed vertical/horizontal (X&1)", 15, (0,0), ["skip"], ["skip"]),
        0x3B: EnemyData(0x3B, "Urchin, wall detect v/h (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x3C: EnemyData(0x3C, "Urchin, wall follow clockwise/counter (X&1)", 20, (0,0), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0x26: EnemyData(0x26, "Thwomp", 15, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x9F: EnemyData(0x9F, "Banzai Bill", 10, (0,0), ["skip"], ["skip"]),
        0x90: EnemyData(0x90, "Large green gas bubble", 5, (0,3), ["skip"], ["skip"]),
        0x97: EnemyData(0x97, "Puntin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x98: EnemyData(0x98, "Pitchin' Chuck", 10, (0,0), ["skip"], ["skip"]),
        0x48: EnemyData(0x48, "Diggin' Chuck's rock", 18, (0,0), ["skip"], ["skip"]),
        0xBC: EnemyData(0xBC, "Bowser statue, normal/fire/leap (X&3)", 20, (0,0), ["skip"], ["skip"]),
        0x46: EnemyData(0x46, "Diggin' Chuck", 10, (0,0), ["skip"], ["skip"]),
    },
    0x1E2: {
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x20: EnemyData(0x20, "Magikoopa's magic, stationary", 20, (0,0), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
    },
    0x024: {
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0xDE: EnemyData(0xDE, "Group of 5 eeries, wave motion", 10, (0,0), ["skip"], ["skip"]),
    },
    0x0E7: {
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["stay on ledge"], ["skip"]),
        0x70: EnemyData(0x70, "Pokey", 15, (0,4), ["skip"], ["skip"]),
        0x27: EnemyData(0x27, "Thwimp", 20, (0,0), ["skip"], ["skip"]),
        0xB4: EnemyData(0xB4, "Grinder, non-line-guided", 17, (0,0), ["skip"], ["skip"]),
    },
    0x008: {
        0xDB: EnemyData(0xDB, "Red Koopa shell", 2, (0,0), ["skip"], ["skip"]),
    },
    0x006: {
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["kickable"], ["skip"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["bounceable"], ["skip"]),
    },
    0x117: {
        0x11: EnemyData(0x11, "Buzzy Beetle", 15, (0,0), ["bounceable", "kickable"], ["ground", "kickable", "bounceable"]),
    },
    0x118: {
        0x11: EnemyData(0x11, "Buzzy Beetle", 15, (0,0), ["bounceable", "kickable"], ["ground", "kickable", "bounceable"]),
    },
    0x010: {
        0xC5: EnemyData(0xC5, "Big Boo Boss", 20, (0,0), ["kickable"], ["skip"]),
        0xA1: EnemyData(0xA1, "Bowser's bowling ball", 20, (0,0), ["bounceable"], ["skip"]),
    },
}

full_displacement_tags = [
    "ground",
    "buried",
]

half_displacement_tags = [
    "flying",
    "floating",
    "water",
]

def build_enemy_replacements(current_enemy_list: dict[int, EnemyData]):
    # Creates a per-level database with special cases for enemies
    database = copy.deepcopy(tag_list)
    for enemy_id, data in current_enemy_list.items():
        for tag in data.replaces:
            if tag != "skip":
                database[tag] += [enemy_id for _ in range(data.weight)]
    return database

ci3_koopa_placements = [
    0x03D8C2,
    0x03D8C8,
    0x03D8CE,
    0x03D8D7,
    0x03D8DA,
    0x03D8DD,
    0x03D8E6,
    0x03D8E9,
    0x03D8F2,
    0x03D8F5,
    0x03D8FE,
    0x03D901,
    0x03D904,
    0x03D90A,
    0x03D910,
    0x03D913,
    0x03D94C,
]

yi3_koopa_placements = [
    0x03C5AF,
    0x03C5BE,
    0x03C5B8,
]

dp2_koopa_placements = [
    0x03C755,
    0x03C75B,
    0x03C761,
    0x03C767,
]

vs2_koopa_placements = [
    0x03CE23,
    0x03CE29,
    0x03CE2C,
    0x03CE2F,
    0x03CE32,
]

sw4_koopa_placements = [
    0x03E2B6,
    0x03E2B9,
    0x03E2BF,
    0x03E2C2,
    0x03E2C5,
    0x03E2C8,
    0x03E2CB,
    0x03E2E3,
    0x03E2EF,
    0x03E2F5,
    0x03E31C,
    0x03E325,
]

sw5_koopa_placements_1 = [
    0x03E33C,
    0x03E348,
    0x03E351,
    0x03E354,
    0x03E35D,
    0x03E366,
    0x03E36C,
]
    
sw5_koopa_placements_2 = [
    0x03E372,
    0x03E375,
    0x03E378,
    0x03E37B,
    0x03E37E,
    0x03E381,
    0x03E384,
    0x03E387,
    0x03E38D,
    0x03E393,
    0x03E396,
    0x03E39C,
]

dp1_koopa_placements = [
    0x03C6E8,
    0x03C6EB,
    0x03C6E5,
    0x03C6F7,
    0x03C718,
    0x03C71E,
    0x03C721,
    0x03C724,
    0x03C727,
    0x03C72A,
    0x03C733,
    0x03C73F,
    0x03C742,
]

def modify_sprite_data(rom: bytearray, seed: int) -> bytearray:
    # Several of these edits consist in adding an unused sprite id on the original level so it can be replaced
    # by a specific sprite group that's manually crafted for that specific level instead of relying on the generic solution
    #
    # Mainly done to reduce dynamic sprite load which usually leads to corrupted graphics data for the rest of the level
    # Sprites are loaded in columns, so we have to be **extra** careful with the replacements in specific levels
    # At level load the sprites are loaded **two screens** in advance, so some levels might not see a very high amount
    # of randomness in them
    # 
    # Other cases are handled so new sprites don't block the current path and create **new** logic requirements
    # At this point we want to fully avoid this, as this runs during the patching process which shouldn't include logic changes

    # We'd like to keep a consistent randomization between patching sessions
    random.seed(seed)

    # level 00D edits
    rom[0x03D304-20] = 0x71

    # DS2 (10B)
    # Guarantees a kickable sprite at the start
    rom[0x03CA18+2] = 0xA1

    # Guarantees only koopas at the end of the level
    rom[0x03CA51+2] = 0xC5
    rom[0x03CA54+2] = 0xC5
    rom[0x03CA57+2] = 0xC5
    rom[0x03CA5A+2] = 0xC5
    rom[0x03CA5D+2] = 0xC5
    rom[0x03CA60+2] = 0xC5
    rom[0x03CA63+2] = 0xC5
    rom[0x03CA66+2] = 0xC5

    # Star World 1 edits (134)
    # Makes a wall of koopas be always koopas and not something else
    rom[0x03E1F3+2] = 0xA1
    rom[0x03E1F6+2] = 0xA1
    rom[0x03E1F9+2] = 0xA1
    rom[0x03E1FC+2] = 0xA1
    rom[0x03E1FF+2] = 0xA1

    # Star World 4 edits (135)
    # Makes walls of vertical koopas unreplaceable, also guarantees some koopas
    rom[0x03E2CE+2] = 0xA1
    rom[0x03E2D1+2] = 0xA1
    rom[0x03E2D4+2] = 0xA1
    rom[0x03E2D7+2] = 0xA1
    rom[0x03E2DA+2] = 0xA1
    rom[0x03E2DD+2] = 0xA1
    rom[0x03E2E0+2] = 0xA1
    
    rom[0x03E2F8+2] = 0xA1
    rom[0x03E2FB+2] = 0xA1
    rom[0x03E2FE+2] = 0xA1
    rom[0x03E301+2] = 0xA1
    rom[0x03E304+2] = 0xA1
    
    guaranteed_koopas = random.randint(1, 3)
    rom_offsets = random.choices(sw4_koopa_placements, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xC5

    # Star World 5 (136)
    # Guarantees some flying koopas
    guaranteed_koopas = random.randint(1, 2)
    rom_offsets = random.choices(sw5_koopa_placements_1, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1
    guaranteed_koopas = random.randint(1, 3)
    rom_offsets = random.choices(sw5_koopa_placements_2, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1

    # Star World 1 (135)
    rom[0x03E2C5+1] = 0x94
    rom[0x03E2C8+1] = 0x84
    rom[0x03E2CB+1] = 0x74

    # CI3 (023)
    # Guarantees some blue koopas
    guaranteed_koopas = random.randint(2, 5)
    rom_offsets = random.choices(ci3_koopa_placements, k=guaranteed_koopas)
    for offset in rom_offsets:
        rom[offset+2] = 0xA1

    # YI3 (103)
    # Guarantees one blue koopa
    offset = random.choice(yi3_koopa_placements)
    rom[offset+2] = 0xA1

    # DP1 (015)
    # Guarantees one blue koopa
    offset = random.choice(dp1_koopa_placements)
    rom[offset+2] = 0xA1

    # DP3 (005)
    # Guarantees bouncing koopa
    rom[0x03C7E6+2] = 0xA1

    # Groovy (128)
    # Guarantees a kickable enemy at the start and fixes wall of pokeys
    rom[0x03E5BA+1] = 0x3F
    rom[0x03E5BD+1] = 0x4F
    rom[0x03E5C0+1] = 0x5F
    rom[0x03E5C3+1] = 0x6F

    rom[0x03E575+2] = 0xA1

    # DP2 (009)
    # Guarantees a kickable enemy before pipe
    offset = random.choice(dp2_koopa_placements)
    rom[offset+2] = 0xA1

    rom[0x03C758+2] = 0xC5
    rom[0x03C75E+2] = 0xC5
    rom[0x03C77F+2] = 0xC5
    rom[0x03C785+2] = 0xC5
    rom[0x03C788+2] = 0xC5
    rom[0x03C78E+2] = 0xC5

    # VS2 (001)
    # Guarantees a bouncing koopa at the start and a kickable enemy near the grounded switch block
    rom[0x03CE26+2] = 0xC5
    offset = random.choice(vs2_koopa_placements)
    rom[offset+2] = 0xA1

    # CBA (00F)
    # Guarantees spinjumpable enemies at the end of the level
    rom[0x03D00D+2] = 0xA1
    rom[0x03D010+2] = 0xA1
    rom[0x03D013+2] = 0xA1
    rom[0x03D016+2] = 0xA1
    rom[0x03D019+2] = 0xA1
    rom[0x03D01C+2] = 0xA1
    rom[0x03D01F+2] = 0xA1
    rom[0x03D022+2] = 0xA1
    rom[0x03D025+2] = 0xA1

    # FGH (11D)
    # Move a bit the wall of boos
    rom[0x03D53B+1] = 0x84
    rom[0x03D53E+1] = 0x94
    rom[0x03D541+1] = 0xA4
    rom[0x03D544+1] = 0xB4
    rom[0x03D547+1] = 0xC4

    # VB1 (116)
    # Guarantee Mega Mole on Munchers
    rom[0x03DD4B+2] = 0xC5

    # Morton Castle (0E7)
    # Guarantees enemy that stays on ledges
    rom[0x03C930+2] = 0xC5
    rom[0x03C933+2] = 0xC5

    # DP4 (006)
    # Guarantees kickable and bounceable enemies
    rom[0x03C869+2] = 0xC5

    rom[0x03C86C+2] = 0xA1
    rom[0x03C86F+2] = 0xA1
    rom[0x03C872+2] = 0xA1
    rom[0x03C875+2] = 0xA1
    rom[0x03C878+2] = 0xA1
    rom[0x03C87B+2] = 0xA1
    rom[0x03C87E+2] = 0xA1

    # Sublevel now has guaranteed koopas
    rom[0x03C8DD+2] = 0xC5
    rom[0x03C8E0+2] = 0xC5
    rom[0x03C8E3+2] = 0xC5

    # VD4 (10F)
    # Guarantees a koopa at the end of the level
    rom[0x03DF69+2] = 0xA1

    # COM (010)
    # Guarantees kickable and bounceable enemies
    rom[0x03D05C+2] = 0xC5

    rom[0x03D05F+2] = 0xA1
    rom[0x03D062+2] = 0xA1
    rom[0x03D065+2] = 0xA1
    rom[0x03D068+2] = 0xA1
    rom[0x03D06B+2] = 0xA1
    rom[0x03D06E+2] = 0xA1
    rom[0x03D071+2] = 0xA1
    rom[0x03D074+2] = 0xA1

    return rom
