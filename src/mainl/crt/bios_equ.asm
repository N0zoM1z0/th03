; Reconstructed Borland 16-bit large-model bios_equ.
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
public __ibmpc_bios_equiplist,__ibmpc_bios_memsize,__ibmpc_bios_timeofday

__ibmpc_bios_equiplist:
    push si
    push di
    int 11h
    pop di
    pop si
    retf

__ibmpc_bios_memsize:
    push si
    push di
    int 12h
    pop di
    pop si
    retf

__ibmpc_bios_timeofday:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    les bx, dword ptr [bp + 8]
    mov cx, word ptr es:[bx + 2]
    mov dx, word ptr es:[bx]
    int 1ah
    cmp byte ptr [bp + 6], 0
    jne label_002f
    mov word ptr es:[bx], dx
    mov word ptr es:[bx + 2], cx

label_002f:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
