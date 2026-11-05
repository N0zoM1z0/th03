; Original Japanese Borland large-model CRT member: del.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn _free:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @$bdele$qnv
@$bdele$qnv proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _free
    pop cx
    pop cx
    pop di
    pop si
    pop bp
    retf
@$bdele$qnv endp
_TEXT ends
end
