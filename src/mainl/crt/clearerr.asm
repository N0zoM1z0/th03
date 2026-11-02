; Original DOS far-cdecl clearerr: reset FILE EOF and error status only.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _clearerr
_clearerr proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    and word ptr es:[bx+2],0FFCFh
    pop di
    pop si
    pop bp
    retf
_clearerr endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
