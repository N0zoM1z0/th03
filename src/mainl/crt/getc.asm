; Original 8086 DOS getc multi-entry buffered stream helper.
; These are genuine instruction/branch source ranges in the original
; Borland native OMF FIXUPP chronological order. ORG does not emit
; padding and each code interval is disjoint, exhaustive and typed.
; Four real near/far CRT public entries, one byte of BSS lookahead.
.8086
extrn __streams:word
extrn _fflush:far
extrn _eof:far
extrn ___read:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
getc_unget_byte db ?
_BSS ends
DGROUP group _DATA,_BSS
public __fgetc
public __Nfgetc
public _fgetc
public _fgetchar
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0166h
    mov ax,offset DGROUP:getc_unget_byte
    push ax
    les bx, dword ptr [bp+6]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01B3h
read_crlf_lookahead:
    cmp byte ptr DGROUP:getc_unget_byte,0dh
    jne short restore_stream_flags
    les bx, dword ptr [bp+6]
    test byte ptr es:[bx+2], 040h
    je short fallback_read_one_byte
restore_stream_flags:
    les bx, dword ptr [bp+6]
    and word ptr es:[bx+2], 0ffdfh
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01CCh
    mov al,byte ptr DGROUP:getc_unget_byte
getc_at_1cf:
    mov ah, 0
fgetc_return:
    pop di
    pop si
    pop bp
    retf
_fgetchar label far
    push si
    push di
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 010h
    mov word ptr [bp-4],offset DGROUP:__streams
    jmp short continue_flush_loop
consider_next_file:
    les bx, dword ptr [bp-4]
    mov ax, word ptr es:[bx+2]
    and ax, 0300h
    cmp ax, 0300h
    jne short advance_flush_cursor
    push word ptr [bp-2]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02Ah
    call _fflush
    pop cx
    pop cx
advance_flush_cursor:
    add word ptr [bp-4], 014h
continue_flush_loop:
    mov ax, word ptr [bp-6]
    dec word ptr [bp-6]
    or ax, ax
    jne short consider_next_file
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
getc_fill_internal_buffer label near
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+4]
    test byte ptr es:[bx+3], 2
    je short skip_stream_flush
    call getc_flush_outbound_streams
skip_stream_flush:
    les bx, dword ptr [bp+4]
    push word ptr es:[bx+6]
    mov dx, word ptr es:[bx+0ah]
    mov ax, word ptr es:[bx+8]
    mov word ptr es:[bx+0eh], dx
    mov word ptr es:[bx+0ch], ax
    push dx
    push ax
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 076h
    call ___read
    add sp, 8
    les bx, dword ptr [bp+4]
    mov word ptr es:[bx], ax
    or ax, ax
    jle short handle_empty_buffer
    and word ptr es:[bx+2], 0ffdfh
    xor ax, ax
    jmp short fill_buffer_return
handle_empty_buffer:
    les bx, dword ptr [bp+4]
    cmp word ptr es:[bx], 0
    jne short mark_input_error
    mov ax, word ptr es:[bx+2]
    and ax, 0fe7fh
    or ax, 020h
    mov word ptr es:[bx+2], ax
    jmp short mark_stream_eof
mark_input_error:
    les bx, dword ptr [bp+4]
    mov word ptr es:[bx], 0
    or word ptr es:[bx+2], 010h
mark_stream_eof:
    mov ax, 0ffffh
fill_buffer_return:
    pop di
    pop si
    pop bp
    ret 4
__fgetc label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+6]
    inc word ptr es:[bx]
    push word ptr [bp+8]
    push bx
    push cs
    call near ptr _fgetc
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
__Nfgetc label near
    pop ax
    push cs
    push ax
_fgetc label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    jne short stream_is_present
    jmp near ptr emit_EOF
stream_is_present:
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx], 0
    jle short evaluate_current_stream
    dec word ptr es:[bx]
    jmp short pull_from_buffer
evaluate_current_stream:
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx], 0
    jl short set_stream_failure
    test word ptr es:[bx+2], 0110h
    jne short set_stream_failure
    test byte ptr es:[bx+2], 1
    jne short set_input_buffer_active
set_stream_failure:
    les bx, dword ptr [bp+6]
    or word ptr es:[bx+2], 010h
    jmp near ptr emit_EOF
set_input_buffer_active:
    les bx, dword ptr [bp+6]
    or word ptr es:[bx+2], 080h
    cmp word ptr es:[bx+6], 0
    je short fallback_read_one_byte
    push word ptr [bp+8]
    push bx
    call getc_fill_internal_buffer
    or ax, ax
    jne short emit_EOF
    les bx, dword ptr [bp+6]
    dec word ptr es:[bx]
pull_from_buffer:
    les bx, dword ptr [bp+6]
    mov dx, word ptr es:[bx+0eh]
    mov si, word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es, dx
    mov al, byte ptr es:[si]
    jmp short getc_at_1cf
fallback_read_one_byte:
    les bx, dword ptr [bp+6]
    test byte ptr es:[bx+3], 2
    je short prepare_actual_read
    call getc_flush_outbound_streams
prepare_actual_read:
    mov ax, 1
    push ax
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0173h
    call ___read
    add sp, 8
    or ax, ax
    jne short read_crlf_lookahead
    les bx, dword ptr [bp+6]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0188h
    call _eof
    pop cx
    cmp ax, 1
    je short set_input_eof_flag
    les bx, dword ptr [bp+6]
    or word ptr es:[bx+2], 010h
    jmp short emit_EOF
set_input_eof_flag:
    les bx, dword ptr [bp+6]
    mov ax, word ptr es:[bx+2]
    and ax, 0fe7fh
    or ax, 020h
    mov word ptr es:[bx+2], ax
emit_EOF:
    mov ax, 0ffffh
    jmp short fgetc_return
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01D8h
    mov ax,offset DGROUP:__streams
    push ax
    push cs
    call near ptr _fgetc
    pop cx
    pop cx
    pop di
    pop si
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
getc_flush_outbound_streams label near
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov word ptr [bp-6], 014h
    mov word ptr [bp-2], ds
_TEXT ends
end
