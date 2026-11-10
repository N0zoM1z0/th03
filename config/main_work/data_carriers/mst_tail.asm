		.386
		.model use16 large _TEXT



include ReC98.inc
include th02/gaiji/boldfont.inc
include th03/arg_bx.inc
include th03/th03.inc
include th03/main/playfld.inc
include th03/main/collmap.inc
include th03/sprites/main_s16.inc
include th03/sprite16.inc
include libs/sprite16/sprite16.inc


include th03/math/subpixel.inc

speed_t struc
	aligned  SPPoint8 <?>
	diagonal SPPoint8 <?>
speed_t ends

playchar_speed_t struc
	motion speed_t <?>
	gauge_charge db ?
playchar_speed_t ends


GBA_GAUGE_LEVEL_MIN = 1
GBA_GAUGE_LEVEL_MAX = 16
GBA_BOSS_LEVEL_MAX = 16
WARNING_FLASH_RED_FRAMES = 30
WF_NONE = 0
WF_PORTRAIT = 1
WF_FLASH_WHITE = 2
WF_FLASH_RED = 3
WF_FLASH_RED_END = (WF_FLASH_RED + WARNING_FLASH_RED_FRAMES)
MOVE_INVALID = 0
MOVE_VALID = 1
MOVE_NOINPUT = 2
BG_1 = 0
BG_1_AIMED = 1
BG_2_SPREAD_NARROW = 2
BG_2_SPREAD_NARROW_AIMED = 5
BG_3_SPREAD_NARROW = 8
BG_3_SPREAD_NARROW_AIMED = 11
BG_4_SPREAD_NARROW = 14
BG_4_SPREAD_MEDIUM = 15
BG_4_SPREAD_WIDE = 16
BG_4_SPREAD_NARROW_AIMED = 17
BG_4_SPREAD_MEDIUM_AIMED = 18
BG_5_SPREAD_NARROW = 20
BG_5_SPREAD_MEDIUM = 21
BG_5_SPREAD_WIDE = 22
BG_5_SPREAD_NARROW_AIMED = 23
BG_5_SPREAD_MEDIUM_AIMED = 24
BG_RANDOM_ANGLE_AND_SPEED = 28
BG_RANDOM_CONSTRAINED_ANGLE_AIMED = 29
BG_2_RING = 33
BG_4_RING = 32
BG_8_RING = 35
BG_16_RING = 36
BG_32_RING = 37
BG_RING = 38
BG_RING_AIMED = 44
BG_2_SPREAD_HORIZONTALLY_SYMMETRIC = 34
BT_PELLET = 1
BT_BULLET16_DEFAULT = 2
BT_PELLET_CLOUD = 4
BT_BULLET16_DEFAULT_WITH_ACCEL = 7
BT_BULLET16_CUSTOM_WITH_ACCEL = 8
BAT_Y = 80h
PID_NONE = -1
EXPLOSION_CELS = 4
MRS_SLOT_COUNT = 8
FORMATIONS_MAX = 24
HITCIRCLE_FRAMES = 16
HITCIRCLE_ENEMY_COUNT = 12
HITCIRCLE_PLAYER_COUNT = 1
HITCIRCLE_COUNT = (HITCIRCLE_ENEMY_COUNT + HITCIRCLE_PLAYER_COUNT)
GBAF_NONE = 0
GBAF_GAUGE_PELLET_INIT = 1
GBAF_GAUGE_BULLET_INIT = 3
GBAF_BOSS = 5
GBAF_PELLET_TO_BULLET = (GBAF_GAUGE_BULLET_INIT - GBAF_GAUGE_PELLET_INIT)
HSF_DONE = 0
HSF_INIT = 1
HSF_ACTIVE = 2
DF_NONE = 0
DF_EXPLODE = 1
DF_BANNER = 2
EFF_FREE = 0
EFF_EXPLOSION_IGNORING_ENEMIES = 9
EFF_EXPLOSION_HITTING_ENEMIES = 10
EF_RUNNING_SPAWNED = 1
EFE_COUNT = 64
ENEMY_COUNT = 40
CHAIN_RING_SIZE = 16
EXTENDS_MAX = 2
EXTENDS_DISABLE = 255
BOMB_FRAMES = 180
BF_INACTIVE = 0
BF_PREPARING = 1
BF_ACTIVE = 2
ROUND_SPEED_MAX = ((8 shl 4) - 1)
public _playfield_transition_vertices,_transition_hmask
_playfield_transition_vertices = word_1FBC4
_transition_hmask = trapezoid_hmask
public fp_1FBC0,byte_1FBC2,byte_1FBC3,word_1FBC4,word_1FBC6,word_1FBC8,word_1FBCA,word_1FBCC,word_1FBCE,word_1FBD0,word_1FBD2,trapezoid_hmask
public _pid_PID_so_attack,_sprite16_put_w,_sprite16_put_h,_sprite16_clip_left,_sprite16_clip_right,palette_1F2F4,_palette_changed,BYTE_MASK
public mem_TopSeg,mem_MyOwn,mem_AllocID,mem_Reserve,header,super_buffer,super_patnum,super_charfree
public ResPalID,vsync_delay_count,mem_OutSeg,mem_TopHeap,mem_FirstHole,mem_EndMark,super_patdata,super_patsize
public parfilename,pfint21_pf,pfint21_handle,pfint21_entries
	.data

include libs/master.lib/wordmask[data].asm
include libs/master.lib/mem[data].asm
include libs/master.lib/super_entry_bfnt[data].asm
include libs/master.lib/superpa[data].asm
public _snd_active
_snd_active	db 0
		db 0
include libs/master.lib/respal_exist[data].asm
include libs/master.lib/draw_trapezoid[data].asm
include th03/snd/se_state[data].asm
include th02/formats/pfopen[data].asm
include th03/snd/se_priority[data].asm
include th03/formats/cfg_lres[data].asm
	evendata
public _gba_boss_launched_by
_gba_boss_launched_by	db PID_NONE
	evendata
