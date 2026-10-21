; Maintained ZUN sprite16 procedure group, UTF-8 LF.
; The stage places each complete procedure at its existing source position.
; This group owns no inter-procedure bytes, digit table, fields or trailing data.
; No target bytes, padding or output rewriting. Original behavior is preserved.

; DS:DX format and SS:BX 4-byte argument slots; render into 208-byte
; stack buffer, then print through DOS. No output-capacity check is added.
public sprite16_format_print
sprite16_format_print		proc near

print_buffer		= byte ptr -0D0h

		enter	0D0h, 0
		push	es
		push	di
		push	ss
		pop	es
		lea	di, [bp+print_buffer]
		call	sprite16_format_into
		push	ds
		push	dx
		push	ss
		pop	ds
		assume ds:_TEXT
		lea	dx, [bp+print_buffer]
		call	sprite16_print_string
		pop	dx
		pop	ds
		pop	di
		pop	es
		leave
		retn
sprite16_format_print		endp

; DS:DX NUL string to DOS INT 21h/AH=2 character output.
; Preserve AX/DX/SI, not flags; DOS effects remain unverified here.
public sprite16_print_string
sprite16_print_string		proc near
		push	ax
		push	dx
		push	si
		mov	si, dx

print_next_character:
		mov	dl, [si]
		or	dl, dl
		jz	short print_string_return
		mov	ah, 2
		int	21h

		inc	si
		jmp	short print_next_character

print_string_return:
		pop	si
		pop	dx
		pop	ax
		retn
sprite16_print_string		endp

; Near callee-popped WORD offset argument, interpreted in SS.
; Switch DS to SS for printing, restore DS/DX/BP, return with RETN 2.
public sprite16_print_stack_string
sprite16_print_stack_string		proc near

print_string_argument		= word ptr  4

		push	bp
		mov	bp, sp
		push	dx
		push	ds
		mov	dx, [bp+print_string_argument]
		push	ss
		pop	ds
		call	sprite16_print_string
		pop	ds
		pop	dx
		pop	bp
		retn	2
sprite16_print_stack_string		endp

; DL classification: CF=1 exactly for ASCII 0..9, else CF=0.
; No register result is returned; all other comparison flags remain observed.
public sprite16_is_decimal_digit
sprite16_is_decimal_digit		proc near
		cmp	dl, 30h
		jb	short digit_not_decimal
		cmp	dl, 3Ah
		retn

digit_not_decimal:
		clc
		retn
sprite16_is_decimal_digit		endp

; AL classification: CF=1 exactly for ASCII a..z, else CF=0.
public sprite16_is_ascii_lower
sprite16_is_ascii_lower		proc near
		cmp	al, 61h
		jb	short character_not_lower
		cmp	al, 7Bh
		retn

character_not_lower:
		clc
		retn
sprite16_is_ascii_lower		endp

; Fold only ASCII a..z in AL, using the classification carry flag.
public sprite16_ascii_upper
sprite16_ascii_upper		proc near
		call	sprite16_is_ascii_lower
		jnb	short uppercase_return
		and	al, 0DFh

uppercase_return:
		retn
sprite16_ascii_upper		endp

; DS:DX format, ES:DI destination, SS:BX packed 4-byte argument slots.
; Supports numeric/string/character fields and backslash n/r/t escapes.
; PUSHA preserves WORD registers, not every 32-bit high half. No bounds checks.
; Numeric padding helpers share this exact BP frame and original flag state.
public sprite16_format_into
sprite16_format_into		proc near

format_number_buffer		= byte ptr -50h
format_lowercase		= word ptr -18h
format_radix		= dword	ptr -14h
format_zero_pad		= word ptr -10h
format_left_align		= word ptr -0Ch
format_output_length		= word ptr -8
format_field_width		= word ptr -4

		enter	50h, 0
		pusha
		push	ds
		push	es
		mov	si, dx
		jmp	format_test_end

format_next:
		cmp	byte ptr [si], 25h
		jnz	format_check_newline
		mov	[bp+format_field_width], 0
		mov	[bp+format_output_length], 0
		mov	[bp+format_left_align], 0
		mov	[bp+format_zero_pad], 0
		inc	si
		cmp	byte ptr [si], 2Dh
		jnz	short format_check_zero_pad
		inc	si
		mov	[bp+format_left_align], 1

