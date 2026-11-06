; Proved identical iostream/istream streambuf assignment bodies.
; Each enclosing TU retains a distinct public, original segment and object.
STREAM_BUFFER_ASSIGNMENT macro api_name
org 18
    call @ios@init$qn9streambuf
    add sp,8
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf

org 0
api_name label far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
endm