public _character_filename_template
_character_filename_template label byte
a00ch_bf2	db '00ch.bf2',0
		db 0
		db    0
		db    0
include src/main/graphics/gauge_masks.inl
public _ENEDAT_DAT
_ENEDAT_DAT	db 'ENEDAT.DAT',0
	evendata
public _mima_chargeshot_angles
_mima_chargeshot_angles label byte
angles_1DBD8	db 192, 182, 202, 192, 176, 208
public _cpu_dodge_patterns
_cpu_dodge_patterns label word
		db    0
		db    4
		db    8
		db    0
		db    0
		db    8
		db    1
		db    0
		db    8
		db    0
		db    8
		db    0
		db    0
		db    1
		db    0
		db    4
		db    0
		db    4
		db    4
		db    0
		db    4
		db    0
		db    0
		db    1
		db    2
		db    0
		db    2
		db    0
		db    2
		db    0
		db    0
		db    1
		db    1
		db    0
		db    0
		db    4
		db    4
		db    0
		db    4
		db    0
		db    0
		db    1
		db    4
		db    0
		db    4
		db    0
		db    0
		db    1
		db    0
		db    1
		db    4
		db    0
		db    0
		db    1
		db    0
		db    2
		db    0
		db    2
		db    8
		db    0
		db    2
		db    0
		db    0
		db    8
		db    0
		db    8
		db    4
		db    0
		db    8
		db    0
		db    8
		db    0
		db    0
		db    2
		db    0
		db    2
		db    0
		db    8
		db    1
		db    0
		db    0
		db    2
		db    1
		db    0
		db    1
		db    0
		db    4
		db    0
		db    8
		db    0
		db    4
		db    0
		db    0
		db    2
		db    2
		db    0
		db    0
		db    2
		db    0
		db    1
		db    0
		db    4
		db    0
		db    1
		db    4
		db    0
		db    1
		db    0
		db    1
		db    0
		db    0
		db    4
		db    2
		db    0
		db    0
		db    1
		db    0
		db    4
		db    0
		db    4
		db    1
		db    0
		db    0
		db    8
		db    1
		db    0
		db    0
		db    1
		db    8
		db    0
		db    8
		db    0
		db    0
		db    1
		db    0
		db    4
		db    0
		db    8
		db    4
		db    0
		db    8
		db    0
		db    1
		db    0
		db    0
		db    2
		db    0
		db    8
		db    0
		db    8
		db    0
		db    1
		db    0
		db    2
		db    1
		db    0
		db    1
		db    0
		db    0
		db    4
		db    0
		db    4
		db    2
		db    0
		db    0
		db    8
		db    8
		db    0
		db    2
		db    0
		db    0
		db    8
		db    0
		db    8
		db    4
		db    0
		db    8
		db    0
		db    8
		db    0
		db    0
		db    2
		db    0
		db    2
		db    0
		db    8
		db    2
		db    0
		db    0
		db    2
		db    2
		db    0
		db    2
		db    0
		db    4
		db    0
		db    8
		db    0
		db    4
		db    0
		db    0
		db    2
		db    2
		db    0
		db    0
		db    2
		db    0
		db    1
		db    0
		db    4
		db    0
		db    1
		db    4
		db    0
		db    1
		db    0
public _cpu_retry_directions
_cpu_retry_directions label word
		db    8
		db    0
		db    0
		db    8
		db    2
		db    0
		db    0
		db    0
		db    0
		db    4
		db    0
		db    2
		db    0
		db    1
		db    4
		db    0
		db    1
		db    0
		db    4
		db    0
		db    8
		db    0
		db    2
		db    0
		db    0
		db    2
		db    0
		db    8
		db    0
		db    0
		db    0
		db    1
		db    0
		db    4
		db    1
		db    0
		db    4
		db    0
		db    0
		db    2
		db    2
		db    0
		db    0
		db    0
		db    0
		db    1
		db    0
		db    8
		db    0
		db    4
		db    8
		db    0
		db    1
		db    0
public _yumemi_bomb_triangle_angles
_yumemi_bomb_triangle_angles label byte
		db 0C0h
		db  15h
		db  6Bh	; k
		db  40h
		db 0EBh
		db  95h
public _yumemi_groups
_yumemi_groups label byte
yumemi_group_1DCF2 label byte
	db BG_3_SPREAD_NARROW
	db BG_4_SPREAD_NARROW
	db BG_2_SPREAD_NARROW
	db BG_5_SPREAD_NARROW
	db BG_1
	evendata
public _warning_flag
_warning_flag label byte
warning_flag_p1	db WF_NONE
warning_flag_p2	db WF_NONE
public _warning_title_top
_warning_title_top label byte
gbWARNING_1	db 50h,	51h, 52h, 53h, 54h, 55h, 56h, 57h, 58h, 59h, 5Ah
		db 5Bh,	5Ch, 5Dh, 5Eh, 5Fh, 0
public _warning_title_middle
_warning_title_middle label byte
gbWARNING_2	db 60h,	61h, 62h, 63h, 64h, 65h, 66h, 67h, 68h, 69h, 6Ah
		db 6Bh,	6Ch, 6Dh, 6Eh, 6Fh, 0
public _warning_title_bottom
_warning_title_bottom label byte
gbWARNING_3	db 70h,	71h, 72h, 73h, 74h, 75h, 76h, 77h, 78h, 79h, 7Ah
		db 7Bh,	7Ch, 7Dh, 7Eh, 7Fh, 0
public _warning_forced_to_evade
_warning_forced_to_evade label byte
gpYOU_ARE_FORCED_TO_EVADE_FROM db 82h, 83h, 84h, 85h, 86h, 87h, 88h
		db 89h, 8Ah, 8Bh, 8Ch, 0
