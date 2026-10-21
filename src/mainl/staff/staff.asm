; Maintained MAINL transitions, verdict and staff orchestration: eight complete
; near procedures, 2541 CODE bytes. Included inside MAINL_STAFF_TEXT with root
; declarations/macros in scope. External assets, tables and storage remain contextual.
; Symbol names remain stable; these are symbolic instructions, not encoded byte arrays.
; See docs/reconstruction/MAINL_TRANSITIONS_REVIEW.md for behavior and model limits.
; Entrance frame: near RET 2; duration/8 divisor is unguarded, center clamp and alpha ordering retained.
sub_BDF4	proc near

arg_0		= word ptr  4

		push	bp
		mov	bp, sp
		push	si
		push	di
		mov	di, [bp+arg_0]
		call	_mainl_clear_blue
		mov	ax, word_10BB2
		cmp	ax, word_10BBE
		jg	loc_BEC1
		push	(RES_X / 2)
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		push	_stf_center_y_on_page[bx]
		push	di
		call	cdg_unput_for_upwards_motion_e_8
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	ax, _stf_center_y_on_page[bx]
		cmp	ax, word_10BC0
		jle	short loc_BE66
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	dx, word_10BBC
		mov	bx, ax
		sub	_stf_center_y_on_page[bx], dx
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	ax, _stf_center_y_on_page[bx]
		cmp	ax, word_10BC0
		jge	short loc_BE66
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	dx, word_10BC0
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], dx

loc_BE66:
		mov	ax, word_10BBE
		mov	bx, 8
		cwd
		idiv	bx
		push	ax
		mov	ax, word_10BB2
		cwd
		pop	bx
		idiv	bx
		mov	dx, 7
		sub	dx, ax
		mov	si, dx
		or	si, si
		jge	short loc_BE84
		xor	si, si

loc_BE84:
		cmp	byte_10BB5, 0
		jz	short loc_BEA7
		cmp	byte_10BC6, 0
		jz	short loc_BEA7
		push	(504 shl 16) or 200
		mov	al, byte_10BC6
		mov	ah, 0
		push	ax
		push	si
		call	cdg_put_dissolve_e_8
		mov	byte_10BC7, 1

loc_BEA7:
		push	(RES_X / 2)
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		push	_stf_center_y_on_page[bx]
		push	di
		push	si
		call	cdg_put_dissolve_e_8
		mov	byte_10BC7, 0

loc_BEC1:
		pop	di
		pop	si
		pop	bp
		retn	2
sub_BDF4	endp

; Exit frame: near RET 2; upward motion until frame 160; clear interior at 160 and 161.
sub_BEC7	proc near

arg_0		= word ptr  4

		push	bp
		mov	bp, sp
		push	si
		push	di
		mov	di, [bp+arg_0]
		call	_mainl_clear_blue
		cmp	word_10BB2, 0A1h
		jg	loc_BF78
		cmp	word_10BB2, 0A0h
		jge	short loc_BF57
		push	(RES_X / 2)
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		push	_stf_center_y_on_page[bx]
		push	di
		call	cdg_unput_for_upwards_motion_e_8
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		dec	_stf_center_y_on_page[bx]
		mov	ax, word_10BB2
		mov	bx, 20
		cwd
		idiv	bx
		mov	si, ax
		cmp	si, 7
		jle	short loc_BF18
		mov	si, 7

loc_BF18:
		cmp	byte_10BB5, 0
		jz	short loc_BF3B
		cmp	byte_10BC6, 0
		jz	short loc_BF3B
		push	(504 shl 16) or 200
		mov	al, byte_10BC6
		mov	ah, 0
		push	ax
		push	si
		call	cdg_put_dissolve_e_8
		mov	byte_10BC7, 1

loc_BF3B:
		push	(RES_X / 2)
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		push	_stf_center_y_on_page[bx]
		push	di
		push	si
		call	cdg_put_dissolve_e_8
		mov	byte_10BC7, 0
		jmp	short loc_BF78

loc_BF57:
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off

loc_BF78:
		pop	di
		pop	si
		pop	bp
		retn	2
sub_BEC7	endp

; Gallery frame: near RET 6; draw through frame 160; strength max(0, 7-frame/20).
sub_BF7E	proc near

