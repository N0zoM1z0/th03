; Reconstructed Borland 16-bit large-model fstricmp.
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
public __fstricmp

__fstricmp:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, ds
    cld
    lds si, dword ptr [bp + 6]
    les di, dword ptr [bp + 0ah]
    xor ax, ax
    mov bx, ax
    mov cx, 617ah

label_0015:
    lodsb
    mov bl, byte ptr es:[di]
    or al, al
    je label_0039
    scasb
    je label_0015
    cmp al, ch
    jb label_002a
    cmp al, cl
    ja label_002a
    sub al, 20h

label_002a:
    cmp bl, ch
    jb label_0035
    cmp bl, cl
    ja label_0035
    sub bl, 20h

label_0035:
    cmp al, bl
    je label_0015

label_0039:
    sub ax, bx
    mov ds, dx
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