public _warning_gauge_level
_warning_gauge_level label byte
gpGAUGE_ATTACK_LEVEL db 0C7h, 0C8h, 0C9h, 0CAh, 0CBh, 0CCh, 0CDh, 0CEh,	0
public _warning_boss_level
_warning_boss_level label byte
gpBOSS_ATTACK_LEVEL db 0D0h, 0D1h, 0D2h, 0CAh, 0CBh, 0CCh, 0CDh, 0CEh, 0
public _warning_life_in_peril
_warning_life_in_peril label byte
gpYOUR_LIFE_IS_IN_PERIL_BE_CAREFUL db 8Dh, 8Eh, 8Fh, 92h, 93h, 94h, 95h
		db 96h, 97h, 98h, 99h, 9Ah, 9Bh, 9Ch, 0
public _warning_clear_line
_warning_clear_line label byte
asc_1DD5A	db '                                ',0
		db 0
include th03/main/player/combo[data].asm
	evendata

EXPLOSION_CELS = 4
public _SO_ENEMIES,_SO_EXPLOSIONS
label _SO_ENEMIES word
	dw ((104 * ROW_SIZE) + ( 48 / BYTE_DOTS))	; 16x16
	dw ((112 * ROW_SIZE) + ( 96 / BYTE_DOTS))	; 32x32
	dw ((104 * ROW_SIZE) + (272 / BYTE_DOTS))	; 48x48
	dw ((128 * ROW_SIZE) + (192 / BYTE_DOTS))	; 64x64
label _SO_EXPLOSIONS word
label _SO_EXPLOSION_32X32 word
	dw ((128 * ROW_SIZE) + (256 / BYTE_DOTS))
	dw ((128 * ROW_SIZE) + (288 / BYTE_DOTS))
	dw ((144 * ROW_SIZE) + (256 / BYTE_DOTS))
	dw ((144 * ROW_SIZE) + (288 / BYTE_DOTS))
label _SO_EXPLOSION_48X48 word
	dw ((104 * ROW_SIZE) + (320 / BYTE_DOTS))
	dw ((128 * ROW_SIZE) + (320 / BYTE_DOTS))
	dw ((152 * ROW_SIZE) + (320 / BYTE_DOTS))
	dw ((168 * ROW_SIZE) + (368 / BYTE_DOTS))
label _SO_EXPLOSION_64X64 word
	dw ((104 * ROW_SIZE) + (368 / BYTE_DOTS))
	dw ((136 * ROW_SIZE) + (368 / BYTE_DOTS))
	dw ((104 * ROW_SIZE) + (432 / BYTE_DOTS))
	dw ((136 * ROW_SIZE) + (432 / BYTE_DOTS))
label _SO_EXPLOSION_80X80 word
	dw ((160 * ROW_SIZE) + (  0 / BYTE_DOTS))
	dw ((160 * ROW_SIZE) + ( 80 / BYTE_DOTS))
	dw ((160 * ROW_SIZE) + (160 / BYTE_DOTS))
	dw ((160 * ROW_SIZE) + (240 / BYTE_DOTS))
public _chain_ring_p
_chain_ring_p	db	PLAYER_COUNT dup(0)

include th03/sprites/score.asp
include th03/main/5_powers_of_10[data].asm
public _ellen_render_y_offsets,_ellen_render_heights
_ellen_render_y_offsets label word
		db  6Ch	; l
		db    0
		db  60h
		db    0
		db  50h	; P
		db    0
		db  40h
		db    0
		db  30h	; 0
		db    0
		db  20h
		db    0
		db  10h
		db    0
		db    8
		db    0
		db    4
		db    0
_ellen_render_heights label word
		db    2
		db    0
		db    8
		db    0
		db  10h
		db    0
		db  10h
		db    0
		db  10h
		db    0
		db  10h
		db    0
		db  10h
		db    0
		db    8
		db    0
		db    2
		db    0
public _chiyuri_boss_x_words,_chiyuri_boss_y_words
_chiyuri_boss_x_words label word
		db    0
		db    3
_chiyuri_boss_y_words label word
		db    0
		db    7
		db    0
		db    6
		db    0
		db    6
		db    0
		db    9
		db    0
		db    5
		db    0
		db  0Ch
		db    0
		db    6
		db    0
		db  0Fh
		db    0
		db    7
public _result_label_combo
_result_label_combo label byte
aMAX_COMBO	db 'ÇlÇ`ÇwÅ@ÇbÇèÇçÇÇÇèÅ@Å@Å@Å~',0
public _result_label_gauge
_result_label_gauge label byte
aGAUGE_ATTACK_TIMES	db 'ÉQÅ[ÉWÉAÉ^ÉbÉNâÒêîÅ@Å@Å@Å~',0
public _result_label_boss
_result_label_boss label byte
aBOSS_ATTACK_TIMES	db 'É{ÉXÉAÉ^ÉbÉNâÒêîÅ@Å@Å@Å@Å~',0
public _result_label_reversal
_result_label_reversal label byte
aBOSS_REVERSAL_TIMES	db 'É{ÉXÉäÉoÅ[ÉTÉãâÒêîÅ@Å@Å@Å~',0
public _result_label_panic
_result_label_panic label byte
aBOSS_PANIC_TIMES	db 'É{ÉXÉpÉjÉbÉNâÒêîÅ@Å@Å@Å@Å~',0
public _result_label_total
_result_label_total label byte
aTOTAL	db 'Å@Å@Å@ÇsÇnÇsÇ`ÇkÅ@Å@Å@Å@Å@',0
public _result_label_winner
_result_label_winner label byte
aWINNER_BONUS	db 'Å@Å@ÇvÇhÇmÇmÇdÇqÅ@ÇaÇnÇmÇtÇrÅ@Å@',0
public _result_label_clear
_result_label_clear label byte
aALL_CLEAR	db 'Å@Å@Å@Ç`ÇkÇkÅ@ÇbÇkÇdÇ`ÇqÅIÅIÅ@Å@',0
public _result_label_lives
_result_label_lives label byte
aPLAYER_REM	db 'écÇËêlêîÅ@Å@Å@Å@Å@Å@Å@Å@Å~',0
	evendata
include th03/sprites/pellet.asp
		db    1
		db    0

	.data?

