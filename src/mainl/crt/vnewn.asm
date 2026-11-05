; Original Japanese Borland large-model CRT member: vnewn.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn _abort:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @_vector_new_$qpvuiuiuie
@_vector_new_$qpvuiuiuie proc far
    push si
    push di
    call _abort
    xor ax,ax
    pop di
    pop si
    retf
@_vector_new_$qpvuiuiuie endp
_TEXT ends
end
