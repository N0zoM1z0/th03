; Low-level translated write: append seek,128-byte flush threshold and short-write
; accounting. CountFFFF returns zero just like count0 after WORD increment.
.8086
include stdio_layout.inc
extrn __nfile:word,_lseek:far,__rtl_write:far,__IOERROR:near,__openfd:word
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___write
___write proc far
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
    mov ax,6
    push ax
    call __IOERROR
    jmp write_done
 count_test:
    mov ax,[bp+12]
    inc ax
    cmp ax,2
    jae append_test
    xor ax,ax
    jmp write_done
 append_test:
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],O_APPEND shr 8
    je translation_test
    mov ax,2
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+6]
    call _lseek
    add sp,8
 translation_test:
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:__openfd[bx+1],O_TEXT shr 8
    jne translate_text
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_write
    add sp,8
    jmp write_done
 translate_text:
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
 translate_byte:
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
 copy_byte:
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
 write_chunk:
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
 short_chunk:
    mov ax,[bp+12]
    sub ax,[bp-8]
    jmp short account_short_write
 reset_translation_buffer:
    lea ax,[bp-144]
    mov [bp-4],ss
    mov [bp-6],ax
 bytes_remaining:
    cmp word ptr [bp-8],0
    je final_chunk
    jmp translate_byte
 final_chunk:
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
 short_final_chunk:
    mov ax,[bp+12]
 account_short_write:
    add ax,dx
    sub ax,[bp-2]
 translated_return:
    jmp short write_done
 all_written:
    mov ax,[bp+12]
 write_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___write endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
