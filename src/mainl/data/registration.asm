; Registration glyph names, mutable near filename pointers and initial hold state.
; Maintained UTF-8; native staging encodes CP932 without changing source content.
; The historical extra final zero is excluded; the linker owns any following gap.
.386
.model use16 large _TEXT
include src/mainl/hiscore/regi_codes.inc

	.data
public aNoEntry
public aB@b@sCB@b@
public aB@b@cgcvb@b@
public aB@cvcanB@
public aB@gggmgub@
public aB@pmuexpb@
public aB@Gjgi
public aB@canboq
public aB@vVfvsb@
public aB@CF
public aYume_nem
public aRft0_cdg
public aOver_m
public _REGI_PLAYCHAR
_REGI_PLAYCHAR label byte
	db REGI_R, REGI_E, REGI_I, REGI_M, REGI_U, regi_sp, regi_sp, regi_sp
	db REGI_M, REGI_I, REGI_M, REGI_A, regi_sp, regi_sp, regi_sp, regi_sp
	db REGI_M, REGI_A, REGI_R, REGI_I, REGI_S, REGI_A, regi_sp, regi_sp
	db REGI_E, REGI_L, REGI_E, REGI_N, regi_sp, regi_sp, regi_sp, regi_sp
	db REGI_K, REGI_O, REGI_T, REGI_O, REGI_H, REGI_I, REGI_M, REGI_E
	db REGI_K, REGI_A, REGI_N, REGI_A, regi_sp, regi_sp, regi_sp, regi_sp
	db REGI_R, REGI_I, REGI_K, REGI_A, REGI_K, REGI_O, regi_sp, regi_sp
	db REGI_C, REGI_H, REGI_I, REGI_Y, REGI_U, REGI_R, REGI_I, regi_sp
	db REGI_Y, REGI_U, REGI_M, REGI_E, REGI_M, REGI_I, regi_sp, regi_sp
public _SCOREDAT_FN_PTR
_SCOREDAT_FN_PTR	dw offset aYume_nem
public _rank_image_fn, _REGIST_INPUT_HOLD_INIT
_rank_image_fn	dw offset aRft0_cdg
_REGIST_INPUT_HOLD_INIT	dw 4 dup(0)
public _mainl_name_none
_mainl_name_none label byte
aNoEntry	db '  No Entry! ',0
public _mainl_name_reimu
_mainl_name_reimu label byte
aB@b@sCB@b@	db '　　靈夢　　',0
public _mainl_name_mima
_mainl_name_mima label byte
aB@b@cgcvb@b@	db '　　魅魔　　',0
public _mainl_name_marisa
_mainl_name_marisa label byte
aB@cvcanB@	db ' 　魔理沙　 ',0
public _mainl_name_ellen
_mainl_name_ellen label byte
aB@gggmgub@	db ' 　エレン　 ',0
public _mainl_name_kotohime
_mainl_name_kotohime label byte
aB@pmuexpb@	db ' 　小兎姫　 ',0
public _mainl_name_kana
_mainl_name_kana label byte
aB@Gjgi		db ' 　 カナ    ',0
public _mainl_name_rikako
_mainl_name_rikako label byte
aB@canboq	db ' 　理香子   ',0
public _mainl_name_chiyuri
_mainl_name_chiyuri label byte
aB@vVfvsb@	db ' 　ちゆり　 ',0
public _mainl_name_yumemi
_mainl_name_yumemi label byte
aB@CF		db ' 　 夢美　  ',0
aYume_nem	db 'YUME.NEM',0
aRft0_cdg	db 'rft0.cdg',0
public _regib_pi, _regi2_bft, _regi1_bft, _score_m, _conti_pi, _conti_cd2
public _GAMEOVER_BG_FN
_regib_pi 	db 'regib.pi',0
_regi2_bft	db 'regi2.bft',0
_regi1_bft	db 'regi1.bft',0
_score_m	db 'score.m',0
_conti_pi	db 'conti.pi',0
_conti_cd2	db 'conti.cd2',0
_GAMEOVER_BG_FN	db 'over.pi',0
public _mainl_over_music
_mainl_over_music label byte
aOver_m		db 'over.m',0

	end
