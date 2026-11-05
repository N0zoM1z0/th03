; Original Borland vector-delete dispatch for FAR arrays with hidden
; array-ownership flags, optional heap pointer adjustment and
; reference-destructor count. Keeps original unchecked 16-bit ABI.
.8086
extrn @_vector_delete_$qnvuiuluie:far
extrn @__RefDestructorCount$qv:far
extrn N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @_vector_delete_$qnvuiuiuluie
@_vector_delete_$qnvuiuiuluie proc far
    push bp
    mov bp,sp
    sub sp,0eh
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short nonnull_array
    xor dx,dx
    xor ax,ax
    jmp near ptr return_array
nonnull_array:
    lea ax,[bp+14h]
    mov [bp-2],ss
    mov [bp-4],ax
    test byte ptr [bp+12h],1
    jz short near_dtor_count
    add word ptr [bp-4],4
    les bx,dword ptr [bp-4]
    mov dx,word ptr es:[bx-2]
    mov ax,word ptr es:[bx-4]
    mov [bp-8],dx
    mov [bp-0ah],ax
    jmp short read_array_length
near_dtor_count:
    add word ptr [bp-4],2
    les bx,dword ptr [bp-4]
    mov ax,word ptr es:[bx-2]
    mov [bp-6],ax
read_array_length:
    test byte ptr [bp+12h],10h
    jz short size_from_args
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx-2]
    mov ax,word ptr es:[bx-4]
    jmp short save_array_size
size_from_args:
    mov dx,[bp+10h]
    mov ax,[bp+0eh]
save_array_size:
    mov [bp-0ch],dx
    mov [bp-0eh],ax
    mov bx,[bp+0ah]
    xor cx,cx
    mov dx,[bp-0ch]
    mov ax,[bp-0eh]
    call N_LXMUL@
    push ax
    push dx
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    pop ax
    pop dx
    add word ptr es:[bx],dx
    adc word ptr es:[bx+2],ax
    test byte ptr [bp+12h],1
    jz short call_near_element_destructor
    push word ptr [bp-8]
    push word ptr [bp-0ah]
    push word ptr [bp+12h]
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @_vector_delete_$qnvuiuluie
    add sp,10h
    jmp short return_array
call_near_element_destructor:
    push word ptr [bp-6]
    push word ptr [bp+12h]
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @_vector_delete_$qnvuiuluie
    add sp,0eh
return_array:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@_vector_delete_$qnvuiuiuluie endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
