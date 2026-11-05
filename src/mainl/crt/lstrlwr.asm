; Entire original Borland Japanese CRT lstrlwr.
; In-place far string lowercase mapping with DS restoration.
; Full native 8086 code, original far ABI and group-frame semantics.
.8086
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __lstrlwr

__lstrlwr:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    les bx,dword ptr __pLocale
    les di,es:[bx+342]
    lds si,[bp+6]
    mov dx,si

lstrlwr_0014:
    xor ah,ah
    mov al,[si]
    test al,al
    jz lstrlwr_0026
    mov bx,ax
    mov al,es:[bx+di]
    mov [si],al
    inc si
    jmp short lstrlwr_0014

lstrlwr_0026:
    mov ax,dx
    mov dx,ds
    pop ds
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
