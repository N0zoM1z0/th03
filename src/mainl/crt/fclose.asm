; Original Borland DOS fclose: validated far FILE/stream identity, buffered
; flush, temporary-path unlink, DOS descriptor close and owned-name release.
; Real 16-bit BCC caller stack, far FILE pointers and original return value.
; Original OMF uses descending far/near calls; disjoint ORG blocks reproduce
; those literal native writer sites without artificial executable filler.
.8086
extrn _fflush:far
extrn _unlink:far
extrn _free:far
extrn _close:far
extrn __MKNAME:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _fclose
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A7h
    call _unlink
    pop cx
    pop cx
    les bx, dword ptr [bp+6]
    mov word ptr es:[bx+010h], 0
return_close_result:
    mov ax, word ptr [bp-2]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A2h
    call __MKNAME
    push dx
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 06Fh
    call _close
    pop cx
    mov word ptr [bp-2], ax
reset_stream_owner:
    les bx, dword ptr [bp+6]
    mov word ptr es:[bx+2], 0
    mov word ptr es:[bx+6], 0
    mov word ptr es:[bx], 0
    mov byte ptr es:[bx+4], 0ffh
    cmp word ptr es:[bx+010h], 0
    je short return_close_result
    xor ax, ax
    push ax
    push ax
    push ax
    push ax
    push word ptr es:[bx+010h]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 058h
    call _free
    pop cx
    pop cx
close_stream_handle:
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx+4], 0
    jl short reset_stream_owner
    mov al, byte ptr es:[bx+4]
    cbw
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03Bh
    call _fflush
    pop cx
    pop cx
    or ax, ax
    jne short return_close_result
check_temporary_stream:
    les bx, dword ptr [bp+6]
    test byte ptr es:[bx+2], 4
    je short close_stream_handle
    push word ptr es:[bx+0ah]
    push word ptr es:[bx+8]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_fclose label far
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov word ptr [bp-2], 0ffffh
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    jne short validate_FILE_identity
    jmp near ptr return_close_result
validate_FILE_identity:
    les bx, dword ptr [bp+6]
    mov ax, word ptr es:[bx+012h]
    cmp ax, word ptr [bp+6]
    je short flush_if_buffered
    jmp near ptr return_close_result
flush_if_buffered:
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx+6], 0
    je short close_stream_handle
    cmp word ptr es:[bx], 0
    jge short check_temporary_stream
    push word ptr [bp+8]
    push bx
_TEXT ends
end
