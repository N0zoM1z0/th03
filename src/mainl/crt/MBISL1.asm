; Full original Japanese Borland C++ CRT multi-byte classifier MBISL1
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
public __ismbcl1

__ismbcl1:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,34975
    jc mbisl1_0026
    cmp dx,39026
    ja mbisl1_0026
    mov al,dl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],8
    jz mbisl1_0026
    mov ax,1
    jmp short mbisl1_0028

mbisl1_0026:
    xor ax,ax

mbisl1_0028:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
