; Reconstructed Borland 16-bit large-model biosdisk.
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
public __ibmpc_biosdisk

__ibmpc_biosdisk:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, byte ptr [bp + 6]
    mov al, byte ptr [bp + 10h]
    les bx, dword ptr [bp + 12h]
    mov cx, word ptr [bp + 0ch]
    shr cx, 1
    shr cx, 1
    and cl, 0c0h
    add cl, byte ptr [bp + 0eh]
    mov ch, byte ptr [bp + 0ch]
    mov dh, byte ptr [bp + 0ah]
    mov dl, byte ptr [bp + 8]
    int 13h
    cmp byte ptr [bp + 6], 8
    jne label_0036
    les bx, dword ptr [bp + 12h]
    mov word ptr es:[bx], cx
    mov word ptr es:[bx + 2], dx

label_0036:
    mov al, ah
    mov ah, 0
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
