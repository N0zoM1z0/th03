; Original Japanese Borland xfclose: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include stdio_layout.inc
extrn __streams:byte
extrn __nfile:word
extrn _fclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __xfclose
; Complete disjoint instruction chunks preserve original native field order.

org 54
    cmp ax, word ptr DGROUP:__nfile
    jb short inspect_open_stream
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 37
    call _fclose
    pop cx
    pop cx
advance_stream:
    add word ptr [bp-4], FILE_BYTES
    inc word ptr [bp-6]
test_stream_limit:
    mov ax, word ptr [bp-6]

org 16
    mov word ptr [bp-4],offset DGROUP:__streams
    jmp short test_stream_limit
inspect_open_stream:
    les bx, dword ptr [bp-4]
    test byte ptr es:[bx+FILE_FLAGS], F_RDWR
    je short advance_stream
    push word ptr [bp-2]
    push bx

org 0
__xfclose label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov word ptr [bp-6], 0
    mov word ptr [bp-2], ds
_TEXT ends
end
