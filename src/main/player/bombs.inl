; TH03 MAIN character bomb owner (MAIN_05_TEXT:0001..0C29).
; Complete symbolic 16-bit source: seven contiguous procedures, no raw opcode arrays.
; The two Ellen address-derived labels are retained until semantics justify a byte-neutral rename.
; This file is injected into the frozen monolithic carrier by the exact-owner replay.

chiyuri_bomb	proc far

var_2		= byte ptr -2
@@frame		= byte ptr -1

		enter	2, 0
		push	si
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		call	egc_off
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	al, _bomb_frame[bx]
		mov	[bp+@@frame], al
		cmp	[bp+@@frame], 64
		jnb	short loc_18455
		push	GC_RMW
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	grcg_setcolor
		mov	bx, 3932h
		cmp	_pid_current, 0
		jz	short loc_1840A
		add	bx, 28h	; '('

loc_1840A:
		call	sub_B39E
		call	grcg_off
		mov	al, [bp+@@frame]
		shl	al, 2
		mov	dl, 255
		sub	dl, al
		mov	[bp+var_2], dl
		mov	al, [bp+var_2]
		mov	ah, 0
		push	ax
		push	word ptr _pid_current
		call	sub_A3D2
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 8
		cwd
		idiv	bx
		or	dx, dx
		jnz	loc_185A3
		push	9000B80h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE0C
		jmp	loc_185A3
; ---------------------------------------------------------------------------

loc_18455:
		cmp	[bp+@@frame], 144
		jnb	loc_1853F
		mov	_palette_changed, 1
		mov	al, [bp+@@frame]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_1848B
		mov	PaletteTone, 60
		mov	_palette_changed, 1
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 4
		jmp	short loc_184A5
; ---------------------------------------------------------------------------

loc_1848B:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -4
		mov	PaletteTone, 120
		mov	_palette_changed, 1

loc_184A5:
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 16
		cwd
		idiv	bx
		or	dx, dx
		jnz	short loc_18518
		call	snd_se_play pascal, 10
		mov	al, [bp+@@frame]
		mov	ah, 0
		add	ax, -64
		add	ax, ax
		shl	ax, 4
		mov	si, ax
		mov	ax, 900h
		sub	ax, si
		push	ax
		push	0B80h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE5B
		lea	ax, [si+900h]
		push	ax
		push	0B80h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE5B
		push	900h
		mov	ax, 0B80h
		sub	ax, si
		push	ax
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE5B
		push	900h
		lea	ax, [si+0B80h]
		push	ax
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE5B

loc_18518:
		mov	si, PLAYFIELD_LEFT
		cmp	_pid_current, 0
		jz	short loc_18526
		add	si, PLAYFIELD_W_BORDERED

loc_18526:
		push	si	; left
		push	PLAYFIELD_TOP	; top
		mov	al, _pid_current
		mov	ah, 0
		add	ax, 2
		push	ax	; slot
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; altered_colors
		call	@mrs_put_noalpha_8$qiuiiuc
		jmp	short loc_185A3
; ---------------------------------------------------------------------------

loc_1853F:
		mov	PaletteTone, 100
		mov	_palette_changed, 1
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	al, [bp+@@frame]
		shl	al, 3
		mov	dl, 255
		sub	dl, al
		mov	[bp+@@frame], dl
		mov	al, [bp+@@frame]
		add	al, al
		mov	[bp+var_2], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+@@frame]
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1

loc_185A3:
		call	egc_on

@@ret:
		pop	si
		leave
		retf
chiyuri_bomb	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

ellen_185AB	proc far
		push	bp
		mov	bp, sp
		push	si
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_PREPARING
		jnz	short loc_1860D
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	_bomb_flag[bx], BF_ACTIVE
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	_bomb_frame[bx], 0
		xor	si, si
		jmp	short loc_18601
; ---------------------------------------------------------------------------

loc_185E9:
		mov	al, _pid_current
		mov	ah, 0
		shl	ax, 6
		mov	dx, si
		shl	dx, 3
		add	ax, dx
		mov	bx, ax
		mov	word ptr [bx+25DEh], 4E1Fh
		inc	si

loc_18601:
		cmp	si, 8
		jl	short loc_185E9
		call	snd_se_play pascal, 17

loc_1860D:
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		inc	_bomb_frame[bx]
		mov	_playfield_clip_negative_radius.x, (-32 shl 4)
		mov	_playfield_clip_negative_radius.y, (-32 shl 4)
		mov	al, _pid_current
		mov	ah, 0
		shl	ax, 6
		add	ax, 25DEh
		mov	word_1FBBE, ax
		xor	si, si
		jmp	short loc_18698
