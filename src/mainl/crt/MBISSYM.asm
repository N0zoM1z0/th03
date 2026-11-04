; Reconstructed Borland 16-bit large-model MBISSYM.
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
public __ismbcsymbol

__ismbcsymbol:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ax, 8141h
    jb label_001c
    cmp ax, 81ach
    ja label_001c
    cmp ax, 817fh
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
