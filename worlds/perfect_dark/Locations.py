import typing

from BaseClasses import Location
from .Names import LocationName

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PerfectDarkWorld

class PerfectDarkLocation(Location):
    game = "Perfect Dark"

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)

STARTING_ID = 0xC00000

missions = {
    LocationName.mission_1_1_a:         STARTING_ID + 0x0000,
    LocationName.mission_1_1_sa:        STARTING_ID + 0x0001,
    LocationName.mission_1_1_pa:        STARTING_ID + 0x0002,
    LocationName.mission_1_2_a:         STARTING_ID + 0x0003,
    LocationName.mission_1_2_sa:        STARTING_ID + 0x0004,
    LocationName.mission_1_2_pa:        STARTING_ID + 0x0005,
    LocationName.mission_1_3_a:         STARTING_ID + 0x0006,
    LocationName.mission_1_3_sa:        STARTING_ID + 0x0007,
    LocationName.mission_1_3_pa:        STARTING_ID + 0x0008,

    LocationName.mission_2_1_a:         STARTING_ID + 0x0009,
    LocationName.mission_2_1_sa:        STARTING_ID + 0x000A,
    LocationName.mission_2_1_pa:        STARTING_ID + 0x000B,

    LocationName.mission_3_1_a:         STARTING_ID + 0x000C,
    LocationName.mission_3_1_sa:        STARTING_ID + 0x000D,
    LocationName.mission_3_1_pa:        STARTING_ID + 0x000E,
    LocationName.mission_3_2_a:         STARTING_ID + 0x000F,
    LocationName.mission_3_2_sa:        STARTING_ID + 0x0010,
    LocationName.mission_3_2_pa:        STARTING_ID + 0x0011,

    LocationName.mission_4_1_a:         STARTING_ID + 0x0012,
    LocationName.mission_4_1_sa:        STARTING_ID + 0x0013,
    LocationName.mission_4_1_pa:        STARTING_ID + 0x0014,
    LocationName.mission_4_2_a:         STARTING_ID + 0x0015,
    LocationName.mission_4_2_sa:        STARTING_ID + 0x0016,
    LocationName.mission_4_2_pa:        STARTING_ID + 0x0017,
    LocationName.mission_4_3_a:         STARTING_ID + 0x0018,
    LocationName.mission_4_3_sa:        STARTING_ID + 0x0019,
    LocationName.mission_4_3_pa:        STARTING_ID + 0x001A,

    LocationName.mission_5_1_a:         STARTING_ID + 0x001B,
    LocationName.mission_5_1_sa:        STARTING_ID + 0x001C,
    LocationName.mission_5_1_pa:        STARTING_ID + 0x001D,
    LocationName.mission_5_2_a:         STARTING_ID + 0x001E,
    LocationName.mission_5_2_sa:        STARTING_ID + 0x001F,
    LocationName.mission_5_2_pa:        STARTING_ID + 0x0020,
    LocationName.mission_5_3_a:         STARTING_ID + 0x0021,
    LocationName.mission_5_3_sa:        STARTING_ID + 0x0022,
    LocationName.mission_5_3_pa:        STARTING_ID + 0x0023,

    LocationName.mission_6_1_a:         STARTING_ID + 0x0024,
    LocationName.mission_6_1_sa:        STARTING_ID + 0x0025,
    LocationName.mission_6_1_pa:        STARTING_ID + 0x0026,
    LocationName.mission_6_2_a:         STARTING_ID + 0x0027,
    LocationName.mission_6_2_sa:        STARTING_ID + 0x0028,
    LocationName.mission_6_2_pa:        STARTING_ID + 0x0029,

    LocationName.mission_7_1_a:         STARTING_ID + 0x002A,
    LocationName.mission_7_1_sa:        STARTING_ID + 0x002B,
    LocationName.mission_7_1_pa:        STARTING_ID + 0x002C,

    LocationName.mission_8_1_a:         STARTING_ID + 0x002D,
    LocationName.mission_8_1_sa:        STARTING_ID + 0x002E,
    LocationName.mission_8_1_pa:        STARTING_ID + 0x002F,

    LocationName.mission_9_1_a:         STARTING_ID + 0x0030,
    LocationName.mission_9_1_sa:        STARTING_ID + 0x0031,
    LocationName.mission_9_1_pa:        STARTING_ID + 0x0032,

    LocationName.special_1_a:           STARTING_ID + 0x0033,
    LocationName.special_1_sa:          STARTING_ID + 0x0034,
    LocationName.special_1_pa:          STARTING_ID + 0x0035,
    LocationName.special_2_a:           STARTING_ID + 0x0036,
    LocationName.special_2_sa:          STARTING_ID + 0x0037,
    LocationName.special_2_pa:          STARTING_ID + 0x0038,
    LocationName.special_3_a:           STARTING_ID + 0x0039,
    LocationName.special_3_sa:          STARTING_ID + 0x003A,
    LocationName.special_3_pa:          STARTING_ID + 0x003B,
    LocationName.special_4_a:           STARTING_ID + 0x003C,
    LocationName.special_4_sa:          STARTING_ID + 0x003D,
    LocationName.special_4_pa:          STARTING_ID + 0x003E,
}