; ---------------------------------------------------------------------------

loc_18636:
		mov	bx, word_1FBBE
		cmp	word ptr [bx], 270Fh
		jz	short loc_18667
		mov	bx, word_1FBBE
		cmp	word ptr [bx], 4E1Fh
		jz	short loc_18692
		mov	bx, word_1FBBE
		mov	ax, [bx+4]
		add	[bx], ax
		mov	ax, [bx+6]
		add	[bx+2],	ax
		call	@PLAYFIELD_CLIP$Q20%SUBPIXELBASE$TI$TI%T1 pascal, word ptr [bx], word ptr [bx+2]
		or	al, al
		jz	short loc_18692

loc_18667:
		mov	bx, word_1FBBE
		mov	word ptr [bx], 900h
		mov	word ptr [bx+2], 0B80h
		push	ds
		mov	ax, word_1FBBE
		add	ax, 4
		push	ax
		push	ds
		mov	ax, word_1FBBE
		add	ax, 6
		push	ax
		call	@randring_far_next16$qv
		push	ax
		push	224
		call	vector2

loc_18692:
		inc	si
		add	word_1FBBE, 8

loc_18698:
		cmp	si, 8
		jl	short loc_18636
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_frame[bx], BOMB_FRAMES
		jb	short @@ret
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	_bomb_flag[bx], BF_INACTIVE
		push	word ptr _pid_current
		call	sub_A3A8

@@ret:
		pop	si
		pop	bp
		retf
ellen_185AB	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

ellen_bomb_186C3	proc near

@@sprite_offset		= word ptr -6
@@top		= word ptr -4
@@left		= word ptr -2

		enter	6, 0
		push	si
		mov	al, _pid_current
		mov	ah, 0
		shl	ax, 6
		add	ax, 25DEh
		mov	word_1FBBE, ax
		mov	_sprite16_put_w, (64 / 16)
		mov	_sprite16_put_h, 32
		cmp	_pid_current, 0
		jnz	short loc_186F6
		mov	_sprite16_clip_left, PLAYFIELD1_CLIP_LEFT
		mov	_sprite16_clip_right, PLAYFIELD1_CLIP_RIGHT
		jmp	short loc_18702
; ---------------------------------------------------------------------------

loc_186F6:
		mov	_sprite16_clip_left, PLAYFIELD2_CLIP_LEFT
		mov	_sprite16_clip_right, PLAYFIELD2_CLIP_RIGHT

loc_18702:
		mov	al, _pid_PID_so_attack
		mov	ah, 0
		add	ax, 29Ch
		mov	[bp+@@sprite_offset], ax
		xor	si, si
		jmp	short loc_1875E
; ---------------------------------------------------------------------------

loc_18711:
		mov	bx, word_1FBBE
		cmp	word ptr [bx], 4E1Fh
		jz	short loc_18758
		mov	bx, word_1FBBE
		cmp	word ptr [bx], 270Fh
		jz	short loc_18758
		mov	bx, word_1FBBE
		push	word ptr [bx]	; x
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; pid
		call	@playfield_fg_x_to_screen$qii
		add	ax, -32
		mov	[bp+@@left], ax
		mov	bx, word_1FBBE
		mov	ax, [bx+2]
		sar	ax, 4
		add	ax, -16
		mov	[bp+@@top], ax
		call	sprite16_put pascal, [bp+@@left], ax, [bp+@@sprite_offset]

loc_18758:
		inc	si
		add	word_1FBBE, 8

loc_1875E:
		cmp	si, 8
		jl	short loc_18711
		pop	si
		leave
		retn
ellen_bomb_186C3	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

ellen_bomb	proc far

var_4		= byte ptr -4
@@frame		= byte ptr -3
var_2		= word ptr -2

		enter	4, 0
		push	si
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		call	egc_off
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	al, _bomb_frame[bx]
		mov	[bp+@@frame], al
		cmp	[bp+@@frame], 64
		jnb	short loc_18801
		push	GC_RMW
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	grcg_setcolor
		mov	bx, 3932h
		cmp	_pid_current, 0
		jz	short loc_187AF
		add	bx, 28h	; '('

loc_187AF:
		call	sub_B39E
		call	grcg_off
		mov	al, [bp+@@frame]
		add	al, al
		mov	[bp+var_4], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_4]
		add	dl, dl
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_4]
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1
		mov	word_1FB3C, 0
		jmp	loc_18964
; ---------------------------------------------------------------------------

loc_18801:
		cmp	[bp+@@frame], 128
		jnb	loc_18911
		test	[bp+@@frame], 1
		jz	short loc_18845
		call	snd_se_play pascal, 10
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].r, 255
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, 128
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].b, 128
		jmp	short loc_18872
