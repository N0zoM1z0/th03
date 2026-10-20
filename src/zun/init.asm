; TH03 ZUN option -2 complete semantic source proposal (not accepted).
; Derived from pinned ReC98 b6ba5b0a529edbb31efdf8c0e939263804f8ee47.
; UTF-8/LF maintenance format; stage strictly as Shift-JIS/CRLF before TASM.
; Inner COM 0100h..066Dh, 1390 bytes: 607 instruction bytes + 783 initialized data bytes.
; Labels/comments only are changed from the pinned reference token stream.

		.286
		.model tiny
_TEXT		segment use16
		assume cs:_TEXT
		org 100h
		assume es:nothing, ss:nothing, ds:_TEXT
		public start
start		proc near
		jmp	parse_install_or_remove
start		endp

; INT 59h: AX indexes six near pointers without a bounds check. IRET ABI.
error_interrupt		proc far
		pushf
		push	ax
		push	bx
		push	cx
		push	dx
		push	ds
		push	di
		push	es
		mov	bx, ax
		shl	bx, 1
		xor	ax, ax
		mov	dx, cs:error_message_table[bx]
		call	draw_doublebyte_text
		mov	ax, 0A0h
		mov	dx, offset text_press_return
		call	draw_doublebyte_text
wait_return_key:
		mov	ah, 4
		mov	al, 3
		int	18h
		test	ah, 10h
		jz	short wait_return_key
		pop	es
		pop	di
		pop	ds
		pop	dx
		pop	cx
		pop	bx
		pop	ax
		popf
		iret
error_interrupt		endp

; INT 06h: any nonzero latch suppresses entry; otherwise sets 1.
; Uses interrupt caller stack.
stop_interrupt		proc far
		cmp	cs:key_message_latch, 0
		jnz	short stop_interrupt_return
		mov	cs:key_message_latch, 1
		call	show_key_message
stop_interrupt_return:
		iret
stop_interrupt		endp

; INT 05h: any nonzero latch suppresses entry; otherwise sets 2.
; Uses interrupt caller stack.
copy_interrupt		proc far
		cmp	cs:key_message_latch, 0
		jnz	short copy_interrupt_return
		mov	cs:key_message_latch, 2
		call	show_key_message
copy_interrupt_return:
		iret
copy_interrupt		endp

; Preserve flags/DF. PC-98 INT 18h calls, not IBM-PC ROM BASIC.
; Observed AH sequence: 41h, 04h key-group polls, 40h, 06h.
; Device meanings remain provisional; release then press uses mask 1 or 2.
show_key_message		proc near
		pushf
		push	ax
		push	bx
		push	cx
		push	dx
		push	ds
		push	di
		push	es
		mov	ah, 41h
		int	18h
		cmp	cs:key_message_latch, 2
		jz	short show_copy_message
		mov	ax, 650h
		mov	dx, offset text_stop_line1
		call	draw_doublebyte_text
		mov	ax, 6F0h
		mov	dx, offset text_stop_line2
		call	draw_doublebyte_text
		mov	ax, 790h
		mov	dx, offset text_stop_line3
		call	draw_doublebyte_text
		mov	bl, 1
		jmp	short wait_key_release
show_copy_message:
		mov	ax, 650h
		mov	dx, offset text_copy_line1
		call	draw_doublebyte_text
		mov	ax, 6F0h
		mov	dx, offset text_copy_line2
		call	draw_doublebyte_text
		mov	ax, 790h
		mov	dx, offset text_copy_line3
		call	draw_doublebyte_text
		mov	bl, 2
wait_key_release:
		mov	ah, 4
		mov	al, 0Ch
		int	18h
		test	ah, bl
		jnz	short wait_key_release
wait_key_press:
		mov	ah, 4
		mov	al, 0Ch
		int	18h
		test	ah, bl
		jz	short wait_key_press
		mov	ah, 40h
		int	18h
		mov	ax, 650h
		mov	dx, offset text_clear_line
		call	draw_doublebyte_text
		mov	ax, 6F0h
		mov	dx, offset text_clear_line
		call	draw_doublebyte_text
		mov	ax, 790h
		mov	dx, offset text_clear_line
		call	draw_doublebyte_text
		mov	ah, 6
		int	18h
		pop	es
		pop	di
		pop	ds
		pop	dx
		pop	cx
		pop	bx
		pop	ax
		popf
		mov	cs:key_message_latch, 0
		retn