hidden_weapons = {
    LocationName.mission_1_1_w1:        STARTING_ID + 0x0100,
    LocationName.mission_1_2_w1:        STARTING_ID + 0x0101,
    LocationName.mission_1_2_w2:        STARTING_ID + 0x0102,
    LocationName.mission_1_3_w1:        STARTING_ID + 0x0103,
    LocationName.mission_2_1_w1:        STARTING_ID + 0x0104,
    LocationName.mission_2_1_w2:        STARTING_ID + 0x0105,
    LocationName.mission_3_1_w1:        STARTING_ID + 0x0106,
    LocationName.mission_3_1_w2:        STARTING_ID + 0x0107,
    LocationName.mission_3_2_w1:        STARTING_ID + 0x0108,
    LocationName.mission_4_1_w1:        STARTING_ID + 0x0109,
    LocationName.mission_4_2_w1:        STARTING_ID + 0x010A,
    LocationName.mission_4_2_w2:        STARTING_ID + 0x010B,
    LocationName.mission_4_3_w1:        STARTING_ID + 0x010C,
    LocationName.mission_4_3_w2:        STARTING_ID + 0x010D,
    LocationName.mission_5_1_w1:        STARTING_ID + 0x010E,
    LocationName.mission_5_1_w2:        STARTING_ID + 0x010F,
    LocationName.mission_5_2_w1:        STARTING_ID + 0x0110,
    LocationName.mission_5_3_w1:        STARTING_ID + 0x0111,
    LocationName.mission_5_3_w2:        STARTING_ID + 0x0112,
    LocationName.mission_6_1_w1:        STARTING_ID + 0x0113,
    LocationName.mission_6_2_w1:        STARTING_ID + 0x0114,
    LocationName.mission_7_1_w1:        STARTING_ID + 0x0115,
    LocationName.mission_8_1_w1:        STARTING_ID + 0x0116,
    LocationName.mission_8_1_w2:        STARTING_ID + 0x0117,
    LocationName.mission_9_1_w1:        STARTING_ID + 0x0118,
    LocationName.special_1_w1:          STARTING_ID + 0x0119,
    LocationName.special_2_w1:          STARTING_ID + 0x0119,
    LocationName.special_2_w2:          STARTING_ID + 0x0119,
}

