; Original Borland DOS far-cdecl strpbrk: first text byte contained
; in a far accept set, returned as a far pointer in DX:AX.
; The two-byte halves of the original local set cursor are at BP-4/-2.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strpbrk
_strpbrk proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    jmp short text_head
restart_set:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short set_head
compare_set:
    les bx,dword ptr [bp+6]
    mov al,es:[bx]
    les bx,dword ptr [bp-4]
    cmp al,es:[bx]
    jne short next_set
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short done
next_set:
    inc word ptr [bp-4]
set_head:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jne short compare_set
    inc word ptr [bp+6]
text_head:
    les bx,dword ptr [bp+6]
    cmp byte ptr es:[bx],0
    jne short restart_set
    xor dx,dx
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strpbrk endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
