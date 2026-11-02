; Original Borland DOS putc/fputc/fputchar/FPUTN CRT output subsystem.
; __fputc: unbuffered front end with original manual CS/FAR call ABI.
; _fputc: stream buffer, text CRLF, flush and device status handling.
; _fputchar: stdout FILE via genuine __streams+20 pointer.
; __FPUTN: near Pascal buffered output of many bytes, direct/FILE
; and device output using the original far/near CRT helper calls.
; The one actual initialized DATA byte is DOS carriage return (0Dh);
; the one original BSS byte holds the last current write character.
; Natural symbolic native instruction blocks preserve descending OMF
; writer order. ORG positions are original disjoint function ranges;
; no executable byte arrays or binary output patching.
.8086
extrn __streams:word
extrn _fflush:far
extrn ___write:far
extrn __openfd:word
extrn _lseek:far
extrn __rtl_write:far
extrn _memcpy:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
fputc_CR db 0Dh ; actual initialized text-mode carriage return
_DATA ends
_BSS segment word public 'BSS'
fputc_character db ? ; genuine one-byte uninitialized output state
_BSS ends
DGROUP group _BSS,_DATA
public __fputc,_fputc,_fputchar,__FPUTN
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03B2h
    call ___write
    add sp, 8
    cmp ax, word ptr [bp+8]
    je short complete_FPUTN
abort_FPUTN:
    xor ax, ax
    jmp short return_FPUTN
complete_FPUTN:
    mov ax, word ptr [bp-2]
return_FPUTN:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ah
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0334h
    call __rtl_write
    add sp, 8
    cmp ax, word ptr [bp+8]
    jne short putc_at_344
    jmp near ptr complete_FPUTN
putc_at_344:
    jmp short abort_FPUTN
check_current_FILE_state:
    les bx, dword ptr [bp+4]
    cmp word ptr es:[bx+6], 0
    je short putc_at_3a0
    jmp short loop_write_length
write_char_loop:
    les bx, dword ptr [bp+4]
    inc word ptr es:[bx]
    jge short putc_at_378
    mov dx, word ptr es:[bx+0eh]
    mov si, word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    les bx, dword ptr [bp+0ah]
    inc word ptr [bp+0ah]
    mov al, byte ptr es:[bx]
    mov es, dx
    mov byte ptr es:[si], al
    mov ah, 0
    jmp short putc_at_38f
putc_at_378:
    push word ptr [bp+6]
    push word ptr [bp+4]
    les bx, dword ptr [bp+0ah]
    inc word ptr [bp+0ah]
    mov al, byte ptr es:[bx]
    push ax
    push cs
    call near ptr __fputc
    add sp, 6
putc_at_38f:
    cmp ax, 0ffffh
    je short abort_FPUTN
loop_write_length:
    mov ax, word ptr [bp+8]
    dec word ptr [bp+8]
    or ax, ax
    jne short write_char_loop
    jmp short complete_FPUTN
putc_at_3a0:
    push word ptr [bp+8]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 031Ah
    call _lseek
    add sp, 8
putc_at_322:
    push word ptr [bp+8]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0302h
    test byte ptr DGROUP:[bx+__openfd+1],8
    je short putc_at_322
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push ax
    mov bx, word ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02D8h
    call _memcpy
    add sp, 0ah
    les bx, dword ptr [bp+4]
    mov ax, word ptr es:[bx]
    add ax, word ptr [bp+8]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp+8]
    add word ptr es:[bx+0ch], ax
    jmp near ptr complete_FPUTN
write_direct_unbuffered:
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    add ax, ax
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02B6h
    call _fflush
    pop cx
    pop cx
    or ax, ax
    je short copy_to_FILE_buffer
    jmp near ptr abort_FPUTN
copy_to_FILE_buffer:
    push word ptr [bp+8]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+4]
    push word ptr es:[bx+0eh]
    push word ptr es:[bx+0ch]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0280h
    call __rtl_write
    add sp, 8
    cmp ax, word ptr [bp+8]
    jne short putc_at_290
    jmp near ptr complete_FPUTN
