; Reconstructed Borland 16-bit large-model pc98gfnt.
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
public _pc98getfont

_pc98getfont:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ah, 80h
    jbe label_001d
    cmp al, 80h
    adc al, 61h
    jb label_0015
    sub al, 0a2h

label_0015:
    rcl ah, 1
    and ah, 7fh
    add ax, 1f21h

label_001d:
    xor dx, dx
    mov es, dx
    test byte ptr es:[501h], 8
    push ds
    je label_0031
    lds bx, dword ptr [bp + 8]
    mov dh, 1fh
    jmp short label_0039

label_0031:
    mov cx, word ptr [bp + 8]
    mov bx, word ptr [bp + 0ah]
    mov dh, 14h

label_0039:
    xchg dx, ax
    int 18h
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
