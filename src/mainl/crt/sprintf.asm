; Borland large-model sprintf/vsprintf. The shared near callback copies its
; counted span into the destination cursor, advances it, and writes a NUL.
; _sprintf passes a stack-argument cursor; _vsprintf passes its va_list.
; These far entry points share the original _VPRINTER formatting engine.
.8086
extrn _memcpy:far,__VPRINTER:near
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

format_output proc near
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,[bp+4]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call _memcpy
    add sp,10
    mov ax,[bp+8]
    les bx,[bp+4]
    add word ptr es:[bx],ax
    push bx
    push es
    mov es,word ptr es:[bx+2]
    mov ax,es
    pop es
    pop bx
    mov bx,word ptr es:[bx]
    mov es,ax
    mov byte ptr es:[bx],0
    mov ax,[bp+8]
    pop di
    pop si
    pop bp
    ret 10
format_output endp

public _sprintf,_vsprintf
_sprintf proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov byte ptr es:[bx],0
    mov ax,offset format_output
    push ax
    push ss
    lea ax,[bp+6]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    lea ax,[bp+14]
    push ax
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_sprintf endp

_vsprintf proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+6]
    mov byte ptr es:[bx],0
    mov ax,offset format_output
    push ax
    push ss
    lea ax,[bp+6]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+14]
    call __VPRINTER
    pop di
    pop si
    pop bp
    retf
_vsprintf endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
