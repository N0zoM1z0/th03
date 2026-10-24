; Maintained ZUN sprite16 procedure group, UTF-8 LF.
; The stage places each complete procedure at its existing source position.
; This group owns no inter-procedure bytes, digit table, fields or trailing data.
; No target bytes, padding or output rewriting. Original behavior is preserved.

; Resident service: preserve general WORD registers and DS/ES; bind caller
; DX/BX/DI/AL/CX as x/y/source/width/height, then perform vertical clipping.
; Negative Y clips only the top, without a second bottom pass.
; EGC must already be enabled. No horizontal/zero-height safety checks added.
public sprite16_draw_clipped
sprite16_draw_clipped		proc near
		push	ax
		push	bx
		push	cx
		push	dx
		push	si
		push	di
		push	bp
		push	ds
		push	es
		push	cs
		pop	ds
		xor	ah, ah
		mov	sprite16_draw_x, dx
		mov	sprite16_draw_y, bx
		mov	sprite16_draw_source_offset, di
		mov	sprite16_draw_width, ax
		mov	sprite16_draw_height, cx
		mov	sprite16_clipped_rows, 0
		cmp	sprite16_draw_y, 0
		jge	short draw_check_bottom
		mov	ax, sprite16_draw_y
		add	ax, sprite16_draw_height
		cmp	ax, 0
		jg	short draw_clip_top
		jmp	short draw_restore

		jmp	short draw_apply_clipping

draw_clip_top:
		mov	ax, 0
		sub	ax, sprite16_draw_y
		mov	sprite16_clipped_rows, ax
		shl	ax, 4
		mov	dx, ax
		shl	ax, 2
		add	ax, dx
		add	sprite16_draw_source_offset, ax
		mov	sprite16_draw_y, 0
		jmp	short draw_apply_clipping

draw_check_bottom:
		cmp	sprite16_draw_y, 0C8h
		jb	short draw_clip_bottom
		jmp	short draw_restore

		jmp	short draw_apply_clipping

draw_clip_bottom:
		mov	dx, sprite16_draw_y
		add	dx, sprite16_draw_height
		cmp	dx, 0C8h
		jle	short draw_apply_clipping
		mov	ax, 0C8h
		sub	ax, sprite16_draw_y
		mov	dx, sprite16_draw_height
		sub	dx, ax
		mov	sprite16_clipped_rows, dx
		jmp	short $+2

draw_apply_clipping:
		mov	ax, sprite16_clipped_rows
		sub	sprite16_draw_height, ax
		call	sprite16_blit_egc

draw_restore:
		pop	es
		pop	ds
		pop	bp
		pop	di
		pop	si
		pop	dx
		pop	cx
		pop	bx
		pop	ax
		retn
sprite16_draw_clipped		endp

; Internal blit setup consumes shared geometry and six service fields.
; Programs EGC ports and branches on mono/overlap mode before copying rows.
; Original accumulator encodings differ at six target bytes here; preserve them.
public sprite16_blit_egc
sprite16_blit_egc		proc near
		mov	si, sprite16_draw_source_offset
		mov	ax, sprite16_draw_x
		shr	ax, 3
		and	ax, 0FFFEh
		xor	dx, dx
		mov	cx, sprite16_draw_y
		imul	di, cx,	50h
		add	di, ax
		mov	ax, sprite16_draw_x
		and	ax, 0Fh
		mov	sprite16_bit_shift, ax
		mov	dx, EGC_ADDRRESSREG
		mov	ax, sprite16_bit_shift
		shl	ax, 4
		out	dx, ax
		mov	sprite16_has_shift, 0
		xor	ax, ax
		cmp	sprite16_bit_shift, 0
		setnz	al
		mov	sprite16_has_shift, ax
		mov	ax, 0A800h
		mov	es, ax
		assume es:nothing
		mov	dx, EGC_BITLENGTHREG
		mov	ax, sprite16_draw_width
		shl	ax, 4
		dec	ax
		out	dx, ax
		mov	ax, sprite16_draw_width
		add	ax, sprite16_has_shift
		mov	sprite16_row_words, ax
		mov	ax, sprite16_row_words
		shl	ax, 1
		mov	dx, 50h
		sub	dx, ax
		mov	sprite16_row_skip_bytes, dx
		cmp	cs:sprite16_mono_enabled, 0
		jz	short draw_color_mode
		outw	EGC_READPLANEREG, 0FFh
		outw	EGC_MASKREG, cs:sprite16_mask
		outw	EGC_READPLANEREG, 40FFh
		outw	EGC_MODE_ROP_REG, EGC_WS_ROP or EGC_SHIFT_CPU or 0ACh
		outw	EGC_FGCOLORREG, cs:sprite16_mono_color
		mov	ds, cs:sprite16_solid_buffer_segment
		jmp	short draw_copy_mask

