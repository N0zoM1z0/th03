; Reconfigure a FILE after preserving its position; retain original validation,
; first-stdin/stdout flags and allocation ownership behavior.
.8086
include stdio_layout.inc
extrn __streams:byte,_fseek:far,_free:far,_malloc:far,__exitbuf:dword,__xfflush:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setvbuf
_setvbuf proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov ax,es:[bx+FILE_TOKEN]
    cmp ax,[bp+6]
    je check_mode
    jmp buffer_failed
 check_mode:
    cmp word ptr [bp+14],2
    jle check_size
    jmp buffer_failed
 check_size:
    cmp word ptr [bp+16],7fffh
    jbe mark_standard_stream
    jmp buffer_failed
 mark_standard_stream:
    cmp word ptr DGROUP:stdout_configured,0
    jne test_stdin
    cmp word ptr [bp+6],offset DGROUP:__streams+FILE_BYTES
    jne test_stdin
    mov word ptr DGROUP:stdout_configured,1
    jmp short flush_old_buffer
 test_stdin:
    cmp word ptr DGROUP:stdin_configured,0
    jne flush_old_buffer
    cmp word ptr [bp+6],offset DGROUP:__streams
    jne flush_old_buffer
    mov word ptr DGROUP:stdin_configured,1
 flush_old_buffer:
    les bx,[bp+6]
    cmp word ptr es:[bx+FILE_LEVEL],0
    je release_old_buffer
    mov ax,1
    push ax
    xor ax,ax
    push ax
    push ax
    push word ptr [bp+8]
    push bx
    call _fseek
    add sp,10
 release_old_buffer:
    les bx,[bp+6]
    test byte ptr es:[bx+FILE_FLAGS],F_BUF
    je default_unbuffered
    push word ptr es:[bx+FILE_BUFFER+2]
    push word ptr es:[bx+FILE_BUFFER]
    call _free
    pop cx
    pop cx
 default_unbuffered:
    les bx,[bp+6]
    and word ptr es:[bx+FILE_FLAGS],not (F_BUF or F_LBUF)
    mov word ptr es:[bx+FILE_BSIZE],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,FILE_HOLD
    mov es:[bx+FILE_BUFFER+2],dx
    mov es:[bx+FILE_BUFFER],ax
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    cmp word ptr [bp+14],2
    je buffer_success
    cmp word ptr [bp+16],0
    jbe buffer_success
    mov word ptr DGROUP:__exitbuf+2,seg __xfflush
    mov word ptr DGROUP:__exitbuf,offset __xfflush
    mov ax,[bp+10]
    or ax,[bp+12]
    jne install_buffer
    push word ptr [bp+16]
    call _malloc
    pop cx
    mov [bp+12],dx
    mov [bp+10],ax
    or ax,dx
    je buffer_failed
    les bx,[bp+6]
    or word ptr es:[bx+FILE_FLAGS],F_BUF
    jmp short install_buffer
 buffer_failed:
    mov ax,-1
    jmp short buffer_done
 install_buffer:
    les bx,[bp+6]
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    mov es:[bx+FILE_BUFFER+2],dx
    mov es:[bx+FILE_BUFFER],ax
    mov ax,[bp+16]
    mov es:[bx+FILE_BSIZE],ax
    cmp word ptr [bp+14],1
    jne buffer_success
    or word ptr es:[bx+FILE_FLAGS],F_LBUF
 buffer_success:
    xor ax,ax
 buffer_done:
    pop di
    pop si
    pop bp
    retf
_setvbuf endp
_TEXT ends
_DATA segment word public 'DATA'
stdin_configured dw 0
stdout_configured dw 0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
