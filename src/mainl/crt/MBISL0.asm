; Full original Japanese Borland C++ CRT multi-byte classifier MBISL0
; Source retains original 16-bit far ABI, character range and ctype bitmasks.
.8086
extrn __mbctype:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ismbcl0

__ismbcl0:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,33088
    jc mbisl0_0026
    cmp dx,34974
    ja mbisl0_0026
    mov al,dl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],8
    jz mbisl0_0026
    mov ax,1
    jmp short mbisl0_0028

mbisl0_0026:
    xor ax,ax

mbisl0_0028:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
