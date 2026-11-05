; Complete original Japanese Borland DOS CRT findfirs member.
; full C findfirst/findnext preserving DOS DTA and near IOERROR.
; Each instruction and far entry preserves the original 16-bit ABI, including
; genuine carry/error and DTA state. No opaque executable byte arrays.
.8086
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
public _findfirst,_findnext

_findfirst:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,47
    int 21h
    push es
    push bx
    mov ah,26
    lds dx,[bp+10]
    int 21h
    mov ah,78
    mov cx,[bp+14]
    lds dx,[bp+6]
    int 21h
    pushf
    pop cx
    xchg ax,bx
    mov ah,26
    pop dx
    pop ds
    int 21h
    push cx
    popf
    pop ds
    jc findfirs_002f
    xor ax,ax
    jmp short findfirs_0033

findfirs_002f:
    push bx
    call __IOERROR

findfirs_0033:
    pop di
    pop si
    pop bp
    retf

_findnext:
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,47
    int 21h
    push es
    push bx
    mov ah,26
    lds dx,[bp+6]
    int 21h
    mov ah,79
    int 21h
    pushf
    pop cx
    xchg ax,bx
    mov ah,26
    pop dx
    pop ds
    int 21h
    push cx
    popf
    pop ds
    jc findfirs_0060
    xor ax,ax
    jmp short findfirs_0064

findfirs_0060:
    push bx
    call __IOERROR

findfirs_0064:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
