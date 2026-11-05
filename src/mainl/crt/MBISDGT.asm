; Full original Japanese Borland C++ CRT multi-byte classifier MBISDGT
; Source retains original 16-bit far ABI, character range and ctype bitmasks.
.8086
extrn __ctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ismbcdigit

__ismbcdigit:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    jna mbisdgt_0011
    xor ax,ax
    jmp short mbisdgt_001c

mbisdgt_0011:
    mov bx,ax
    mov al,DGROUP:__ctype[bx+1]
    mov ah,0
    and ax,2

mbisdgt_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