show_key_message		endp

; Preserve the carry-dependent character-word arithmetic exactly.
convert_character_word		proc near
		shl	ah, 1
		cmp	al, 9Fh
		jnb	short finish_character_conversion
		cmp	al, 80h
		adc	ax, 0FEDFh
finish_character_conversion:
		sbb	ax, 0DFFEh
		and	ax, 7F7Fh
		retn
convert_character_word		endp

; CS:DX points at Shift-JIS pairs terminated by $. AX is text offset.
; A000h receives two character words; A200h receives attribute 0041h.
; No CLD: inherited DF affects STOSW. Empty text wraps CX and writes 65536 words.
draw_doublebyte_text		proc near
		mov	bx, dx
		mov	di, 0A000h
		mov	es, di
		assume es:nothing
		mov	di, ax
		mov	dx, ax
		xor	ax, ax
		xor	cx, cx
draw_character_pair:
		mov	ax, cs:[bx]
		cmp	al, 24h
		jz	short begin_attributes
		xchg	ah, al
		call	convert_character_word
		xchg	ah, al
		sub	al, 20h
		stosw
		or	ah, 80h
		stosw
		inc	bx
		inc	bx
		inc	cx
		inc	cx
		jmp	short draw_character_pair
begin_attributes:
		mov	di, 0A200h
		mov	es, di
		assume es:nothing
		mov	di, dx
		mov	ax, 41h
write_attribute:
		dec	cx
		stosw
		jz	short draw_text_return
		jmp	short write_attribute
draw_text_return:
		retn
draw_doublebyte_text		endp

; Preserve assembler word literals 'ZU','NP': stored bytes 55 5A 50 4E.
resident_signature		dw 'ZU', 'NP'
saved_error_vector	dd 0
saved_copy_vector	dd 0
saved_stop_vector	dd 0
key_message_latch	db 0
text_press_return	db 'リターンキーを押してね$'
text_unknown_error		db 'なんかのエラーですぅ$'
text_file_not_found	db 'ファイルがみつかんないよぉ$'
text_out_of_memory	db 'メモリが足りないんですぅ$'
text_start_from_batch	db 'バッチファイルから起動してよぉ$'
text_highscore_invalid	db 'ハイスコアのファイルがおかしいよぅ、だからハイスコアは消えちゃったよ$'
error_message_table		dw offset text_unknown_error
		dw offset text_unknown_error
		dw offset text_file_not_found
		dw offset text_out_of_memory
		dw offset text_start_from_batch
		dw offset text_highscore_invalid
text_stop_line1	db 'むやみにＳＴＯＰキー押したりしない$'
text_stop_line2		db '方がいいと思うの。（ゲーム中はね）$'
text_stop_line3	db '（ＳＴＯＰキーで戻れるよ、ねっ）　$'
text_clear_line	db '　　　　　　　　　　　　　　　　　$'
text_copy_line1		db 'なんでＣＯＰＹキー押したりしてるの$'
text_copy_line2	db 'かな〜。ふしぎ〜。　　（もう一度、$'
text_copy_line3	db 'ＣＯＰＹキー押せば戻れるよ、ねっ）$'

; Transient detector: compares fixed ES:resident_signature, not ES:BX.
; Resident retention rounds this address to 42h PSP-relative paragraphs.
print_banner_and_detect_resident		proc near
		mov	dx, offset text_banner
		mov	ah, 9
		int	21h
		mov	ax, 3559h
		int	21h
		cmp	es:resident_signature, 'ZU'
		jnz	short resident_not_found
		cmp	es:resident_signature+2, 'NP'
		jnz	short resident_not_found
		mov	ax, 1
		jmp	short resident_detection_return
resident_not_found:
		mov	ax, 0
resident_detection_return:
		retn
print_banner_and_detect_resident		endp

; Inherits wrapper PSP DS/ES, stack and cleared DF; no separate resident stack.
; Empty/ordinary first word installs; /R or -R ignores trailing text.
parse_install_or_remove		proc near
		mov	si, 81h