putc_at_290:
    jmp near ptr abort_FPUTN
fill_available_buffer:
    les bx, dword ptr [bp+4]
    mov ax, word ptr es:[bx]
    add ax, word ptr [bp+8]
    jl short copy_to_FILE_buffer
    cmp word ptr es:[bx], 0
    jne short putc_at_2b0
    mov ax, 0ffffh
    sub ax, word ptr es:[bx+6]
    mov word ptr es:[bx], ax
    jmp short copy_to_FILE_buffer
putc_at_2b0:
    push word ptr [bp+6]
    push word ptr [bp+4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0266h
    call _lseek
    add sp, 8
putc_at_26e:
    push word ptr [bp+8]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 024Eh
    test byte ptr DGROUP:[bx+__openfd+1],8
    je short putc_at_26e
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push ax
    mov bx, word ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0234h
    call _fflush
    pop cx
    pop cx
    or ax, ax
    je short flush_pending_buffer
    jmp near ptr abort_FPUTN
flush_pending_buffer:
    les bx, dword ptr [bp+4]
    mov al, byte ptr es:[bx+4]
    cbw
    add ax, ax
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01C3h
__FPUTN label near
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ax, word ptr [bp+8]
    mov word ptr [bp-2], ax
    les bx, dword ptr [bp+4]
    test byte ptr es:[bx+2], 8
    je short write_raw_chunk
    jmp short putc_at_1fd
write_record_per_char:
    push word ptr [bp+6]
    push word ptr [bp+4]
    les bx, dword ptr [bp+0ah]
    inc word ptr [bp+0ah]
    mov al, byte ptr es:[bx]
    cbw
    push ax
    push cs
    call near ptr _fputc
    add sp, 6
    cmp ax, 0ffffh
    jne short putc_at_1fd
    jmp near ptr abort_FPUTN
putc_at_1fd:
    mov ax, word ptr [bp+8]
    dec word ptr [bp+8]
    or ax, ax
    jne short write_record_per_char
    jmp near ptr complete_FPUTN
write_raw_chunk:
    les bx, dword ptr [bp+4]
    test byte ptr es:[bx+2], 040h
    jne short putc_at_217
    jmp near ptr check_current_FILE_state
putc_at_217:
    cmp word ptr es:[bx+6], 0
    jne short putc_at_221
    jmp near ptr write_direct_unbuffered
putc_at_221:
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+8]
    jae short fill_available_buffer
    cmp word ptr es:[bx], 0
    je short flush_pending_buffer
    push word ptr [bp+6]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01B1h
    mov ax,offset DGROUP:__streams+20
    push ax
    push word ptr [bp+6]
    push cs
    call near ptr _fputc
    add sp, 6
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01ABh
_fputchar label far
    push bp
    mov bp, sp
    push si
    push di
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01A2h
return_putc_status:
    mov al,byte ptr DGROUP:fputc_character
    mov ah, 0
putc_at_1a7:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0181h
    call __rtl_write
    add sp, 8
    cmp ax, 1
    je short return_putc_status
putc_at_18e:
    les bx, dword ptr [bp+8]
    test byte ptr es:[bx+3], 2
    jne short return_putc_status
    or word ptr es:[bx+2], 010h
set_stream_failure:
    mov ax, 0ffffh
    jmp short putc_at_1a7
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0174h
    mov ax,offset DGROUP:fputc_character
    push ax
    les bx, dword ptr [bp+8]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0162h
    call __rtl_write
    add sp, 8
    cmp ax, 1
    jne short putc_at_18e
