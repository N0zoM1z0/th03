; Original Japanese Borland large-model CRT member: newarray.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn @$bnew$qui:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @$bnwa$qui
@$bnwa$qui proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+6]
    call @$bnew$qui
    pop cx
    pop di
    pop si
    pop bp
    retf
@$bnwa$qui endp
_TEXT ends
end
