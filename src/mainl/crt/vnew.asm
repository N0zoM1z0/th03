; Complete original Borland C++ array-construction dispatcher, __vector_new_.
; Reconstructs near/far callbacks, 8 calling-convention modes, allocation,
; two-byte array count header and the seven symbolic CODE table relocations.
.8086
extrn @$bnew$qui:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __vector_new_
__vector_new_ proc far
    push bp
    mov bp,sp
    sub sp,16
    push si
    push di
    lea ax,[bp+16]
    mov [bp-2],ss
    mov [bp-4],ax
    test byte ptr [bp+14],1
    jz short callback_near
    add word ptr [bp-4],4
    les bx,dword ptr [bp-4]
    mov dx,word ptr es:[bx-2]
    mov ax,word ptr es:[bx-4]
    mov [bp-8],dx
    mov [bp-10],ax
    jmp short callback_ready
callback_near:
    add word ptr [bp-4],2
    les bx,dword ptr [bp-4]
    mov ax,word ptr es:[bx-2]
    mov [bp-6],ax
callback_ready:
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short buffer_ready
    mov ax,[bp+14]
    and ax,16
    mov [bp-12],ax
    cmp word ptr [bp-12],0
    jz short no_array_header
    mov ax,[bp+10]
    imul word ptr [bp+12]
    add ax,2
    jmp short allocation_size_ready
no_array_header:
    mov ax,[bp+10]
    imul word ptr [bp+12]
allocation_size_ready:
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocation_ok
    xor dx,dx
    xor ax,ax
    jmp near ptr return_array
allocation_ok:
    cmp word ptr [bp-12],0
    jz short buffer_ready
    les bx,dword ptr [bp+6]
    mov ax,[bp+12]
    mov word ptr es:[bx],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,2
    mov [bp+8],dx
    mov [bp+6],ax
buffer_ready:
    and word ptr [bp+14],7
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-14],dx
    mov [bp-16],ax
    jmp short count_test
choose_ctor:
    mov bx,[bp+14]
    cmp bx,6
    ja short mode7
    add bx,bx
    jmp word ptr cs:[bx+offset ctor_table]
mode0:
    push word ptr [bp-16]
    call word ptr [bp-6]
    pop cx
    jmp short advance
mode1:
    push word ptr [bp-16]
    call dword ptr [bp-10]
    pop cx
    jmp short advance
mode2:
    push word ptr [bp-16]
    call word ptr [bp-6]
    jmp short advance
mode3:
    push word ptr [bp-16]
    call dword ptr [bp-10]
    jmp short advance
mode4:
    push word ptr [bp-14]
    push word ptr [bp-16]
    call word ptr [bp-6]
    pop cx
    pop cx
    jmp short advance
mode5:
    push word ptr [bp-14]
    push word ptr [bp-16]
    call dword ptr [bp-10]
    pop cx
    pop cx
    jmp short advance
mode6:
    push word ptr [bp-14]
    push word ptr [bp-16]
    call word ptr [bp-6]
    jmp short advance
mode7:
    push word ptr [bp-14]
    push word ptr [bp-16]
    call dword ptr [bp-10]
advance:
    mov ax,[bp+10]
    add [bp-16],ax
count_test:
    mov ax,[bp+12]
    dec word ptr [bp+12]
    or ax,ax
    ja short choose_ctor
    mov dx,[bp+8]
    mov ax,[bp+6]
return_array:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__vector_new_ endp
ctor_table label word
    dw offset mode0,offset mode1,offset mode2,offset mode3
    dw offset mode4,offset mode5,offset mode6
_TEXT ends
end
