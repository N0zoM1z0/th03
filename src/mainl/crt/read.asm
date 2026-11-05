; Original Borland 16-bit ___read: DOS descriptor bounds, translated
; text-mode CRLF / Ctrl-Z semantics and genuine FAR I/O fallbacks.
.8086
extrn __nfile:word
extrn _lseek:far
extrn __rtl_read:far
extrn __read:far
extrn __IOERROR:near
extrn __openfd:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___read
___read proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov ax,[bp+6]
    cmp ax,word ptr DGROUP:__nfile
    jb short check_count
    mov ax,6
    push ax
    call __IOERROR
    jmp near ptr done
check_count:
    mov ax,[bp+0ch]
    inc ax
    cmp ax,2
    jb short no_data
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],2
    jz short perform_read
no_data:
    xor ax,ax
    jmp near ptr done
perform_read:
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_read
    add sp,8
    mov [bp-2],ax
    inc ax
    cmp ax,2
    jb short unchanged_result
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],40h
    jnz short translate_ascii
unchanged_result:
    mov ax,[bp-2]
    jmp short done
translate_ascii:
    mov cx,[bp-2]
    les si,dword ptr [bp+8]
    mov di,si
    mov bx,si
    cld
next_char:
    lods byte ptr es:[si]
    cmp al,1ah
    jz short handle_ctrl_z
    cmp al,0dh
    jz short handle_cr
copy_char:
    stosb
    loop next_char
    jmp short input_end
handle_cr:
    loop next_char
    push es
    push bx
    mov ax,1
    push ax
    lea ax,[bp-3]
    push ss
    push ax
    push word ptr [bp+6]
    call __read
    add sp,8
    pop bx
    pop es
    cld
    mov al,[bp-3]
    stosb
input_end:
    cmp di,bx
    jnz short compute_read_length
    jmp perform_read
compute_read_length:
    jmp short return_count
handle_ctrl_z:
    push bx
    mov ax,1
    push ax
    neg cx
    sbb ax,ax
    push ax
    push cx
    push word ptr [bp+6]
    call _lseek
    add sp,8
    mov bx,[bp+6]
    add bx,bx
    or word ptr DGROUP:__openfd[bx],200h
    pop bx
return_count:
    sub di,bx
    xchg di,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___read endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