; ---------------------------------------------------------------------------

loc_18845:
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].r, 0
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, 0
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].b, 32

loc_18872:
		mov	_palette_changed, 1
		mov	al, [bp+@@frame]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_18895
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 4
		jmp	short loc_188A4
; ---------------------------------------------------------------------------

loc_18895:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -4

loc_188A4:
		mov	si, PLAYFIELD_LEFT
		cmp	_pid_current, 0
		jz	short loc_188B2
		add	si, PLAYFIELD_W_BORDERED

loc_188B2:
		push	si	; left
		push	PLAYFIELD_TOP	; top
		mov	al, _pid_current
		mov	ah, 0
		add	ax, 2
		push	ax	; slot
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; altered_colors
		call	@mrs_put_noalpha_8$qiuiiuc
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 4
		cwd
		idiv	bx
		or	dx, dx
		jnz	loc_18964
		push	9000B80h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		cmp	word_1FB3C, 8
		jge	short loc_18964
		mov	al, _pid_current
		mov	ah, 0
		shl	ax, 6
		mov	dx, word_1FB3C
		shl	dx, 3
		add	ax, dx
		mov	bx, ax
		mov	word ptr [bx+25DEh], 270Fh
		inc	word_1FB3C
		jmp	short loc_18964
; ---------------------------------------------------------------------------

loc_18911:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	al, [bp+@@frame]
		shl	al, 3
		mov	dl, 255
		sub	dl, al
		mov	[bp+var_4], dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		add	dl, dl
		and	dl, 255
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_4]
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1

loc_18964:
		call	egc_on
		cmp	[bp+@@frame], 64
		jb	short @@ret
		cmp	[bp+@@frame], 128
		jnb	short @@ret
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	ax, _playfield_fg_shift_x[bx]
		mov	[bp+var_2], ax
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		call	ellen_bomb_186C3
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	dx, [bp+var_2]
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], dx

@@ret:
		pop	si
		leave
		retf
ellen_bomb	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

kana_bomb	proc far

var_2		= byte ptr -2
@@frame		= byte ptr -1

		enter	2, 0
		push	si
		push	di
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	al, _bomb_frame[bx]
		mov	[bp+@@frame], al
		cmp	[bp+@@frame], 64
		jnb	short loc_18A10
		mov	al, 64
		sub	al, [bp+@@frame]
		mov	[bp+var_2], al
		mov	ah, 0
		push	ax
		push	word ptr _pid_current
		call	sub_A3D2
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 8
		cwd
		idiv	bx
		or	dx, dx
		jnz	short loc_18A08
		push	9000B80h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CE0C

loc_18A08:
		mov	angle_1FBD4, 0
		jmp	@@ret
; ---------------------------------------------------------------------------

loc_18A10:
		cmp	[bp+@@frame], 128
		jnb	loc_18B5B
		call	egc_off
		mov	al, [bp+@@frame]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_18A4E
		call	snd_se_play pascal, 10
		push	160
		push	word ptr _pid_current
		call	sub_A3D2
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 4
		jmp	short loc_18A68
; ---------------------------------------------------------------------------

loc_18A4E:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -4
		push	0
		push	word ptr _pid_current
		call	sub_A3D2

loc_18A68:
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 4
		cwd
		idiv	bx
		or	dx, dx
		jnz	loc_18B2F
		mov	al, angle_1FBD4
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, large (144 shl 16) or 144, _CosTable8[bx]
		mov	si, ax
		mov	al, angle_1FBD4
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, large (144 shl 16) or 184, _SinTable8[bx]
		mov	di, ax
		mov	ax, si
		shl	ax, 4
		push	ax
		mov	ax, di
		shl	ax, 4
		push	ax
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		mov	al, 80h
		sub	al, angle_1FBD4
		mov	angle_1FBD4, al
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, large (144 shl 16) or 144, _CosTable8[bx]
		mov	si, ax
		mov	al, angle_1FBD4
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		call	@polar$qiii c, large (144 shl 16) or 184, _SinTable8[bx]
		mov	di, ax
		mov	ax, si
		shl	ax, 4
		push	ax
		mov	ax, di
		shl	ax, 4
		push	ax
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		mov	al, 80h
		sub	al, angle_1FBD4
		mov	angle_1FBD4, al
		add	al, 10h
		mov	angle_1FBD4, al

loc_18B2F:
		mov	si, PLAYFIELD_LEFT
		cmp	_pid_current, 0
		jz	short loc_18B3D
		add	si, PLAYFIELD_W_BORDERED