@@slot    	= word ptr  4
@@y_center	= word ptr  6
@@x_center	= word ptr  8

		push	bp
		mov	bp, sp
		push	si
		cmp	word_10BB2, 0A0h
		jg	short loc_BFAD
		mov	ax, word_10BB2
		mov	bx, 20
		cwd
		idiv	bx
		mov	dx, 7
		sub	dx, ax
		mov	si, dx
		or	si, si
		jge	short loc_BFA0
		xor	si, si

loc_BFA0:
		call	cdg_put_dissolve_e_8 pascal, [bp+@@x_center], [bp+@@y_center], [bp+@@slot], si

loc_BFAD:
		pop	si
		pop	bp
		retn	6
sub_BF7E	endp

; Single transition: near RET 6; two gated phases followed by two cleanup snow frames.
sub_BFB2	proc near

arg_0		= word ptr  4
arg_2		= word ptr  6
arg_4		= word ptr  8

		push	bp
		mov	bp, sp
		push	si
		mov	si, [bp+arg_4]
		cmp	word_10BBC, 2
		jnz	short loc_BFE3
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 264
		mov	al, _page_back
		mov	ah, 0
		xor	ax, 1
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 263
		jmp	short loc_C00E

loc_BFE3:
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	dx, 280
		sub	dx, word_10BC4
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], dx
		mov	al, _page_back
		mov	ah, 0
		xor	ax, 1
		add	ax, ax
		mov	dx, 280
		sub	dx, word_10BC4
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], dx

loc_C00E:
		mov	word_10BB2, 0

loc_C014:
		push	si
		call	sub_BDF4
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_2]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C014
		mov	word_10BB2, 0

loc_C032:
		push	si
		call	sub_BEC7
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_0]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C032
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off
		call	sub_BCD5
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off
		call	sub_BCD5
		pop	si
		pop	bp
		retn	6
sub_BFB2	endp

; Paired transition: near RET 6; preserve secondary slot/alpha selection independently.
sub_C097	proc near

arg_0		= word ptr  4
arg_2		= word ptr  6
arg_4		= word ptr  8

		push	bp
		mov	bp, sp
		push	si
		push	di
		mov	si, [bp+arg_4]
		cmp	word_10BBC, 2
		jnz	short loc_C0C9
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 264
		mov	al, _page_back
		mov	ah, 0
		xor	ax, 1
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 263
		jmp	short loc_C0D6

loc_C0C9:
		mov	ax, 280
		sub	ax, word_10BC4
		mov	_stf_center_y_on_page[0 * word], ax
		mov	_stf_center_y_on_page[1 * word], ax

loc_C0D6:
		mov	word_10BB2, 0

loc_C0DC:
		push	si
		call	sub_BDF4
		mov	byte_10BC7, 1
		push	320
		push	word_10BC2
		lea	ax, [si-1]
		push	ax
		push	0
		call	cdg_put_dissolve_e_8
		mov	byte_10BC7, 0
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_2]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C0DC
		mov	word_10BB2, 0

loc_C114:
		cmp	word_10BB2, 0A1h
		jg	short loc_C12A
		push	320
		push	word_10BC2
		lea	ax, [si-1]
		push	ax
		call	cdg_unput_for_upwards_motion_e_8

loc_C12A:
		push	si
		call	sub_BEC7
		cmp	word_10BB2, 0A1h
		jg	short loc_C199
		mov	ax, word_10BB2
		dec	ax
		mov	bx, 20
		cwd
		idiv	bx
		mov	di, ax
		cmp	di, 7
		jle	short loc_C14A
		mov	di, 7

loc_C14A:
		cmp	_page_back, 0
		jnz	short loc_C155
		dec	word_10BC2

loc_C155:
		mov	byte_10BC7, 1
		cmp	word_10BB2, 0A0h
		jge	short loc_C173
		push	320
		push	word_10BC2
		lea	ax, [si-1]
		push	ax
		push	di
		call	cdg_put_dissolve_e_8
		jmp	short loc_C194

loc_C173:
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off

loc_C194:
		mov	byte_10BC7, 0

loc_C199:
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_0]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	loc_C114
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off
		call	sub_BCD5
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off
		call	sub_BCD5
		pop	di
		pop	si
		pop	bp
		retn	6
sub_C097	endp

