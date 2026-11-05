; Original Borland large-model C++ array destructor __vector_delete_.
; Fully seven-mode callback dispatch, reverse element traversal, free-on-own
; and embedded element-count adjustment. Mode table holds real CODE offsets.
.8086
extrn @$bdele$qnv:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __vector_delete_
__vector_delete_ proc far
    push bp
    mov bp,sp
    sub sp,18
    push si
    push di
    mov ax,[bp+14]
    and ax,8
    mov [bp-12],ax
    mov ax,[bp+14]
    and ax,16
    mov [bp-14],ax
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short initialized_array
    jmp near ptr all_done
initialized_array:
    lea ax,[bp+16]
    mov [bp-2],ss
    mov [bp-4],ax
    test byte ptr [bp+14],1
    jz short callback_is_near
    add word ptr [bp-4],4
    les bx,dword ptr [bp-4]
    mov dx,word ptr es:[bx-2]
    mov ax,word ptr es:[bx-4]
    mov [bp-8],dx
    mov [bp-10],ax
    jmp short callback_ready
callback_is_near:
    add word ptr [bp-4],2
    les bx,dword ptr [bp-4]
    mov ax,word ptr es:[bx-2]
    mov [bp-6],ax
callback_ready:
    cmp word ptr [bp-14],0
    jz short count_ready
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx-2]
    mov [bp+12],ax
count_ready:
    and word ptr [bp+14],7
    mov ax,[bp+12]
    dec ax
    imul word ptr [bp+10]
    mov dx,[bp+8]
    mov bx,[bp+6]
    add bx,ax
    mov [bp-16],dx
    mov [bp-18],bx
    jmp near ptr count_test
select_callback:
    mov bx,[bp+14]
    cmp bx,6
    ja short mode7
    add bx,bx
    jmp word ptr cs:[bx+offset mode_table]
mode0:
    mov ax,2
    push ax
    push word ptr [bp-18]
    call word ptr [bp-6]
    pop cx
    pop cx
    jmp short advance
mode1:
    mov ax,2
    push ax
    push word ptr [bp-18]
    call dword ptr [bp-10]
    pop cx
    pop cx
    jmp short advance
mode2:
    push word ptr [bp-18]
    mov ax,2
    push ax
    call word ptr [bp-6]
    jmp short advance
mode3:
    push word ptr [bp-18]
    mov ax,2
    push ax
    call dword ptr [bp-10]
    jmp short advance
mode4:
    mov ax,2
    push ax
    push word ptr [bp-16]
    push word ptr [bp-18]
    call word ptr [bp-6]
    add sp,6
    jmp short advance
mode5:
    mov ax,2
    push ax
    push word ptr [bp-16]
    push word ptr [bp-18]
    call dword ptr [bp-10]
    add sp,6
    jmp short advance
mode6:
    push word ptr [bp-16]
    push word ptr [bp-18]
    mov ax,2
    push ax
    call word ptr [bp-6]
    jmp short advance
mode7:
    push word ptr [bp-16]
    push word ptr [bp-18]
    mov ax,2
    push ax
    call dword ptr [bp-10]
advance:
    mov ax,[bp+10]
    sub [bp-18],ax
count_test:
    mov ax,[bp+12]
    dec word ptr [bp+12]
    or ax,ax
    jna short count_done
    jmp near ptr select_callback
count_done:
    cmp word ptr [bp-12],0
    jz short all_done
    cmp word ptr [bp-14],0
    jz short do_free
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,0FFFEh
    mov [bp+8],dx
    mov [bp+6],ax
do_free:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
all_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__vector_delete_ endp
mode_table label word
    dw offset mode0,offset mode1,offset mode2,offset mode3
    dw offset mode4,offset mode5,offset mode6
_TEXT ends
end
