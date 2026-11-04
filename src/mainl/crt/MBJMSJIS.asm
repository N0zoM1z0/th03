; Reconstructed Borland 16-bit large-model MBJMSJIS.
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
public __mbcjmstojis

__mbcjmstojis:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp + 6]
    cmp ah, 81h
    jb label_003a
    cmp ah, 0a0h
    jb label_001c
    cmp ah, 0e0h
    jb label_003a
    cmp ah, 0f0h
    jae label_003a

label_001c:
    cmp al, 40h
    jb label_003a
    cmp al, 0fdh
    jae label_003a
    cmp al, 7fh
    je label_003a
    cmp al, 80h
    adc al, 61h
    jb label_0030
    sub al, 0a2h

label_0030:
    rcl ah, 1
    and ah, 7fh
    add ax, 1f21h
    jmp short label_003c

label_003a:
    xor ax, ax

label_003c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
