; Borland 8086 DOS far-cdecl strspn.
; Count the maximal text prefix whose bytes appear in a far set string.
; Both pointers are far; the temporary set pointer lives at SS:[BP-4].
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strspn
_strspn proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    xor cx,cx
    jmp short text_head
restart_accept:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short accept_head
compare_accept:
    les bx,dword ptr [bp+6]
    mov al,es:[bx]
    les bx,dword ptr [bp-4]
    cmp al,es:[bx]
    je short matched
    inc word ptr [bp-4]
accept_head:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    jne short compare_accept
matched:
    les bx,dword ptr [bp-4]
    cmp byte ptr es:[bx],0
    je short done
    inc word ptr [bp+6]
    inc cx
text_head:
    les bx,dword ptr [bp+6]
    cmp byte ptr es:[bx],0
    jne short restart_accept
done:
    mov ax,cx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strspn endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
; This original zero-sized group is DATA before BSS in the OMF.
DGROUP group _BSS,_DATA
end
