; Original Borland large-model bsearch: far comparator, count and stride.
; Keep the original 16-bit midpoint/element-stride arithmetic and unchecked ABI.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _bsearch
_bsearch proc far
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short have_remaining
try_midpoint:
    mov ax,[bp+14]
    shr ax,1
    mov [bp-10],ax
    imul word ptr [bp+16]
    mov dx,[bp-2]
    mov bx,[bp-4]
    add bx,ax
    mov [bp-6],dx
    mov [bp-8],bx
    push dx
    push bx
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr [bp+18]
    add sp,8
    mov dx,ax
    or dx,dx
    jne unequal
    mov dx,[bp-6]
    mov ax,[bp-8]
    jmp short done
unequal:
    or dx,dx
    jge after_midpoint
    mov ax,[bp-10]
    jmp short update_remaining
after_midpoint:
    mov dx,[bp-6]
    mov ax,[bp-8]
    add ax,[bp+16]
    mov [bp-2],dx
    mov [bp-4],ax
    mov ax,[bp+14]
    sub ax,[bp-10]
    dec ax
update_remaining:
    mov [bp+14],ax
have_remaining:
    cmp word ptr [bp+14],0
    ja try_midpoint
    xor dx,dx
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_bsearch endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
