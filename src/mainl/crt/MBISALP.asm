; Full original Japanese Borland C++ CRT multi-byte classifier MBISALP
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
public __ismbcalpha

__ismbcalpha:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    jna mbisalp_0011
    xor ax,ax
    jmp short mbisalp_001c

mbisalp_0011:
    mov bx,ax
    mov al,DGROUP:__ctype[bx+1]
    mov ah,0
    and ax,12

mbisalp_001c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
