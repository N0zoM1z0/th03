; Original Borland DOS temporary filename generation: actual TMP prefix,
; numeric suffix, persistent 13-byte BSS name buffer and fileattr retries.
.8086
extrn __UTOA:near
extrn _strcat:far
extrn __stpcpy:far
extrn __dos_getfileattr:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __MKNAME,__TMPNAM

__MKNAME proc near
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+0ah]
    or ax,[bp+0ch]
    jnz short name_dest_ready
    mov word ptr [bp+0ch],ds
    mov word ptr [bp+0ah],offset DGROUP:tmp_name_buffer
name_dest_ready:
    push word ptr [bp+4]
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short given_prefix
    mov dx,ds
    mov ax,offset DGROUP:tmp_prefix
    jmp short prefix_ready
given_prefix:
    mov dx,[bp+8]
    mov ax,[bp+6]
prefix_ready:
    push dx
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call __stpcpy
    add sp,8
    push dx
    push ax
    call __UTOA
    push ds
    mov ax,offset DGROUP:tmp_suffix
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call _strcat
    add sp,8
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    pop di
    pop si
    pop bp
    ret 0ah
__MKNAME endp

__TMPNAM proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
try_unused_filename:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    xor ax,ax
    push ax
    push ax
    les bx,dword ptr [bp+4]
    cmp word ptr es:[bx],-1
    jne short advance_counter_by_one
    mov ax,2
    jmp short have_counter_stride
advance_counter_by_one:
    mov ax,1
have_counter_stride:
    les bx,dword ptr [bp+4]
    add word ptr es:[bx],ax
    mov ax,word ptr es:[bx]
    push ax
    call near ptr __MKNAME
    mov [bp+0ah],dx
    mov [bp+8],ax
    push ss
    lea ax,[bp-2]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    call __dos_getfileattr
    add sp,8
    or ax,ax
    je short try_unused_filename
    mov dx,[bp+0ah]
    mov ax,[bp+8]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 8
__TMPNAM endp
_TEXT ends

_DATA segment word public 'DATA'
tmp_prefix db 'TMP',0
tmp_suffix db '.$$$',0
_DATA ends
_BSS segment word public 'BSS'
tmp_name_buffer db 13 dup(?)
_BSS ends
end
