; Reconstructed Borland 16-bit large-model dosext.
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
public _dosexterr

_dosexterr:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    push bp
    mov bx, 0
    mov ah, 59h
    int 21h
    pop bp
    lds di, dword ptr [bp + 6]
    mov word ptr [di], ax
    mov byte ptr [di + 2], bh
    mov byte ptr [di + 3], bl
    mov byte ptr [di + 4], ch
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
