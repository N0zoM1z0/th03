; Original Japanese Borland CRT member ostends
; C++ ends inserts original NUL character into ostream.
; Complete 16-bit ABI and imported target relocations, no patched objects.
.8086
extrn @ostream@$blsh$qc:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ends$qm7ostream

@ends$qm7ostream:
    push bp
    mov bp,sp
    push si
    push di
    mov al,0
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@$blsh$qc
    add sp,6
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_TEXTA ends
end
