; Near priority2 startup callback. Preserve stdin/stdout terminal-dependent modes.
.8086
include stdio_layout.inc
extrn __streams:byte,__nfile:word,_setvbuf:far,_isatty:far,__openfd:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __setupio
__setupio proc near
    push si
    push di
    mov cx,5
    jmp short initialize_slot_test
 initialize_slot:
    mov bx,cx
    add bx,bx
    mov word ptr DGROUP:__openfd[bx],0
    mov ax,FILE_BYTES
    imul cx
    mov dx,ax
    mov bx,ax
    mov byte ptr DGROUP:__streams[bx+FILE_FD],-1
    add ax,offset DGROUP:__streams
    mov bx,dx
    mov word ptr DGROUP:__streams[bx+FILE_TOKEN],ax
    inc cx
 initialize_slot_test:
    cmp cx,DGROUP:__nfile
    jb initialize_slot
    mov al,DGROUP:__streams+FILE_FD
    cbw
    push ax
    call _isatty
    pop cx
    or ax,ax
    jne configure_stdin
    and word ptr DGROUP:__streams+FILE_FLAGS,not F_TERM
 configure_stdin:
    mov ax,512
    push ax
    test byte ptr DGROUP:__streams+FILE_FLAGS+1,F_TERM shr 8
    je stdin_fully_buffered
    mov ax,1
    jmp short stdin_mode_selected
 stdin_fully_buffered:
    xor ax,ax
 stdin_mode_selected:
    push ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:__streams
    push ax
    call _setvbuf
    add sp,12
    mov al,DGROUP:__streams+FILE_BYTES+FILE_FD
    cbw
    push ax
    call _isatty
    pop cx
    or ax,ax
    jne configure_stdout
    and word ptr DGROUP:__streams+FILE_BYTES+FILE_FLAGS,not F_TERM
 configure_stdout:
    mov ax,512
    push ax
    test byte ptr DGROUP:__streams+FILE_BYTES+FILE_FLAGS+1,F_TERM shr 8
    je stdout_fully_buffered
    mov ax,2
    jmp short stdout_mode_selected
 stdout_fully_buffered:
    xor ax,ax
 stdout_mode_selected:
    push ax
    xor ax,ax
    push ax
    push ax
    push ds
    mov ax,offset DGROUP:__streams+FILE_BYTES
    push ax
    call _setvbuf
    add sp,12
    pop di
    pop si
    ret
__setupio endp
_TEXT ends
_INIT_ segment word public 'INITDATA'
    db 0,2
    dw offset __setupio
    dw 0
_INIT_ ends
end
