; Reconstructed Borland 16-bit large-model fstrnicm.
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
public __fstrnicmp

__fstrnicmp:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    cld
    lds si, dword ptr [bp + 6]
    les di, dword ptr [bp + 0ah]
    mov cx, word ptr [bp + 0eh]
    xor ax, ax
    mov bx, ax
    mov dx, 617ah

label_0017:
    jcxz label_003d
    lodsb
    mov bl, byte ptr es:[di]
    or al, al
    je label_003d
    scasb
    loope label_0017
    cmp al, dh
    jb label_002e
    cmp al, dl
    ja label_002e
    sub al, 20h

label_002e:
    cmp bl, dh
    jb label_0039
    cmp bl, dl
    ja label_0039
    sub bl, 20h

label_0039:
    cmp al, bl
    je label_0017

label_003d:
    sub ax, bx
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
