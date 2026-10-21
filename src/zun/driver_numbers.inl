; Maintained ZUN sprite16 command/numeric/string group, UTF-8 LF.
; Complete near procedures only. Containing driver owns tables/messages/state.
; Keep original widths, branches, flag behavior and malformed-input oddities.

; DS:DX string to 16-bit AX, CF reports validity. Preserve BX/DX/SI.
; Supports one/two quoted bytes, $hex, H/B suffix, decimal and ON/OFF.
; Preserve temporary suffix mutation, the DS:[SI-1] empty-input read and
; wraparound semantics. Source text must be writable for H/B suffix parsing.
public sprite16_parse_number
sprite16_parse_number		proc near
		push	bx
		push	dx
		push	si
		mov	si, dx
		cmp	byte ptr [si], 27h
		jnz	short parse_number_prefix
		cmp	word ptr [si+2], 27h
		jnz	short parse_number_two_chars
		mov	al, [si+1]
		xor	ah, ah
		clc
		jmp	short parse_number_return

parse_number_two_chars:
		cmp	word ptr [si+3], 27h
		jnz	short parse_number_invalid_quote
		mov	ax, [si+1]
		xchg	ah, al
		clc
		jmp	short parse_number_return

parse_number_invalid_quote:
		xor	ax, ax
		stc
		jmp	short parse_number_return

parse_number_prefix:
		cmp	byte ptr [si], 24h
		jnz	short parse_number_suffix
		inc	si
		call	sprite16_parse_hex
		jmp	short parse_number_return

parse_number_suffix:
		mov	dx, si
		call	sprite16_string_length
		mov	bx, ax
		mov	al, [bx+si-1]
		call	sprite16_ascii_upper
		cmp	al, 48h
		jnz	short parse_number_binary_suffix
		mov	dl, [bx+si-1]
		mov	byte ptr [bx+si-1], 0
		call	sprite16_parse_hex
		mov	[bx+si-1], dl
		jmp	short parse_number_return

parse_number_binary_suffix:
		cmp	al, 42h
		jnz	short parse_number_decimal_or_switch
		mov	dl, [bx+si-1]
		mov	byte ptr [bx+si-1], 0
		call	sprite16_parse_binary
		mov	[bx+si-1], dl
		jmp	short parse_number_return

parse_number_decimal_or_switch:
		call	sprite16_parse_decimal
		jnb	short parse_number_return
		call	sprite16_parse_switch

parse_number_return:
		pop	si
		pop	dx
		pop	bx
		retn
sprite16_parse_number		endp

; DS:SI signed decimal to AX with CF=0 success, CF=1 invalid digit.
; Preserve SI/DX/CX/BP. Arithmetic wraps at 16 bits; overflow is not rejected.
; Empty and sign-only strings follow the original zero result.
public sprite16_parse_decimal
sprite16_parse_decimal		proc near
		push	si
		push	dx
		push	cx
		push	bp
		xor	ax, ax
		xor	dx, dx
		mov	bp, 0
		cmp	byte ptr [si], 2Dh
		jnz	short parse_decimal_plus
		inc	si
		mov	bp, 0FFFFh
		jmp	short parse_decimal_digit

parse_decimal_plus:
		cmp	byte ptr [si], 2Bh
		jnz	short parse_decimal_digit
		inc	si

parse_decimal_digit:
		mov	dl, [si]
		inc	si
		or	dl, dl
		jz	short parse_decimal_sign
		call	sprite16_is_decimal_digit
		jb	short parse_decimal_accumulate
		stc
		jmp	short parse_decimal_return

parse_decimal_accumulate:
		push	dx
		mov	cx, 0Ah
		mul	cx
		pop	dx
		sub	dl, 30h
		add	ax, dx
		jmp	short parse_decimal_digit

parse_decimal_sign:
		cmp	bp, 0FFFFh
		jnz	short parse_decimal_success
		neg	ax

parse_decimal_success:
		clc

parse_decimal_return:
		pop	bp
		pop	cx
		pop	dx
		pop	si
		retn
sprite16_parse_decimal		endp

; DS:SI hexadecimal to AX; preserve SI/DX and original permissive
; character folding, flag path and 16-bit wraparound. Punctuation :..@ and
; [..` is accepted by the original arithmetic. DF=0 is required by LODSB.
; Terminating OR clears success CF; overflow is not checked.
public sprite16_parse_hex
sprite16_parse_hex		proc near
		push	si
		push	dx
		xor	dx, dx

parse_hex_digit:
		lodsb
		or	al, al
		jz	short parse_hex_return
		cmp	al, 5Bh
		jb	short parse_hex_value
		sub	al, 20h

parse_hex_value:
		sub	al, 30h
		cmp	al, 0Ah
		jb	short parse_hex_accumulate
		sub	al, 7
		cmp	al, 10h
		jnb	short parse_hex_invalid

parse_hex_accumulate:
		xor	ah, ah
		shl	dx, 4
		add	dx, ax
		jmp	short parse_hex_digit

parse_hex_invalid:
		stc

parse_hex_return:
		mov	ax, dx
		pop	dx
		pop	si
		retn
sprite16_parse_hex		endp

; DS:SI binary to AX; CF=0 success or CF=1 invalid digit.
; Preserve SI/BX/DX; empty input yields zero and long input wraps at 16 bits.
public sprite16_parse_binary
sprite16_parse_binary		proc near
		push	si
		push	bx
		push	dx
		mov	dx, si
		call	sprite16_string_length
		mov	bx, si
		add	bx, ax
		xor	ax, ax
		jmp	short parse_binary_test_end

parse_binary_digit:
		mov	dl, [si]
		cmp	dl, 30h
		jz	short parse_binary_accumulate
		cmp	dl, 31h
		jz	short parse_binary_accumulate
		stc
		jmp	short parse_binary_return

parse_binary_accumulate:
		shr	dl, 1
		rcl	ax, 1
		inc	si

parse_binary_test_end:
		cmp	si, bx
		jnz	short parse_binary_digit
		clc

parse_binary_return:
		pop	dx
		pop	bx
		pop	si
		retn
sprite16_parse_binary		endp

; DS:SI folded ON/OFF to AX=1/0, CF=0; otherwise AX=0, CF=1.
; Preserve DI/ES. String storage remains in the containing driver.
public sprite16_parse_switch
sprite16_parse_switch		proc near
		push	di
		push	es
		push	cs
		pop	es
		assume es:_TEXT
		mov	ax, 1
		mov	di, offset sprite16_switch_on
		call	sprite16_string_equal_folded
		jz	short parse_switch_success
		mov	ax, 0
		mov	di, offset sprite16_switch_off
		call	sprite16_string_equal_folded
		jz	short parse_switch_success
		mov	ax, 0
		stc
		jmp	short parse_switch_return

parse_switch_success:
		clc

parse_switch_return:
		pop	es
		assume es:nothing
		pop	di
		retn
sprite16_parse_switch		endp

