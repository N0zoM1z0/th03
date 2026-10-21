; Maintained MAINL snow and frame control: six complete near procedures, 443 CODE bytes.
; Included inside MAINL_SNOW_TEXT by the opt-in source composer, with the root
; declarations/macros and group_01 assumptions in scope. No DATA/BSS/resource ownership.
; Symbol names remain stable to preserve all source call sites and cross-references.
; See docs/reconstruction/MAINL_SNOW_REVIEW.md for ABI and bounded CPU model limits.
FLAKE_W = 8
FLAKE_H = 8
FLAKE_CELS = 4

public @flakes_reset$qv

; Reset: clear exactly 80 alive bytes; leave coordinates, padding and adjacent state intact.
@flakes_reset$qv proc near
		push	bp
		mov	bp, sp
		push	si
		mov	si, offset _flakes
		xor	ax, ax
		jmp	short loc_BB78

loc_BB71:
		mov	[si+flake_t.FLAKE_alive], 0
		inc	ax
		add	si, size flake_t

loc_BB78:
		cmp	ax, FLAKE_COUNT
		jl	short loc_BB71
		pop	si
		pop	bp
		retn
@flakes_reset$qv endp

; Spawn: signed IRand remainder, frame-gated slots, inherited capacity; retain full-word angle push.
sub_BB80	proc near

@@length		= byte ptr -2
@@angle		= byte ptr -1

		enter	2, 0
		push	si
		push	di
		mov	si, offset _flakes
		xor	di, di
		jmp	loc_BC1A

loc_BB8E:
		cmp	[si+flake_t.FLAKE_alive], 0
		jnz	loc_BC16
		mov	ax, di
		shl	ax, 3
		cmp	ax, word_10BB2
		jg	short loc_BC16
		mov	[si+flake_t.FLAKE_alive], 1
		test	di, 3
		jz	short loc_BBBE
		call	IRand
		mov	bx, ((RES_X - FLAKE_W) shl 4)
		cwd
		idiv	bx
		mov	[si+flake_t.FLAKE_left], dx
		mov	[si+flake_t.FLAKE_top], 0
		jmp	short loc_BBD1

loc_BBBE:
		mov	[si+flake_t.FLAKE_left], ((RES_X - FLAKE_W) shl 4)
		call	IRand
		mov	bx, ((RES_Y - FLAKE_H) shl 4)
		cwd
		idiv	bx
		mov	[si+flake_t.FLAKE_top],	dx

loc_BBD1:
		call	IRand
		mov	bx, 20h
		cwd
		idiv	bx
		add	dl, 50h
		mov	[bp+@@angle], dl
		call	IRand
		mov	bx, (4 shl 4)
		cwd
		idiv	bx
		add	dl, (3 shl 4)
		mov	[bp+@@length], dl
		call	IRand
		and	ax, (FLAKE_CELS - 1)
		mov	[si+flake_t.FLAKE_cel], ax
		push	ds
		lea	ax, [si+flake_t.FLAKE_velocity.x]
		push	ax
		push	ds
		lea	ax, [si+flake_t.FLAKE_velocity.y]
		push	ax
		push	word ptr [bp+@@angle]
		mov	al, [bp+@@length]
		mov	ah, 0
		push	ax
		call	vector2

loc_BC16:
		inc	di
		add	si, size flake_t

loc_BC1A:
		mov	al, byte_106B0
		mov	ah, 0
		cmp	ax, di
		jg	loc_BB8E
		pop	di
		pop	si
		leave
		retn
sub_BB80	endp

; Update: signed Q12.4 motion; one wrap adjustment per axis, not modulo or clipping.
sub_BC29	proc near
		push	bp
		mov	bp, sp
		push	si
		mov	si, offset _flakes
		xor	dx, dx
		jmp	short loc_BC63

