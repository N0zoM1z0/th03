; Partial field-order recovery: the two MOV operand-fixup pairs remain open.
; Original complete CODE/DATA and all per-site attributes are retained.
.8086
include stdio_layout.inc
extrn __streams:byte,_fseek:far,_free:far,_malloc:far,__exitbuf:dword,__xfflush:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _setvbuf
_setvbuf label far
org 20
check_mode label near
org 29
check_size label near
org 39
mark_standard_stream label near
org 61
test_stdin label near
org 81
flush_old_buffer label near
org 110
release_old_buffer label near
org 135
default_unbuffered label near
org 235
buffer_failed label near
org 240
install_buffer label near
org 283
buffer_success label near
org 285
buffer_done label near
org 198
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
    mov ax,-1
    jmp short buffer_done
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
    xor ax,ax
    pop di
    pop si
    pop bp
    retf
org 192
    mov word ptr DGROUP:__exitbuf,offset __xfflush
org 186
    mov word ptr DGROUP:__exitbuf+2,seg __xfflush
org 110
    les bx,[bp+6]
    test byte ptr es:[bx+FILE_FLAGS],F_BUF
    je default_unbuffered
    push word ptr es:[bx+FILE_BUFFER+2]
    push word ptr es:[bx+FILE_BUFFER]
    call _free
    pop cx
    pop cx
    les bx,[bp+6]
    and word ptr es:[bx+FILE_FLAGS],not (F_BUF or F_LBUF)
    mov word ptr es:[bx+FILE_BSIZE],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    add ax,word ptr FILE_HOLD
    mov es:[bx+FILE_BUFFER+2],dx
    mov es:[bx+FILE_BUFFER],ax
    mov es:[bx+FILE_CURP+2],dx
    mov es:[bx+FILE_CURP],ax
    cmp word ptr [bp+14],2
    je buffer_success
    cmp word ptr [bp+16],0
    jbe buffer_success
org 81
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
org 75
    mov word ptr DGROUP:stdin_configured,1
org 68
    cmp word ptr [bp+6],offset DGROUP:__streams
    jne flush_old_buffer
org 61
    cmp word ptr DGROUP:stdin_configured,0
    jne flush_old_buffer
org 53
    mov word ptr DGROUP:stdout_configured,1
    jmp short flush_old_buffer
org 46
    cmp word ptr [bp+6],offset DGROUP:__streams+FILE_BYTES
    jne test_stdin
org 0
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov ax,es:[bx+FILE_TOKEN]
    cmp ax,[bp+6]
    je check_mode
    jmp buffer_failed
    cmp word ptr [bp+14],2
    jle check_size
    jmp buffer_failed
    cmp word ptr [bp+16],7fffh
    jbe mark_standard_stream
    jmp buffer_failed
    cmp word ptr DGROUP:stdout_configured,0
    jne test_stdin
_TEXT ends
_DATA segment word public 'DATA'
stdin_configured dw 0
stdout_configured dw 0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
