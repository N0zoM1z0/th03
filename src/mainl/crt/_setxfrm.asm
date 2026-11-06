; Original Japanese Borland _setxfrm: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
include locale_fields.inc
extrn _strcmp:far
extrn _strxfrm:far
extrn __strxfrm:far
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
c_locale_name db 'C',0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __setstrxfrm
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 75
store_transform:
    les bx, dword ptr DGROUP:__pLocale
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr es:[bx+LOCALE_STRXFRM+2], dx
    mov word ptr es:[bx+LOCALE_STRXFRM], ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 70
    mov word ptr [bp-4],offset __strxfrm

org 65
choose_locale_transform:
    mov word ptr [bp-2],seg __strxfrm

org 58
    mov word ptr [bp-4],offset _strxfrm
    jmp short store_transform

org 53
    mov word ptr [bp-2],seg _strxfrm

org 41
    call _strcmp
    add sp, 8
    or ax, ax
    jne short choose_locale_transform

org 36
    push word ptr DGROUP:__pLocale+2
    push ax

org 30
    mov ax, word ptr DGROUP:__pLocale
    add ax, LOCALE_NAME

org 26
    mov ax,offset DGROUP:c_locale_name
    push ax

org 0
__setstrxfrm label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, word ptr [bp+8]
    jne short store_transform
    push ds
_TEXT ends
end
