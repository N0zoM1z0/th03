; Original filebuf::attach(int descriptor) far C++ method.
; Attaches an existing DOS handle, optionally allocates its 0x204-byte
; work buffer, then initializes put/get windows by the Borland streambuf API.
.8086
extrn @$bnwa$qui:far
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
extrn @streambuf@setb$qnct1i:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@attach$qi
@filebuf@attach$qi proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2ah],0
    jz short attach_descriptor
    xor dx,dx
    xor ax,ax
    jmp near ptr return_result
attach_descriptor:
    les bx,dword ptr [bp+6]
    mov ax,[bp+10]
    mov word ptr es:[bx+26h],ax
    mov word ptr es:[bx+2ah],1
    mov word ptr es:[bx+28h],0
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,[bp-2]
    jnz short initialize_windows
    mov ax,204h
    push ax
    call @$bnwa$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,[bp-2]
    jz short initialize_windows
    mov ax,1
    push ax
    mov ax,[bp-4]
    add ax,204h
    push dx
    push ax
    push dx
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setb$qnct1i
    add sp,0eh
initialize_windows:
    mov ax,[bp-4]
    or ax,[bp-2]
    jz short no_buffer
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+0ah]
    xor dx,dx
    sub ax,word ptr es:[bx+6]
    sbb dx,0
    cmp ax,8
    jle short small_buffer
    mov ax,4
    jmp short buffer_size_selected
small_buffer:
    mov ax,1
buffer_size_selected:
    jmp short have_size
no_buffer:
    xor ax,ax
have_size:
    mov [bp-6],ax
    mov ax,[bp-4]
    add ax,[bp-6]
    mov [bp-8],ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setp$qnct1
    mov ax,[bp-4]
    add ax,[bp-6]
    mov [bp-0ah],ax
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
    mov dx,[bp+8]
    mov ax,[bp+6]
return_result:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@filebuf@attach$qi endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
