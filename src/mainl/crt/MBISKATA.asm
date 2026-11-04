; Reconstructed Borland 16-bit large-model MBISKATA.
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
public __ismbckata

__ismbckata:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ax, 8340h
    jb label_001c
    cmp ax, 8396h
    ja label_001c
    cmp ax, 837fh
    je label_001c
    mov ax, 1
    jmp short label_001e

label_001c:
    xor ax, ax

label_001e:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
