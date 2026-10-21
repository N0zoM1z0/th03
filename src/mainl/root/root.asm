; MAINL root orchestration, decoded 095F:0186..0B3D (2488 bytes).
; Nine complete procedures (2470 bytes), then/in-between the 18-byte symbolic
; enemy switch table. Provider macros, declarations and DATA remain contextual.
; Preserve the original labels for carrier calls and original symbolic operands.
; This is source, not a dumped opcode stream. No padding or target-byte repair.
;
public CDG_FREE_ALL
; Free all 32 CDG slots in order; ignore provider failures. Near return.
cdg_free_all	proc near
	push	bp
	mov	bp, sp
	push	si
	xor	si, si
	jmp	short @@done?

@@loop:
	call	cdg_free pascal, si
	inc	si

@@done?:
	cmp	si, CDG_SLOT_COUNT
	jl	short @@loop
	pop	si
	pop	bp
	retn
cdg_free_all	endp

; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Win animation: graphics/sound/clock are foreign interfaces. Near return.
sub_978D	proc near
		push	bp
		mov	bp, sp
		push	si
		graph_accesspage 1
		call	graph_clear
		graph_accesspage 0
		call	graph_clear
		graph_showpage 0
		mov	PaletteTone, 0
		call	far ptr	palette_show
		call	graph_show
		call	cdg_put_noalpha_8 pascal, large (352 shl 16) or 300, 0
		kajacall	KAJA_SONG_PLAY
		push	2
		call	palette_black_in
		call	snd_delay_until_measure pascal, (6 shl 16) or 16
		mov	si, 1
		jmp	short loc_97FC
; ---------------------------------------------------------------------------

loc_97E8:
		call	cdg_put_noalpha_8 pascal, large (352 shl 16) or 300, si
		call	@frame_delay$qi pascal, 6
		inc	si

loc_97FC:
		cmp	si, 5
		jl	short loc_97E8
		call	snd_delay_until_measure pascal, (10 shl 16) or 64
		mov	PaletteTone, 200
		call	far ptr	palette_show
		call	cdg_put_noalpha_8 pascal, large (224 shl 16) or 64, 6
		call	cdg_put_noalpha_8 pascal, large (352 shl 16) or 300, 5
		push	ds
		push	offset aLogo1_rgb ; "logo1.rgb"
		call	palette_entry_rgb
		call	far ptr	palette_show
		call	cdg_free_all
		call	snd_delay_until_measure pascal, (11 shl 16) or 4
		push	1
		call	palette_white_in
		call	@frame_delay$qi pascal, 8
		call	@win_text_put$qv
		call	sub_9887
		or	ax, ax
		jnz	short loc_9868
		call	sub_990C

loc_9868:
		call	@input_mode_interface$qv
		cmp	_input_sp, INPUT_NONE
		jnz	short loc_987D
		call	@frame_delay$qi pascal, 1
		jmp	short loc_9868
; ---------------------------------------------------------------------------

loc_987D:
		push	1
		call	palette_black_out
		pop	si
		pop	bp
		retn
sub_978D	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Story dispatch: read unchecked story_opponents[stage] before stage tests.
; Do not add a bounds check or change signed optional-character truncation.
sub_9887	proc near

var_2		= word ptr -2

		enter	2, 0
		les	bx, _resident
		cmp	es:[bx+resident_t.game_mode], GM_STORY
		jnz	short loc_98A1
		les	bx, _resident
		cmp	es:[bx+resident_t.pid_winner], 0
		jz	short loc_98A6

loc_98A1:
		mov	ax, 1
		leave
		retn
; ---------------------------------------------------------------------------

loc_98A6:
		les	bx, _resident
		mov	al, es:[bx+resident_t.story_stage]
		mov	ah, 0
		add	bx, ax
		mov	al, es:[bx+resident_t.story_opponents]
		mov	bx, word ptr _resident
		mov	es:[bx+resident_t.RESIDENT_playchar_paletted][1], al
		cmp	es:[bx+resident_t.story_stage], 7
		jnz	short loc_98CA
		mov	ax, 3
		leave
		retn
; ---------------------------------------------------------------------------

loc_98CA:
		les	bx, _resident
		cmp	es:[bx+resident_t.story_stage], 8
		jnz	short loc_98DA
		mov	ax, 4
		leave
		retn
