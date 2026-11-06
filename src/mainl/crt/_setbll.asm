; Original Japanese Borland _setbll: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn ___find_localelib:far
extrn __LocaleLibName:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __setlocalelib
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 39
    mov ax,offset DGROUP:__LocaleLibName
locale_library_return:
    pop di
    pop si
    pop bp
    retf

org 19
    call ___find_localelib
    pop cx
    pop cx
    cmp ax, 0ffffh
    jne short return_locale_library_name
    xor dx, dx
    xor ax, ax
    jmp short locale_library_return
return_locale_library_name:
    mov dx, ds

org 0
__setlocalelib label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    je short return_locale_library_name
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
