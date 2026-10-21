; Maintained ZUN sprite16 startup/resident lifecycle, UTF-8 LF.
; Eight complete procedures, IP 010Ch..033Fh: 564 instruction bytes.
; Retained driver owns referenced tables, messages, fields and graphics/parser
; helpers. This include owns no storage, zero gaps, launcher or packaging.
; Instruction widths, near/far returns, dead paths and oddities are intentional.

; COM entry: CS=DS=ES=PSP segment. Clears DF, prints header, shrinks the
; DOS block, terminates on invalid command usage, otherwise dispatches options.
; The signature check and optional INT 40h path are retained, not runtime-proven.
public sprite16_entry
sprite16_entry		proc near

		cld
		push	offset sprite16_banner
		call	sprite16_print_stack_string
		push	es
		mov	ax, 0
		mov	es, ax
		assume es:_TEXT
		mov	bx, word ptr es:start
		mov	es, word ptr es:sprite16_signature
		assume es:nothing
		mov	ax, es:[bx+2]
		xchg	al, ah
		pop	es
		assume es:nothing
		cmp	ax, 'OK'
		jnz	short entry_no_int40_signature
		mov	sprite16_int40_signature_found, 1
		jmp	short entry_resize_block

entry_no_int40_signature:
		mov	sprite16_int40_signature_found, 0

entry_resize_block:
		mov	ax, 1180h
		shr	ax, 4
		inc	ax
		mov	sprite16_resident_paragraphs, ax
		mov	sp, offset sprite16_previous_vector_segment
		push	ds
		pop	es
		assume es:_TEXT
		mov	bx, sprite16_resident_paragraphs
		mov	ah, 4Ah
		int	21h

		jnb	short entry_parse_command_tail
		push	offset sprite16_resize_failed_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

entry_parse_command_tail:
		mov	di, 81h
		mov	al, 0Dh
		mov	cx, 80h
		repne scasb
		mov	byte ptr [di-1], 0
		mov	si, 81h
		call	sprite16_tokenize_command
		cmp	sprite16_argument_count, 0
		jbe	short entry_no_arguments
		call	sprite16_dispatch_options
		mov	ax, 4C00h
		int	21h

		jmp	short entry_optional_int40

entry_no_arguments:
		push	offset sprite16_usage
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

entry_optional_int40:
		cmp	cs:sprite16_int40_signature_found, 0
		jz	short entry_return
		int	40h

entry_return:
		retn
sprite16_entry		endp

; Allocate two 1000-paragraph DOS blocks (mask then solid pixel data).
; Updates resident size and segment fields; DOS error exits with code 1.
; AX/BX/flags and global fields are modified. No synthetic allocation fallback.
public sprite16_allocate_buffers
sprite16_allocate_buffers		proc near
		mov	bx, 1000
		mov	ah, 48h
		int	21h

		jnb	short allocate_solid_buffer
		push	offset sprite16_memory_failed_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

allocate_solid_buffer:
		mov	sprite16_mask_buffer_segment, ax
		add	sprite16_resident_paragraphs, 1000
		mov	bx, 1000
		mov	ah, 48h
		int	21h

		jnb	short allocate_buffers_done
		push	offset sprite16_memory_failed_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

allocate_buffers_done:
		mov	sprite16_solid_buffer_segment, ax
		add	sprite16_resident_paragraphs, 1000
		retn
sprite16_allocate_buffers		endp

; Option adapter: consume one parsed number through retained sprite16_require_number.
; Stores only AL as the software-interrupt number. Near caller owns arguments.
public sprite16_set_interrupt_argument
sprite16_set_interrupt_argument		proc near
		call	sprite16_require_number
		mov	sprite16_interrupt_number, al
		retn
sprite16_set_interrupt_argument		endp

; MASKTEST adapter: allocate buffers, call retained graphics setup helpers,
; then copy 1F40h words of mask data to A800:0000. DS and ES are restored.
; Other register/flag effects follow the original instruction sequence.
public sprite16_mask_test_command
sprite16_mask_test_command		proc near
		call	sprite16_allocate_buffers
		call	sprite16_prepare_vram
		call	sprite16_build_mask
		call	sprite16_clear_upper
		push	ds
		push	es
		mov	ds, sprite16_mask_buffer_segment
		xor	si, si
		mov	ax, 0A800h
		mov	es, ax
		assume es:nothing
		xor	di, di
		mov	cx, 1F40h
		rep movsw
		pop	es
		assume es:nothing
		pop	ds
		retn
sprite16_mask_test_command		endp

; SPRITE option adapter: consume five numeric arguments into DX/BX/DI/AX/CX,
; then invoke retained setup, drawing and cleanup helpers in original order.
; No argument validation is invented beyond the retained parser calls.
public sprite16_draw_command
sprite16_draw_command		proc near
		call	sprite16_allocate_buffers
		call	sprite16_build_mask
		call	sprite16_require_number
		mov	dx, ax
		call	sprite16_require_number
		mov	bx, ax
		call	sprite16_require_number
		mov	di, ax
		call	sprite16_require_number
		push	ax
		call	sprite16_require_number
		mov	cx, ax
		pop	ax
		call	sprite16_egc_begin
		call	sprite16_draw_clipped
		call	sprite16_egc_end
		retn
