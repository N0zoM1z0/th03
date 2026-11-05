; Full original Japanese Borland C++ CRT multi-byte classifier MBTOLWR
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
public __mbctolower

__mbctolower:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    cmp ax,255
    ja mbtolwr_0019
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],4
    jz mbtolwr_0019
    add ax,32

mbtolwr_0019:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
