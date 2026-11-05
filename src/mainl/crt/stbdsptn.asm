; Original large-model Borland streambuf::do_sputn bulk output.
; Buffer-span memcpy precedes per-character overflow() fallback.
.8086
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
public @streambuf@do_sputn$qnxci
@streambuf@do_sputn$qnxci proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+16h]
    xor dx,dx
    sub ax,word ptr es:[bx+12h]
    sbb dx,0
    mov [bp-2],ax
    cmp word ptr [bp-2],0
    jng short check_count
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr es:[bx+14h]
    push word ptr es:[bx+12h]
    call _memcpy
    add sp,10
    mov ax,[bp-2]
    add [bp+10],ax
    mov [bp-4],ax
    les bx,dword ptr [bp+6]
    add word ptr es:[bx+12h],ax
    jmp short check_count
next_count:
    inc word ptr [bp-2]
check_count:
    mov ax,[bp-2]
    cmp ax,[bp+14]
    jnc short return_count
    les bx,dword ptr [bp+10]
    inc word ptr [bp+10]
    mov al,byte ptr es:[bx]
    cbw
    mov cx,ax
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+12h]
    cmp ax,word ptr es:[bx+16h]
    jc short put_in_buffer
    mov al,cl
    mov ah,0
    push ax
    push word ptr [bp+8]
    push bx
    mov bx,word ptr es:[bx]
    call dword ptr [bx+18h]
    add sp,6
    jmp short check_write
put_in_buffer:
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+14h]
    mov si,word ptr es:[bx+12h]
    inc word ptr es:[bx+12h]
    mov al,cl
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
check_write:
    cmp ax,0ffffh
    jnz short next_count
return_count:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@streambuf@do_sputn$qnxci endp
_TEXTA ends
end
