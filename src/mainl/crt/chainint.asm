; Original Japanese Borland chainint: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __chain_intr
; Complete disjoint instruction chunks follow original OMF field chronology.

org 0
__chain_intr label far
    pop ax
    pop ax
    mov bx, word ptr [bp+0eh]
    mov ax, word ptr [bp+010h]
    pop word ptr [bp+0eh]
    pop word ptr [bp+010h]
    mov sp, bp
    pop bp
    pop di
    pop si
    pop ds
    pop es
    pop dx
    pop cx
    cli
    retf
_TEXT ends
end
