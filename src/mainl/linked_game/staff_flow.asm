; Maintained TH03 MAINL early STAFF_TEXT music and ending flow.
; Original near interfaces, FAR script pointer, signed division and unchecked execl
; return path are retained. The flake procdesc is contextual, not an extra body.


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_B92E	proc near
		push	bp
		mov	bp, sp
		kajacall	KAJA_SONG_STOP
		call	_snd_load c, offset aOver_m, ds, SND_LOAD_SONG
		kajacall	KAJA_SONG_PLAY
		push	1
		call	palette_black_in
		call	snd_delay_until_measure pascal, (3 shl 16) or 64
		push	1
		call	palette_black_out
		kajacall	KAJA_SONG_STOP
		pop	bp
		retn
sub_B92E	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

sub_B972	proc near

var_1		= byte ptr -1

		enter	2, 0
		call	cdg_free pascal, 0
		call	cdg_free pascal, 1
		call	cdg_free pascal, 2
		freePISlotLarge	0
		les	bx, _resident
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][0]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	[bp+var_1], al
		cmp	[bp+var_1], 10
		jl	short loc_B9DD
		les	bx, off_EE4E
		mov	al, es:[bx+1]
		push	ax
		mov	al, [bp+var_1]
		cbw
		mov	bx, 10
		cwd
		idiv	bx
		pop	dx
		add	dl, al
		mov	bx, word ptr off_EE4E
		mov	es:[bx+1], dl
		mov	al, [bp+var_1]
		cbw
		mov	bx, 10
		cwd
		idiv	bx
		mov	[bp+var_1], dl

loc_B9DD:
		les	bx, off_EE4E
		mov	al, [bp+var_1]
		add	es:[bx+2], al
		mov	PaletteTone, 0
		call	far ptr	palette_show
		call	@frame_delay$qi pascal, 96
		graph_accesspage 0
		graph_showpage al
		call	graph_clear
		call	graph_show
		push	dword ptr [off_EE4E]
		call	@cutscene_script_load$qnxc
		call	@cutscene_animate$qv
		call	@cutscene_script_free$qv
		call	sub_C40D
		les	bx, _resident
		mov	es:[bx+resident_t.story_stage], STAGE_ALL
		call	@regist_menu$qv
		les	bx, _resident
		cmp	es:[bx+resident_t.rem_credits], 3
		jnz	short loc_BA66
		cmp	es:[bx+resident_t.RESIDENT_playchar_paletted], (1 + (PLAYCHAR_CHIYURI * 2))
		jnb	short loc_BA66
		graph_accesspage 1
		call	graph_clear
		graph_accesspage 0
		call	graph_clear
		graph_showpage 0
		push	ds
		push	offset a@99ed_txt ; "@99ED.TXT"
		call	@cutscene_script_load$qnxc
		call	@cutscene_animate$qv
		call	@cutscene_script_free$qv

loc_BA66:
		call	text_clear
		call	gaiji_restore
		call	@game_exit$qv
		pushd	0
		push	ds
		push	offset aOp_0	; "op"
		push	ds
		push	offset aOp_0	; "op"
		call	_execl
		add	sp, 0Ch
		leave
		retn
sub_B972	endp

	@FLAKE_PUT$QIII procdesc pascal near \
		left:word, top:word, cel:word