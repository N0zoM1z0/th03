; Full original Japanese Borland C++ CRT multi-byte classifier MBTOUPR
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
public __mbctoupper

__mbctoupper:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    ja mbtoupr_0019
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],8
    jz mbtoupr_0019
    sub ax,32

mbtoupr_0019:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
