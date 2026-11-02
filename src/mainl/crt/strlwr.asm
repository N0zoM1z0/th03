; Original DOS far-cdecl strlwr: in-place far ASCII lowercase conversion.
; Original intentionally reads through DS:SI using LODSB and returns
; original far pointer in DX:AX with DS restored from stack.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strlwr
_strlwr proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    push ds
    lds si,dword ptr [bp+6]
    mov dx,si
    jmp short read_character
try_uppercase:
    sub al,41h
    cmp al,19h
    ja short read_character
    add al,61h
    mov byte ptr [si-1],al
read_character:
    lodsb
    and al,al
    jne short try_uppercase
    xchg dx,ax
    mov dx,ds
    pop ds
    pop di
    pop si
    pop bp
    retf
_strlwr endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
