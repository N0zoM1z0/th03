; Reconstructed Borland 16-bit large-model strupr.
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
public _strupr

_strupr:
    push bp
    mov bp, sp
    push si
    push di
    cld
    push ds
    lds si, dword ptr [bp + 6]
    mov dx, si
    jmp short label_0019

label_000e:
    sub al, 61h
    cmp al, 19h
    ja label_0019
    add al, 41h
    mov byte ptr [si - 1], al

label_0019:
    lodsb
    and al, al
    jne label_000e
    xchg dx, ax
    mov dx, ds
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
