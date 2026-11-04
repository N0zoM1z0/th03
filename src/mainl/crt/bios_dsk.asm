; Reconstructed Borland 16-bit large-model bios_dsk.
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
public __ibmpc_bios_disk

__ibmpc_bios_disk:
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp + 8]
    mov ah, byte ptr [bp + 6]
    mov al, byte ptr es:[bx + 8]
    mov cx, word ptr es:[bx + 4]
    shr cx, 1
    shr cx, 1
    and cl, 0c0h
    add cl, byte ptr es:[bx + 6]
    mov ch, byte ptr es:[bx + 4]
    mov dh, byte ptr es:[bx + 2]
    mov dl, byte ptr es:[bx]
    les bx, dword ptr es:[bx + 0ah]
    int 13h
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
