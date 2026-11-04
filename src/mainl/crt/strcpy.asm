; Original Borland far strcpy, including terminating NUL.
; Source length is scanned by SCASB; bytes are copied with far REP MOVSB.
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
public _strcpy
_strcpy proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    les di,[bp+10]
    mov si,di
    xor al,al
    mov cx,-1
    repne scasb
    not cx
    push ds
    mov ax,es
    mov ds,ax
    les di,[bp+6]
    rep movsb
    pop ds
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_strcpy endp
_TEXT ends
end
