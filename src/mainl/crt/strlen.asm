; DOS large-model far-cdecl strlen; preserve the original null far-pointer
; fast path and the 16-bit REPNE SCASB counter arithmetic.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strlen
_strlen proc far
    push bp
    mov bp,sp
    push si
    push di
    les di,dword ptr [bp+6]
    xor ax,ax
    cmp ax,[bp+8]
    jne short scan_string
    cmp ax,di
    je short string_done
scan_string:
    cld
    mov cx,0FFFFh
    repne scasb
    xchg cx,ax
    not ax
    dec ax
string_done:
    pop di
    pop si
    pop bp
    retf
_strlen endp
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
