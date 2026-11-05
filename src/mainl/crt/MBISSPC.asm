; Full original Japanese Borland C++ CRT multi-byte classifier MBISSPC
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
public __ismbcspace

__ismbcspace:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    jna mbisspc_0011
    xor ax,ax
    jmp short mbisspc_001c

mbisspc_0011:
    mov bx,ax
    mov al,DGROUP:__ctype[bx+1]
    mov ah,0
    and ax,1

mbisspc_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
