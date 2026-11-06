; Original Japanese Borland _setcoll: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
include locale_fields.inc
extrn _strcmp:far
extrn __strcoll:far
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
public __setstrcoll
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 80
store_collator:
    les bx, dword ptr DGROUP:__pLocale
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr es:[bx+LOCALE_STRCOLL+2], dx
    mov word ptr es:[bx+LOCALE_STRCOLL], ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 61
    mov word ptr [bp-4],offset __strcoll
    jmp short store_collator
use_explicit_collator:
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax

org 56
choose_locale_collator:
    mov word ptr [bp-2],seg __strcoll

org 49
    mov word ptr [bp-4],offset _strcmp
    jmp short store_collator

org 44
    mov word ptr [bp-2],seg _strcmp

org 32
    call _strcmp
    add sp, 8
    or ax, ax
    jne short choose_locale_collator

org 27
    push word ptr DGROUP:__pLocale+2
    push ax

org 21
    mov ax, word ptr DGROUP:__pLocale
    add ax, LOCALE_NAME

org 17
    mov ax,offset DGROUP:c_locale_name
    push ax

org 0
__setstrcoll label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    jne short use_explicit_collator
    push ds
_TEXT ends
end
