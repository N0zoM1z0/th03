; Original large-model Borland streambuf::do_sgetn bulk input.
; Reads buffered bytes by far memcpy, then falls back to the original
; virtual underflow slot and copies one character per iteration.
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
public @streambuf@do_sgetn$qnci
@streambuf@do_sgetn$qnci proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+22h]
    cmp ax,word ptr es:[bx+1eh]
    jna short empty_input
    xor dx,dx
    sub ax,word ptr es:[bx+1eh]
    sbb dx,0
    jmp short available_ready
empty_input:
    xor ax,ax
available_ready:
    mov [bp-4],ax
    cmp word ptr [bp-4],0
    jng short check_count
    push ax
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+20h]
    push word ptr es:[bx+1eh]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call _memcpy
    add sp,10
    mov ax,[bp-4]
    add [bp+10],ax
    mov [bp-6],ax
    les bx,dword ptr [bp+6]
    add word ptr es:[bx+1eh],ax
    jmp short check_count
read_character:
    les bx,dword ptr [bp+10]
    mov al,[bp-2]
    mov byte ptr es:[bx],al
    inc word ptr [bp+10]
    inc word ptr [bp-4]
check_count:
    mov ax,[bp-4]
    cmp ax,[bp+14]
    jnl short return_count
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+1eh]
    cmp ax,word ptr es:[bx+22h]
    jc short have_character
    push word ptr [bp+8]
    push bx
    mov bx,word ptr es:[bx]
    call dword ptr [bx+0ch]
    pop cx
    pop cx
    cmp ax,0ffffh
    jnz short have_character
    mov ax,0ffffh
    jmp short store_character
have_character:
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+20h]
    mov si,word ptr es:[bx+1eh]
    inc word ptr es:[bx+1eh]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
store_character:
    mov [bp-2],ax
    cmp ax,0ffffh
    jnz short read_character
return_count:
    mov ax,[bp-4]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@streambuf@do_sgetn$qnci endp
_TEXTA ends
end
