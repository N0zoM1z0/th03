; Original Borland near/far ungetch with a single saved keyboard byte.
.8086
extrn __cFlag:byte,__cChar:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __Nungetch,_ungetch
__Nungetch:
    pop ax
    push cs
    push ax
_ungetch proc far
    push bp
    mov bp,sp
    push si
    push di
    cmp byte ptr DGROUP:__cFlag,0
    je store_byte
    mov ax,-1
    jmp short finished
store_byte:
    mov byte ptr DGROUP:__cFlag,1
    mov al,byte ptr [bp+6]
    mov byte ptr DGROUP:__cChar,al
    mov ah,0
finished:
    pop di
    pop si
    pop bp
    retf
_ungetch endp
_TEXT ends
end