include libs/master.lib/vsync[bss].asm
include libs/master.lib/mem[bss].asm
include libs/master.lib/superpa[bss].asm
include th01/hardware/vram_planes[bss].asm
include th02/snd/snd[bss].asm
include libs/master.lib/pfint21[bss].asm
include th03/hardware/input[bss].asm
include th02/formats/pi_slots[bss].asm
include th03/formats/hfliplut[bss].asm
MRS_SLOT_COUNT = 8
public _mrs_images
_mrs_images	dd MRS_SLOT_COUNT dup(?)
include th03/sprite16[bss].asm
public _playfield_clip_negative_radius
_playfield_clip_negative_radius	Point <?>
public _resident
_resident	dd ?
palette_1F2F4	palette_t <?>
public _boss_pattern_previous,_boss_target_x,_boss_target_y,_boss_active
_boss_pattern_previous label byte
byte_1F324	db ?
		db ?
_boss_target_x label word
word_1F326	dw ?
_boss_target_y label word
word_1F328	dw ?
_boss_active label word
word_1F32A	dw ?
word_1F32C	dw ?
public _gba_boss_update,_gba_boss_render
_gba_boss_update label
gba_boss_update_p1	dd ?
gba_boss_update_p2	dd ?
_gba_boss_render label
gba_boss_render_p1	dd ?
gba_boss_render_p2	dd ?
public _boss_state,_boss_center_x,_boss_center_y
public _boss_velocity_x,_boss_velocity_y,_boss_hp,_boss_sprite_offset
public _boss_hit,_boss_mode,_boss_angle,_boss_pattern_i,_boss_pattern_count
public _boss_render_mode
_boss_state label byte
_boss_center_x label word
word_1F33E	dw ?
_boss_center_y label word
word_1F340	dw ?
public _boss_aux_point
_boss_aux_point label Point
point_1F342	Point <?>
_boss_velocity_x label word
word_1F346	dw ?
_boss_velocity_y label word
word_1F348	dw ?
_boss_hp label word
word_1F34A	dw ?
_boss_sprite_offset label word
sprite_1F34C	dw ?
_boss_hit label byte
byte_1F34E	db ?
_boss_mode label byte
byte_1F34F	db ?
_boss_angle label byte
angle_1F350	db ?
_boss_pattern_i label byte
byte_1F351	db ?
_boss_pattern_count label byte
byte_1F352	db ?
_boss_render_mode label byte
byte_1F353	db ?
public _boss_render_frame,_boss_move_phase,_boss_effect_radius,_boss_spin_delta
_boss_render_frame label byte
byte_1F354	db ?
_boss_move_phase label byte
byte_1F355	db ?
_boss_effect_radius label word
word_1F356	dw ?
_boss_spin_delta label byte
byte_1F358	db ?
		db 5 dup(?)
public _boss_character_template
_boss_character_template label byte
		db 64 dup(?)
public _gba_boss_level
_gba_boss_level	db ?
public _marisa_bullet_speed,_marisa_cloud_count_low,_marisa_cloud_speed
public _marisa_ring_speed,_marisa_ring_count,_marisa_cloud_count_high
public _mima_bullet_speed,_mima_random_count,_mima_random_speed
public _mima_trail_interval,_mima_pellet_speed,_mima_pellet_until,_mima_orbit_speed
public _yumemi_ring_speed,_yumemi_ring_count,_yumemi_aimed_speed_base
public _yumemi_cross_interval,_yumemi_chase_until,_yumemi_rain_interval
public _reimu_cloud_interval,_reimu_unused_param,_reimu_bullet_speed
public _reimu_orbit_count,_reimu_ring_speed,_reimu_ring_count
public _ellen_bullet_speed,_ellen_extra_count,_ellen_pellet_speed,_ellen_pellet_interval
public _kotohime_random_ring_speed,_kotohime_orbit_count
public _kotohime_aimed_speed_slow,_kotohime_aimed_speed_fast
public _kotohime_pellet_speed,_kotohime_pellet_interval,_kotohime_burst_count
public _chiyuri_cardinal_speed,_chiyuri_cardinal_interval,_chiyuri_ring_speed
public _chiyuri_ring_interval,_chiyuri_trail_speed,_chiyuri_fan_speed,_chiyuri_fan_count
public _kana_accel_count,_kana_ring_count_slow,_kana_ring_count_mid,_kana_ring_count_fast
public _kana_cloud_interval,_kana_cloud_count,_kana_rotating_speed
public _rikako_orbit_count,_rikako_entity_count,_rikako_pellet_count
public _rikako_burst_interval,_rikako_burst_speed
_marisa_bullet_speed label byte
_mima_bullet_speed label byte
_yumemi_ring_speed label byte
_reimu_cloud_interval label byte
_ellen_bullet_speed label byte
_kotohime_random_ring_speed label byte
_chiyuri_cardinal_speed label byte
_kana_accel_count label byte
_rikako_orbit_count label byte
byte_1F39F	db ?
_marisa_cloud_count_low label byte
_mima_random_count label byte
_yumemi_ring_count label byte
_reimu_unused_param label byte
_ellen_extra_count label byte
_kotohime_orbit_count label byte
_chiyuri_cardinal_interval label byte
_kana_ring_count_slow label byte
_rikako_entity_count label byte
byte_1F3A0	db ?
_marisa_cloud_speed label byte
_mima_random_speed label byte
_yumemi_aimed_speed_base label byte
_reimu_bullet_speed label byte
_ellen_pellet_speed label byte
_kotohime_aimed_speed_slow label byte
_chiyuri_ring_speed label byte
_kana_ring_count_mid label byte
_rikako_pellet_count label byte
byte_1F3A1	db ?
_marisa_ring_speed label byte
_mima_trail_interval label byte
_yumemi_cross_interval label byte
_reimu_orbit_count label byte
_ellen_pellet_interval label byte
_kotohime_aimed_speed_fast label byte
_chiyuri_ring_interval label byte
_kana_ring_count_fast label byte
_rikako_burst_interval label byte
byte_1F3A2	db ?
_marisa_ring_count label byte
_mima_pellet_speed label byte
_yumemi_chase_until label byte
_reimu_ring_speed label byte
_kotohime_pellet_speed label byte
_chiyuri_trail_speed label byte
_kana_cloud_interval label byte
_rikako_burst_speed label byte
byte_1F3A3	db ?
_marisa_cloud_count_high label byte
_mima_pellet_until label byte
_yumemi_rain_interval label byte
_reimu_ring_count label byte
_kotohime_pellet_interval label byte
_chiyuri_fan_speed label byte
_kana_cloud_count label byte
byte_1F3A4	db ?
_mima_orbit_speed label byte
_kotohime_burst_count label byte
_chiyuri_fan_count label byte
_kana_rotating_speed label byte
byte_1F3A5	db ?
		db 10 dup(?)
