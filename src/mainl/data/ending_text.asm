; Ending/verdict/staff strings, with original compatibility aliases.
; Maintained UTF-8; native staging encodes CP932 without changing source content.
.386
.model use16 large _TEXT

	.data
public a@00ed_txt
public a@99ed_txt
public aOp_0
public aFocab@sC_0
public aCgCv_0
public aCIjb@cvcan_0
public aB@b@gggmgu_0
public aPmuexp_0
public aGjgibegagigx_0
public aB@tisqb@canb_0
public aCkftiB@vVfvs_0
public aB@iknsb@cF_0
public aVdvbvuvs
public aVmvpvtvnvbvm
public aVgvbvtvd
public aVkvxvovbvfvivg
public aVo
public aVp
public aVq
public aVr
public aVs
public aVt
public aVu
public aVv
public aVw
public aVx
public aU_
public aEd_m
public aEdbk1_rgb
public aStf1_cdg
public aStf11_cdg
public aStf3_cdg
public aStf4_cdg
public aStf5_cdg
public aStf6_cdg
public aStf7_cdg
public aStf8_cdg
public aStf9_cdg
public aStf10_cdg
public aStf2_cdg
public aStf12_cdg
public _mainl_ending_template
_mainl_ending_template label byte
a@00ed_txt	db '@00ED.TXT',0
public _mainl_bonus_script
_mainl_bonus_script label byte
a@99ed_txt	db '@99ED.TXT',0
; char aOp_0[]
public _mainl_op_name
_mainl_op_name label byte
aOp_0		db 'op',0
public _mainl_vname_0
_mainl_vname_0 label byte
aFocab@sC_0	db '   博麗　靈夢',0
public _mainl_vname_1
_mainl_vname_1 label byte
aCgCv_0		db '     魅 魔',0
public _mainl_vname_2
_mainl_vname_2 label byte
aCIjb@cvcan_0	db '  霧雨　魔理沙 ',0
public _mainl_vname_3
_mainl_vname_3 label byte
aB@b@gggmgu_0	db '　　エレン',0
public _mainl_vname_4
_mainl_vname_4 label byte
aPmuexp_0	db '    小兎姫',0
public _mainl_vname_5
_mainl_vname_5 label byte
aGjgibegagigx_0	db 'カナ・アナベラル',0
public _mainl_vname_6
_mainl_vname_6 label byte
aB@tisqb@canb_0	db '　朝倉　理香子',0
public _mainl_vname_7
_mainl_vname_7 label byte
aCkftiB@vVfvs_0	db ' 北白河　ちゆり',0
public _mainl_vname_8
_mainl_vname_8 label byte
aB@iknsb@cF_0	db ' 　岡崎　夢美',0
public _mainl_vrank_0
_mainl_vrank_0 label byte
aVdvbvuvs	db '   Ｅａｓｙ',0
public _mainl_vrank_1
_mainl_vrank_1 label byte
aVmvpvtvnvbvm	db ' Ｎｏｒｍａｌ',0
public _mainl_vrank_2
_mainl_vrank_2 label byte
aVgvbvtvd	db '   Ｈａｒｄ',0
public _mainl_vrank_3
_mainl_vrank_3 label byte
aVkvxvovbvfvivg	db 'Ｌｕｎａｔｉｃ',0
public _mainl_vdigit_0
_mainl_vdigit_0 label byte
aVo		db '０',0
public _mainl_vdigit_1
_mainl_vdigit_1 label byte
aVp		db '１',0
public _mainl_vdigit_2
_mainl_vdigit_2 label byte
aVq		db '２',0
public _mainl_vdigit_3
_mainl_vdigit_3 label byte
aVr		db '３',0
public _mainl_vdigit_4
_mainl_vdigit_4 label byte
aVs		db '４',0
public _mainl_vdigit_5
_mainl_vdigit_5 label byte
aVt		db '５',0
public _mainl_vdigit_6
_mainl_vdigit_6 label byte
aVu		db '６',0
public _mainl_vdigit_7
_mainl_vdigit_7 label byte
aVv		db '７',0
public _mainl_vdigit_8
_mainl_vdigit_8 label byte
aVw		db '８',0
public _mainl_vdigit_9
_mainl_vdigit_9 label byte
aVx		db '９',0
public _mainl_verdict_unit
_mainl_verdict_unit label byte
aU_		db '点',0
public _mainl_staff_music
_mainl_staff_music label byte
aEd_m		db 'ed.m',0
public _mainl_staff_palette
_mainl_staff_palette label byte
aEdbk1_rgb	db 'edbk1.rgb',0
public _mainl_stf1
_mainl_stf1 label byte
aStf1_cdg	db 'stf1.cdg',0
public _mainl_stf11
_mainl_stf11 label byte
aStf11_cdg	db 'stf11.cdg',0
public _mainl_stf3
_mainl_stf3 label byte
aStf3_cdg	db 'stf3.cdg',0
public _mainl_stf4
_mainl_stf4 label byte
aStf4_cdg	db 'stf4.cdg',0
public _mainl_stf5
_mainl_stf5 label byte
aStf5_cdg	db 'stf5.cdg',0
public _mainl_stf6
_mainl_stf6 label byte
aStf6_cdg	db 'stf6.cdg',0
public _mainl_stf7
_mainl_stf7 label byte
aStf7_cdg	db 'stf7.cdg',0
public _mainl_stf8
_mainl_stf8 label byte
aStf8_cdg	db 'stf8.cdg',0
public _mainl_stf9
_mainl_stf9 label byte
aStf9_cdg	db 'stf9.cdg',0
public _mainl_stf10
_mainl_stf10 label byte
aStf10_cdg	db 'stf10.cdg',0
public _mainl_stf2
_mainl_stf2 label byte
aStf2_cdg	db 'stf2.cdg',0
public _mainl_stf12
_mainl_stf12 label byte
aStf12_cdg	db 'stf12.cdg',0


	end
