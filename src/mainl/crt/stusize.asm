; Original Borland ios::usersize(int), with full FAR user-word array
; reallocation, copy, delete and zero-initialization of added slots.
.8086
extrn @$bnwa$qui:far
extrn @$bdla$qnv:far
extrn _memcpy:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@usersize$qi
@ios@usersize$qi proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,[bp+0ah]
    mov cl,2
    shl ax,cl
    push ax
    call @$bnwa$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,[bp-2]
    jz short usersize_done
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+26h],0
    je short assign_new_storage
    mov ax,word ptr es:[bx+26h]
    mov cl,2
    shl ax,cl
    push ax
    push word ptr es:[bx+24h]
    push word ptr es:[bx+22h]
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _memcpy
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+24h]
    push word ptr es:[bx+22h]
    call @$bdla$qnv
    add sp,0eh
assign_new_storage:
    les bx,dword ptr [bp+6]
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov word ptr es:[bx+24h],dx
    mov word ptr es:[bx+22h],ax
zero_each_new_slot:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+26h]
    mov cl,2
    shl ax,cl
    les bx,dword ptr [bp-4]
    add bx,ax
    mov word ptr es:[bx+2],0
    mov word ptr es:[bx],0
    les bx,dword ptr [bp+6]
    inc word ptr es:[bx+26h]
    mov ax,word ptr es:[bx+26h]
    cmp ax,[bp+0ah]
    jl short zero_each_new_slot
usersize_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@ios@usersize$qi endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
