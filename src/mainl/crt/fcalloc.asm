; Original farcalloc on 8086: native 32-bit count multiplication,
; FAR heap allocation, 0xFA00-byte zeroing chunks and near pointer advance.
.8086
extrn _farmalloc:far
extrn _setmem:far
extrn N_LXMUL@:near
extrn N_PADA@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _farcalloc
_farcalloc proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    mov cx,[bp+0ch]
    mov bx,[bp+0ah]
    mov dx,[bp+8]
    mov ax,[bp+6]
    call N_LXMUL@
    mov [bp+8],dx
    mov [bp+6],ax
    push dx
    push ax
    call _farmalloc
    pop cx
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    je short calloc_return
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    jmp short calloc_count
calloc_next_chunk:
    cmp word ptr [bp+8],0
    jb short calloc_remaining
    ja short calloc_limit
    cmp word ptr [bp+6],0fa00h
    jbe short calloc_remaining
calloc_limit:
    mov ax,0fa00h
    jmp short calloc_chosen_chunk
calloc_remaining:
    mov ax,[bp+6]
calloc_chosen_chunk:
    mov [bp-0ah],ax
    mov al,0
    push ax
    push word ptr [bp-0ah]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call _setmem
    add sp,8
    mov bx,[bp-0ah]
    xor cx,cx
    mov dx,ss
    lea ax,[bp-8]
    call N_PADA@
    mov ax,[bp-0ah]
    sub word ptr [bp+6],ax
    sbb word ptr [bp+8],0
calloc_count:
    mov ax,[bp+6]
    or ax,word ptr [bp+8]
    jne short calloc_next_chunk
calloc_return:
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_farcalloc endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
