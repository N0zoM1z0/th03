; Reconstructed Borland 16-bit large-model JISLOWER.
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
public _jislower

_jislower:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ax, 8281h
    jb label_0017
    cmp ax, 829ah
    ja label_0017
    mov ax, 1
    jmp short label_0019

label_0017:
    xor ax, ax

label_0019:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
