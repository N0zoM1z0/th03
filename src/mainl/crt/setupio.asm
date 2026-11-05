; Original Borland stdio startup: initialize inherited FILE tables,
; select terminal/binary buffering and register a real CRT INITDATA hook.
.8086
extrn __streams:byte
extrn __nfile:word
extrn _setvbuf:far
extrn _isatty:far
extrn __openfd:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __setupio
__setupio proc near
    push si
    push di
    mov cx,5
    jmp short check_stream_count
init_extra_stream:
    mov bx,cx
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],0
    mov ax,14h
    imul cx
    mov dx,ax
    mov bx,ax
    mov byte ptr DGROUP:__streams[bx+4],-1
    add ax,offset DGROUP:__streams
    mov bx,dx
    mov word ptr DGROUP:__streams[bx+12h],ax
    inc cx
check_stream_count:
    cmp cx,word ptr DGROUP:__nfile
    jb short init_extra_stream
    mov al,byte ptr DGROUP:__streams+4
    cbw
    push ax
    call _isatty
    pop cx
    or ax,ax
    jne short configured_stdin
    and word ptr DGROUP:__streams+2,0fdffh
configured_stdin:
    mov ax,200h
    push ax
    test byte ptr DGROUP:__streams+3,2
    je short stdin_normal_mode
    mov ax,1
    jmp short stdin_mode_ready
stdin_normal_mode:
    xor ax,ax
stdin_mode_ready:
    push ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:__streams
    push ax
    call _setvbuf
    add sp,0ch
    mov al,byte ptr DGROUP:__streams+18h
    cbw
    push ax
    call _isatty
    pop cx
    or ax,ax
    jne short configured_stdout
    and word ptr DGROUP:__streams+16h,0fdffh
configured_stdout:
    mov ax,200h
    push ax
    test byte ptr DGROUP:__streams+17h,2
    je short stdout_normal_mode
    mov ax,2
    jmp short stdout_mode_ready
stdout_normal_mode:
    xor ax,ax
stdout_mode_ready:
    push ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:__streams+14h
    push ax
    call _setvbuf
    add sp,0ch
    pop di
    pop si
    ret
__setupio endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_INIT_ segment word public 'INITDATA'
    dw 0200h
    dw __setupio
    dw 0
_INIT_ ends
end
