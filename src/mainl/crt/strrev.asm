; Original DOS far-cdecl strrev: in-place reversal of a far string.
; DS temporarily selects the input far segment; ES mirrors DS for
; string writes. The original preserves SI,DI,DS and returns DX:AX.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strrev
_strrev proc far
    push bp
    mov bp,sp
    push si
    push di
    cld
    push ds
    lds si,dword ptr [bp+6]
    mov dx,si
    mov di,si
    push ds
    pop es
    xor al,al
    mov cx,0ffffh
    repne scasb
    cmp cx,0fffeh
    je short reversal_done
    dec di
    dec di
    xchg si,di
    jmp short compare_ends
reverse_next:
    mov al,[di]
    xchg byte ptr [si],al
    stosb
    dec si
compare_ends:
    cmp di,si
    jb short reverse_next
reversal_done:
    xchg dx,ax
    mov dx,ds
    pop ds
    pop di
    pop si
    pop bp
    retf
_strrev endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