draw_color_mode:
		cmp	cs:sprite16_overlap, 0
		jz	short draw_no_overlap
		outw	EGC_ACTIVEPLANEREG, 0FFF0h
		outw	EGC_READPLANEREG, 0FFh
		outw	EGC_MODE_ROP_REG, EGC_WS_ROP or EGC_SHIFT_CPU or 0C0h
		outw	EGC_MASKREG, cs:sprite16_mask
		mov	ds, cs:sprite16_mask_buffer_segment
		call	sprite16_copy_rows
		jmp	short draw_color_copy

draw_no_overlap:
		outw	EGC_READPLANEREG, 0FFh
		outw	EGC_MASKREG, cs:sprite16_mask

draw_color_copy:
		outw	EGC_MODE_ROP_REG, cs:sprite16_rop
		mov	ax, 0A800h
		mov	ds, ax
		assume ds:nothing
		add	si, 3E80h

draw_copy_mask:
		outw	EGC_ACTIVEPLANEREG, cs:sprite16_access_plane
		call	sprite16_copy_rows
		retn
sprite16_blit_egc		endp

; Copy shared height rows from DS:SI to ES:DI using REP MOVSW,
; shared word count and per-row skips. SI/DI restored; DF=0 is required.
; Height zero underflows BX and visits 65,536 rows; zero row words still
; advance SI/DI by the skip but issue no source reads or destination writes.
public sprite16_copy_rows
sprite16_copy_rows		proc near
		push	si
		push	di
		mov	bx, cs:sprite16_draw_height
		mov	dx, cs:sprite16_row_words
		mov	ax, cs:sprite16_row_skip_bytes

copy_next_row:
		mov	cx, dx
		rep movsw
		add	si, ax
		add	di, ax
		dec	bx
		jnz	short copy_next_row
		pop	di
		pop	si
		retn
sprite16_copy_rows		endp

; Retain the original graphics setup, page-port writes and helper order.
; Saves WORD registers and DS/ES; resets display/access pages to 0 afterward.
; This is source ownership, not PC-98 validation.
public sprite16_prepare_vram
sprite16_prepare_vram		proc near
		push	ds
		push	es
		pusha
		mov	al, 1
		out	6Ah, al

		xor	al, al
		out	0A6h, al
		call	sprite16_compress_rows
		call	sprite16_copy_upper_to_lower
		call	sprite16_copy_lower_page
		xor	al, al
		out	0A4h, al
		xor	al, al
		out	0A6h, al
		popa
		pop	es
		assume es:nothing
		pop	ds
		assume ds:DGROUP
		retn
sprite16_prepare_vram		endp

; Build solid/mask buffers from graphics planes, retaining page selection,
; EGC setup and inversion order. Preserve WORD registers and DS/ES.
public sprite16_build_mask
sprite16_build_mask		proc near
		push	ds
		push	es
		pusha
		call	sprite16_egc_end
		xor	al, al
		out	0A6h, al
		mov	es, cs:sprite16_solid_buffer_segment
		xor	di, di
		xor	ax, ax
		mov	cx, 1F40h
		rep stosw
		mov	es, cs:sprite16_solid_buffer_segment
		mov	ax, 0A800h
		call	sprite16_accumulate_plane
		mov	ax, 0B000h
		call	sprite16_accumulate_plane
		mov	ax, 0B800h
		call	sprite16_accumulate_plane
		mov	ax, 0E000h
		call	sprite16_accumulate_plane
		mov	ds, cs:sprite16_solid_buffer_segment
		mov	es, cs:sprite16_mask_buffer_segment
		xor	si, si
		xor	di, di
		mov	cx, 1F40h

mask_invert_next:
		lodsw
		not	ax
		stosw
		loop	mask_invert_next
		popa
		pop	es
		pop	ds
		retn
sprite16_build_mask		endp

; OR words from source plane AX at offset 3E80h into ES solid buffer.
; AX/BX/CX/DS change; no segment/device validation is introduced.
public sprite16_accumulate_plane
sprite16_accumulate_plane		proc near
		mov	ds, ax
		xor	bx, bx
		mov	cx, 1F40h

mask_accumulate_next:
		mov	ax, [bx+3E80h]
		or	es:[bx], ax
		add	bx, 2
		loop	mask_accumulate_next
		retn
