; Original DOS Borland far-cdecl strrchr.
; Seek from the NUL terminator backwards, including the terminator
; itself. The far cursor stays in the original BP-4/BP-2 stack slots.
.8086
extrn _strlen:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _strrchr
_strrchr proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strlen
    pop cx
    pop cx
    inc ax
    mov cx,ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,cx
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short check_remaining
backward:
    dec word ptr [bp-4]
    les bx,dword ptr [bp-4]
    mov al,es:[bx]
    cmp al,[bp+10]
    jne short next_char
    mov dx,[bp-2]
    mov ax,[bp-4]
    jmp short done
next_char:
    dec cx
check_remaining:
    or cx,cx
    jne short backward
    xor dx,dx
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_strrchr endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
