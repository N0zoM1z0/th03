; Original Borland DOS keyboard input-ready / buffered-character ownership.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
public __cFlag,__cChar
__cFlag db 0
__cChar db 0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _kbhit
_kbhit proc far
    push si
    push di
    cmp byte ptr DGROUP:__cFlag,0
    je query_dos
    mov ax,1
    jmp short finished
query_dos:
    mov ah,0bh
    int 21h
    cbw
finished:
    pop di
    pop si
    retf
_kbhit endp
_TEXT ends
end
