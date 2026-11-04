; Reconstructed Borland 16-bit large-model bioscom.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ibmpc_bioscom

__ibmpc_bioscom:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    mov al, byte ptr [bp + 8]
    mov dx, word ptr [bp + 0ah]
    int 14h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