firing_range = {
    LocationName.falcon_2_bronze:           STARTING_ID + 0x0200,
    LocationName.falcon_2_silver:           STARTING_ID + 0x0201,
    LocationName.falcon_2_gold:             STARTING_ID + 0x0202,
    LocationName.falcon_2_silencer_bronze:  STARTING_ID + 0x0203,
    LocationName.falcon_2_silencer_silver:  STARTING_ID + 0x0204,
    LocationName.falcon_2_silencer_gold:    STARTING_ID + 0x0205,
    LocationName.falcon_2_scope_bronze:     STARTING_ID + 0x0206,
    LocationName.falcon_2_scope_silver:     STARTING_ID + 0x0207,
    LocationName.falcon_2_scope_gold:       STARTING_ID + 0x0208,
    LocationName.magsec_4_bronze:           STARTING_ID + 0x0209,
    LocationName.magsec_4_silver:           STARTING_ID + 0x020A,
    LocationName.magsec_4_gold:             STARTING_ID + 0x020B,
    LocationName.mauler_bronze:             STARTING_ID + 0x020C,
    LocationName.mauler_silver:             STARTING_ID + 0x020D,
    LocationName.mauler_gold:               STARTING_ID + 0x020E,
    LocationName.phoenix_bronze:            STARTING_ID + 0x020F,
    LocationName.phoenix_silver:            STARTING_ID + 0x0210,
    LocationName.phoenix_gold:              STARTING_ID + 0x0211,
    LocationName.dy357_magnum_bronze:       STARTING_ID + 0x0212,
    LocationName.dy357_magnum_silver:       STARTING_ID + 0x0213,
    LocationName.dy357_magnum_gold:              STARTING_ID + 0x0214,
    LocationName.dy357_lx_bronze:           STARTING_ID + 0x0215,
    LocationName.dy357_lx_silver:           STARTING_ID + 0x0216,
    LocationName.dy357_lx_gold:             STARTING_ID + 0x0217,
    LocationName.cmp150_bronze:             STARTING_ID + 0x0218,
    LocationName.cmp150_silver:             STARTING_ID + 0x0219,
    LocationName.cmp150_gold:               STARTING_ID + 0x021A,
    LocationName.cyclone_bronze:            STARTING_ID + 0x021B,
    LocationName.cyclone_silver:            STARTING_ID + 0x021C,
    LocationName.cyclone_gold:              STARTING_ID + 0x021D,
    LocationName.callisto_ntg_bronze:       STARTING_ID + 0x021E,
    LocationName.callisto_ntg_silver:       STARTING_ID + 0x021F,
    LocationName.callisto_ntg_gold:         STARTING_ID + 0x0220,
    LocationName.rc_p120_bronze:            STARTING_ID + 0x0221,
    LocationName.rc_p120_silver:            STARTING_ID + 0x0222,
    LocationName.rc_p120_gold:              STARTING_ID + 0x0223,
    LocationName.laptop_gun_bronze:         STARTING_ID + 0x0224,
    LocationName.laptop_gun_silver:         STARTING_ID + 0x0225,
    LocationName.laptop_gun_gold:           STARTING_ID + 0x0226,
    LocationName.dragon_bronze:             STARTING_ID + 0x0227,
    LocationName.dragon_silver:             STARTING_ID + 0x0228,
    LocationName.dragon_gold:               STARTING_ID + 0x0229,
    LocationName.k7_avenger_bronze:         STARTING_ID + 0x022A,
    LocationName.k7_avenger_silver:         STARTING_ID + 0x022B,
    LocationName.k7_avenger_gold:           STARTING_ID + 0x022C,
    LocationName.ar34_bronze:               STARTING_ID + 0x022D,
    LocationName.ar34_silver:               STARTING_ID + 0x022E,
    LocationName.ar34_gold:                 STARTING_ID + 0x022F,
    LocationName.superdragon_bronze:        STARTING_ID + 0x0230,
    LocationName.superdragon_silver:        STARTING_ID + 0x0231,
    LocationName.superdragon_gold:          STARTING_ID + 0x0232,
    LocationName.shotgun_bronze:            STARTING_ID + 0x0233,
    LocationName.shotgun_silver:            STARTING_ID + 0x0234,
    LocationName.shotgun_gold:              STARTING_ID + 0x0235,
    LocationName.reaper_bronze:             STARTING_ID + 0x0236,
    LocationName.reaper_silver:             STARTING_ID + 0x0237,
    LocationName.reaper_gold:               STARTING_ID + 0x0238,
    LocationName.sniper_rifle_bronze:       STARTING_ID + 0x0239,
    LocationName.sniper_rifle_silver:       STARTING_ID + 0x023A,
    LocationName.sniper_rifle_gold:         STARTING_ID + 0x023B,
    LocationName.farsight_xr_20_bronze:     STARTING_ID + 0x023C,
    LocationName.farsight_xr_20_silver:     STARTING_ID + 0x023D,
    LocationName.farsight_xr_20_gold:       STARTING_ID + 0x023E,
    LocationName.devastator_bronze:         STARTING_ID + 0x023F,
    LocationName.devastator_silver:         STARTING_ID + 0x0240,
    LocationName.devastator_gold:           STARTING_ID + 0x0241,
    LocationName.rocket_launcher_bronze:    STARTING_ID + 0x0242,
    LocationName.rocket_launcher_silver:    STARTING_ID + 0x0243,
    LocationName.rocket_launcher_gold:           STARTING_ID + 0x0244,
    LocationName.slayer_bronze:             STARTING_ID + 0x0245,
    LocationName.slayer_silver:             STARTING_ID + 0x0246,
    LocationName.slayer_gold:               STARTING_ID + 0x0247,
    LocationName.combat_knife_bronze:       STARTING_ID + 0x0248,
    LocationName.combat_knife_silver:       STARTING_ID + 0x0249,
    LocationName.combat_knife_gold:         STARTING_ID + 0x024A,
    LocationName.crossbow_bronze:           STARTING_ID + 0x024B,
    LocationName.crossbow_silver:           STARTING_ID + 0x024C,
    LocationName.crossbow_gold:             STARTING_ID + 0x024D,
    LocationName.tranquilizer_bronze:       STARTING_ID + 0x024E,
    LocationName.tranquilizer_silver:       STARTING_ID + 0x024F,
    LocationName.tranquilizer_gold:         STARTING_ID + 0x0250,
    LocationName.laser_bronze:              STARTING_ID + 0x0251,
    LocationName.laser_silver:              STARTING_ID + 0x0252,
    LocationName.laser_gold:                STARTING_ID + 0x0253,
    LocationName.grenade_bronze:            STARTING_ID + 0x0254,
    LocationName.grenade_silver:            STARTING_ID + 0x0255,
    LocationName.grenade_gold:              STARTING_ID + 0x0256,
    LocationName.timed_mine_bronze:         STARTING_ID + 0x0257,
    LocationName.timed_mine_silver:         STARTING_ID + 0x0258,
    LocationName.timed_mine_gold:           STARTING_ID + 0x0259,
    LocationName.proximity_mine_bronze:     STARTING_ID + 0x025A,
    LocationName.proximity_mine_silver:     STARTING_ID + 0x025B,
    LocationName.proximity_mine_gold:       STARTING_ID + 0x025C,
    LocationName.remote_mine_bronze:        STARTING_ID + 0x025D,
    LocationName.remote_mine_silver:        STARTING_ID + 0x025E,
    LocationName.remote_mine_gold:          STARTING_ID + 0x025F,
}

