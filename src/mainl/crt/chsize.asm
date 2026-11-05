; Original Borland _chsize(handle, new_size), including true DOS seek,
; zero-filling growth in 128-byte chunks and current offset restoration.
.8086
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
public _chsize
_chsize proc far
    push bp
    mov bp,sp
    sub sp,84h
    push si
    push di
    mov ax,4201h
    mov bx,[bp+6]
    sub cx,cx
    mov dx,cx
    int 21h
    jb short resize_error
    mov [bp-4],ax
    mov [bp-2],dx
    mov ax,4202h
    sub cx,cx
    mov dx,cx
    int 21h
    jb short resize_error
    cmp dx,[bp+0ah]
    ja short truncate_file
    jb short grow_file
    cmp ax,[bp+8]
    jae short truncate_file
grow_file:
    sub [bp+8],ax
    sbb [bp+0ah],dx
    mov cx,dx
    xchg ax,dx
    mov ax,4200h
    int 21h
    jb short resize_error
    push ss
    pop es
    lea di,[bp-84h]
    xor ax,ax
    mov cx,40h
    cld
    rep stosw
fill_chunk:
    mov cx,80h
    cmp word ptr [bp+0ah],0
    jnz short use_chunk_size
    cmp cx,[bp+8]
    jbe short use_chunk_size
    mov cx,[bp+8]
use_chunk_size:
    sub [bp+8],cx
    sbb word ptr [bp+0ah],0
    lea dx,[bp-84h]
    push ds
    push ss
    pop ds
    push cx
    mov ah,40h
    int 21h
    pop cx
    pop ds
    jb short resize_error
    cmp ax,cx
    jne short resize_error
    mov ax,[bp+8]
    or ax,[bp+0ah]
    jnz short fill_chunk
    jmp short restore_position
resize_error:
    push ax
    call __IOERROR
    jmp short done
truncate_file:
    mov ax,4200h
    mov bx,[bp+6]
    mov dx,[bp+8]
    mov cx,[bp+0ah]
    int 21h
    jb short resize_error
    mov ah,40h
    sub cx,cx
    int 21h
    jb short resize_error
restore_position:
    mov dx,[bp-4]
    mov cx,[bp-2]
    xchg si,ax
    mov ax,4200h
    int 21h
    jb short resize_error
    mov bx,[bp+6]
    add bx,bx
    or word ptr DGROUP:__openfd[bx],1000h
    xor ax,ax
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_chsize endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