loc_18B3D:
		push	si	; left
		push	PLAYFIELD_TOP	; top
		mov	al, _pid_current
		mov	ah, 0
		add	ax, 2
		push	ax	; slot
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; altered_colors
		call	@mrs_put_noalpha_8$qiuiiuc
		call	egc_on
		jmp	short @@ret
; ---------------------------------------------------------------------------

loc_18B5B:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	al, [bp+@@frame]
		shl	al, 3
		mov	dl, 255
		sub	dl, al
		mov	[bp+@@frame], dl

loc_18B77:
		mov	al, [bp+@@frame]
		add	al, al
		mov	[bp+var_2], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+@@frame]
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1

@@ret:
		pop	di
		pop	si
		leave
		retf
kana_bomb	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

kotohime_bomb	proc far

var_2		= byte ptr -2
@@frame		= byte ptr -1

		enter	2, 0
		push	si
		push	di
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		call	egc_off
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	al, _bomb_frame[bx]
		mov	[bp+@@frame], al
		cmp	[bp+@@frame], 64
		jnb	loc_18C95
		push	GC_RMW
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	grcg_setcolor
		mov	bx, 3932h
		cmp	_pid_current, 0
		jz	short loc_18C04
		add	bx, 28h	; '('

loc_18C04:
		call	sub_B39E
		call	grcg_off
		mov	al, [bp+@@frame]
		mov	ah, 0
		imul	ax, 3
		mov	[bp+var_2], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		add	dl, 64
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		add	dl, 32
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 8
		cwd
		idiv	bx
		or	dx, dx
		jnz	loc_18DBF
		mov	al, [bp+@@frame]
		mov	ah, 0
		imul	ax, 48h
		mov	dx, 11B8h
		sub	dx, ax
		mov	si, dx
		mov	al, [bp+@@frame]
		mov	ah, 0
		imul	ax, 5Ch
		add	ax, 5Ch
		mov	word_1FE56, ax
		push	dx
		push	ax
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		jmp	loc_18DBF
; ---------------------------------------------------------------------------

loc_18C95:
		cmp	[bp+@@frame], 128
		jnb	loc_18D5B
		mov	_palette_changed, 1
		mov	al, [bp+@@frame]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_18CD2
		call	snd_se_play pascal, 10
		mov	PaletteTone, 170
		mov	_palette_changed, 1
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 4
		jmp	short loc_18CEC
; ---------------------------------------------------------------------------

loc_18CD2:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -4
		mov	PaletteTone, 100
		mov	_palette_changed, 1

loc_18CEC:
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 8
		cwd
		idiv	bx
		or	dx, dx
		jnz	short loc_18D34
		xor	si, si
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 10h
		cwd
		idiv	bx
		mov	ax, dx
		cwd
		sub	ax, dx
		sar	ax, 1
		mov	di, ax
		jmp	short loc_18D28
; ---------------------------------------------------------------------------

loc_18D13:
		push	si
		push	word_1FE56
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		add	si, 600h
		inc	di

loc_18D28:
		cmp	si, 1200h
		jle	short loc_18D13
		sub	word_1FE56, 2E0h

loc_18D34:
		mov	si, PLAYFIELD_LEFT
		cmp	_pid_current, 0
		jz	short loc_18D42
		add	si, PLAYFIELD_W_BORDERED

loc_18D42:
		push	si	; left
		push	PLAYFIELD_TOP	; top
		mov	al, _pid_current
		mov	ah, 0
		add	ax, 2
		push	ax	; slot
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; altered_colors
		call	@mrs_put_noalpha_8$qiuiiuc
		jmp	short loc_18DBF
; ---------------------------------------------------------------------------

loc_18D5B:
		mov	PaletteTone, 100
		mov	_palette_changed, 1
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	al, [bp+@@frame]
		shl	al, 3
		mov	dl, 255
		sub	dl, al
		mov	[bp+@@frame], dl
		mov	al, [bp+var_2]
		add	al, al
		mov	[bp+var_2], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+@@frame]
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1

loc_18DBF:
		call	egc_on

@@ret:
		pop	di
		pop	si
		leave
		retf
kotohime_bomb	endp


; =============== S U B	R O U T	I N E =======================================

; Attributes: bp-based frame

rikako_bomb	proc far

var_2		= byte ptr -2
@@frame		= byte ptr -1

		enter	2, 0
		push	si
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		cmp	_bomb_flag[bx], BF_INACTIVE
		jz	@@ret
		mov	al, _pid_current
		mov	ah, 0
		mov	bx, ax
		mov	al, _bomb_frame[bx]
		mov	[bp+@@frame], al
		call	egc_off
		cmp	[bp+@@frame], 64
		jnb	short loc_18E39
		push	GC_RMW
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	grcg_setcolor
		mov	bx, 3932h
		cmp	_pid_current, 0
		jz	short loc_18E11
		add	bx, 28h	; '('

