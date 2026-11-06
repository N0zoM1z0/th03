; Original Japanese Borland _setudef: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
include locale_fields.inc
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __setlocalebuff
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 5
    les bx, dword ptr DGROUP:__pLocale
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr es:[bx+LOCALE_USER_BUFFER+2], dx
    mov word ptr es:[bx+LOCALE_USER_BUFFER], ax
    pop di
    pop si
    pop bp
    retf

org 0
__setlocalebuff label far
    push bp
    mov bp, sp
    push si
    push di
_TEXT ends
end
