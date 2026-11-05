; Entire original Borland Japanese CRT ftoupper.
; Original global __ctype plus-one bit-test and ASCII fold uppercase.
; Full native 8086 code, original far ABI and group-frame semantics.
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
public __ftoupper

__ftoupper:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,-1
    jnz ftoupper_0012
    mov ax,65535
    jmp short ftoupper_002c

ftoupper_0012:
    mov al,dl
    mov ah,0
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],8
    jz ftoupper_0028
    mov al,dl
    mov ah,0
    add ax,65504
    jmp short ftoupper_002c

ftoupper_0028:
    mov al,dl
    mov ah,0

ftoupper_002c:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
