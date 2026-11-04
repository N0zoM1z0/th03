; Reconstructed Borland 16-bit large-model JISALPHA.
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
public _jisalpha

_jisalpha:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ax, 8260h
    jb label_0012
    cmp ax, 8279h
    jbe label_001c

label_0012:
    cmp ax, 8281h
    jb label_0021
    cmp ax, 829ah
    ja label_0021

label_001c:
    mov ax, 1
    jmp short label_0023

label_0021:
    xor ax, ax

label_0023:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
