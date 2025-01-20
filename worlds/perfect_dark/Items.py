import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

STARTING_ID = 0xC00000

class PDItem(Item):
    game = "Perfect Dark"

# Item tables
weapons = {
    ItemName.falcon_2:              ItemData(STARTING_ID + 0x0000, ItemClassification.progression),
    ItemName.falcon_2_silencer:     ItemData(STARTING_ID + 0x0001, ItemClassification.progression),
    ItemName.falcon_2_scope:        ItemData(STARTING_ID + 0x0002, ItemClassification.progression),
    ItemName.magsec_4:              ItemData(STARTING_ID + 0x0003, ItemClassification.progression),
    ItemName.mauler:                ItemData(STARTING_ID + 0x0004, ItemClassification.progression),
    ItemName.phoenix:               ItemData(STARTING_ID + 0x0005, ItemClassification.progression),
    ItemName.dy357_magnum:          ItemData(STARTING_ID + 0x0006, ItemClassification.progression),
    ItemName.dy357_lx:              ItemData(STARTING_ID + 0x0007, ItemClassification.progression),
    ItemName.cmp150:                ItemData(STARTING_ID + 0x0008, ItemClassification.progression),
    ItemName.cyclone:               ItemData(STARTING_ID + 0x0009, ItemClassification.progression),
    ItemName.callisto_ntg:          ItemData(STARTING_ID + 0x000A, ItemClassification.progression),
    ItemName.rc_p120:               ItemData(STARTING_ID + 0x000B, ItemClassification.progression),
    ItemName.laptop_gun:            ItemData(STARTING_ID + 0x000C, ItemClassification.progression),
    ItemName.dragon:                ItemData(STARTING_ID + 0x000D, ItemClassification.progression),
    ItemName.k7_avenger:            ItemData(STARTING_ID + 0x000E, ItemClassification.progression),
    ItemName.ar34:                  ItemData(STARTING_ID + 0x000F, ItemClassification.progression),
    ItemName.superdragon:           ItemData(STARTING_ID + 0x0010, ItemClassification.progression),
    ItemName.shotgun:               ItemData(STARTING_ID + 0x0011, ItemClassification.progression),
    ItemName.reaper:                ItemData(STARTING_ID + 0x0012, ItemClassification.progression),
    ItemName.sniper_rifle:          ItemData(STARTING_ID + 0x0013, ItemClassification.progression),
    ItemName.farsight_xr_20:        ItemData(STARTING_ID + 0x0014, ItemClassification.progression),
    ItemName.devastator:            ItemData(STARTING_ID + 0x0015, ItemClassification.progression),
    ItemName.rocket_launcher:        ItemData(STARTING_ID + 0x0016, ItemClassification.progression),
    ItemName.slayer:                ItemData(STARTING_ID + 0x0017, ItemClassification.progression),
    ItemName.combat_knife:          ItemData(STARTING_ID + 0x0018, ItemClassification.progression),
    ItemName.crossbow:              ItemData(STARTING_ID + 0x0019, ItemClassification.progression),
    ItemName.tranquilizer:          ItemData(STARTING_ID + 0x001A, ItemClassification.progression),
    ItemName.laser:                 ItemData(STARTING_ID + 0x001B, ItemClassification.progression),
    ItemName.grenade:               ItemData(STARTING_ID + 0x001C, ItemClassification.progression),
    ItemName.timed_mine:            ItemData(STARTING_ID + 0x001D, ItemClassification.progression),
    ItemName.proximity_mine:        ItemData(STARTING_ID + 0x001E, ItemClassification.progression),
    ItemName.remote_mine:           ItemData(STARTING_ID + 0x001F, ItemClassification.progression),
    ItemName.psychosis_gun:         ItemData(STARTING_ID + 0x0020, ItemClassification.useful),
    ItemName.pp9i:                  ItemData(STARTING_ID + 0x0021, ItemClassification.useful),
    ItemName.cci3:                  ItemData(STARTING_ID + 0x0022, ItemClassification.useful),
    ItemName.klo1313:               ItemData(STARTING_ID + 0x0023, ItemClassification.useful),
    ItemName.kf7_special:           ItemData(STARTING_ID + 0x0024, ItemClassification.useful),
    ItemName.zzt_9mm:               ItemData(STARTING_ID + 0x0025, ItemClassification.useful),
    ItemName.dmc:                   ItemData(STARTING_ID + 0x0026, ItemClassification.useful),
    ItemName.ar53:                  ItemData(STARTING_ID + 0x0027, ItemClassification.useful),
    ItemName.rc_p45:                ItemData(STARTING_ID + 0x0028, ItemClassification.useful),
    ItemName.n_bomb:                ItemData(STARTING_ID + 0x0028, ItemClassification.useful),
}

