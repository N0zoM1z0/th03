; Maintained ZUN sprite16 command/numeric/string group, UTF-8 LF.
; Complete near procedures only. Containing driver owns tables/messages/state.
; Keep original widths, branches, flag behavior and malformed-input oddities.

; DS:DX NUL-terminated string length to AX; preserve SI/DX.
; Requires the existing forward direction flag and accessible terminator.
public sprite16_string_length
sprite16_string_length		proc near
		push	si
		push	dx
		mov	si, dx
		mov	dx, 0FFFFh

string_length_next:
		inc	dx
		lodsb
		or	al, al
		jnz	short string_length_next
		mov	ax, dx
		pop	dx
		pop	si
		retn
sprite16_string_length		endp

; Compare DS:SI with ES:DI after retained ASCII folding helper.
; Preserve AX/DX/SI/DI; return CMP flags (ZF indicates equality), not AX.
public sprite16_string_equal_folded
sprite16_string_equal_folded		proc near
		push	ax
		push	dx
		push	si
		push	di

string_compare_next:
		mov	al, [si]
		call	sub_69D
		mov	dl, al
		mov	al, es:[di]
		call	sub_69D
		mov	dh, al
		inc	si
		inc	di
		cmp	dl, dh
		jnz	short string_compare_return
		or	dl, dl
		jnz	short string_compare_next

string_compare_return:
		cmp	dl, dh
		pop	di
		pop	si
		pop	dx
		pop	ax
		retn
sprite16_string_equal_folded		endp

