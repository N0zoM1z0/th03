; Original Japanese Borland MBISPRN: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __ctype:byte
extrn __mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ismbcprint
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 65
    test byte ptr DGROUP:__mbctype[bx+1], 3
    je short not_printable
printable:
    mov ax, 1
    jmp short printable_return
not_printable:
    xor ax, ax
printable_return:
    pop di
    pop si
    pop bp
    retf

org 52
    test byte ptr DGROUP:__ctype[bx+1], 0deh
    jne short printable
    mov al, dl
    mov ah, 0
    mov bx, ax

org 37
    test byte ptr DGROUP:__mbctype[bx+1], 8
    je short not_printable
    jmp short printable
check_single_byte:
    mov al, dl
    mov ah, 0
    mov bx, ax

org 24
    test byte ptr DGROUP:__mbctype[bx+1], 4
    je short not_printable
    mov al, dl
    mov ah, 0
    mov bx, ax

org 0
__ismbcprint label far
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp+6]
    cmp dx, 0ffh
    jbe short check_single_byte
    mov ax, dx
    mov cl, 8
    shr ax, cl
    mov ah, 0
    mov bx, ax
_TEXT ends
end
