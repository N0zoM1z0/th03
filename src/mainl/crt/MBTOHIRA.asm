; Reconstructed Borland 16-bit large-model MBTOHIRA.
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
public __mbctohira

__mbctohira:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ax, 8340h
    jb label_0024
    cmp ax, 8393h
    ja label_0024
    cmp ax, 837fh
    je label_0024
    cmp ax, 837fh
    jae label_0021
    sub ax, 0a1h
    jmp short label_0024

label_0021:
    sub ax, 0a2h

label_0024:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