; ---------------------------------------------------------------------------

loc_98DA:
		les	bx, _resident
		cmp	es:[bx+resident_t.story_stage], 9
		jnz	short loc_98EA
		mov	ax, 5
		leave
		retn
; ---------------------------------------------------------------------------

loc_98EA:
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_2], ax
		cmp	[bp+var_2], 7
		jl	short loc_9908
		mov	es:[bx+resident_t.RESIDENT_playchar_paletted][1], (1 + (PLAYCHAR_REIMU * 2))

loc_9908:
		xor	ax, ax
		leave
		retn
sub_9887	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Next-stage load: mutate the shared stnx filename cumulatively.
sub_990C	proc near

var_1		= byte ptr -1

		enter	2, 0
		graph_showpage 0
		graph_accesspage 1
		mov	al, _playchar[0]
		mov	[bp+var_1], al
		push	0
		push	ds
		mov	ah, 0
		cwd
		sub	ax, dx
		mov	bx, ax
		sar	bx, 1
		add	bx, bx
		push	_PIC_FN[bx]
		mov	al, [bp+var_1]
		mov	ah, 0
		and	ax, 1
		push	ax
		call	cdg_load_single
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		add	al, -1
		mov	[bp+var_1], al
		push	1
		push	ds
		mov	ah, 0
		cwd
		sub	ax, dx
		mov	bx, ax
		sar	bx, 1
		add	bx, bx
		push	_PIC_FN[bx]
		mov	al, [bp+var_1]
		mov	ah, 0
		and	ax, 1
		push	ax
		call	cdg_load_single
		mov	al, [bp+var_1]
		mov	ah, 0
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_1], al
		mov	_do_not_show_stage_number, 1
		les	bx, _resident
		cmp	es:[bx+resident_t.game_mode], GM_STORY
		jz	short loc_9997
		mov	bx, word_E504
		mov	al, [bx+4]
		add	al, 4
		jmp	short loc_99CB
; ---------------------------------------------------------------------------

loc_9997:
		cmp	[bp+var_1], 7
		jnz	short loc_99A8
		mov	bx, word_E504
		mov	al, [bx+4]
		add	al, 2
		jmp	short loc_99CB
; ---------------------------------------------------------------------------

loc_99A8:
		cmp	[bp+var_1], 8
		jnz	short loc_99B7
		mov	bx, word_E504
		inc	byte ptr [bx+4]
		jmp	short loc_99F1
; ---------------------------------------------------------------------------

loc_99B7:
		les	bx, _resident
		cmp	es:[bx+resident_t.story_stage], 6
		jnz	short loc_99D4
		mov	bx, word_E504
		mov	al, [bx+4]
		add	al, 3

loc_99CB:
		mov	bx, word_E504
		mov	[bx+4],	al
		jmp	short loc_99F1
; ---------------------------------------------------------------------------

loc_99D4:
		push	2
		push	ds
		push	word_E502
		les	bx, _resident
		mov	al, es:[bx+resident_t.story_stage]
		mov	ah, 0
		inc	ax
		push	ax
		call	cdg_load_single
		mov	_do_not_show_stage_number, 0

loc_99F1:
		call	@pi_load$qinxc pascal, 0, ds, offset aStnx0_pi
		call	@pi_put_8$qiii pascal, large 0, 0
		freePISlotLarge	0
		call	@pi_load$qinxc pascal, 0, ds, word_E504
		call	@pi_put_8$qiii pascal, large 0, 0
		leave
		retn
sub_990C	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Next-stage present: symbolic enemy jump table; mutable BGM filename.
; The clock gate busy-polls at <=32 even if input is already held.
sub_9A2C	proc near

var_4		= word ptr -4
@@dec_bgm_fn	= word ptr -2

		enter	4, 0
		push	si
		mov	si, offset _PLAYCHAR_BGM_FN
		mov	[bp+@@dec_bgm_fn], offset aDec_m
		mov	PaletteTone, 0
		call	far ptr	palette_show
		call	@pi_palette_apply$qi pascal, 0
		call	graph_copy_page pascal, 0
		freePISlotLarge	0
		call	cdg_put_8 pascal, large (96 shl 16) or 96, 0
		call	cdg_put_hflip_8 pascal, large (352 shl 16) or 96, 1
		cmp	_do_not_show_stage_number, 0
		jnz	short loc_9A8E
		call	cdg_put_8 pascal, large (384 shl 16) or 46, 2

