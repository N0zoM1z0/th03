; Original Borland far-heap binary search over counted FAR elements.
; Use original near 32-bit multiply/add helpers, true caller-supplied
; FAR comparison callback and native unsigned count update.
.8086
extrn N_LXMUL@:near
extrn N_PADD@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __hbsearch
__hbsearch proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short check_remaining
next_middle:
    mov ax,[bp+0eh]
    shr ax,1
    mov [bp-0ah],ax
    cwd
    push ax
    mov ax,[bp+10h]
    push dx
    xor dx,dx
    pop cx
    pop bx
    call N_LXMUL@
    push ax
    push dx
    mov dx,[bp-2]
    mov ax,[bp-4]
    pop cx
    pop bx
    call N_PADD@
    mov [bp-6],dx
    mov [bp-8],ax
    push dx
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call dword ptr [bp+12h]
    add sp,8
    mov dx,ax
    or dx,dx
    jne short compare_direction
    mov dx,[bp-6]
    mov ax,[bp-8]
    jmp short return_search
compare_direction:
    or dx,dx
    jge short advance_search
    mov ax,[bp-0ah]
    jmp short update_count
advance_search:
    mov bx,[bp+10h]
    xor cx,cx
    mov dx,[bp-6]
    mov ax,[bp-8]
    call N_PADD@
    mov [bp-2],dx
    mov [bp-4],ax
    mov ax,[bp+0eh]
    sub ax,[bp-0ah]
    dec ax
update_count:
    mov [bp+0eh],ax
check_remaining:
    cmp word ptr [bp+0eh],0
    ja short next_middle
    xor dx,dx
    xor ax,ax
return_search:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__hbsearch endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
