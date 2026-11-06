; Shared DOS runtime: original ABI, unchecked widths and literal field order.
.8086
include stdio_layout.inc
extrn __nfile:word,_lseek:far,__rtl_write:far,__IOERROR:near,__openfd:word
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___write
___write label far
org 28
count_test label near
org 42
append_test label near
org 73
translation_test label near
org 108
translate_text label near
org 139
translate_byte label near
org 168
copy_byte label near
org 206
write_chunk label near
org 254
short_chunk label near
org 262
reset_translation_buffer label near
org 272
bytes_remaining label near
org 281
final_chunk label near
org 339
short_final_chunk label near
org 342
account_short_write label near
org 347
translated_return label near
org 349
all_written label near
org 352
write_done label near
org 281
    lea ax,[bp-144]
    mov dx,[bp-6]
    xor bx,bx
    sub dx,ax
    sbb bx,0
    mov [bp-2],dx
    mov ax,dx
    or ax,ax
    jbe all_written
    push dx
    push ss
    lea ax,[bp-144]
    push ax
    push word ptr [bp+6]
    call __rtl_write
    add sp,8
    mov dx,ax
    cmp ax,[bp-2]
    je all_written
    cmp dx,-1
    jne short_final_chunk
    mov ax,-1
    jmp short translated_return
    mov ax,[bp+12]
    add ax,dx
    sub ax,[bp-2]
    jmp short write_done
    mov ax,[bp+12]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
org 206
    lea ax,[bp-144]
    mov dx,[bp-6]
    xor bx,bx
    sub dx,ax
    sbb bx,0
    mov [bp-2],dx
    push dx
    push ss
    push ax
    push word ptr [bp+6]
    call __rtl_write
    add sp,8
    mov dx,ax
    cmp ax,[bp-2]
    je reset_translation_buffer
    cmp dx,-1
    jne short_chunk
    mov ax,-1
    jmp short translated_return
    mov ax,[bp+12]
    sub ax,[bp-8]
    jmp short account_short_write
    lea ax,[bp-144]
    mov [bp-4],ss
    mov [bp-6],ax
    cmp word ptr [bp-8],0
    je final_chunk
    jmp translate_byte
org 108
    mov bx,[bp+6]
    add bx,bx
    and word ptr DGROUP:__openfd[bx],not O_EOF
    mov dx,[bp+10]
    mov ax,[bp+8]
    mov [bp-12],dx
    mov [bp-14],ax
    mov ax,[bp+12]
    mov [bp-8],ax
    jmp short reset_translation_buffer
    dec word ptr [bp-8]
    les bx,[bp-14]
    inc word ptr [bp-14]
    mov al,es:[bx]
    mov [bp-9],al
    cmp al,10
    jne copy_byte
    les bx,[bp-6]
    mov byte ptr es:[bx],13
    inc word ptr [bp-6]
    les bx,[bp-6]
    mov al,[bp-9]
    mov es:[bx],al
    inc word ptr [bp-6]
    lea ax,[bp-144]
    mov dx,[bp-6]
    xor bx,bx
    sub dx,ax
    sbb bx,0
    or bx,bx
    jl bytes_remaining
    jne write_chunk
    cmp dx,128
    jb bytes_remaining
org 85
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_write
    add sp,8
    jmp write_done
org 73
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],O_TEXT shr 8
    jne translate_text
org 54
    mov ax,2
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+6]
    call _lseek
    add sp,8
org 42
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],O_APPEND shr 8
    je translation_test
org 18
    mov ax,6
    push ax
    call __IOERROR
    jmp write_done
    mov ax,[bp+12]
    inc ax
    cmp ax,word ptr 2
    jae append_test
    xor ax,ax
    jmp write_done
org 0
    push bp
    mov bp,sp
    sub sp,144
    push si
    push di
    ; BP-144 translation scratch; -14/-12 source, -9 byte,
    ; -8 remaining, -6/-4 destination and -2 chunk size.
    mov ax,[bp+6]
    cmp ax,DGROUP:__nfile
    jb count_test
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