format_check_zero_pad:
		cmp	byte ptr [si], 30h
		jnz	short format_width_begin
		inc	si
		mov	[bp+format_zero_pad], 1

format_width_begin:
		xor	ax, ax
		xor	dx, dx
		jmp	short format_width_test

format_width_digit:
		imul	ax, 0Ah
		xor	dx, dx
		mov	dl, [si]
		sub	dl, 30h
		add	ax, dx
		inc	si

format_width_test:
		cmp	byte ptr [si], 30h
		jb	short format_check_unsigned
		cmp	byte ptr [si], 39h
		jbe	short format_width_digit

format_check_unsigned:
		mov	[bp+format_field_width], ax
		cmp	byte ptr [si], 75h
		jnz	short format_check_signed
		inc	si
		mov	edx, ss:[bx]
		add	bx, 4
		mov	[bp+format_radix], 0Ah

format_convert_number:
		push	ds
		push	bx
		push	ss
		pop	ds
		lea	bx, [bp+format_number_buffer]
		mov	ecx, [bp+format_radix]
		call	sprite16_format_unsigned
		lea	dx, [bp+format_number_buffer]
		call	sprite16_string_length
		add	[bp+format_output_length], ax
		pop	bx
		pop	ds
		cmp	[bp+format_left_align], 0
		jnz	short format_left_number
		cmp	[bp+format_zero_pad], 0
		jz	short format_leading_spaces
		call	sprite16_pad_zeroes
		jmp	short format_append_number

format_leading_spaces:
		call	sprite16_pad_spaces

format_append_number:
		push	ds
		push	si
		push	ss
		pop	ds
		lea	si, [bp+format_number_buffer]
		call	sprite16_append_string
		pop	si
		pop	ds
		jmp	format_test_end

format_left_number:
		cmp	[bp+format_left_align], 1
		jnz	format_test_end
		push	ds
		push	si
		push	ss
		pop	ds
		lea	si, [bp+format_number_buffer]
		call	sprite16_append_string
		pop	si
		pop	ds
		call	sprite16_pad_spaces
		jmp	format_test_end

format_check_signed:
		cmp	byte ptr [si], 64h
		jnz	short format_check_lower_hex
		inc	si
		mov	edx, ss:[bx]
		add	bx, 4
		or	edx, edx
		jns	short format_signed_radix
		neg	edx
		mov	byte ptr es:[di], 2Dh
		inc	di
		inc	[bp+format_output_length]

format_signed_radix:
		mov	[bp+format_radix], 0Ah
		jmp	short format_convert_number

		jmp	format_test_end

format_check_lower_hex:
		cmp	byte ptr [si], 78h
		jnz	short format_check_upper_hex
		inc	si
		mov	edx, ss:[bx]
		add	bx, 4
		mov	[bp+format_radix], 10h
		mov	[bp+format_lowercase], 1
		jmp	format_convert_number

		jmp	format_test_end

format_check_upper_hex:
		cmp	byte ptr [si], 58h
		jnz	short format_check_binary
		inc	si
		mov	edx, ss:[bx]
		add	bx, 4
		mov	[bp+format_radix], 10h
		mov	[bp+format_lowercase], 0
		jmp	format_convert_number

		jmp	format_test_end

format_check_binary:
		cmp	byte ptr [si], 62h
		jnz	short format_check_string
		inc	si
		mov	edx, ss:[bx]
		add	bx, 4
		mov	[bp+format_radix], 2
		mov	[bp+format_lowercase], 0
		jmp	format_convert_number

		jmp	short format_test_end

format_check_string:
		cmp	byte ptr [si], 73h
		jnz	short format_check_character
		inc	si
		push	ds
		push	si
		lds	si, ss:[bx]
		add	bx, 4
		mov	dx, si
		call	sprite16_string_length
		mov	[bp+format_output_length], ax
		cmp	[bp+format_left_align], 0
		jnz	short format_left_string
		call	sprite16_pad_spaces
		call	sprite16_append_string
		jmp	short format_string_restore

format_left_string:
		call	sprite16_append_string
		call	sprite16_pad_spaces

format_string_restore:
		pop	si
		pop	ds
		jmp	short format_test_end

