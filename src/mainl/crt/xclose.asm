; Original Japanese Borland xclose: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn __nfile:word
extrn _close:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __xclose
; Complete disjoint instruction chunks preserve original native field order.

org 30
    cmp ax, word ptr DGROUP:__nfile
    jb short close_next_descriptor
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 18
    call _close
    pop cx
    inc word ptr [bp-2]
test_descriptor_limit:
    mov ax, word ptr [bp-2]

org 0
__xclose label far
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov word ptr [bp-2], 2
    jmp short test_descriptor_limit
close_next_descriptor:
    push word ptr [bp-2]
_TEXT ends
end
