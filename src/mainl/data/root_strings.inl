; Root stage/shot state and readable CP932 strings; twelve-byte SHOT_FN buffer.
public _mainl_stage_number
_mainl_stage_number label word
word_E502	dw offset aSt_cd2
public _mainl_stage_bg
_mainl_stage_bg label word
word_E504	dw offset aStnx1_pi
public _SHOT_FN
_SHOT_FN db '0016.pi', 0, 0, 0, 0, 0
SHOT_FN_SIZE = ($ - _SHOT_FN)
public a00sl_cd2
a00sl_cd2	db '00sl.cd2',0
public a02sl_cd2
a02sl_cd2	db '02sl.cd2',0
public a04sl_cd2
a04sl_cd2	db '04sl.cd2',0
public a06sl_cd2
a06sl_cd2	db '06sl.cd2',0
public a08sl_cd2
a08sl_cd2	db '08sl.cd2',0
public a10sl_cd2
a10sl_cd2	db '10sl.cd2',0
public a12sl_cd2
a12sl_cd2	db '12sl.cd2',0
public a14sl_cd2
a14sl_cd2	db '14sl.cd2',0
public a16sl_cd2
a16sl_cd2	db '16sl.cd2',0
public _mainl_script_0
_mainl_script_0 label byte
a@00tx_txt	db '@00TX.TXT',0
public _mainl_script_1
_mainl_script_1 label byte
a@01tx_txt	db '@01TX.TXT',0
public _mainl_script_2
_mainl_script_2 label byte
a@02tx_txt	db '@02TX.TXT',0
public _mainl_script_3
_mainl_script_3 label byte
a@03tx_txt	db '@03TX.TXT',0
public _mainl_script_4
_mainl_script_4 label byte
a@04tx_txt	db '@04TX.TXT',0
public _mainl_script_5
_mainl_script_5 label byte
a@05tx_txt	db '@05TX.TXT',0
public _mainl_script_6
_mainl_script_6 label byte
a@06tx_txt	db '@06TX.TXT',0
public _mainl_script_7
_mainl_script_7 label byte
a@07tx_txt	db '@07TX.TXT',0
public _mainl_script_8
_mainl_script_8 label byte
a@08tx_txt	db '@08TX.TXT',0
public _mainl_story_template
_mainl_story_template label byte
a@00dm0_txt	db '@00DM0.TXT',0
public _mainl_title_0
_mainl_title_0 label byte
TITLE_REIMU		db '   夢と伝統を保守する巫女   ',0
public _mainl_name_0
_mainl_name_0 label byte
NAME_REIMU	db '   博麗　靈夢',0
public _mainl_title_1
_mainl_title_1 label byte
TITLE_MIMA	db ' 久遠の夢に運命を任せる精神 ',0
public _mainl_name_1
_mainl_name_1 label byte
NAME_MIMA		db '     魅 魔',0
public _mainl_title_2
_mainl_title_2 label byte
TITLE_MARISA	db '   魔法と紅夢からなる存在   ',0
public _mainl_name_2
_mainl_name_2 label byte
NAME_MARISA	db '  霧雨　魔理沙 ',0
public _mainl_title_3
_mainl_title_3 label byte
TITLE_ELLEN	db 'はたらきもので恋を夢見る魔女',0
public _mainl_name_3
_mainl_name_3 label byte
NAME_ELLEN	db '　　エレン',0
public _mainl_title_4
_mainl_title_4 label byte
TITLE_KOTOHIME		db '     弾幕に美を夢みる姫     ',0
public _mainl_name_4
_mainl_name_4 label byte
NAME_KOTOHIME		db '    小兎姫',0
public _mainl_title_5
_mainl_title_5 label byte
TITLE_KANA		db '     夢を失った少女騒霊     ',0
public _mainl_name_5
_mainl_name_5 label byte
NAME_KANA	db 'カナ・アナベラル',0
public _mainl_title_6
_mainl_title_6 label byte
TITLE_RIKAKO	db '  　　　夢を探す科学        ',0
public _mainl_name_6
_mainl_name_6 label byte
NAME_RIKAKO	db '　朝倉　理香子',0
public _mainl_title_7
_mainl_title_7 label byte
TITLE_CHIYURI		db '　  時をかける夢幻の住人    ',0
public _mainl_name_7
_mainl_name_7 label byte
NAME_CHIYURI	db ' 北白河　ちゆり',0
public _mainl_title_8
_mainl_title_8 label byte
TITLE_YUMEMI	db '　  　　　夢幻伝説　　　    ',0
public _mainl_name_8
_mainl_name_8 label byte
NAME_YUMEMI	db ' 　岡崎　夢美',0
public _CFG_FN
_CFG_FN db 'YUME.CFG',0
public _logo0_rgb, _logo_cd2, _logo5_cdg
_logo0_rgb	db 'logo0.rgb',0
_logo_cd2 	db 'logo.cd2',0
_logo5_cdg	db 'logo5.cdg',0
public _mainl_logo_palette
_mainl_logo_palette label byte
aLogo1_rgb	db 'logo1.rgb',0
aSt_cd2		db 'st.cd2',0
aStnx1_pi	db 'stnx1.pi',0
public _mainl_stage_blank
_mainl_stage_blank label byte
aStnx0_pi	db 'stnx0.pi',0
public _PLAYCHAR_BGM_FN
_PLAYCHAR_BGM_FN	db '00mm.m',0
public _mainl_dec_bgm
_mainl_dec_bgm label byte
aDec_m		db 'dec.m',0
public _mainl_intro_frame
_mainl_intro_frame label byte
aEn2_pi		db 'EN2.pi',0
public _mainl_enemy00
_mainl_enemy00 label byte
aEnemy00_pi	db 'ENEMY00.pi',0
public _mainl_enemy01
_mainl_enemy01 label byte
aEnemy01_pi	db 'ENEMY01.pi',0
public _mainl_enemy02
_mainl_enemy02 label byte
aEnemy02_pi	db 'ENEMY02.pi',0
public _mainl_enemy03
_mainl_enemy03 label byte
aEnemy03_pi	db 'ENEMY03.pi',0
public _mainl_enemy04
_mainl_enemy04 label byte
aEnemy04_pi	db 'ENEMY04.pi',0
public _mainl_sound_effects
_mainl_sound_effects label byte
aYume_efc	db 'YUME.EFC',0
public _mainl_archive_name
_mainl_archive_name label byte
aCOul		db '夢時空1.dat',0
public _mainl_gaiji_font
_mainl_gaiji_font label byte
aMikoft_bft	db 'MIKOFT.bft',0
; char path[]
public _mainl_root_op_name
_mainl_root_op_name label byte
path		db 'op',0
public _mainl_win_bgm
_mainl_win_bgm label byte
aWin_m		db 'win.m',0
; char aMain[]
public _mainl_main_name
_mainl_main_name label byte
aMain		db 'main',0
