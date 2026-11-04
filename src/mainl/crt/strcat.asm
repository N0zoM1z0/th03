; Original Borland far strcat: locate terminator, then copy in aligned words.
; Retain ES/DS ownership, count including the NUL byte, and far return.
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
public _strcat
_strcat proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    push ds
    les di,[bp+6]
    mov dx,di
    xor al,al
    mov cx,-1
    repne scasb
    push es
    lea si,[di-1]
    les di,[bp+10]
    mov cx,-1
    repne scasb
    not cx
    sub di,cx
    push es
    pop ds
    pop es
    xchg si,di
    test si,1
    je aligned
    movsb
    dec cx
aligned:
    shr cx,1
    rep movsw
    jae copied
    movsb
copied:
    xchg dx,ax
    mov dx,es
    pop ds
    pop di
    pop si
    pop bp
    retf
_strcat endp
_TEXT ends
end