emit_char_to_output:
    mov ax, 1
    push ax
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0158h
    mov ax,offset DGROUP:fputc_CR
    push ax
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0142h
translate_LF_if_required:
    cmp byte ptr DGROUP:fputc_character,0Ah
    jne short emit_char_to_output
    les bx, dword ptr [bp+8]
    test byte ptr es:[bx+2], 040h
    jne short emit_char_to_output
    mov ax, 1
    push ax
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 013Ah
    call _lseek
    add sp, 8
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0122h
    test byte ptr DGROUP:[bx+__openfd+1],8
    je short translate_LF_if_required
    mov ax, 2
    push ax
    xor ax, ax
    push ax
    push ax
    mov bx, word ptr [bp+8]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0105h
    call _fflush
    pop cx
    pop cx
    or ax, ax
    jne short putc_at_113
    jmp near ptr return_putc_status
putc_at_113:
    jmp near ptr set_stream_failure
query_output_device_mode:
    les bx, dword ptr [bp+8]
    mov al, byte ptr es:[bx+4]
    cbw
    add ax, ax
    mov bx, ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0F5h
    cmp byte ptr DGROUP:fputc_character,0Dh
    je short flush_buffered_character
    jmp near ptr return_putc_status
flush_buffered_character:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0EEh
check_CRLF_translation:
    cmp byte ptr DGROUP:fputc_character,0Ah
    je short flush_buffered_character
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0D9h
    mov al,byte ptr DGROUP:fputc_character
    mov es, dx
    mov byte ptr es:[si], al
    mov es, word ptr [bp+0ah]
    test byte ptr es:[bx+2], 8
    jne short check_CRLF_translation
    jmp near ptr return_putc_status
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0B3h
    call _fflush
    pop cx
    pop cx
    or ax, ax
    je short store_character_in_FILE_buffer
    jmp near ptr set_stream_failure
store_character_in_FILE_buffer:
    les bx, dword ptr [bp+8]
    mov ax, word ptr es:[bx+6]
    neg ax
    mov word ptr es:[bx], ax
    mov dx, word ptr es:[bx+0eh]
    mov si, word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 06Ch
    call _fflush
    pop cx
    pop cx
    or ax, ax
    jne short putc_at_07a
    jmp near ptr return_putc_status
putc_at_07a:
    jmp near ptr set_stream_failure
initialize_unbuffered_output:
    les bx, dword ptr [bp+8]
    test byte ptr es:[bx+2], 090h
    jne short putc_at_08e
    test byte ptr es:[bx+2], 2
    jne short prepare_buffered_output
putc_at_08e:
    les bx, dword ptr [bp+8]
    or word ptr es:[bx+2], 010h
    jmp near ptr set_stream_failure
prepare_buffered_output:
    les bx, dword ptr [bp+8]
    or word ptr es:[bx+2], 0100h
    cmp word ptr es:[bx+6], 0
    je short query_output_device_mode
    cmp word ptr es:[bx], 0
    je short store_character_in_FILE_buffer
    push word ptr [bp+0ah]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 05Ch
    cmp byte ptr DGROUP:fputc_character,0Dh
    je short flush_text_mode
    jmp near ptr return_putc_status
flush_text_mode:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 055h
check_newline:
    cmp byte ptr DGROUP:fputc_character,0Ah
    je short flush_text_mode
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 028h
    mov byte ptr DGROUP:fputc_character,al
    les bx, dword ptr [bp+8]
    cmp word ptr es:[bx], -1
    jge short initialize_unbuffered_output
    inc word ptr es:[bx]
    mov dx, word ptr es:[bx+0eh]
    mov si, word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es, dx
    mov byte ptr es:[si], al
    mov es, word ptr [bp+0ah]
    test byte ptr es:[bx+2], 8
    jne short check_newline
    jmp near ptr return_putc_status
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 020h
_fputc label far
    push bp
    mov bp, sp
    push si
    push di
    mov al, byte ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 014h
    ; No code is emitted by ASSUME: it prevents TASM from silently
    ; rewriting the original far call as PUSH CS + near CALL.
    ; The genuine native original uses TARGET-frame OMF at CODE+21.
    assume cs:NOTHING
    call far ptr _fputc
    add sp, 6
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
__fputc label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+8]
    dec word ptr es:[bx]
    push word ptr [bp+0ah]
    push bx
    mov al, byte ptr [bp+6]
    cbw
    push ax
_TEXT ends
end
