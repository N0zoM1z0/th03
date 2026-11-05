; Original Japanese Borland large-model CRT member: gexit.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn _exit:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __graphexit
__graphexit proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+6]
    call _exit
    pop cx
    pop di
    pop si
    pop bp
    retf
__graphexit endp
_TEXT ends
end
