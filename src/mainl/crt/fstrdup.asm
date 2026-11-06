; Original Japanese Borland fstrdup: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __fmemcpy:far
extrn __fstrlen:far
extrn __ffarmalloc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fstrdup
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 61
    call __fmemcpy
    add sp, 0ah
duplicate_return:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 31
    call __ffarmalloc
    pop cx
    pop cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    je short duplicate_return
    push word ptr [bp-6]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push dx
    push word ptr [bp-4]

org 14
    call __fstrlen
    pop cx
    pop cx
    inc ax
    mov word ptr [bp-6], ax
    xor ax, ax
    push ax
    push word ptr [bp-6]

org 0
__fstrdup label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
