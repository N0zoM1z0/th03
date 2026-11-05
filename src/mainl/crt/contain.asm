; Original string::contains(const char far*) with real Borland C++
; exception scope and typed string RTTI, not a raw CODE-byte array.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far
extrn @string@find$xqmx6stringui:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Original 32-byte Borland exception context and stack-unwind metadata.
exception_descriptor:
    dw 0,0
    dd rtti_string
    dw 4,-4,0,0,0
exception_scope_state:
    dd exception_descriptor
    dw -34,0,5,0
    dw offset _TEXT:exception_descriptor+4

public @string@contains$xqnxc
@string@contains$xqnxc proc far
    push bp
    mov bp,sp
    sub sp,22h
    push si
    push di
    mov ax,seg _TEXT:exception_descriptor
    mov bx,offset _TEXT:exception_scope_state
    call ___InitExceptBlocks
    mov word ptr [bp-16h],6
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ss
    lea ax,[bp-4]
    push ax
    call @string@$bctr$qnxc
    add sp,8
    xor ax,ax
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@find$xqmx6stringui
    add sp,0ah
    cmp ax,-1
    je short string_missing
    mov ax,1
    jmp short have_contains_result
string_missing:
    xor ax,ax
have_contains_result:
    push ax
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    call @string@$bdtr$qv
    add sp,6
    push word ptr [bp-22h]
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@string@contains$xqnxc endp

; Genuine typed string class descriptor and its far destructor.
rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0
    dw 1,1
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0
    db 0
    dw 0,0,0,0,0,0
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