; Entrance/hold: near RET 6; copy active-page center to other page; no cleanup snow pair.
sub_C1FD	proc near

arg_0		= word ptr  4
arg_2		= word ptr  6
arg_4		= word ptr  8

		push	bp
		mov	bp, sp
		cmp	word_10BBC, 2
		jnz	short loc_C22A
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 264
		mov	al, _page_back
		mov	ah, 0
		xor	ax, 1
		add	ax, ax
		mov	bx, ax
		mov	_stf_center_y_on_page[bx], 263
		jmp	short loc_C237

loc_C22A:
		mov	ax, 280
		sub	ax, word_10BC4
		mov	_stf_center_y_on_page[0 * word], ax
		mov	_stf_center_y_on_page[1 * word], ax

loc_C237:
		mov	word_10BB2, 0

loc_C23D:
		push	[bp+arg_4]
		call	sub_BDF4
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_2]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C23D
		mov	word_10BB2, 0

loc_C25D:
		call	_mainl_clear_blue
		call	sub_BCD5
		inc	word_10BB2
		push	[bp+arg_0]
		push	100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C25D
		mov	al, _page_back
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	ax, _stf_center_y_on_page[bx]
		mov	word_10BC2, ax
		pop	bp
		retn	6
sub_C1FD	endp

; Verdict: score leading-zero suppression includes continue digit; preserve skill digit centering.
sub_C288	proc near

var_4		= word ptr -4
@@digits	= word ptr -2

		enter	4, 0
		push	si
		push	di
		push	(352 shl 16) or 174
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	al, playchar_10BD7
		mov	ah, 0
		shl	ax, 2
		mov	bx, ax
		pushd	aVERDICT_PLAYCHARS[bx]
		call	@graph_putsa_fx$qiiinxuc
		push	(360 shl 16) or 199
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	al, _rank
		mov	ah, 0
		shl	ax, 2
		mov	bx, ax
		pushd	aVERDICT_RANKS[bx]
		call	@graph_putsa_fx$qiiinxuc
		mov	si, 408
		mov	[bp+var_4], 0
		mov	[bp+@@digits], SCORE_DIGITS
		jmp	short loc_C319

loc_C2D5:
		mov	bx, [bp+@@digits]
		mov	al, _score[bx]
		mov	ah, 0
		mov	di, ax
		cmp	[bp+var_4], 0
		jnz	short loc_C2F7
		or	di, di
		jz	short loc_C2F7
		mov	ax, [bp+@@digits]
		shl	ax, 3
		sub	si, ax
		mov	[bp+var_4], 1

