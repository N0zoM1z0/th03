; Maintained ZUN sprite16 command/numeric/string group, UTF-8 LF.
; Complete near procedures only. Containing driver owns tables/messages/state.
; Keep original widths, branches, flag behavior and malformed-input oddities.
; Global state uses DS=driver group; dispatch also requires ES=DS.
; Diagnostic offsets are interpreted in SS by the real print helper.
; Dispatch callbacks preserve DS/SS; PUSHA and saved ES protect other registers.

; DS:SI writable command text. Preserve AX/BX/CX/DX/SI/DI; rebuild the
; global argument vector in place. No vector-capacity check is introduced.
; Semicolon terminates only at the start of the next token; foo;bar stays one.
; Text adjacent to a closing quote is skipped to the next delimiter.
; CR/NUL terminate, and an unclosed quote exits via DOS.
public sprite16_tokenize_command
sprite16_tokenize_command		proc near
		push	ax
		push	bx
		push	cx
		push	dx
		push	si
		push	di
		mov	sprite16_argument_count, 0
		mov	di, offset sprite16_argument_vector

tokenize_next:
		call	sprite16_skip_separators
		mov	al, [si]
		or	al, al
		jz	short tokenize_terminate
		cmp	al, 0Dh
		jz	short tokenize_terminate
		cmp	al, 3Bh
		jnz	short tokenize_check_quote

tokenize_terminate:
		mov	byte ptr [si], 0
		jmp	short tokenize_return

tokenize_check_quote:
		cmp	byte ptr [si], 22h
		jnz	short tokenize_plain
		inc	si
		mov	[di], si
		add	di, 2
		inc	sprite16_argument_count
		call	sprite16_find_quote_end
		jnb	short tokenize_close_quote
		push	offset sprite16_missing_quote_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

tokenize_close_quote:
		mov	byte ptr [si], 0
		inc	si
		call	sprite16_find_token_end
		jmp	short tokenize_next

tokenize_plain:
		mov	[di], si
		add	di, 2
		inc	sprite16_argument_count
		call	sprite16_find_token_end
		jmp	short tokenize_next

tokenize_return:
		pop	di
		pop	si
		pop	dx
		pop	cx
		pop	bx
		pop	ax
		retn
sprite16_tokenize_command		endp

; DS:SI advances over space, comma and TAB, replacing each with NUL.
; AL and flags change; the first nonseparator stays at SI.
public sprite16_skip_separators
sprite16_skip_separators		proc near
		mov	al, [si]
		cmp	al, 20h
		jz	short skip_separator
		cmp	al, 2Ch
		jz	short skip_separator
		cmp	al, 9
		jz	short skip_separator
		jmp	short skip_separators_return

skip_separator:
		mov	byte ptr [si], 0
		inc	si
		jmp	short sprite16_skip_separators

skip_separators_return:
		retn
sprite16_skip_separators		endp

; DS:SI advances to space/comma/TAB/NUL/CR, without overwriting it.
; This scanner deliberately does not treat semicolon as a separator.
public sprite16_find_token_end
sprite16_find_token_end		proc near
		mov	al, [si]
		cmp	al, 20h
		jz	short find_token_done
		cmp	al, 2Ch
		jz	short find_token_done
		cmp	al, 9
		jz	short find_token_done
		or	al, al
		jz	short find_token_done
		cmp	al, 0Dh
		jnz	short find_token_advance

find_token_done:
		jmp	short find_token_return

find_token_advance:
		inc	si
		jmp	short sprite16_find_token_end

find_token_return:
		retn
sprite16_find_token_end		endp

; DS:SI advances to a closing quote (CF=0) or NUL/CR (CF=1).
; Does not consume the terminator; AL and flags are modified.
public sprite16_find_quote_end
sprite16_find_quote_end		proc near
		mov	al, [si]
		cmp	al, 22h
		jnz	short find_quote_check_end
		clc
		jmp	short find_quote_return

find_quote_check_end:
		or	al, al
		jz	short find_quote_missing
		cmp	al, 0Dh
		jnz	short find_quote_advance