public _boss_frame
_boss_frame label word
word_1F3B0	dw ?
include th02/math/randring[bss].asm
public _chiyuri_gauge_x,_chiyuri_gauge_frame,_chiyuri_chargeshots
public _chiyuri_chargeshot_p
_chiyuri_gauge_x label word
		dw PLAYER_COUNT dup(?)
_chiyuri_gauge_frame label byte
		db PLAYER_COUNT dup(?)
_chiyuri_chargeshots label byte
		db 96 dup(?)
_chiyuri_chargeshot_p label word
word_1F51A	dw ?
public _enemy_formation_type,_enemy_formation_i,_enedat_2,_enemy_speed
public _enedat
_enemy_formation_type	db ?
_enemy_formation_i	db ?
_enedat_2	dw ?
_enemy_speed	db ?
	evendata
_enedat	dw ?

FORMATIONS_MAX = 24
public _formation_enemy_count,_formation_scripts,_formation_type_ring
public _formation_pos_type_ring,_formation_p,_formation_count
_formation_enemy_count  	db (FORMATIONS_MAX * 2) dup(?)
_formation_scripts      	dw ?
_formation_type_ring    	dw ?
_formation_pos_type_ring	dw ?
_formation_p            	db PLAYER_COUNT dup(?)
_formation_count        	db ?

		db ?
public _ellen_gauge_x,_ellen_gauge_y,_ellen_gauge_frame
public _ellen_chargeshots,_ellen_chargeshot_p
_ellen_gauge_x label word
		dw PLAYER_COUNT dup(?)
_ellen_gauge_y label word
		dw PLAYER_COUNT dup(?)
_ellen_gauge_frame label byte
		db PLAYER_COUNT dup(?)
_ellen_chargeshots label byte
		db 768 dup(?)
_ellen_chargeshot_p label word
word_1F868	dw ?
public _ellen_exatt_slots
_ellen_exatt_slots label byte
		db 720 dup(?)
public _ellen_exatt_slot_p
_ellen_exatt_slot_p label word
word_1FB3A	dw ?
public _ellen_bomb_particle_spawn_count,_ellen_bomb_particles
public _ellen_bomb_particle_p
_ellen_bomb_particle_spawn_count label word
word_1FB3C	dw ?
_ellen_bomb_particles label byte
		db 128 dup(?)
_ellen_bomb_particle_p label word
word_1FBBE	dw ?
public _stage_background_update
_stage_background_update label word
fp_1FBC0	dw ?
public _playfield_transition_frame
_playfield_transition_frame label byte
byte_1FBC2	db ?
public _playfield_transition_midpoint
_playfield_transition_midpoint label byte
byte_1FBC3	db ?
word_1FBC4	dw ?
word_1FBC6	dw ?
word_1FBC8	dw ?
word_1FBCA	dw ?
word_1FBCC	dw ?
word_1FBCE	dw ?
word_1FBD0	dw ?
word_1FBD2	dw ?
public _kana_bomb_angle
_kana_bomb_angle label byte
angle_1FBD4	db ?
		db ?
public _kana_gauge_x,_kana_gauge_frame,_kana_chargeshots
public _kana_chargeshot_p,_kana_active,_kana_frame
_kana_gauge_x label word
		dw PLAYER_COUNT dup(?)
_kana_gauge_frame label byte
		db PLAYER_COUNT dup(?)
_kana_chargeshots label byte
		db 432 dup(?)
_kana_chargeshot_p label word
word_1FD8C	dw ?
_kana_active label byte
byte_1FD8E	db ?
byte_1FD8F	db ?
_kana_frame label byte
		db PLAYER_COUNT dup(?)

hitcircle_t struct
	HITCIRCLE_age    	db ?
	HITCIRCLE_pid    	db ?
	HITCIRCLE_topleft	Point <?>
hitcircle_t ends

HITCIRCLE_FRAMES = 16
HITCIRCLE_ENEMY_COUNT = 12
HITCIRCLE_PLAYER_COUNT = 1
HITCIRCLE_COUNT = (HITCIRCLE_ENEMY_COUNT + HITCIRCLE_PLAYER_COUNT)
public _hitcircles,_hitcircles_enemy_last_id
public _hitcircles_enemy_add_do_not_rand
_hitcircles	hitcircle_t HITCIRCLE_COUNT dup (<?>)
_hitcircles_enemy_last_id	db ?
_hitcircles_enemy_add_do_not_rand	db ?
		db 2 dup(?)
public _marisa_gauge_y,_marisa_gauge_frame,_marisa_chargeshots
_marisa_gauge_y label word
		dw 2 dup(?)
_marisa_gauge_frame label byte
		db 2 dup(?)
_marisa_chargeshots label byte
byte_1FDEA	db ?
		db 49 dup(?)
byte_1FE1C	db ?
		db 49 dup(?)
public _marisa_chargeshot_p
_marisa_chargeshot_p label word
word_1FE4E	dw ?
public _marisa_bullet_angle
_marisa_bullet_angle label byte
byte_1FE50	db ?
		db ?