scan_command_tail:
		lodsb
		cmp	al, 0Dh
		jz	short check_before_install
		cmp	al, 2Fh
		jz	short read_option_letter
		cmp	al, 2Dh
		jz	short read_option_letter
		cmp	al, 20h
		jbe	short scan_command_tail
check_before_install:
		call	print_banner_and_detect_resident
		test	ax, ax
		jz	short install_resident
		jmp	report_already_resident
read_option_letter:
		lodsb
		cmp	al, 20h
		ja	short check_remove_option
		jmp	report_invalid_option
check_remove_option:
		and	al, 0DFh
		cmp	al, 52h
		jz	short check_before_remove
		jmp	report_invalid_option
check_before_remove:
		call	print_banner_and_detect_resident
		test	ax, ax
		jnz	short remove_resident
		jmp	report_not_resident
install_resident:
		mov	word ptr cs:saved_error_vector, bx
		mov	word ptr cs:saved_error_vector+2, es
		mov	dx, offset error_interrupt
		mov	ax, 2559h
		int	21h
		mov	ah, 35h
		mov	al, 6
		int	21h
		mov	word ptr cs:saved_stop_vector, bx
		mov	word ptr cs:saved_stop_vector+2, es
		mov	dx, offset stop_interrupt
		mov	ax, 2506h
		int	21h
		mov	ah, 35h
		mov	al, 5
		int	21h
		mov	word ptr cs:saved_copy_vector, bx
		mov	word ptr cs:saved_copy_vector+2, es
		mov	dx, offset copy_interrupt
		mov	ax, 2505h
		int	21h
		mov	dx, offset text_installed
		mov	ah, 9
		int	21h
		mov	dx, offset print_banner_and_detect_resident
		mov	cl, 4
		shr	dx, cl
		inc	dx
		mov	ax, 3100h
		int	21h

; Restore all saved far vectors before frees. First free CF is ignored.
remove_resident:
		push	ds
		mov	dx, word ptr es:saved_error_vector
		mov	ds, word ptr es:saved_error_vector+2
		mov	ax, 2559h
		int	21h
		mov	dx, word ptr es:saved_stop_vector
		mov	ds, word ptr es:saved_stop_vector+2
		mov	ax, 2506h
		int	21h
		mov	dx, word ptr es:saved_copy_vector
		mov	ds, word ptr es:saved_copy_vector+2
		mov	ax, 2505h
		int	21h
		pop	ds
		push	es
		mov	es, word ptr es:2Ch
		assume es:nothing
		mov	ah, 49h
		int	21h
		pop	es
		mov	ah, 49h
		int	21h
		mov	dx, offset text_removed
		jnb	short print_remove_result
		mov	dx, offset text_free_error
print_remove_result:
		mov	ah, 9
		int	21h
		jmp	short exit_success
report_already_resident:
		mov	dx, offset text_already_resident
		mov	ah, 9
		int	21h
		jmp	short exit_success
report_not_resident:
		mov	dx, offset text_not_resident
		mov	ah, 9
		int	21h
		jmp	short exit_success

; Preserve the real jmp short $+2 at inner 052Eh and success exit code.
report_invalid_option:
		mov	dx, offset text_invalid_option
		mov	ah, 9
		int	21h
		jmp	short $+2
exit_success:
		mov	ax, 4C00h
		int	21h
parse_install_or_remove		endp
text_banner	db 0Dh,0Ah
		db 0Dh,0Ah
		db 'INTvector set program  zuninit.com Version1.00              (c)zun 1997',0Dh,0Ah,'$'
text_installed	db 'ちょこっとメモリかりるね',0Dh,0Ah
		db 0Dh,0Ah,'$'
text_already_resident	db 'すでに常駐してるの',0Dh,0Ah
		db 0Dh,0Ah,'$'
text_removed	db 'メモリから消えてなくなっちゃったけど、きっとまたあえるよ、ねっ',0Dh,0Ah
		db 0Dh,0Ah,'$'
text_not_resident	db 'まだ、常駐してないわぁ',0Dh,0Ah
		db 0Dh,0Ah,'$'
text_invalid_option	db '意味不明なオプションよぉ（オプションは -Rのみ）',0Dh,0Ah,'$'
text_free_error	db 'メモリ解放エラーです。 : zuninit.com',0Dh,0Ah,'$'
_TEXT		ends
		end start
