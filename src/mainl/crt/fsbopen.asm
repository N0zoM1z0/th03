; filebuf::open(const char far*, int, int).
; Original Borland far member ABI. Converts iostream mode to DOS open flags,
; installs the file descriptor and reconciles streambuf get/put pointers.
.8086
extrn _lseek:far,_open:far
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA

_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@open$qnxcii

@filebuf@open$qnxcii:
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2ah],0
    je check_mode
    jmp near ptr open_failed
check_mode:
    cmp word ptr [bp+0eh],0
    jne choose_access
    jmp near ptr open_failed

choose_access:
    test byte ptr [bp+0eh],2
    je read_only
    test byte ptr [bp+0eh],1
    je write_only
    mov ax,4
    jmp short choose_creation
write_only:
    mov ax,2
choose_creation:
    test byte ptr [bp+0eh],20h
    jne maybe_truncate
    or ax,100h
    test byte ptr [bp+0eh],40h
    je maybe_truncate
    or ax,400h
maybe_truncate:
    test byte ptr [bp+0eh],10h
    je choose_text
    or ax,200h
    jmp short choose_text
read_only:
    test byte ptr [bp+0eh],1
    je open_failed
    mov ax,1

choose_text:
    test byte ptr [bp+0eh],80h
    je binary_mode
    or ax,8000h
    jmp short maybe_noinherit
binary_mode:
    or ax,4000h
maybe_noinherit:
    test byte ptr [bp+0eh],8
    je dos_open
    or ax,800h

dos_open:
    push word ptr [bp+10h]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call _open
    add sp,8
    mov dx,ax
    cmp dx,-1
    je open_failed

    ; Put the original FILE/descriptor and selected mode on the filebuf.
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+26h],dx
    mov word ptr es:[bx+2ah],1
    mov ax,word ptr [bp+0eh]
    mov word ptr es:[bx+28h],ax
    test byte ptr [bp+0eh],4
    je seek_begin
    mov ax,2
    jmp short seek_setup
seek_begin:
    xor ax,ax
seek_setup:
    push ax
    xor ax,ax
    push ax
    push ax
    push dx
    call _lseek
    add sp,8

    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2eh],dx
    mov word ptr es:[bx+2ch],ax
    cmp word ptr es:[bx+2eh],-1
    jne setup_stream
    cmp word ptr es:[bx+2ch],-1
    jne setup_stream
open_failed:
    xor dx,dx
    xor ax,ax
    jmp short return_open

setup_stream:
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    mov word ptr [bp-2],dx
    mov word ptr [bp-4],ax
    or ax,word ptr [bp-2]
    je unbuffered
    mov ax,word ptr es:[bx+0ah]
    xor dx,dx
    sub ax,word ptr es:[bx+6]
    sbb dx,0
    cmp ax,8
    jle small_buffer
    mov ax,4
    jmp short got_buffer_start
small_buffer:
    mov ax,1
got_buffer_start:
    jmp short set_start
unbuffered:
    xor ax,ax
set_start:
    mov word ptr [bp-6],ax
    mov ax,word ptr [bp-4]
    add ax,word ptr [bp-6]
    mov word ptr [bp-8],ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setp$qnct1
    mov ax,word ptr [bp-4]
    add ax,word ptr [bp-6]
    mov word ptr [bp-0ah],ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,1ch
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
return_open:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
