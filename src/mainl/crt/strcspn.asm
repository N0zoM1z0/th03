; Original DOS far-cdecl strcspn: count bytes until first rejection-set hit.
; The stack local at BP-4 holds the far reject-set cursor; original
; comparisons test the text byte first, then the current set byte.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strcspn
_strcspn proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    xor cx,cx
    jmp short text_head
reset_set:
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
    je short done
    inc word ptr [bp-4]
set_head:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jne short compare_set
    inc word ptr [bp+6]
    inc cx
text_head:
    les bx,dword ptr [bp+6]
    cmp byte ptr es:[bx],0
    jne short reset_set
done:
    mov ax,cx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strcspn endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
