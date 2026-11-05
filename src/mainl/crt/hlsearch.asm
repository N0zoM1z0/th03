; Borland far-heap linear search boss: private ABI-aware search core,
; public ___hlsearch (insert) and ___hlfind (find-only).
.8086
extrn __fmovmem:far
extrn N_PADA@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

linear_heap_search_core proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    les bx,dword ptr [bp+0ch]
    mov ax,word ptr es:[bx]
    mov [bp-2],ax
    jmp short check_remaining
compare_next:
    push word ptr [bp+12h]
    push word ptr [bp+10h]
    push word ptr [bp+16h]
    push word ptr [bp+14h]
    call dword ptr [bp+6]
    add sp,8
    or ax,ax
    jz short return_found
    mov bx,[bp+0ah]
    xor cx,cx
    mov dx,ss
    lea ax,[bp+10h]
    call N_PADA@
    dec word ptr [bp-2]
check_remaining:
    cmp word ptr [bp-2],0
    jg short compare_next
    cmp word ptr [bp+4],0
    jz short not_found
    les bx,dword ptr [bp+0ch]
    inc word ptr es:[bx]
    push word ptr [bp+0ah]
    push word ptr [bp+12h]
    push word ptr [bp+10h]
    push word ptr [bp+16h]
    push word ptr [bp+14h]
    call __fmovmem
    add sp,0ah
    jmp short return_found
not_found:
    mov word ptr [bp+12h],0
    mov word ptr [bp+10h],0
return_found:
    mov dx,[bp+12h]
    mov ax,[bp+10h]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 14h
linear_heap_search_core endp

public __hlsearch
__hlsearch proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push word ptr [bp+12h]
    push word ptr [bp+16h]
    push word ptr [bp+14h]
    mov ax,1
    push ax
    call near ptr linear_heap_search_core
    pop di
    pop si
    pop bp
    retf
__hlsearch endp

public __hlfind
__hlfind proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    push word ptr [bp+12h]
    push word ptr [bp+16h]
    push word ptr [bp+14h]
    xor ax,ax
    push ax
    call near ptr linear_heap_search_core
    pop di
    pop si
    pop bp
    retf
__hlfind endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
