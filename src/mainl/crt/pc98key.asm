; Reconstructed Borland 16-bit large-model pc98key.
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
public _pc98key

_pc98key:
    push bp
    mov bp, sp
    push si
    push di
    mov al, byte ptr [bp + 8]
    mov ah, byte ptr [bp + 6]
    int 18h
    xchg dx, ax
    mov al, byte ptr [bp + 6]
    cmp al, 1
    je label_0021
    cmp al, 2
    je label_0029
    cmp al, 4
    je label_0027
    cmp al, 5
    jne label_002b

label_0021:
    or bh, bh
    jne label_002b
    xor dx, dx

label_0027:
    mov dl, dh

label_0029:
    xor dh, dh

label_002b:
    xchg dx, ax
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
