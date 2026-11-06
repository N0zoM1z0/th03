; Shared DOS runtime: original ABI, unchecked widths and literal field order.
.8086
extrn _malloc:far,_strlen:far,__stpcpy:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __DOSENV
__DOSENV label near
org 36
environment_count label near
org 61
environment_count_test label near
org 82
environment_counted label near
org 112
total_counted label near
org 122
environment_allocate label near
org 148
environment_allocated label near
org 199
environment_copy label near
org 243
environment_copy_test label near
org 266
write_empty_environment label near
org 276
write_environment_end label near
org 342
environment_return label near
org 353
environment_failed label near
org 357
environment_done label near
org 243
    les bx,[bp-4]
    mov ax,es:[bx]
    or ax,es:[bx+2]
    je write_environment_end
    les bx,es:[bx]
    cmp byte ptr es:[bx],0
    jne environment_copy
    jmp short write_environment_end
    les bx,[bp-10]
    mov byte ptr es:[bx],0
    inc word ptr [bp-10]
    les bx,[bp-10]
    mov byte ptr es:[bx],0
    inc word ptr [bp-10]
    mov ax,[bp+8]
    or ax,[bp+10]
    je environment_return
    les bx,[bp-10]
    mov word ptr es:[bx],1
    add word ptr [bp-10],2
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp-8]
    push word ptr [bp-10]
    call __stpcpy
    add sp,8
    mov [bp-8],dx
    mov [bp-10],ax
    les bx,[bp-10]
    mov byte ptr es:[bx],0
    inc word ptr [bp-10]
    mov dx,[bp-8]
    mov ax,[bp-10]
    sub ax,[bp-6]
    jmp short environment_done
    xor dx,dx
    xor ax,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 12
org 148
    les bx,[bp+4]
    mov ax,[bp-10]
    mov es:[bx+2],dx
    mov es:[bx],ax
    add word ptr [bp-10],15
    and word ptr [bp-10],0fff0h
    mov dx,[bp+14]
    mov ax,[bp+12]
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    je write_empty_environment
    les bx,[bp-4]
    mov ax,es:[bx]
    or ax,es:[bx+2]
    je write_empty_environment
    jmp short environment_copy_test
    les bx,[bp-4]
    add word ptr [bp-4],4
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push word ptr [bp-8]
    push word ptr [bp-10]
    call __stpcpy
    add sp,8
    mov [bp-8],dx
    mov [bp-10],ax
    les bx,[bp-10]
    mov byte ptr es:[bx],0
    inc word ptr [bp-10]
org 112
    cmp word ptr [bp-6],8000h
    jb environment_allocate
    jmp environment_failed
    mov ax,[bp-6]
    add ax,word ptr 15
    push ax
    call _malloc
    pop cx
    mov [bp-8],dx
    mov [bp-10],ax
    or ax,dx
    jne environment_allocated
    jmp environment_failed
org 82
    inc word ptr [bp-6]
    mov ax,[bp+8]
    or ax,[bp+10]
    je total_counted
    push word ptr [bp+10]
    push word ptr [bp+8]
    call _strlen
    pop cx
    pop cx
    add ax,word ptr 3
    add [bp-6],ax
org 0
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    ; BP-4/-2 environment cursor, BP-6 required bytes,
    ; BP-10/-8 destination cursor. Keep offset-only pointer arithmetic.
    mov word ptr [bp-6],1
    mov dx,[bp+14]
    mov ax,[bp+12]
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    je environment_counted
    mov word ptr [bp-6],0
    jmp short environment_count_test
    les bx,[bp-4]
    add word ptr [bp-4],4
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call _strlen
    pop cx
    pop cx
    inc ax
    add [bp-6],ax
    les bx,[bp-4]
    mov ax,es:[bx]
    or ax,es:[bx+2]
    je environment_counted
    les bx,es:[bx]
    cmp byte ptr es:[bx],0
    jne environment_count
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
