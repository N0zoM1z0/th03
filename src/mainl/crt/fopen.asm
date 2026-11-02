; Original 8086 Borland DOS fopen multi-entry CRT implementation.
; First near Pascal mode parser, then public __OPENFP/__GETFP,
; then far-cdecl fopen. Honors original file stream flags,
; DOS open status, buffering, exit cleanup and shared stream table.
; CRT extern names, far/near calling conventions and mixed FIXUPP
; frame/target types are native source expressions, not binary patches.
.8086
extrn __streams:word
extrn __nfile:word
extrn _fclose:far
extrn _setvbuf:far
extrn __fmode:word
extrn _isatty:far
extrn _open:far
extrn __exitfopen:word
extrn __xfclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
fopen_parse_mode proc near
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov word ptr [bp-2], 0
    les bx, dword ptr [bp+0ch]
    inc word ptr [bp+0ch]
    mov cl, byte ptr es:[bx]
    mov al, cl
    cmp al, 072h
    jne short not_read_mode
    mov dx, 1
    mov word ptr [bp-4], 1
    jmp short check_mode_suffix
not_read_mode:
    cmp cl, 077h
    jne short not_write_mode
    mov dx, 0302h
    jmp short set_write_append_mode
not_write_mode:
    cmp cl, 061h
    jne short invalid_file_mode
    mov dx, 0902h
set_write_append_mode:
    mov word ptr [bp-2], 080h
    mov word ptr [bp-4], 2
    jmp short check_mode_suffix
invalid_file_mode:
    xor ax, ax
    jmp near ptr return_open_mode
check_mode_suffix:
    les bx, dword ptr [bp+0ch]
    mov cl, byte ptr es:[bx]
    inc word ptr [bp+0ch]
    cmp cl, 02bh
    je short mode_has_plus
    les bx, dword ptr [bp+0ch]
    cmp byte ptr es:[bx], 02bh
    jne short test_text_or_binary
    cmp cl, 074h
    je short mode_has_plus
    cmp cl, 062h
    jne short test_text_or_binary
mode_has_plus:
    cmp cl, 02bh
    jne short complete_mode_flags
    les bx, dword ptr [bp+0ch]
    mov cl, byte ptr es:[bx]
complete_mode_flags:
    and dx, 0fffch
    or dx, 4
    mov word ptr [bp-2], 0180h
    mov word ptr [bp-4], 3
test_text_or_binary:
    cmp cl, 074h
    jne short open_at_090
    or dx, 04000h
    jmp short install_exit_cleanup
open_at_090:
    cmp cl, 062h
    jne short inherit_default_fmode
    or dx, 08000h
    jmp short set_exit_cleanup
inherit_default_fmode:
    mov ax, word ptr DGROUP:__fmode
    and ax, 0c000h
    or dx, ax
    mov ax, dx
    test ah, 080h
    je short install_exit_cleanup
set_exit_cleanup:
    or word ptr [bp-4], 040h
install_exit_cleanup:
    mov word ptr DGROUP:__exitfopen+2,seg __xfclose
    mov word ptr DGROUP:__exitfopen,offset __xfclose
    les bx, dword ptr [bp+8]
    mov word ptr es:[bx], dx
    les bx, dword ptr [bp+4]
    mov ax, word ptr [bp-2]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp-4]
return_open_mode:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ch
fopen_parse_mode endp
public __OPENFP
__OPENFP proc near
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ss
    lea ax, [bp-2]
    push ax
    push ss
    lea ax, [bp-4]
    push ax
    call fopen_parse_mode
    les bx, dword ptr [bp+0eh]
    mov word ptr es:[bx+2], ax
    or ax, ax
    je short failed_open_stream
    cmp byte ptr es:[bx+4], 0
    jge short setup_stream_buffer
    push word ptr [bp-4]
    mov ax, word ptr [bp-2]
    or ax, word ptr [bp+4]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call _open
    add sp, 8
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx+4], al
    or al, al
    jge short setup_stream_buffer
failed_open_stream:
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx+4], 0ffh
    mov word ptr es:[bx+2], 0
    jmp short return_openfp_failure
setup_stream_buffer:
    les bx, dword ptr [bp+0eh]
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
    call _isatty
    pop cx
    or ax, ax
    je short select_buffering
    les bx, dword ptr [bp+0eh]
    or word ptr es:[bx+2], 0200h
select_buffering:
    mov ax, 0200h
    push ax
    les bx, dword ptr [bp+0eh]
    test byte ptr es:[bx+3], 2
    je short buffering_flag_value
    mov ax, 1
    jmp short configure_stream_buffer
buffering_flag_value:
    xor ax, ax
configure_stream_buffer:
    push ax
    xor ax, ax
    push ax
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call _setvbuf
    add sp, 0ch
    or ax, ax
    je short return_openfp_success
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    call _fclose
    pop cx
    pop cx
return_openfp_failure:
    xor dx, dx
    xor ax, ax
    jmp short open_at_19e
return_openfp_success:
    les bx, dword ptr [bp+0eh]
    mov word ptr es:[bx+010h], 0
    mov dx, word ptr [bp+010h]
    mov ax, word ptr [bp+0eh]
open_at_19e:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0eh
__OPENFP endp
public __GETFP
__GETFP proc near
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov word ptr [bp-2], ds
    mov word ptr [bp-4],offset DGROUP:__streams
check_free_stream:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx+4], 0
    jl short exhausted_stream_slots
    mov ax, word ptr [bp-4]
    add word ptr [bp-4], 014h
    push ax
    mov ax, 014h
    imul word ptr DGROUP:__nfile
    add ax,offset DGROUP:__streams
    pop dx
    cmp dx, ax
    jb short check_free_stream
exhausted_stream_slots:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx+4], 0
    jl short return_free_stream
    xor dx, dx
    xor ax, ax
    jmp short getfp_exit
return_free_stream:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
getfp_exit:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
__GETFP endp
public _fopen
_fopen proc far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    call __GETFP
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short open_acquired_stream
    xor dx, dx
    xor ax, ax
    jmp short fopen_exit
open_acquired_stream:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    xor ax, ax
    push ax
    call __OPENFP
fopen_exit:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_fopen endp
_TEXT ends
end