loc_BC34:
		cmp	[si+flake_t.FLAKE_alive], 0
		jz	short loc_BC5F
		mov	[si+flake_t.FLAKE_alive], 1
		mov	ax, [si+flake_t.FLAKE_velocity.x]
		add	[si+flake_t.FLAKE_left], ax
		mov	ax, [si+flake_t.FLAKE_velocity.y]
		add	[si+flake_t.FLAKE_top],	ax
		cmp	[si+flake_t.FLAKE_left], 0
		jg	short loc_BC53
		add	[si+flake_t.FLAKE_left], ((RES_X - FLAKE_W) shl 4)

loc_BC53:
		cmp	[si+flake_t.FLAKE_top], ((RES_Y - FLAKE_H) shl 4)
		jl	short loc_BC5F
		sub	[si+flake_t.FLAKE_top], ((RES_Y - FLAKE_H) shl 4)

loc_BC5F:
		inc	dx
		add	si, size flake_t

loc_BC63:
		mov	al, byte_106B0
		mov	ah, 0
		cmp	ax, dx
		jg	short loc_BC34
		pop	si
		pop	bp
		retn
sub_BC29	endp

; Render: arithmetic shift by four; pass left/top/cel to near Pascal flake_put (RET 6).
sub_BC6F	proc near
		push	bp
		mov	bp, sp
		push	si
		push	di
		mov	si, offset _flakes
		xor	di, di
		jmp	short loc_BC98

loc_BC7B:
		cmp	[si+flake_t.FLAKE_alive], 0
		jz	short loc_BC94
		mov	ax, [si+flake_t.FLAKE_left]
		sar	ax, 4
		push	ax	; left
		mov	ax, [si+flake_t.FLAKE_top]
		sar	ax, 4
		push	ax	; top
		push	[si+flake_t.FLAKE_cel]	; cel
		call	@flake_put$qiii

loc_BC94:
		inc	di
		add	si, size flake_t

loc_BC98:
		mov	al, byte_106B0
		mov	ah, 0
		cmp	ax, di
		jg	short loc_BC7B
		pop	di
		pop	si
		pop	bp
		retn
sub_BC6F	endp

; Gate: near RET 4; silent frame > threshold or music measure >= threshold AND frame > 192.
sub_BCA5	proc near

arg_0		= word ptr  4
arg_2		= word ptr  6

		push	bp
		mov	bp, sp
		cmp	_snd_active, 0
		jnz	short loc_BCB9
		mov	ax, word_10BB2
		cmp	ax, [bp+arg_0]
		jle	short loc_BCCF
		jmp	short loc_BCCA

loc_BCB9:
		mov	ah, KAJA_GET_SONG_MEASURE
		int	60h ; KAJA_GET_SONG_MEASURE, not a packet driver.
		cmp	ax, [bp+arg_2]
		jb	short loc_BCCF
		cmp	word_10BB2, 0C0h
		jle	short loc_BCCF

loc_BCCA:
		mov	ax, 1
		jmp	short loc_BCD1

loc_BCCF:
		xor	ax, ax

loc_BCD1:
		pop	bp
		retn	4
sub_BCA5	endp

; Snow frame: spawn/update/render, one-way slow adaptation, wait for vsync, swap pages.
sub_BCD5	proc near
		push	bp
		mov	bp, sp
		call	sub_BB80
		call	sub_BC29
		call	sub_BC6F
		cmp	byte_10BB6, 0
		jz	short loc_BCFE
		cmp	vsync_Count1, 1
		jbe	short loc_BCFE
		mov	byte_10BB5, 0
		mov	byte_106B0, 32h	; '2'
		mov	byte_10BB6, 0

loc_BCFE:
		cmp	vsync_Count1, 0
		jz	short loc_BCFE
		mov	vsync_Count1, 0
		graph_showpage _page_back
		mov	al, 1
		sub	al, _page_back
		mov	_page_back, al
		graph_accesspage al
		pop	bp
		retn
sub_BCD5	endp