public _marisa_bomb_point
_marisa_bomb_point label word
point_1FE52	Point <?>
public _kotohime_bomb_explosion_y
_kotohime_bomb_explosion_y label word
word_1FE56	dw ?
public _kotohime_gauge_frame,_kotohime_chargeshots
public _kotohime_chargeshot_p
_kotohime_gauge_frame label byte
		db PLAYER_COUNT dup(?)
_kotohime_chargeshots label byte
byte_1FE5A	db ?
		db 7 dup(?)
byte_1FE62	db ?
		db 7 dup(?)
_kotohime_chargeshot_p label word
word_1FE6A	dw ?
public _exatt_funcs
_exatt_funcs label byte
exatt_add_p1	dd ?
public _round_exatt_update_p1
_round_exatt_update_p1 label dword
exatt_update_p1	dd ?
public _round_exatt_render_p1
_round_exatt_render_p1 label dword
exatt_render_p1	dd ?
exatt_add_p2	dd ?
public _round_exatt_update_p2
_round_exatt_update_p2 label dword
exatt_update_p2	dd ?
public _round_exatt_render_p2
_round_exatt_render_p2 label dword
exatt_render_p2	dd ?

		db 4 dup(?)
public _pid_current
_pid_current	db ?
	evendata
public _exatt_entities
_exatt_entities label byte
		db 1024 dup(?)
public _exatt_entity_p
_exatt_entity_p label word
word_2028A	dw ?
public _chargeshot_update,_chargeshot_render,_chargeshot_hittest
_chargeshot_update label dword
_chargeshot_update_p1	dd ?
_chargeshot_update_p2	dd ?
_chargeshot_render label dword
_chargeshot_render_p1	dd ?
_chargeshot_render_p2	dd ?
_chargeshot_hittest label dword
chargeshot_hittest_p1	dd ?
chargeshot_hittest_p2	dd ?

GBAF_NONE = 0
GBAF_GAUGE_PELLET_INIT = 1
GBAF_GAUGE_BULLET_INIT = 3
GBAF_BOSS = 5
GBAF_PELLET_TO_BULLET = (GBAF_GAUGE_BULLET_INIT - GBAF_GAUGE_PELLET_INIT)
public _gba_gauge_pattern_pellet,_gba_gauge_pattern_bullet
public _gba_flag_active,_gba_gauge_level
_gba_gauge_pattern_pellet label dword
gba_gauge_pattern_pellet_p1	dd ?
gba_gauge_pattern_pellet_p2	dd ?
_gba_gauge_pattern_bullet label dword
gba_gauge_pattern_bullet_p1	dd ?
gba_gauge_pattern_bullet_p2	dd ?
_gba_flag_active db PLAYER_COUNT dup(?)
_gba_gauge_level	db PLAYER_COUNT dup(?)
public _gauge_pattern_timing
public _kotohime_exatt_pattern
_kotohime_exatt_pattern label byte
_gauge_pattern_timing label byte
		db 8 dup(?)
		db 8 dup(?)
public _reimu_gauge_frame,_reimu_chargeshots
_reimu_gauge_frame label byte
		db 2 dup(?)
_reimu_chargeshots label byte
		db 768 dup(?)
public _reimu_chargeshot_p,_reimu_chargeshot_alternate_hit_f
_reimu_chargeshot_p label word
word_205CA	dw ?
_reimu_chargeshot_alternate_hit_f label byte
byte_205CC	db ?
		db ?
public _round_player_hook_p1
_round_player_hook_p1 label dword
p1_205CE	dd ?
public _round_player_hook_p2
_round_player_hook_p2 label dword
p2_205D2	dd ?
public _round_bomb_p1
_round_bomb_p1 label dword
bomb_p1	dd ?
public _round_bomb_p2
_round_bomb_p2 label dword
bomb_p2	dd ?
public _bomb_frame
_bomb_frame	db PLAYER_COUNT dup(?)
public _reimu_bomb_particles
_reimu_bomb_particles label byte
		db 512 dup(?)
public _reimu_bomb_particle_p
_reimu_bomb_particle_p label word
word_207E0	dw ?

HSF_DONE = 0
HSF_INIT = 1
HSF_ACTIVE = 2
public _hud_start_flag,_round_id
_hud_start_flag	db ?
_round_id	db ?
public _hud_start_particles
_hud_start_particles label byte
		db 150 dup(?)
public _hud_intro_destination_x
_hud_intro_destination_x label word
word_2087A	dw ?
		db 1128 dup(?)
public _hud_start_particle_p
_hud_start_particle_p label word
word_20CE4	dw ?
public _hud_intro_phase
_hud_intro_phase label byte
byte_20CE6	db ?
		db ?
public _hud_intro_frame,_hud_intro_sprite,_hud_intro_x
_hud_intro_frame label word
word_20CE8	dw ?
_hud_intro_sprite label word
word_20CEA	dw ?
_hud_intro_x label word
x_20CEC	dw ?
		db 2 dup(?)
public _mima_gauge_angle,_mima_gauge_angle_step,_mima_gauge_frame
public _mima_chargeshots,_mima_chargeshot_p
public _mima_chargeshot_active,_mima_chargeshot_frame
_mima_gauge_angle label byte
		db 2 dup(?)
_mima_gauge_angle_step label byte
		db 2 dup(?)
_mima_gauge_frame label byte
		db 2 dup(?)
_mima_chargeshots label byte
		db 300 dup(?)
_mima_chargeshot_p label word
word_20E22	dw ?
_mima_chargeshot_active label byte
		db 2 dup(?)
_mima_chargeshot_frame label byte
		db 2 dup(?)
public _mima_spread_angle,_mima_pellet_angle,_mima_orbit_delta,_mima_orbit_angle
_mima_spread_angle label byte
byte_20E28	db ?
_mima_pellet_angle label byte
byte_20E29	db ?
_mima_orbit_delta label byte
byte_20E2A	db ?
_mima_orbit_angle label byte
angle_20E2B	db ?
public _hitbox_hittest_skip_explosions,_hitbox
_hitbox_hittest_skip_explosions	db ?
	evendata
