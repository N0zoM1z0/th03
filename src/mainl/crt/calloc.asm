; Borland large-model calloc: multiply two size_t arguments, reject overflow,
; malloc the resulting word count, then zero the allocated far pointer.
; Retain the original empty-pointer and helper calling conventions.
.8086
extrn _malloc:far,_setmem:far,N_LXMUL@:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _calloc
_calloc proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov bx,[bp+6]
    xor cx,cx
    mov ax,[bp+8]
    xor dx,dx
    call N_LXMUL@
    mov [bp-2],dx
    mov [bp-4],ax
    cmp word ptr [bp-2],0
    jb allocate
    ja out_of_range
    cmp word ptr [bp-4],-1
    jbe allocate
out_of_range:
    xor dx,dx
    xor ax,ax
    jmp short remember
allocate:
    push word ptr [bp-4]
    call _malloc
    pop cx
remember:
    mov [bp-6],dx
    mov [bp-8],ax
    or ax,[bp-6]
    je result
    mov al,0
    push ax
    push word ptr [bp-4]
    push dx
    push word ptr [bp-8]
    call _setmem
    add sp,8
result:
    mov dx,[bp-6]
    mov ax,[bp-8]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_calloc endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