sprite16_draw_command		endp

; Interrupt ABI: AH selects a WORD in the resident service table, unchecked.
; Saves BX while selecting the target, enables interrupts, calls it near, IRET.
; Retain shared dispatch storage and reentrancy behavior; do not claim safety.
public sprite16_interrupt_dispatch
sprite16_interrupt_dispatch		proc far
		push	bx
		mov	bl, ah
		xor	bh, bh
		shl	bx, 1
		mov	bx, cs:sprite16_service_table[bx]
		mov	cs:sprite16_dispatch_target, bx
		pop	bx
		sti
		call	cs:sprite16_dispatch_target
		iret
sprite16_interrupt_dispatch		endp

; Compare the ten-byte signature at the configured interrupt vector.
; If absent, allocate buffers, exchange the vector, save its previous values,
; print the selected interrupt, and terminate-and-stay-resident via INT 21h/31h.
public sprite16_install
sprite16_install		proc near
		push	es
		xor	ax, ax
		mov	es, ax
		assume es:_TEXT
		mov	bl, sprite16_interrupt_number
		xor	bh, bh
		shl	bx, 2
		mov	es, word ptr es:[bx+2]
		assume es:nothing
		mov	di, 102h
		mov	si, 102h
		mov	cx, 0Ah
		repe cmpsb
		pop	es
		jz	short install_already_present
		call	sprite16_allocate_buffers
		push	es
		xor	ax, ax
		mov	es, ax
		assume es:_TEXT
		mov	dx, cs
		mov	ax, offset sprite16_interrupt_dispatch
		mov	bl, sprite16_interrupt_number
		xor	bh, bh
		shl	bx, 2
		xchg	dx, es:[bx+2]
		xchg	ax, es:[bx]
		mov	sprite16_previous_vector_segment, dx
		mov	sprite16_previous_vector_offset, ax
		pop	es
		assume es:nothing
		movzx	eax, sprite16_interrupt_number
		push	eax
		mov	bx, sp
		mov	dx, offset sprite16_installed_message
		call	sprite16_format_print
		add	sp, 4
		mov	dx, sprite16_resident_paragraphs
		mov	ax, 3100h
		int	21h

		jmp	short install_return

install_already_present:
		push	offset sprite16_already_installed_message
		call	sprite16_print_stack_string

install_return:
		retn
sprite16_install		endp

; Locate the configured resident instance, restore the vector and free its
; environment, mask, solid and code segments using DOS services.
; Preserve the observed XOR AX before writing the vector offset, even though
; it discards the saved offset. This is not a behavioral correction or DOS proof.
public sprite16_uninstall
sprite16_uninstall		proc near
		xor	ax, ax
		mov	es, ax
		assume es:_TEXT
		mov	bl, sprite16_interrupt_number
		xor	bh, bh
		shl	bx, 2
		mov	es, word ptr es:[bx+2]
		assume es:nothing
		mov	di, 102h
		mov	si, 102h
		mov	cx, 0Ah
		repe cmpsb
		jnz	short uninstall_not_present
		mov	dx, es:sprite16_previous_vector_segment
		mov	ax, es:sprite16_previous_vector_offset
		push	es
		xor	ax, ax
		mov	es, ax
		assume es:_TEXT
		mov	bl, sprite16_interrupt_number
		xor	bh, bh
		shl	bx, 2
		mov	es:[bx+2], dx
		mov	es:[bx], ax
		pop	es
		assume es:nothing
		push	es
		mov	es, word ptr es:2Ch
		mov	ah, 49h
		int	21h

		jnb	short uninstall_free_mask
		push	offset sprite16_environment_free_failed_message
		call	sprite16_print_stack_string

uninstall_free_mask:
		pop	es
		push	es
		mov	es, word ptr es:0F3Ch
		mov	ah, 49h
		int	21h

		jnb	short uninstall_free_solid
		push	offset sprite16_mask_free_failed_message
		call	sprite16_print_stack_string

uninstall_free_solid:
		pop	es
		push	es
		mov	es, word ptr es:0F3Eh
		mov	ah, 49h
		int	21h

		jnb	short uninstall_free_code
		push	offset sprite16_solid_free_failed_message
		call	sprite16_print_stack_string

uninstall_free_code:
		pop	es
		mov	ah, 49h
		int	21h

		jnb	short uninstall_removed
		push	offset sprite16_code_free_failed_message
		call	sprite16_print_stack_string
		jmp	short uninstall_return

uninstall_removed:
		push	offset sprite16_removed_message
		call	sprite16_print_stack_string
		jmp	short uninstall_return

uninstall_not_present:
		push	offset sprite16_not_installed_message
		call	sprite16_print_stack_string

uninstall_return:
		retn
sprite16_uninstall		endp