loc_9A8E:
		call	cdg_free pascal, 0
		call	cdg_free pascal, 1
		call	cdg_free pascal, 2
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][0]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		add	ax, ax
		mov	[bp+var_4], ax
		push	(80 shl 16) or 292
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, [bp+var_4]
		shl	bx, 2
		pushd	CHAR_TITLE[bx]
		call	@graph_putsa_fx$qiiinxuc
		push	(128 shl 16) or 308
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, [bp+var_4]
		shl	bx, 2
		pushd	CHAR_NAME[bx]
		call	@graph_putsa_fx$qiiinxuc
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		add	ax, ax
		mov	[bp+var_4], ax
		push	(336 shl 16) or 292
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, [bp+var_4]
		shl	bx, 2
		pushd	CHAR_TITLE[bx]
		call	@graph_putsa_fx$qiiinxuc
		push	(384 shl 16) or 308
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, [bp+var_4]
		shl	bx, 2
		pushd	CHAR_NAME[bx]
		call	@graph_putsa_fx$qiiinxuc
		push	1
		call	palette_black_in
		mov	vsync_Count1, 0
		graph_accesspage 1
		call	graph_clear
		push	0
		call	sub_9D20
		push	1
		call	sub_9D20
		call	@pi_load$qinxc pascal, 0, ds, offset aEn2_pi
		call	@pi_put_interlace_8$qiii pascal, large 280, 0
		freePISlotLarge	0
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_4], ax
		mov	bx, [bp+var_4]
		cmp	bx, 8
		ja	short loc_9BC2
		add	bx, bx
		jmp	cs:off_9C9F[bx]

loc_9B97:
		push	0
		push	ds
		push	offset aEnemy00_pi ; "ENEMY00.pi"
		jmp	short loc_9BBD
; ---------------------------------------------------------------------------

loc_9B9F:
		push	0
		push	ds
		push	offset aEnemy01_pi ; "ENEMY01.pi"
		jmp	short loc_9BBD
; ---------------------------------------------------------------------------

loc_9BA7:
		push	0
		push	ds
		push	offset aEnemy02_pi ; "ENEMY02.pi"
		jmp	short loc_9BBD
; ---------------------------------------------------------------------------

loc_9BAF:
		push	0
		push	ds
		push	offset aEnemy03_pi ; "ENEMY03.pi"
		jmp	short loc_9BBD
; ---------------------------------------------------------------------------

loc_9BB7:
		push	0
		push	ds
		push	offset aEnemy04_pi ; "ENEMY04.pi"

loc_9BBD:
		call	@pi_load$qinxc

loc_9BC2:
		call	@pi_put_interlace_8$qiii pascal, large 304, 0
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_4], ax
		cmp	[bp+var_4], 0Ah
		jl	short loc_9BFB
		mov	bx, 10
		cwd
		idiv	bx
		add	al, [si]
		mov	[si], al
		mov	ax, [bp+var_4]
		cwd
		idiv	bx
		mov	[bp+var_4], dx

loc_9BFB:
		mov	al, [si+1]
		add	al, byte ptr [bp+var_4]
		mov	[si+1],	al
		kajacall	KAJA_SONG_STOP
		les	bx, _resident
		cmp	es:[bx+resident_t.story_stage], 6
		jz	short loc_9C1E
		push	SND_LOAD_SONG
		push	ds
		push	si
		jmp	short loc_9C25
; ---------------------------------------------------------------------------

loc_9C1E:
		push	SND_LOAD_SONG
		push	ds
		push	[bp+@@dec_bgm_fn]

loc_9C25:
		call	_snd_load
		add	sp, 6
		call	_snd_load c, offset aYume_efc, ds, SND_LOAD_SE
		mov	_input_sp, INPUT_NONE

loc_9C42:
		cmp	vsync_Count1, 20h ; ' '
		jbe	short loc_9C42
		jmp	short loc_9C50
; ---------------------------------------------------------------------------

loc_9C4B:
		call	@input_mode_interface$qv

loc_9C50:
		cmp	vsync_Count1, 60h
		ja	short loc_9C5E
		cmp	_input_sp, INPUT_NONE
		jz	short loc_9C4B