_hitbox label byte
_hitbox_origin_center label Point
_hitbox_origin_topleft label Point
	Point <?>
_hitbox_radius	Point <?>
_hitbox_right 	dw ?
_hitbox_bottom	dw ?
_hitbox_pid	db ?
	evendata

DF_NONE = 0
DF_EXPLODE = 1
DF_BANNER = 2
public _defeat_flag
_defeat_flag	db ?
public _round_defeated_player
_round_defeated_player label byte
byte_20E3D	db ?
public _player_lose_left
_player_lose_left label word
word_20E3E	dw ?
public _player_lose_top
_player_lose_top label word
word_20E40	dw ?
public _player_lose_radius
_player_lose_radius label word
word_20E42	dw ?
public _player_hittest_collision_top
_player_hittest_collision_top	Point <?>
public _target_formation_marker
_target_formation_marker label byte
byte_20E48	db ?
		db ?
public _cpu_dodge_pattern
_cpu_dodge_pattern label word
word_20E4A	dw ?
public _yumemi_speed_add,_yumemi_angle_delta,_yumemi_angle
public _yumemi_origin_x,_yumemi_origin_y
_yumemi_speed_add label byte
byte_20E4C	db ?
_yumemi_angle_delta label byte
byte_20E4D	db ?
_yumemi_angle label byte
byte_20E4E	db ?
		db ?
_yumemi_origin_x label word
word_20E50	dw ?
_yumemi_origin_y label word
word_20E52	dw ?
public _rikako_gauge_frame,_rikako_chargeshots
public _rikako_chargeshot_p,_rikako_active,_rikako_frame
public _rikako_radius,_rikako_center_x,_rikako_center_y
_rikako_gauge_frame label byte
		db PLAYER_COUNT dup(?)
_rikako_chargeshots label byte
		db 48 dup(?)
_rikako_chargeshot_p label word
word_20E86	dw ?
_rikako_active label byte
byte_20E88	db ?
byte_20E89	db ?
_rikako_frame label byte
		db PLAYER_COUNT dup(?)
_rikako_radius label word
		dw PLAYER_COUNT dup(?)
_rikako_center_x label word
		dw PLAYER_COUNT dup(?)
_rikako_center_y label word
		dw PLAYER_COUNT dup(?)
public _warning_brightness,_warning_fading_out
_warning_brightness label byte
		db 2 dup(?)
_warning_fading_out label byte
		db 2 dup(?)
public _gba_flag_next
_gba_flag_next	db PLAYER_COUNT dup(?)
include th03/main/player/combo[bss].asm
public _player_effects
_player_effects label byte
		db 120 dup(?)
public _player_effect_cursor
_player_effect_cursor label byte
byte_20F1E	db ?
		db ?
public _main_background_init
_main_background_init label dword
farfp_20F20	dd ?
public _background_render
_background_render label dword
public _round_render_hook
_round_render_hook label dword
farfp_20F24	dd ?
public _round_background_reset
_round_background_reset label dword
farfp_20F28	dd ?
; Zero-byte alias to existing, nonexclusive DGROUP storage.
public _background_particles
_background_particles label byte
		db 1280 dup(?)
public _background_angle
_background_angle label byte
angle_2142C	db ?
		db ?
public _ellen_target_x,_ellen_target_y
_ellen_target_x label word
word_2142E	dw ?
_ellen_target_y label word
word_21430	dw ?
		db 2 dup(?)
public _combo_points_for_boss_attack
_combo_points_for_boss_attack	dw ?

EFF_FREE = 0
EFF_EXPLOSION_IGNORING_ENEMIES = 9
EFF_EXPLOSION_HITTING_ENEMIES = 10

efe_t struct
	EFE_flag                         	db ?
	EFE_frame                        	db ?
	EFE_center                       	Point <?>
	EFE_explosion_max_enemy_hits_half	db ?
		db ?
	EFE_pid                          	db ?
	EFE_size_pixels                  	db ?
		db 18 dup (?)
	EFE_chain_slot                   	db ?
		db 19 dup(?)
efe_t ends

EF_RUNNING_SPAWNED = 1

enemy_t struct
	ENEMY_flag           	db ?
	ENEMY_frame          	db ?
	ENEMY_center         	Point <?>
	ENEMY_size_words     	db ?
	ENEMY_hp             	db ?
	ENEMY_pid            	db ?
	ENEMY_size_pixels    	db ?
	ENEMY_script_ip      	dw ?
	ENEMY_script_op_frame	dw ?
	ENEMY_script_base    	dw ?
	ENEMY_velocity       	Point <?>
		db 4 dup (?)
	ENEMY_angle_wide label word
	ENEMY_angle_fine     	db ?
	ENEMY_angle_coarse   	db ?
	ENEMY_angle_speed    	db ?
		db ?
	ENEMY_chain_slot     	db ?
	ENEMY_formation_type 	db ?
	ENEMY_formation_i    	db ?
	ENEMY_speed          	db ?
	ENEMY_loop_i         	db ?
	ENEMY_pos_type       	db ?
		db 14 dup(?)
enemy_t ends

EFE_COUNT = 64
ENEMY_COUNT = 40
public _efes,_enemies_alive,_boss_panic_fired_in_current_comb
public _explosion_hittest_against,_explosion_collision_in_last_hitt,_efe_p
label enemies enemy_t
_efes	efe_t EFE_COUNT dup(<?>)
_enemies_alive	db PLAYER_COUNT dup(?)
_boss_panic_fired_in_current_comb db PLAYER_COUNT dup(?)
_explosion_hittest_against	db ?
_explosion_collision_in_last_hitt	db ?
_efe_p	dw ?

CHAIN_RING_SIZE = 16

chains_t struc
	CHAIN_hits                    	db PLAYER_COUNT dup (CHAIN_RING_SIZE dup(?))
	CHAIN_pellet_or_fireball_value	db PLAYER_COUNT dup (CHAIN_RING_SIZE dup(?))
	CHAIN_charge_fireball         	db PLAYER_COUNT dup (CHAIN_RING_SIZE dup(?))
	CHAIN_charge_exatt            	db PLAYER_COUNT dup (CHAIN_RING_SIZE dup(?))