format_check_character:
		cmp	byte ptr [si], 'c'
		jnz	short format_test_end
		inc	si
		mov	al, ss:[bx]
		add	bx, 4
		stosb
		jmp	short format_test_end

format_check_newline:
		cmp	word ptr [si], 'n\'
		jnz	short format_check_carriage
		add	si, 2
		mov	al, 0Dh
		stosb
		mov	al, 0Ah
		stosb
		jmp	short format_test_end

format_check_carriage:
		cmp	word ptr [si], 'r\'
		jnz	short format_check_tab
		add	si, 2
		mov	al, 0Dh
		stosb
		jmp	short format_test_end

format_check_tab:
		cmp	word ptr [si], 't\'
		jnz	short format_literal
		add	si, 2
		mov	al, 9
		stosb
		jmp	short format_test_end

format_literal:
		movsb

format_test_end:
		cmp	byte ptr [si], 0
		jnz	format_next
		mov	byte ptr es:[di], 0
		pop	es
		pop	ds
		popa
		leave
		retn
sprite16_format_into		endp

; Formatter-frame helper: emit zero padding using shared BP width/length.
public sprite16_pad_zeroes
sprite16_pad_zeroes		proc near
		mov	al, 30h
		call	sprite16_pad_field
		retn
sprite16_pad_zeroes		endp

; Formatter-frame helper: emit space padding using shared BP width/length.
public sprite16_pad_spaces
sprite16_pad_spaces		proc near
		mov	al, 20h
		call	sprite16_pad_field
		retn
sprite16_pad_spaces		endp

; AL fill byte, ES:DI destination, BP-4 width and BP-8 used length.
; Signed comparison controls REP STOSB; modifies CX/DI, requires DF=0.
public sprite16_pad_field
sprite16_pad_field		proc near
		mov	cx, [bp-4]
		sub	cx, [bp-8]
		cmp	cx, 1
		jl	short padding_return
		rep stosb

padding_return:
		retn
sprite16_pad_field		endp

; Copy DS:SI NUL string to ES:DI, leaving DI on the terminator.
; Uses LODSB/STOSB and requires DF=0; no destination-size check.
public sprite16_append_string
sprite16_append_string		proc near
		lodsb
		stosb
		or	al, al
		jnz	short sprite16_append_string
		dec	di
		retn
sprite16_append_string		endp

; EDX value, ECX radix, DS:BX destination, shared BP lowercase flag.
; Preserve EAX/EBX/ECX/EDX, emit digits then reverse the buffer.
; The original CS/address-size prefix order accounts for two target differences.
public sprite16_format_unsigned
sprite16_format_unsigned		proc near
		push	eax
		push	ebx
		push	ecx
		push	edx
		mov	eax, edx
		push	bx

unsigned_next_digit:
		xor	edx, edx
		div	ecx
		mov	dl, byte ptr cs:sprite16_hex_digits[edx]
		cmp	word ptr [bp-18h], 0
		jz	short unsigned_store_digit
		or	dl, 20h

unsigned_store_digit:
		mov	[bx], dl
		inc	bx
		or	eax, eax
		jnz	short unsigned_next_digit
		mov	byte ptr [bx], 0
		pop	bx
		mov	dx, bx
		call	sprite16_reverse_string
		pop	edx
		pop	ecx
		pop	ebx
		pop	eax
		retn
sprite16_format_unsigned		endp

; DS:DX writable NUL string, reverse in place. Preserve ES and
; AX/CX/DX/SI/DI; forward REPNE SCASB requires DF=0.
public sprite16_reverse_string
sprite16_reverse_string		proc near
		push	es
		push	ax
		push	cx
		push	dx
		push	si
		push	di
		push	ds
		pop	es
		assume es:_TEXT
		mov	di, dx
		xor	al, al
		mov	cx, 0FFFFh
		repne scasb
		sub	di, 2
		mov	si, dx
		jmp	short reverse_test

reverse_swap:
		mov	al, [si]
		xchg	al, [di]
		mov	[si], al
		inc	si
		dec	di

reverse_test:
		cmp	si, di
		jnb	short reverse_return
		cmp	byte ptr [si], 0
		jnz	short reverse_swap

reverse_return:
		pop	di
		pop	si
		pop	dx
		pop	cx
		pop	ax
		pop	es
		assume es:nothing
		retn
sprite16_reverse_string		endp

