; Original Japanese Borland setlocal: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn _strcmp:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
c_locale_name db 'C',0
accepted_c_locale_name db 'C',0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setlocale
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 38
    call _strcmp
    add sp, 8
    or ax, ax
    je short return_requested_locale
    xor dx, dx
    xor ax, ax
    jmp short setlocale_return
return_requested_locale:
    mov dx, word ptr [bp+0ah]
    mov ax, word ptr [bp+8]
setlocale_return:
    pop di
    pop si
    pop bp
    retf

org 30
    mov ax,offset DGROUP:accepted_c_locale_name
    push ax
    push word ptr [bp+0ah]
    push bx

org 15
    mov ax,offset DGROUP:c_locale_name
    jmp short setlocale_return
check_locale_request:
    les bx, dword ptr [bp+8]
    cmp byte ptr es:[bx], 0
    je short return_requested_locale
    push ds

org 0
_setlocale label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+8]
    or ax, word ptr [bp+0ah]
    jne short check_locale_request
    mov dx, ds
_TEXT ends
end