loc_9C5E:
		push	1
		call	palette_white_out
		graph_accesspage 0
		call	graph_clear
		push	1
		call	palette_white_in
		call	text_fillca pascal, (' ' shl 16) + TX_BLACK + TX_REVERSE
		call	@pi_palette_apply$qi pascal, 0
		freePISlotLarge	0
		call	respal_set_palettes
		pop	si
		leave
		retn
sub_9A2C	endp

; ---------------------------------------------------------------------------
off_9C9F	dw offset loc_9B97
		dw offset loc_9B97
		dw offset loc_9B9F
		dw offset loc_9BA7
		dw offset loc_9B9F
		dw offset loc_9BA7
		dw offset loc_9B97
		dw offset loc_9BAF
		dw offset loc_9BB7

; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Shot pair: near Pascal RET 6; caller filename is writable FAR storage.
; The second PI load observes in-place bytes 2/3 changed to ex.
sub_9CB1	proc near

arg_0		= dword	ptr  4
arg_4		= word ptr  8

		push	bp
		mov	bp, sp
		push	si
		mov	si, [bp+arg_4]
		call	@pi_load$qinxc pascal, 0, large [bp+arg_0]
		mov	ax, si
		imul	ax, 320
		call	@pi_put_interlace_8$qiii pascal, ax, (200 shl 16)
		freePISlotLarge	0
		les	bx, [bp+arg_0]
		mov	byte ptr es:[bx+2], 'e'
		mov	byte ptr es:[bx+3], 'x'
		call	@pi_load$qinxc pascal, 0, word ptr [bp+arg_0+2], bx
		mov	ax, si
		imul	ax, 320
		call	@pi_put_interlace_8$qiii pascal, ax, (208 shl 16)
		freePISlotLarge	0
		pop	si
		pop	bp
		retn	6
sub_9CB1	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Shot load: copy all SHOT_FN_SIZE template bytes onto SS stack; RET 2.
sub_9D20	proc near

@@fn	= byte ptr -(2 + SHOT_FN_SIZE)
var_2		= word ptr -2
arg_0		= word ptr  4

		enter	(2 + SHOT_FN_SIZE), 0
		push	si
		push	di
		mov	di, [bp+arg_0]
		xor	si, si
		jmp	short loc_9D35
; ---------------------------------------------------------------------------

loc_9D2D:
		mov	al, _SHOT_FN[si]
		mov	[bp+si+@@fn], al
		inc	si

loc_9D35:
		cmp	si, SHOT_FN_SIZE
		jl	short loc_9D2D
		les	bx, _resident
		add	bx, di
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted]
		mov	ah, 0
		dec	ax
		mov	[bp+var_2], ax
		cmp	[bp+var_2], 10
		jl	short loc_9D65
		mov	bx, 10
		cwd
		idiv	bx
		add	al, [bp+@@fn]
		mov	[bp+@@fn], al
		mov	ax, [bp+var_2]
		cwd
		idiv	bx
		mov	[bp+var_2], dx

loc_9D65:
		mov	al, [bp+@@fn + 1]
		add	al, byte ptr [bp+var_2]
		mov	[bp+@@fn + 1], al
		push	di
		push	ss
		lea	ax, [bp+@@fn]
		push	ax
		call	sub_9CB1
		pop	di
		pop	si
		leave
		retn	2
sub_9D20	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; int __cdecl main(int argc, const char	**argv,	const char **envp)
public _main
; Main is FAR cdecl: RETF preserves caller arguments; exec failures fall through.
_main		proc far

var_2		= byte ptr -2
var_1		= byte ptr -1
_argc		= word ptr  6
_argv		= dword	ptr  8
_envp		= dword	ptr  0Ch

		enter	2, 0
		call	@cfg_load_resident_ptr$qv
		or	ax, ax
		jz	@@ret
		call	@game_init_main$qnxuc pascal, ds, offset aCOul
		call	respal_exist
		mov	_snd_midi_active, 0
		les	bx, _resident
		cmp	es:[bx+resident_t.bgm_mode], SND_BGM_OFF
		jz	short loc_9DAD
		call	_snd_determine_mode

