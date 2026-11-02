; Original Borland far-cdecl tolower consults the genuine __ctype flag
; table and converts only uppercase bytes, preserving EOF (-1).
.8086
extrn __ctype:byte
public _tolower
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
_tolower label far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,word ptr [bp+6]
    cmp dx,-1
    jne short test_character
    mov ax,0FFFFh
    jmp short finished
test_character:
    mov al,dl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:[bx+__ctype+1],4
    je short not_upper
    mov al,dl
    mov ah,0
    add ax,20h
    jmp short finished
not_upper:
    mov al,dl
    mov ah,0
finished:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
