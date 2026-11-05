; Entire original Borland Japanese CRT ltoupper.
; Locale-specific per-byte uppercase map through offset 015Ah.
; Full native 8086 code, original far ABI and group-frame semantics.
.8086
extrn __pLocale:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __ltoupper

__ltoupper:
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    cmp dx,-1
    jnz ltoupper_0012
    mov ax,65535
    jmp short ltoupper_0027

ltoupper_0012:
    les bx,dword ptr DGROUP:__pLocale
    les bx,es:[bx+346]
    mov ax,dx
    and ax,255
    add bx,ax
    mov al,es:[bx]
    mov ah,0

ltoupper_0027:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
