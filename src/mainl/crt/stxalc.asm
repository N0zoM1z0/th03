; Original Japanese Borland large-model CRT member: ios::xalloc.
; Real far-call ABI and symbolic relocation; no target byte payload.
.8086
extrn @ios@usercount:word
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@xalloc$qv
@ios@xalloc$qv proc far
    push si
    push di
    inc word ptr DGROUP:@ios@usercount
    mov ax,word ptr DGROUP:@ios@usercount
    pop di
    pop si
    retf
@ios@xalloc$qv endp
_TEXTA ends
end
