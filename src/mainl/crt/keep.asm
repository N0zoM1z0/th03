; Original Japanese Borland CRT keep: native 16-bit DOS system call.
; Keep real register/flag semantics and near/far error ABI.
.8086
extrn __restorezero:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _keep
_keep proc far
    push bp
    mov bp,sp
    push si
    push di
    call __restorezero
    mov dx,[bp+8]
    mov al,[bp+6]
    mov ah,31h
    int 21h
    pop di
    pop si
    pop bp
    retf
_keep endp
_TEXT ends
end
