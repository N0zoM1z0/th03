; Full original Japanese Borland C++ CRT multi-byte classifier MBISLWR
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
public __ismbclower

__ismbclower:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    jna mbislwr_0011
    xor ax,ax
    jmp short mbislwr_001c

mbislwr_0011:
    mov bx,ax
    mov al,DGROUP:__ctype[bx+1]
    mov ah,0
    and ax,8

mbislwr_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
