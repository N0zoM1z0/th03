; Original Borland buffered single key or DOS 21h AH=07h without echo.
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
public _getch
_getch proc far
    push si
    push di
    cmp byte ptr DGROUP:__cFlag,0
    je read_dos
    mov byte ptr DGROUP:__cFlag,0
    mov al,byte ptr DGROUP:__cChar
    jmp short result
read_dos:
    mov ax,0700h
    int 21h
result:
    mov ah,0
    pop di
    pop si
    retf
_getch endp
_TEXT ends
end