sprite16_accumulate_plane		endp

; Copy lower-half words from access page 0 to page 1 through EGC.
; Select each page per word; preserve WORD registers and DS/ES.
; Uses explicit addressing, not DF; leaves access page 1.
public sprite16_copy_lower_page
sprite16_copy_lower_page		proc near
		push	ds
		push	es
		pusha
		call	sprite16_egc_begin
		mov	ax, 0A800h
		mov	ds, ax
		assume ds:nothing
		mov	bl, 0
		mov	bh, 1
		mov	di, 3E80h
		mov	cx, 1F40h

copy_page_next_word:
		mov	al, bl
		out	0A6h, al
		mov	dx, [di]
		mov	al, bh
		out	0A6h, al
		mov	[di], dx
		inc	di
		inc	di
		loop	copy_page_next_word
		call	sprite16_egc_end
		popa
		pop	es
		pop	ds
		assume ds:DGROUP
		retn
sprite16_copy_lower_page		endp

; Copy 40 words from every other source row into 200 consecutive rows.
; Retain EGC helper ordering and current access-page selection.
; WORD registers and DS/ES restored; memory/device assumptions unchanged.
public sprite16_compress_rows
sprite16_compress_rows		proc near
		push	ds
		push	es
		pusha
		call	sprite16_egc_begin
		mov	ax, 0A800h
		mov	ds, ax
		assume ds:nothing
		mov	es, ax
		assume es:nothing
		xor	si, si
		xor	di, di
		mov	cx, 0C8h

compress_next_row:
		push	cx
		mov	cx, 28h
		rep movsw
		pop	cx
		add	si, 50h
		loop	compress_next_row
		call	sprite16_egc_end
		popa
		pop	es
		assume es:nothing
		pop	ds
		assume ds:DGROUP
		retn
sprite16_compress_rows		endp

; Copy 1F40h words A800:0000 to A800:3E80 on the selected page.
; Does not add the preservation wrapper used by the adjacent helpers.
public sprite16_copy_upper_to_lower
sprite16_copy_upper_to_lower		proc near
		call	sprite16_egc_begin
		mov	ax, 0A800h
		mov	ds, ax
		assume ds:nothing
		mov	es, ax
		assume es:nothing
		mov	si, 0
		mov	di, 3E80h
		mov	cx, 1F40h
		rep movsw
		call	sprite16_egc_end
		retn
sprite16_copy_upper_to_lower		endp

; Retain EGC-assisted upper-plane clear; preserve WORD registers and ES.
; Device side effects and interrupt behavior are exactly the original macros.
public sprite16_clear_upper
sprite16_clear_upper		proc near
		push	es
		pusha
		call	sprite16_egc_begin
		outw	EGC_MODE_ROP_REG, 0
		mov	ax, 0A800h
		mov	es, ax
		xor	di, di
		mov	ax, 0
		mov	cx, 1F40h
		rep stosw
		call	sprite16_egc_end
		popa
		pop	es
		assume es:nothing
		retn
sprite16_clear_upper		endp

; Program original graphics/EGC modes, planes, mask, addresses and length.
; Preserve AX/DX, CLI then STI unconditionally; incoming IF is not restored.
public sprite16_egc_begin
sprite16_egc_begin		proc near
		push	ax
		push	dx
		cli
		graph_egc	1
		GRCG_SETMODE_VIA_MOV al, GC_TDW
		outw	EGC_ACTIVEPLANEREG, 0FFF0h
		outw	EGC_READPLANEREG, 0FFh
		outw	EGC_MODE_ROP_REG, EGC_COMPAREREAD or EGC_WS_ROP or 0F0h
		outw	EGC_MASKREG, 0FFFFh
		mov	dx, EGC_ADDRRESSREG
		xor	ax, ax
		out	dx, ax
		outw	EGC_BITLENGTHREG, 0Fh
		sti
		pop	dx
		pop	ax
		retn
sprite16_egc_begin		endp

; Restore the original EGC register/mode sequence. Preserve AX/DX;
; CLI then STI unconditionally, not a flags-preserving critical section.
public sprite16_egc_end
sprite16_egc_end		proc near
		push	ax
		push	dx
		cli
		outw	EGC_ACTIVEPLANEREG, 0FFF0h
		outw	EGC_READPLANEREG, 0FFh
		outw	EGC_MASKREG, 0FFFFh
		graph_egc	0
		GRCG_OFF_VIA_XOR al
		sti
		pop	dx
		pop	ax
		retn
sprite16_egc_end		endp

