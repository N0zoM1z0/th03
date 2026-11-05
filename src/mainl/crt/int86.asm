; Original Borland int86/int86x real-mode interrupt bridge.
; Saves input register/segment images, synthesizes a true INT nn FAR
; return trampoline on the stack, captures FLAGS, and reports carry.
.8086
extrn _segread:far
extrn __IOERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _int86,_int86x
_int86 proc far
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    push ss
    lea ax,[bp-8]
    push ax
    call _segread
    pop cx
    pop cx
    push ss
    lea ax,[bp-8]
    push ax
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr _int86x
    add sp,0eh
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_int86 endp

_int86x proc far
    push bp
    mov bp,sp
    sub sp,0eh
    push si
    push di
    push ds
    lea cx,[bp-0eh]
    mov [bp-4],cx
    mov [bp-2],ss
    mov byte ptr [bp-0eh],55h
    mov byte ptr [bp-0dh],0cdh
    mov ax,[bp+6]
    mov byte ptr [bp-0ch],al
    mov word ptr [bp-0bh],0cb5dh
    cmp al,25h
    jb short load_registers
    cmp al,26h
    ja short load_registers
    mov byte ptr [bp-0bh],36h
    mov word ptr [bp-0ah],068fh
    mov [bp-8],cx
    mov word ptr [bp-6],0cb5dh
load_registers:
    lds si,dword ptr [bp+10h]
    push word ptr [si]
    push word ptr [si+6]
    lds si,dword ptr [bp+8]
    mov ax,[si]
    mov bx,[si+2]
    mov cx,[si+4]
    mov dx,[si+6]
    mov di,[si+0ah]
    mov si,[si+8]
    pop ds
    pop es
    clc
    call dword ptr [bp-4]
    pushf
    pushf
    push si
    push ds
    push es
    lds si,dword ptr [bp+10h]
    pop word ptr [si]
    pop word ptr [si+6]
    lds si,dword ptr [bp+0ch]
    pop word ptr [si+8]
    pop word ptr [si+0eh]
    pop word ptr [si+0ch]
    and word ptr [si+0ch],1
    mov word ptr [si+0ah],di
    mov word ptr [si+6],dx
    mov word ptr [si+4],cx
    mov word ptr [si+2],bx
    mov word ptr [si],ax
    pop ds
    jz short return_interrupt
    push ax
    push ax
    call __IOERROR
    pop ax
return_interrupt:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_int86x endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
