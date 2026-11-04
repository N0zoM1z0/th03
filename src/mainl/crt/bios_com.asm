; Reconstructed Borland 16-bit large-model bios_com.
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
public __ibmpc_bios_serialcom

__ibmpc_bios_serialcom:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    mov al, byte ptr [bp + 0ah]
    mov dx, word ptr [bp + 8]
    int 14h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
