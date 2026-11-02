; Borland DOS large-model far cdecl strncpy, including original
; counted NUL scan, transfer and zero-fill phases.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strncpy
_strncpy proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    les di,dword ptr [bp+10]
    mov si,di
    xor al,al
    mov bx,[bp+14]
    mov cx,bx
    repne scasb
    sub bx,cx
    push ds
    mov di,es
    mov ds,di
    les di,dword ptr [bp+6]
    xchg cx,bx
    rep movsb
    mov cx,bx
    rep stosb
    pop ds
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_strncpy endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
