; Original six Borland stdio macros as callable far CRT entrypoints.
; Preserve the FILE level, curp and segment arithmetic, not replacement I/O.
.8086
extrn __streams:byte
extrn __fgetc:far
extrn __fputc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getc,_getchar,_putchar,_putc,_feof,_ferror
_getc proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    dec word ptr es:[bx]
    jl short getc_slow
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
    jmp short getc_return
getc_slow:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fgetc
    pop cx
    pop cx
getc_return:
    pop di
    pop si
    pop bp
    retf
_getc endp

_getchar proc far
    push si
    push di
    dec word ptr DGROUP:__streams
    jl short getchar_slow
    les bx,dword ptr DGROUP:__streams+0ch
    inc word ptr DGROUP:__streams+0ch
    mov al,byte ptr es:[bx]
    mov ah,0
    jmp short getchar_return
getchar_slow:
    push ds
    mov ax,offset DGROUP:__streams
    push ax
    call __fgetc
    pop cx
    pop cx
getchar_return:
    pop di
    pop si
    retf
_getchar endp

_putchar proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    inc word ptr DGROUP:__streams+14h
    jge short putchar_slow
    les bx,dword ptr DGROUP:__streams+20h
    inc word ptr DGROUP:__streams+20h
    mov al,dl
    mov byte ptr es:[bx],al
    mov ah,0
    jmp short putchar_return
putchar_slow:
    push ds
    mov ax,offset DGROUP:__streams+14h
    push ax
    push dx
    call __fputc
    add sp,6
putchar_return:
    pop di
    pop si
    pop bp
    retf
_putchar endp

_putc proc far
    push bp
    mov bp,sp
    push si
    push di
    mov cx,[bp+6]
    les bx,dword ptr [bp+8]
    inc word ptr es:[bx]
    jge short putc_slow
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov al,cl
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
    jmp short putc_return
putc_slow:
    push word ptr [bp+10]
    push word ptr [bp+8]
    push cx
    call __fputc
    add sp,6
putc_return:
    pop di
    pop si
    pop bp
    retf
_putc endp

_feof proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+2]
    and ax,20h
    pop di
    pop si
    pop bp
    retf
_feof endp

_ferror proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+2]
    and ax,10h
    pop di
    pop si
    pop bp
    retf
_ferror endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
