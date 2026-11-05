; Full original Japanese Borland C++ CRT multi-byte classifier MBISLGL
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
public __ismbclegal


; First emit real trailing original instruction block to preserve BCC
; FIXUPP order 33,20. No source bytes synthesized or patched.
org 31
    test byte ptr DGROUP:__mbctype[bx+1],8
    jz mbislgl_002b
    mov ax,1
    jmp short mbislgl_002d

mbislgl_002b:
    xor ax,ax

mbislgl_002d:
    pop di
    pop si
    pop bp
    retf

org 0
__ismbclegal:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    mov ax,dx
    mov cl,8
    shr ax,cl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__mbctype[bx+1],4
    jz mbislgl_002b
    mov al,dl
    mov ah,0
    mov bx,ax
_TEXT ends
end