gadgets = {
    ItemName.data_uplink:           ItemData(STARTING_ID + 0x0100, ItemClassification.progression),
    ItemName.ecm_mine:              ItemData(STARTING_ID + 0x0101, ItemClassification.progression),
    ItemName.cam_spy:               ItemData(STARTING_ID + 0x0102, ItemClassification.progression),
    ItemName.drug_spy:              ItemData(STARTING_ID + 0x0103, ItemClassification.progression),
    ItemName.bomb_spy:              ItemData(STARTING_ID + 0x0104, ItemClassification.progression),
    ItemName.night_vision:          ItemData(STARTING_ID + 0x0105, ItemClassification.progression),
    ItemName.door_decoder:          ItemData(STARTING_ID + 0x0106, ItemClassification.progression),
    ItemName.r_tracker:             ItemData(STARTING_ID + 0x0107, ItemClassification.progression),
    ItemName.ir_scanner:            ItemData(STARTING_ID + 0x0108, ItemClassification.progression),
    ItemName.x_ray_scanner:         ItemData(STARTING_ID + 0x0109, ItemClassification.progression),
    ItemName.horizon_scanner:       ItemData(STARTING_ID + 0x010A, ItemClassification.useful),
    ItemName.cloaking_device:       ItemData(STARTING_ID + 0x010B, ItemClassification.progression),
    ItemName.disguise:              ItemData(STARTING_ID + 0x010C, ItemClassification.progression),
    ItemName.combat_boost:          ItemData(STARTING_ID + 0x010D, ItemClassification.useful),
}

missions = {
    ItemName.mission_1:             ItemData(STARTING_ID + 0x0200, ItemClassification.progression),
    ItemName.mission_2:             ItemData(STARTING_ID + 0x0201, ItemClassification.progression),
    ItemName.mission_3:             ItemData(STARTING_ID + 0x0202, ItemClassification.progression),
    ItemName.mission_4:             ItemData(STARTING_ID + 0x0203, ItemClassification.progression),
    ItemName.mission_5:             ItemData(STARTING_ID + 0x0204, ItemClassification.progression),
    ItemName.mission_6:             ItemData(STARTING_ID + 0x0205, ItemClassification.progression),
    ItemName.mission_7:             ItemData(STARTING_ID + 0x0206, ItemClassification.progression),
    ItemName.mission_8:             ItemData(STARTING_ID + 0x0207, ItemClassification.progression),
    ItemName.mission_9:             ItemData(STARTING_ID + 0x0208, ItemClassification.progression),
    ItemName.special_assignments:   ItemData(STARTING_ID + 0x0209, ItemClassification.progression),
}

misc = {
    ItemName.shields:               ItemData(STARTING_ID + 0x0300, ItemClassification.progression),
    ItemName.health:                ItemData(STARTING_ID + 0x0301, ItemClassification.progression),
    ItemName.secondary_action:      ItemData(STARTING_ID + 0x0302, ItemClassification.progression),
    ItemName.akimbo_weapons:        ItemData(STARTING_ID + 0x0303, ItemClassification.useful),
    ItemName.hurricane_fists:       ItemData(STARTING_ID + 0x0304, ItemClassification.useful),
    ItemName.start_slots:           ItemData(STARTING_ID + 0x0305, ItemClassification.useful),
    ItemName.starting_ammo:         ItemData(STARTING_ID + 0x0306, ItemClassification.useful),
}

junk = {
    ItemName.hp_refill:             ItemData(STARTING_ID + 0x0400, ItemClassification.filler),
    ItemName.pistol_ammo:           ItemData(STARTING_ID + 0x0401, ItemClassification.filler),
    ItemName.magnum_ammo:           ItemData(STARTING_ID + 0x0402, ItemClassification.filler),
    ItemName.smg_ammo:              ItemData(STARTING_ID + 0x0403, ItemClassification.filler),
    ItemName.rifle_ammo:            ItemData(STARTING_ID + 0x0404, ItemClassification.filler),
    ItemName.shotgun_ammo:          ItemData(STARTING_ID + 0x0405, ItemClassification.filler),
    ItemName.bolt_ammo:             ItemData(STARTING_ID + 0x0406, ItemClassification.filler),
    ItemName.farsight_ammo:         ItemData(STARTING_ID + 0x0407, ItemClassification.filler),
    ItemName.grenade_ammo:          ItemData(STARTING_ID + 0x0408, ItemClassification.filler),
    ItemName.rocket_ammo:           ItemData(STARTING_ID + 0x0409, ItemClassification.filler),
    ItemName.sedative_ammo:         ItemData(STARTING_ID + 0x040A, ItemClassification.filler),
    ItemName.n_bomb_ammo:           ItemData(STARTING_ID + 0x040B, ItemClassification.filler),
}

item_table = {
    **weapons,
    **gadgets,
    **missions,
    **misc,
    **junk,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}