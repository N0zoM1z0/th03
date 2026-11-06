; Original Japanese Borland srchenv: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn _getenv:far
extrn __searchstr:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
empty_environment_value db 0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __searchenv
; Complete disjoint instruction chunks preserve original native field order.

org 57
    call __searchstr
    add sp, 0ch
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 34
    mov word ptr [bp-4],offset DGROUP:empty_environment_value
search_environment_string:
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 14
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short search_environment_string
    mov word ptr [bp-2], ds

org 0
__searchenv label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
end
