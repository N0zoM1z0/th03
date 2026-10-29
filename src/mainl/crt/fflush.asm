; Reset buffered input or write pending output, preserving original short-write policy.
.8086
include stdio_layout.inc
extrn _flushall:far,___write:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fflush
_fflush proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jne check_stream
    call _flushall
    jmp flush_success
 check_stream:
    les bx,[bp+6]
    mov ax,es:[bx+FILE_TOKEN]
    cmp ax,[bp+6]
    je check_level
    jmp flush_failed
 check_level:
    les bx,[bp+6]
    cmp word ptr es:[bx+FILE_LEVEL],0
    jl write_pending
    test byte ptr es:[bx+FILE_FLAGS],F_LBUF
    jne clear_level
    mov dx,es:[bx+FILE_CURP+2]
    mov ax,[bp+6]
    add ax,FILE_HOLD
    cmp dx,[bp+8]
    je compare_hold
    jmp flush_success
 compare_hold:
    cmp es:[bx+FILE_CURP],ax
    jne flush_success
 clear_level:
    les bx,[bp+6]
    mov word ptr es:[bx+FILE_LEVEL],0
    mov dx,es:[bx+FILE_CURP+2]
    mov ax,[bp+6]
    add ax,FILE_HOLD
    cmp dx,[bp+8]
    jne flush_success
    cmp es:[bx+FILE_CURP],ax
    jne flush_success
    mov dx,es:[bx+FILE_BUFFER+2]
    mov ax,es:[bx+FILE_BUFFER]
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    jmp short flush_success
 write_pending:
    les bx,[bp+6]
    mov ax,es:[bx+FILE_BSIZE]
    add ax,es:[bx+FILE_LEVEL]
    inc ax
    mov [bp-2],ax
    sub es:[bx+FILE_LEVEL],ax
    push ax
    mov dx,es:[bx+FILE_BUFFER+2]
    mov ax,es:[bx+FILE_BUFFER]
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    push dx
    push ax
    mov al,es:[bx+FILE_FD]
    cbw
    push ax
    call ___write
    add sp,8
    cmp ax,[bp-2]
    je flush_success
    les bx,[bp+6]
    test byte ptr es:[bx+FILE_FLAGS+1],F_TERM shr 8
    jne flush_success
    or word ptr es:[bx+FILE_FLAGS],F_ERR
 flush_failed:
    mov ax,-1
    jmp short flush_done
 flush_success:
    xor ax,ax
 flush_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_fflush endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
