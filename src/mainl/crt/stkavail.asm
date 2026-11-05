; Original 16-bit far stack availability query: zero on carry.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _stackavail
_stackavail proc far
    mov ax,sp
    mov cx,4
    sub ax,cx
    jc short no_stack
    retf
no_stack:
    xor ax,ax
    retf
_stackavail endp
_TEXT ends
end