loc_9DAD:
		call	gaiji_backup
		push	ds
		push	offset aMikoft_bft ; "MIKOFT.bft"
		call	gaiji_entry_bfnt
		call	_snd_load c, offset aYume_efc, ds, SND_LOAD_SE
		call	_snd_se_reset
		call	_hflip_lut_generate
		les	bx, _resident
		cmp	es:[bx+resident_t.show_score_menu], 0
		jz	short loc_9E04
		call	@regist_menu$qv
		call	text_clear
		call	gaiji_restore
		call	@game_exit$qv
		pushd	0
		push	ds
		push	offset path	; "op"
		push	ds
		push	offset path	; "op"
		call	_execl
		add	sp, 0Ch

loc_9E04:
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][0]
		add	al, -1
		mov	_playchar[0], al
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][1]
		add	al, -1
		mov	_playchar[1], al
		cmp	es:[bx+resident_t.story_stage], 0
		jz	loc_9F85
		cmp	es:[bx+resident_t.game_mode], GM_STORY
		jnz	short loc_9E3F
		call	sub_9887
		mov	[bp+var_1], al
		cmp	[bp+var_1], 4
		jz	short loc_9E89
		cmp	[bp+var_1], 5
		jnz	short loc_9E3F
		call	sub_B972

loc_9E3F:
		call	_snd_load c,  offset aWin_m, ds, SND_LOAD_SONG
		call	@win_load$qv
		call	sub_978D
		kajacall	KAJA_SONG_STOP
		les	bx, _resident
		cmp	es:[bx+resident_t.game_mode], GM_STORY
		jnz	loc_9F58
		call	sub_9887
		mov	[bp+var_1], al
		cmp	[bp+var_1], 0
		jnz	short loc_9E7B

loc_9E75:
		call	sub_9A2C
		jmp	loc_9F1E
; ---------------------------------------------------------------------------

loc_9E7B:
		cmp	[bp+var_1], 3
		jz	short loc_9E89
		cmp	[bp+var_1], 4
		jnz	loc_9F38

loc_9E89:
		call	cdg_free_all
		freePISlotLarge	0
		mov	al, _playchar[0]
		mov	ah, 0
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_2], al
		cmp	[bp+var_2], 10
		jb	short loc_9EDC
		les	bx, off_E4B6
		mov	al, es:[bx+1]
		mov	dl, [bp+var_2]
		mov	dh, 0
		mov	bx, 10
		push	ax
		mov	ax, dx
		cwd
		idiv	bx
		pop	dx
		add	dl, al
		mov	bx, word ptr off_E4B6
		mov	es:[bx+1], dl
		mov	al, [bp+var_2]
		mov	ah, 0
		mov	bx, 10
		cwd
		idiv	bx
		mov	[bp+var_2], dl

loc_9EDC:
		les	bx, off_E4B6
		mov	al, [bp+var_2]
		add	es:[bx+2], al
		cmp	[bp+var_1], 4
		jnz	short loc_9EF1
		inc	byte ptr es:[bx+5]

loc_9EF1:
		graph_accesspage 0
		graph_showpage al
		call	graph_clear
		call	graph_show
		call	@cutscene_script_load$qnxc pascal, [off_E4B6]
		call	@cutscene_animate$qv
		call	@cutscene_script_free$qv
		call	sub_990C
		call	sub_9A2C
		call	gaiji_restore

loc_9F1E:
		call	@game_exit_from_mainl_to_main$qv
		pushd	0
		push	ds
		push	offset aMain	; "main"
		push	ds
		push	offset aMain	; "main"

loc_9F2E:
		call	_execl
		add	sp, 0Ch
		leave
		retf
; ---------------------------------------------------------------------------

loc_9F38:
		call	cdg_free_all
		freePISlotLarge	0
		call	@regist_menu$qv
		call	sub_9F8D
		or	ax, ax
		jnz	short loc_9F85
		call	sub_B92E
		jmp	short loc_9F69
; ---------------------------------------------------------------------------

loc_9F58:
		call	cdg_free_all
		freePISlotLarge	0

loc_9F69:
		call	text_clear
		call	gaiji_restore
		call	@game_exit$qv
		pushd	0
		push	ds
		push	offset path	; "op"
		push	ds
		push	offset path	; "op"
		jmp	short loc_9F2E
; ---------------------------------------------------------------------------

loc_9F85:
		call	sub_990C
		jmp	loc_9E75
; ---------------------------------------------------------------------------

@@ret:
		leave
		retf
_main		endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

; Continue: clear scores even with zero credit; OK precedes CANCEL.
; All nonzero-credit terminal paths decrement stage (byte 0 wraps to 255).
sub_9F8D	proc near

