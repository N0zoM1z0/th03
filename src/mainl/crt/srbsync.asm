; Reconstructed Japanese original Borland CRT srbsync.
; Original 16-bit ABI, real instructions and symbolic references.
.8086
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@sync$qv
@strstreambuf@sync$qv proc far
    push si
    push di
    xor ax,ax
    pop di
    pop si
    retf
@strstreambuf@sync$qv endp
_TEXTA ends
end