find_quote_missing:
		stc
		jmp	short find_quote_return

find_quote_advance:
		inc	si
		jmp	short sprite16_find_quote_end

find_quote_return:
		retn
sprite16_find_quote_end		endp

; Return next argument pointer in SI and decrement the WORD count.
; Missing arguments print an error and exit DOS; no synthesized default.
public sprite16_require_argument
sprite16_require_argument		proc near
		cmp	sprite16_argument_count, 0
		jnz	short require_argument_consume
		push	offset sprite16_missing_argument_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

require_argument_consume:
		dec	sprite16_argument_count
		mov	si, sprite16_argument_cursor
		add	sprite16_argument_cursor, 2
		mov	si, [si]
		retn
sprite16_require_argument		endp

; Return next pointer in SI with CF=0, or CF=1 without changing SI
; when no arguments remain. Updates count and cursor only on consumption.
public sprite16_optional_argument
sprite16_optional_argument		proc near
		cmp	sprite16_argument_count, 0
		jnz	short optional_argument_consume
		stc
		jmp	short optional_argument_return

optional_argument_consume:
		dec	sprite16_argument_count
		mov	si, sprite16_argument_cursor
		add	sprite16_argument_cursor, 2
		mov	si, [si]
		clc

optional_argument_return:
		retn
sprite16_optional_argument		endp

; Consume a required argument and return parsed AX; preserve SI/DX.
; Parse failure prints an error and exits DOS, preserving original control flow.
public sprite16_require_number
sprite16_require_number		proc near
		push	si
		push	dx
		call	sprite16_require_argument
		mov	dx, si
		call	sprite16_parse_number
		jnb	short require_number_return
		push	offset sprite16_invalid_number_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

require_number_return:
		pop	dx
		pop	si
		retn
sprite16_require_number		endp

; Preserve the observed legacy branch: a consumed argument skips parsing
; and returns AX=0, while no argument enters parsing through the existing SI.
; This surprising behavior is retained, not presented as a safe optional parser.
public sprite16_optional_number_legacy
sprite16_optional_number_legacy		proc near
		push	si
		push	dx
		mov	ax, 0
		call	sprite16_optional_argument
		jnb	short optional_number_return
		mov	dx, si
		call	sprite16_parse_number

optional_number_return:
		pop	dx
		pop	si
		retn
sprite16_optional_number_legacy		endp

; Walk argument pointers and the retained option/callback table. Change
; leading minus to slash, compare folded strings and call the selected near
; callback with PUSHA/ES preservation. Invalid options exit through DOS.
; The pointer is read/advanced before testing the remaining count, even at zero.
public sprite16_dispatch_options
sprite16_dispatch_options		proc near
		mov	sprite16_argument_cursor, offset sprite16_argument_vector

dispatch_option_next:
		mov	si, sprite16_argument_cursor
		add	sprite16_argument_cursor, 2
		mov	si, [si]
		cmp	sprite16_argument_count, 0
		jnz	short dispatch_option_consume
		jmp	short dispatch_option_return

dispatch_option_consume:
		dec	sprite16_argument_count
		mov	al, [si]
		cmp	al, 2Dh
		jnz	short dispatch_option_begin
		mov	al, 2Fh
		mov	[si], al

dispatch_option_begin:
		mov	bx, offset sprite16_option_table

dispatch_option_search:
		cmp	word ptr [bx], 0
		jnz	short dispatch_option_compare
		push	offset sprite16_invalid_option_message
		call	sprite16_print_stack_string
		mov	ax, 4C01h
		int	21h

dispatch_option_compare:
		mov	di, [bx]
		call	sprite16_string_equal_folded
		jnz	short dispatch_option_advance
		pusha
		push	es
		call	word ptr [bx+2]
		pop	es
		popa
		jmp	short dispatch_option_continue

dispatch_option_advance:
		add	bx, 4
		jmp	short dispatch_option_search

dispatch_option_continue:
		jmp	short dispatch_option_next

dispatch_option_return:
		retn
sprite16_dispatch_options		endp