var_6		= dword	ptr -6
var_2		= word ptr -2

		enter	6, 0
		push	si
		push	di
		mov	si, 1
		mov	[bp+var_2], 0
		mov	word ptr [bp+var_6+2], ds
		mov	word ptr [bp+var_6], offset a0
		xor	di, di
		jmp	short loc_9FB3
; ---------------------------------------------------------------------------

loc_9FA7:
		les	bx, _resident
		add	bx, di
		mov	es:[bx+resident_t.score_last], 0
		inc	di

loc_9FB3:
		cmp	di, (PLAYER_COUNT * SCORE_DIGITS)
		jl	short loc_9FA7
		les	bx, _resident
		cmp	es:[bx+resident_t.rem_credits], 0
		jnz	short loc_9FC8
		xor	ax, ax
		jmp	loc_A12A
; ---------------------------------------------------------------------------

loc_9FC8:
		call	cdg_put_noalpha_8 pascal, large (192 shl 16) or 272, 0
		call	cdg_put_noalpha_8 pascal, large (352 shl 16) or 272, 3
		les	bx, _resident
		mov	al, es:[bx+resident_t.rem_credits]
		les	bx, [bp+var_6]
		add	al, es:[bx]
		mov	es:[bx], al
		call	@graph_putsa_fx$qiiinxuc pascal, (576 shl 16) or 371, 2Fh, word ptr [bp+var_6+2], bx
		push	1
		call	palette_black_in

loc_A00B:
		call	@input_mode_interface$qv
		test	_input_sp.lo, low INPUT_LEFT
		jnz	short loc_A01E
		test	_input_sp.lo, low INPUT_RIGHT
		jz	short loc_A056

loc_A01E:
		cmp	[bp+var_2], 0
		jnz	short loc_A05B
		mov	ax, 1
		sub	ax, si
		mov	si, ax
		push	(192 shl 16) or 272
		add	ax, ax
		mov	dx, 2
		sub	dx, ax
		push	dx
		call	cdg_put_noalpha_8
		push	(352 shl 16) or 272
		mov	ax, si
		add	ax, ax
		inc	ax
		push	ax
		call	cdg_put_noalpha_8
		mov	[bp+var_2], 1
		jmp	short loc_A05B
; ---------------------------------------------------------------------------

loc_A056:
		mov	[bp+var_2], 0

loc_A05B:
		test	_input_sp.hi, high INPUT_OK
		jnz	short loc_A069
		test	_input_sp.lo, low INPUT_SHOT
		jz	short loc_A0B0

loc_A069:
		cmp	si, 1
		jnz	short loc_A0C5
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_boxfill pascal, (576 shl 16) or 371, (592 shl 16) or 387
		call	grcg_off
		les	bx, _resident
		dec	es:[bx+resident_t.rem_credits]
		les	bx, [bp+var_6]
		dec	byte ptr es:[bx]
		call	@graph_putsa_fx$qiiinxuc pascal, (576 shl 16) or 371, 2Fh, word ptr [bp+var_6+2], bx
		jmp	short loc_A0C5
; ---------------------------------------------------------------------------

loc_A0B0:
		test	_input_sp.hi, high INPUT_CANCEL
		jz	short loc_A0BB
		xor	si, si
		jmp	short loc_A0C5
; ---------------------------------------------------------------------------

loc_A0BB:
		call	@frame_delay$qi pascal, 1
		jmp	loc_A00B
; ---------------------------------------------------------------------------

loc_A0C5:
		kajacall	KAJA_SONG_FADE, 3
		push	1
		call	palette_black_out
		graph_accesspage 0
		graph_showpage al
		mov	PaletteTone, 0
		call	far ptr	palette_show
		call	@pi_load$qinxc pascal, 0, ds, offset aOver_pi
		call	@pi_palette_apply$qi pascal, 0
		call	@pi_put_8$qiii pascal, large 0, 0
		freePISlotLarge	0
		kajacall	KAJA_SONG_STOP
		les	bx, _resident
		dec	es:[bx+resident_t.story_stage]
		mov	es:[bx+resident_t.story_lives], CREDIT_LIVES
		mov	ax, si

loc_A12A:
		pop	di
		pop	si
		leave
		retn
sub_9F8D	endp
