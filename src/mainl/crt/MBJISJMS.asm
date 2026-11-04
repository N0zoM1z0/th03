; Reconstructed Borland 16-bit large-model MBJISJMS.
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
public __mbcjistojms

__mbcjistojms:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ah, 21h
    jb label_002a
    cmp ah, 7fh
    jae label_002a
    cmp al, 21h
    jb label_002a
    cmp al, 7fh
    jae label_002a
    sub ax, 0de82h
    rcr ah, 1
    jb label_0025
    cmp al, 0deh
    sbb al, 5eh

label_0025:
    xor ah, 20h
    jmp short label_002c

label_002a:
    xor ax, ax

label_002c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
