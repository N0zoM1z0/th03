; Reconstructed Borland 16-bit large-model JTOUPPER.
; Original far ABI, semantic branches and normal assembler source.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _jtoupper

_jtoupper:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    cmp dx, 8281h
    jb label_001b
    cmp dx, 829ah
    ja label_001b
    mov ax, dx
    sub ax, 21h
    jmp short label_001d

label_001b:
    mov ax, dx

label_001d:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
