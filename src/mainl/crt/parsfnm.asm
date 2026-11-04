; Reconstructed Borland 16-bit large-model parsfnm.
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
public _parsfnm

_parsfnm:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    lds si, dword ptr [bp + 6]
    les di, dword ptr [bp + 0ah]
    mov al, byte ptr [bp + 0eh]
    mov ah, 29h
    int 21h
    pop ds
    cmp al, 0ffh
    jne label_001e
    xor dx, dx
    xor ax, ax
    jmp short label_0025

label_001e:
    mov es, word ptr [bp + 8]
    mov ax, si
    mov dx, es

label_0025:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
