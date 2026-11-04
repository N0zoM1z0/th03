; Reconstructed Borland 16-bit large-model pc98prnt.
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
public _pc98print

_pc98print:
    push bp
    mov bp, sp
    push si
    push di
    mov cx, word ptr [bp + 8]
    mov bx, word ptr [bp + 0ah]
    mov es, word ptr [bp + 0ch]
    mov ah, byte ptr [bp + 6]
    mov al, cl
    int 1ah
    cmp byte ptr [bp + 6], 30h
    jne label_001c
    xchg cx, ax

label_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
