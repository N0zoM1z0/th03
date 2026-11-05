; Original Borland DOS _putenv: mutable far environment-vector entries.
; Preserve the unchecked 16-bit scanning/replacement/removal and actual
; near-heap vector-growth behavior, not a modern libc putenv implementation.
.8086
extrn _free:far,_malloc:far,__environ:dword,__envSize:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _putenv
_putenv proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les di,dword ptr [bp+6]
    mov ax,es
    or ax,di
    jz short invalid_argument
    mov ah,byte ptr es:[di]
    mov al,'='
    mov cx,0ffffh
    cld
    repne scasb
    not cx
    dec cx
    jz short invalid_argument
    les di,dword ptr __environ
    mov [bp-2],es
    mov bx,es
    or bx,di
    mov [bp-4],di
    jnz short compare_entry
invalid_argument:
    mov ax,0ffffh
    jmp near ptr return_result
next_entry:
    add word ptr [bp-4],4
    les di,dword ptr [bp-4]
compare_entry:
    les di,dword ptr es:[di]
    mov bx,es
    or bx,di
    jz short append_new_entry
    mov al,byte ptr es:[di]
    or al,al
    jz short append_new_entry
    cmp ah,al
    jnz short next_entry
    mov bx,cx
    cmp byte ptr es:[bx+di],'='
    jnz short next_entry
    push ds
    lds si,dword ptr [bp+6]
    repe cmpsb
    pop ds
    xchg cx,bx
    jnz short next_entry
    les di,dword ptr [bp+6]
    mov bx,cx
    inc bx
    mov al,byte ptr es:[bx+di]
    and al,al
    jz short erase_entry
    mov ax,di
    mov dx,es
    les di,dword ptr [bp-4]
    mov word ptr es:[di],ax
    mov word ptr es:[di+2],dx
    jmp short success
erase_entry:
    les di,dword ptr [bp-4]
shift_entry:
    mov dx,word ptr es:[di+6]
    mov ax,word ptr es:[di+4]
    mov word ptr es:[di+2],dx
    mov word ptr es:[di],ax
    add di,4
    or ax,dx
    jnz short shift_entry
    jmp short success
append_new_entry:
    mov bx,[bp-4]
    sub bx,word ptr __environ
    add bx,4
    cmp bx,word ptr __envSize
    jc short capacity_available
    add bx,16
    push bx
    call _malloc
    pop cx
    mov di,ax
    mov es,dx
    mov bx,ax
    or bx,dx
    jnz short memory_allocated
    jmp near ptr invalid_argument
memory_allocated:
    xchg cx,word ptr __envSize
    push cx
    push ds
    lds si,dword ptr __environ
    rep movsb
    pop ds
    xchg ax,word ptr __environ
    xchg dx,word ptr __environ+2
    push dx
    push ax
    call _free
    add sp,4
    pop bx
capacity_available:
    les di,dword ptr __environ
    mov ax,[bp+6]
    xchg ax,word ptr es:[bx+di-4]
    mov word ptr es:[bx+di],ax
    mov ax,[bp+8]
    xchg ax,word ptr es:[bx+di-2]
    mov word ptr es:[bx+di+2],ax
success:
    xor ax,ax
return_result:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_putenv endp
_TEXT ends
end
