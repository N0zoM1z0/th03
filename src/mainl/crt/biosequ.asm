; Reconstructed Borland 16-bit large-model biosequ.
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
public __ibmpc_biosequip,__ibmpc_biosmemory,__ibmpc_biostime

__ibmpc_biosequip:
    push si
    push di
    int 11h
    pop di
    pop si
    retf

__ibmpc_biosmemory:
    push si
    push di
    int 12h
    pop di
    pop si
    retf

__ibmpc_biostime:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    mov cx, word ptr [bp + 0ah]
    mov dx, word ptr [bp + 8]
    int 1ah
    xchg dx, ax
    mov dx, cx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