loc_C2F7:
		cmp	[bp+var_4], 0
		jz	short loc_C316
		push	si
		push	(224 shl 16) or (V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		add	si, 16

loc_C316:
		dec	[bp+@@digits]

loc_C319:
		cmp	[bp+@@digits], 0
		jg	short loc_C2D5
		mov	al, continues_used
		mov	ah, 0
		mov	di, ax
		push	si
		push	(224 shl 16) or (V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		push	(408 shl 16) or 248
		push	(V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		mov	al, _skill
		mov	ah, 0
		mov	bx, 100
		cwd
		idiv	bx
		mov	di, ax
		mov	si, 408
		mov	[bp+var_4], 0
		or	di, di
		jz	short loc_C38D
		sub	si, 16
		mov	[bp+var_4], 1
		push	si
		push	(291 shl 16) or (V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		add	si, 16

loc_C38D:
		mov	al, _skill
		mov	ah, 0
		mov	bx, 100
		cwd
		idiv	bx
		mov	bx, 10
		mov	ax, dx
		cwd
		idiv	bx
		mov	di, ax
		or	di, di
		jz	short loc_C3B4
		cmp	[bp+var_4], 0
		jnz	short loc_C3B4
		mov	[bp+var_4], 1
		sub	si, 8

loc_C3B4:
		cmp	[bp+var_4], 0
		jz	short loc_C3D3
		push	si
		push	(291 shl 16) or (V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		add	si, 16

loc_C3D3:
		mov	al, _skill
		mov	ah, 0
		mov	bx, 10
		cwd
		idiv	bx
		mov	di, dx
		push	si
		push	(291 shl 16) or (V_WHITE or FX_WEIGHT_BOLD)
		mov	bx, di
		shl	bx, 2
		pushd	aVERDICT_NUMBERS[bx]
		call	@graph_putsa_fx$qiiinxuc
		lea	ax, [si+16]
		call	@graph_putsa_fx$qiiinxuc pascal, ax, (291 shl 16) or (V_WHITE or FX_WEIGHT_BOLD), ds, offset aU_ ; Original generated character annotation omitted.
		pop	di
		pop	si
		leave
		retn
sub_C288	endp

; Staff root: ignored load returns, wrapping skill arithmetic, 12 slots, 9 transitions and gallery; wait/fade/free ordering.
sub_C40D	proc near
		push	bp
		mov	bp, sp
		push	si
		push	di
		kajacall	KAJA_SONG_FADE, 16
		push	4
		call	palette_black_out
		call	_snd_delay_until_volume stdcall, 255
		pop	cx
		kajacall	KAJA_SONG_STOP
		mov	byte_106B0, 50h	; 'P'
		mov	si, 1
		jmp	short loc_C44B

loc_C43C:
		les	bx, _resident
		assume es:nothing
		add	bx, si
		mov	al, es:[bx+resident_t.pid_winner]
		mov	_score[si], al
		inc	si

loc_C44B:
		cmp	si, 9
		jl	short loc_C43C
		les	bx, _resident
		mov	al, 3
		sub	al, es:[bx+resident_t.rem_credits]
		mov	continues_used, al
		mov	al, es:[bx+resident_t.RESIDENT_playchar_paletted][0]
		mov	ah, 0
		dec	ax
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	playchar_10BD7, al
		mov	al, es:[bx+resident_t.rank]
		mov	_rank, al
		mov	al, es:[bx+resident_t.skill]
		mov	_skill, al
		mov	al, _score[7]
		mov	ah, 0
		cmp	ax, 3
		jz	short loc_C48B
		cmp	ax, 4
		jz	short loc_C49E
		jmp	short loc_C4B1

loc_C48B:
		mov	al, _score[6]
		mov	ah, 0
		cwd
		sub	ax, dx
		sar	ax, 1
		add	al, _skill
		add	al, 2
		mov	_skill, al

loc_C49E:
		mov	al, _score[6]
		mov	ah, 0
		cwd
		sub	ax, dx
		sar	ax, 1
		add	al, _skill
		add	al, 7
		mov	_skill, al

loc_C4B1:
		cmp	_score[7], 5
		jb	short loc_C4C0
		mov	al, _skill
		add	al, 15
		mov	_skill, al

loc_C4C0:
		cmp	_score[8], 0
		jz	short loc_C4CC
		mov	_skill, 100

loc_C4CC:
		cmp	_skill, 100
		jbe	short loc_C4D8
		mov	_skill, 100

loc_C4D8:
		call	_snd_load c, offset aEd_m, ds, SND_LOAD_SONG
		mov	PaletteTone, 0
		call	far ptr	palette_show
		push	ds
		push	offset aEdbk1_rgb ; "edbk1.rgb"
		call	palette_entry_rgb
		call	far ptr	palette_show
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 8
		graph_accesspage 1
		call	grcg_byteboxfill_x pascal, large 0, (((RES_X - 1) / 8) shl 16) or (RES_Y - 1)
		graph_accesspage 0
		call	grcg_byteboxfill_x pascal, large 0, (((RES_X - 1) / 8) shl 16) or (RES_Y - 1)
		call	grcg_setcolor pascal, (GC_RMW shl 16) + 0
		graph_accesspage 1
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		graph_accesspage 0
		call	grcg_byteboxfill_x pascal, ((8 / 8) shl 16) or 8, (((RES_X - 1 - 8) / 8) shl 16) or (RES_Y - 1 - 8)
		call	grcg_off
		graph_showpage 1
		call	cdg_load_single_noalpha pascal, 0, ds, offset aStf1_cdg, 0
		call	cdg_load_single_noalpha pascal, 1, ds, offset aStf11_cdg, 0
		call	cdg_load_single pascal, 2, ds, offset aStf3_cdg, 0
		call	cdg_load_single pascal, 3, ds, offset aStf4_cdg, 0
		call	cdg_load_single_noalpha pascal, 4, ds, offset aStf5_cdg, 0
		call	cdg_load_single_noalpha pascal, 5, ds, offset aStf6_cdg, 0
		call	cdg_load_single_noalpha pascal, 6, ds, offset aStf7_cdg, 0
		call	cdg_load_single_noalpha pascal, 7, ds, offset aStf8_cdg, 0
		call	cdg_load_single_noalpha pascal, 8, ds, offset aStf9_cdg, 0
		call	cdg_load_single_noalpha pascal, 9, ds, offset aStf10_cdg, 0
		call	cdg_load_single_noalpha pascal, 10, ds, offset aStf2_cdg, 0
		call	cdg_load_single_noalpha pascal, 11, ds, offset aStf12_cdg, 0
		call	@flakes_reset$qv
		mov	word_10BB2, 0
		les	bx, _resident
		mov	eax, es:[bx+resident_t.rand]
		mov	random_seed, eax
		mov	_page_back, 0
		mov	PaletteTone, 100
		call	far ptr	palette_show
		kajacall	KAJA_SONG_PLAY
		mov	byte_10BB6, 1
		mov	byte_10BB5, 1
		call	@frame_delay$qi pascal, 1
		mov	vsync_Count1, 0

loc_C657:
		call	_mainl_clear_blue
		call	sub_BCD5
		inc	word_10BB2
		push	40100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C657
		mov	byte_10BC7, 0
		mov	word_10BC4, 0
		mov	word_10BC0, 0C8h
		mov	word_10BBC, 2
		mov	word_10BBE, 41h	; 'A'
		mov	byte_10BC6, 0
		pushd	8
		push	0Ah
		call	sub_BFB2
		mov	word_10BBC, 1
		mov	word_10BBE, 0A1h
		mov	byte_10BB6, 0
		push	10010h
		push	14h
		call	sub_BFB2
		mov	word_10BC4, 20h	; ' '
		mov	word_10BC0, 0A8h ; Original generated character annotation omitted.
		push	20016h
		push	18h
		call	sub_C1FD
		mov	byte_10BC6, 7
		mov	word_10BC0, 0D8h
		mov	word_10BC4, 0FFF0h
		push	30020h
		push	22h ; '"'
		call	sub_C097
		mov	byte_10BC6, 0
		mov	word_10BC0, 0C8h
		mov	word_10BC4, 0
		push	40024h
		push	26h ; '&'
		call	sub_BFB2
		push	0B002Ah
		push	2Ch ; ','
		call	sub_BFB2
		push	50030h
		push	32h ; '2'
		call	sub_BFB2
		push	60036h
		push	38h ; '8'
		call	sub_BFB2
		push	0A003Ch
		push	3Eh ; '>'
		call	sub_BFB2
		mov	word_10BB2, 0

loc_C735:
		call	_mainl_clear_blue
		push	1400080h
		push	8
		call	sub_BF7E
		push	0C000F0h
		push	9
		call	sub_BF7E
		call	sub_BCD5
		inc	word_10BB2
		push	420100h
		call	sub_BCA5
		or	ax, ax
		jz	short loc_C735
		mov	al, 1
		sub	al, _page_back
		graph_accesspage al
		call	sub_C288
		graph_accesspage _page_back
		call	sub_C288
		mov	word_10BB2, 0
		xor	di, di

loc_C781:
		call	@input_mode_interface$qv
		call	_mainl_clear_blue
		call	sub_BCD5
		inc	word_10BB2
		or	di, di
		jz	short loc_C7AB
		mov	PaletteTone, di
		call	far ptr	palette_show
		test	byte ptr word_10BB2, 1
		jz	short loc_C781
		dec	di
		or	di, di
		jnz	short loc_C781
		jmp	short loc_C7CD

loc_C7AB:
		cmp	_input_sp, INPUT_NONE
		jz	short loc_C781
		cmp	word_10BB2, 100h
		jle	short loc_C781
		kajacall	KAJA_SONG_FADE, 8
		mov	di, 100
		mov	word_10BB2, 0
		jmp	short loc_C781

loc_C7CD:
		xor	si, si
		jmp	short loc_C7D8

loc_C7D1:
		call	cdg_free pascal, si
		inc	si

loc_C7D8:
		cmp	si, CDG_SLOT_COUNT
		jl	short loc_C7D1
		pop	di
		pop	si
		pop	bp
		retn
sub_C40D	endp