loc_18E11:
		call	sub_B39E
		call	grcg_off
		mov	al, [bp+@@frame]
		shl	al, 2
		mov	[bp+var_2], al
		mov	ah, 0
		push	ax
		push	word ptr _pid_current
		call	sub_A3D2
		mov	word_220EC, 0
		jmp	loc_18FE2
; ---------------------------------------------------------------------------

loc_18E39:
		cmp	[bp+@@frame], 128
		jnb	loc_18F89
		mov	al, [bp+@@frame]
		mov	ah, 0
		and	ax, 3
		cmp	ax, 2
		jge	short loc_18E5F
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 4
		jmp	short loc_18E6E
; ---------------------------------------------------------------------------

loc_18E5F:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], -4

loc_18E6E:
		mov	si, PLAYFIELD_LEFT
		cmp	_pid_current, 0
		jz	short loc_18E7C
		add	si, PLAYFIELD_W_BORDERED

loc_18E7C:
		push	si	; left
		push	PLAYFIELD_TOP	; top
		mov	al, _pid_current
		mov	ah, 0
		add	ax, 2
		push	ax	; slot
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; altered_colors
		call	@mrs_put_noalpha_8$qiuiiuc
		call	grcg_setcolor pascal, (GC_RMW shl 16) + V_WHITE
		mov	ax, (144 shl 4)
		sub	ax, word_220EC
		push	ax	; x
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; pid
		call	@playfield_fg_x_to_screen$qii
		mov	si, ax
		call	grcg_vline pascal, ax, (8 shl 16) or 192
		mov	ax, word_220EC
		add	ax, (144 shl 4)
		push	ax	; x
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; pid
		call	@playfield_fg_x_to_screen$qii
		mov	si, ax
		call	grcg_vline pascal, ax, (8 shl 16) or 192
		mov	ax, word_220EC
		add	ax, ax
		mov	dx, (144 shl 4)
		sub	dx, ax
		push	dx	; x
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; pid
		call	@playfield_fg_x_to_screen$qii
		mov	si, ax
		call	grcg_vline pascal, ax, (8 shl 16) or 192
		mov	ax, word_220EC
		add	ax, ax
		add	ax, (144 shl 4)
		push	ax	; x
		mov	al, _pid_current
		mov	ah, 0
		push	ax	; pid
		call	@playfield_fg_x_to_screen$qii
		mov	si, ax
		call	grcg_vline pascal, ax, (8 shl 16) or 192
		add	word_220EC, 41h	; 'A'
		cmp	word_220EC, 480h
		jl	short loc_18F38
		mov	word_220EC, 0

loc_18F38:
		call	grcg_off
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 8
		cwd
		idiv	bx
		or	dx, dx
		jnz	short loc_18F71
		push	3FFh
		call	@randring_far_next16_and$qui
		mov	si, ax
		jmp	short loc_18F6B
; ---------------------------------------------------------------------------

loc_18F58:
		push	si
		push	1700h
		mov	al, _pid_current
		mov	ah, 0
		push	ax
		call	sub_CDBD
		add	si, 600h

loc_18F6B:
		cmp	si, 1200h
		jle	short loc_18F58

loc_18F71:
		mov	al, [bp+@@frame]
		mov	ah, 0
		mov	bx, 4
		cwd
		idiv	bx
		or	dx, dx
		jnz	short loc_18FE2
		call	snd_se_play pascal, 5
		jmp	short loc_18FE2
; ---------------------------------------------------------------------------

loc_18F89:
		mov	al, _pid_current
		mov	ah, 0
		add	ax, ax
		mov	bx, ax
		mov	_playfield_fg_shift_x[bx], 0
		mov	al, [bp+@@frame]
		shl	al, 3
		mov	dl, 255
		sub	dl, al
		mov	[bp+@@frame], dl
		mov	al, [bp+@@frame]
		add	al, al
		mov	[bp+var_2], al
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+var_2]
		mov	bx, ax
		mov	Palettes[bx].r, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	bx, ax
		mov	Palettes[bx].g, dl
		mov	al, _pid_current
		mov	ah, 0
		imul	ax, size rgb_t
		mov	dl, [bp+@@frame]
		mov	bx, ax
		mov	Palettes[bx].b, dl
		mov	_palette_changed, 1

loc_18FE2:
		call	egc_on

@@ret:
		pop	si
		leave
		retf
rikako_bomb	endp
