; Original Japanese Borland streambuf::dbp fully reconstructs the debug
; print of alloc/unbuf, base/ebuf, put and get cursor state.
; Natural 8086 source and typed four original DATA format strings.
.8086
extrn _write:far,_sprintf:far,_strlen:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
format_flags: db 'alloc_ = %d, unbuf_ = %d',10,0
format_base: db 'base_ = %p, ebuf_ = %p',10,0
format_put: db 'pbase_ = %p, pptr_ = %p, epptr_ = %p',10,0
format_get: db 'gptr_ = %p, egptr_ = %p, eback_ = %p',10,0
_DATA ends
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@dbp$qv
@streambuf@dbp$qv:
    push bp
    mov bp,sp
    sub sp,80
    push si
    push di
    les bx,[bp+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push ds
    mov ax,offset DGROUP:format_flags
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call _sprintf
    add sp,12
    push ss
    lea ax,[bp-80]
    push ax
    call _strlen
    pop cx
    pop cx
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    mov ax,1
    push ax
    call _write
    les bx,[bp+6]
    push word ptr es:[bx+12]
    push word ptr es:[bx+10]
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    push ds
    mov ax,offset DGROUP:format_base
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call _sprintf
    add sp,24
    push ss
    lea ax,[bp-80]
    push ax
    call _strlen
    pop cx
    pop cx
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    mov ax,1
    push ax
    call _write
    les bx,[bp+6]
    push word ptr es:[bx+24]
    push word ptr es:[bx+22]
    push word ptr es:[bx+20]
    push word ptr es:[bx+18]
    push word ptr es:[bx+16]
    push word ptr es:[bx+14]
    push ds
    mov ax,offset DGROUP:format_put
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call _sprintf
    add sp,28
    push ss
    lea ax,[bp-80]
    push ax
    call _strlen
    pop cx
    pop cx
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    mov ax,1
    push ax
    call _write
    les bx,[bp+6]
    push word ptr es:[bx+28]
    push word ptr es:[bx+26]
    push word ptr es:[bx+36]
    push word ptr es:[bx+34]
    push word ptr es:[bx+32]
    push word ptr es:[bx+30]
    push ds
    mov ax,offset DGROUP:format_get
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    call _sprintf
    add sp,28
    push ss
    lea ax,[bp-80]
    push ax
    call _strlen
    pop cx
    pop cx
    push ax
    push ss
    lea ax,[bp-80]
    push ax
    mov ax,1
    push ax
    call _write
    add sp,8
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
