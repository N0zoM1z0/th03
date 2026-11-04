; Reconstructed Borland 16-bit large-model cibmsond.
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
public ___ibm_sound,___ibm_nosound

___ibm_sound:
    push bp
    mov bp, sp
    push si
    push di
    mov bx, word ptr [bp + 6]
    mov ax, 34ddh
    mov dx, 12h
    cmp dx, bx
    jae label_002c
    div bx
    mov bx, ax
    in al, 61h
    test al, 3
    jne label_0024
    or al, 3
    out 61h, al
    mov al, 0b6h
    out 43h, al

label_0024:
    mov al, bl
    out 42h, al
    mov al, bh
    out 42h, al

label_002c:
    pop di
    pop si
    pop bp
    retf

___ibm_nosound:
    push si
    push di
    in al, 61h
    and al, 0fch
    out 61h, al
    pop di
    pop si
    retf
_TEXT ends
end
