; Original Japanese Borland large-model CRT member: coreleft.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn _farcoreleft:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _coreleft
_coreleft proc far
    push si
    push di
    call _farcoreleft
    pop di
    pop si
    retf
_coreleft endp
_TEXT ends
end