chains_t ends
public _chains,_explosion_collision_chain_slot
public _enemy_killed_in_previous_hittest
_chains	chains_t <?>
		dd ?
_explosion_collision_chain_slot	db ?
_enemy_killed_in_previous_hittest	db ?
include th03/main/player/score[bss].asm

EXTENDS_MAX = 2
EXTENDS_DISABLE = 255
public _extends_gained
_extends_gained	db ?
		db ?
public _yumemi_gauge_frame,_yumemi_chargeshots
_yumemi_gauge_frame label byte
		db 2 dup(?)
_yumemi_chargeshots label byte
byte_220E0	db ?
		db 5 dup(?)
byte_220E6	db ?
		db 5 dup(?)
public _rikako_bomb_line_offset
_rikako_bomb_line_offset label word
word_220EC	dw ?
public _collmap_topleft,_collmap_center,_collmap_stripe_tile_w
public _collmap_tile_h,_collmap_bottomright,_collmap_pid,_collmap
_collmap_topleft label Point
_collmap_center label Point
	Point <?>
_collmap_stripe_tile_w	dw ?
_collmap_tile_h	dw ?
_collmap_bottomright	Point <?>
_collmap_pid	db ?
		db ?
public _shot_release_frames
_shot_release_frames db 2 dup(?)
		db 2 dup(?)
_collmap	db (PLAYER_COUNT * COLLMAP_SIZE) dup(?)

BOMB_FRAMES = 180

BF_INACTIVE = 0
BF_PREPARING = 1
BF_ACTIVE = 2
public _bomb_flag,_player_speed_base,_player_velocity
_bomb_flag	db PLAYER_COUNT dup(?)
_player_speed_base	speed_t <?>
_player_velocity  	SPPoint8 <?>
public _player_cur,_cpu_hit_damage_additional,_damage_all_on
_player_cur	dw ?
_cpu_hit_damage_additional	db ?
_damage_all_on	db PLAYFIELD_COUNT dup(?)
		db ?
include th02/hardware/pages[bss].asm
public _pid
_pid_PID_current  	label byte
_pid_PID_so_attack	label byte
_pid	db ?
	evendata

ROUND_SPEED_MAX = ((8 shl 4) - 1)
public _round_frame,_round_or_result_frame,_round_speed
_round_frame	dd ?
_round_or_result_frame	dw ?
_round_speed	db ?
public _round_reset_flag
_round_reset_flag label byte
byte_23AF9	db ?
public _stage_render_timing_flag
_stage_render_timing_flag label byte
byte_23AFA	db ?
		db ?
include th03/main/playfield_fg_x[bss].asm
public _round_quit_requested
_round_quit_requested label byte
public _round_reset_clear_flag
_round_reset_clear_flag label byte
byte_23B00	db ?
include th03/hardware/palette_changed[bss].asm
include th03/main/frame_mod[bss].asm
include th03/main/player/players[bss].asm
include th03/main/player/shots[bss].asm
public _reimu_direction,_reimu_cloud_speed,_reimu_orbit_angle
public _reimu_orbit_x,_reimu_orbit_y
_reimu_direction label byte
byte_23DC6	db ?
_reimu_cloud_speed label byte
byte_23DC7	db ?
_reimu_orbit_angle label byte
byte_23DC8	db ?
		db ?
_reimu_orbit_x label word
		dw 6 dup(?)
_reimu_orbit_y label word
		dw 6 dup(?)
public _ellen_spread_angle,_ellen_pellet_angle
_ellen_spread_angle label byte
byte_23DE2	db ?
_ellen_pellet_angle label byte
byte_23DE3	db ?
public _chiyuri_cardinal_angle,_chiyuri_cardinal_reverse
_chiyuri_cardinal_angle label byte
byte_23DE4	db ?
_chiyuri_cardinal_reverse label byte
byte_23DE5	db ?
public _kana_rotating_angle,_kana_rotating_delta
_kana_rotating_angle label byte
byte_23DE6	db ?
_kana_rotating_delta label byte
byte_23DE7	db ?
public _rikako_random_angle,_rikako_bullet_type
_rikako_random_angle label byte
byte_23DE8	db ?
_rikako_bullet_type label byte
bullet_type_23DE9	db ?
public _result_bonus_step
_result_bonus_step label word
score_23DEA	dw ?
public _result_bonus_low
_result_bonus_low label word
word_23DEC	dw ?
public _result_bonus_high
_result_bonus_high label word
word_23DEE	dw ?
public _result_bonus_remaining
_result_bonus_remaining label dword
score_23DF0	dd ?
public _defeat_combo_hits_max
public _defeat_gauge_attacks_fired,_defeat_boss_attacks_fired
public _defeat_boss_attacks_reversed,_defeat_boss_panics_fired
_defeat_combo_hits_max       	db ?
_defeat_gauge_attacks_fired  	db ?
_defeat_boss_attacks_fired   	db ?
_defeat_boss_attacks_reversed	db ?
_defeat_boss_panics_fired    	db ?

public _result_lives_remaining
_result_lives_remaining label byte
byte_23DF9	db ?
public _mima_bomb_columns,_mima_bomb_column_p
_mima_bomb_columns label byte
		db 64 dup(?)
_mima_bomb_column_p label word
word_23E3A	dw ?

bullet_template_t struc
	BT_center       	Point <?>
	BT_speed        	db ?
	BT_angle        	db ?
	BT_pid          	db ?
	BT_group        	db ?
	BT_accel_type   	db ?
	BT_count        	db ?
	BT_velocity_tmp 	Point <?>
	BT_sprite_offset	dw ?
	BT_type         	db ?
	BT_is_collidable	db ?
	BT_is_animated  	db ?
	BT_has_trail    	db ?
bullet_template_t ends

	extern _bullet_base_speed:byte
	extern _bullet_template:bullet_template_t
	extern _ef_onehit:byte

		end