device_training = {
    LocationName.data_uplink:       STARTING_ID + 0x0300,
    LocationName.ecm_mine:          STARTING_ID + 0x0301,
    LocationName.cam_spy:           STARTING_ID + 0x0302,
    LocationName.night_vision:      STARTING_ID + 0x0303,
    LocationName.door_decoder:      STARTING_ID + 0x0304,
    LocationName.r_tracker:         STARTING_ID + 0x0305,
    LocationName.ir_scanner:        STARTING_ID + 0x0306,
    LocationName.x_ray_scanner:     STARTING_ID + 0x0307,
    LocationName.cloaking_device:   STARTING_ID + 0x0308,
    LocationName.disguise:          STARTING_ID + 0x0309,
}

holo_vr = {
    LocationName.holo_1:    STARTING_ID + 0x0400,
    LocationName.holo_2:    STARTING_ID + 0x0401,
    LocationName.holo_3:    STARTING_ID + 0x0402,
    LocationName.holo_4:    STARTING_ID + 0x0403,
    LocationName.holo_5:    STARTING_ID + 0x0404,
    LocationName.holo_6:    STARTING_ID + 0x0405,
    LocationName.holo_7:    STARTING_ID + 0x0406,
}

carrington_locations = [
    *device_training.keys(),
    *holo_vr.keys(),
]

all_locations = {
    **missions,
    **firing_range,
    #**hidden_weapons,
    **device_training,
    **holo_vr,
}

location_groups = {
}
    
def setup_locations(world: "PerfectDarkWorld"):
    location_table = {
        **missions,
        **firing_range,
        #**hidden_weapons,
        **device_training,
        **holo_vr,
    }

    return location_table

lookup_id_to_name: typing.Dict[int, str] = {id: name for name, _ in all_locations.items()}
