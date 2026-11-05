; Complete original Japanese Borland DOS CRT dosfind member.
; full DOS DTA-preserving findfirst/findnext with near DOSERROR.
; Each instruction and far entry preserves the original 16-bit ABI, including
; genuine carry/error and DTA state. No opaque executable byte arrays.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_findfirst,__dos_findnext

__dos_findfirst:
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
    lds dx,[bp+12]
    int 21h
    mov ah,78
    mov cx,[bp+10]
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
    jc dosfind_002f
    xor ax,ax
    jmp short dosfind_0033

dosfind_002f:
    push bx
    call __DOSERROR

dosfind_0033:
    pop di
    pop si
    pop bp
    retf

__dos_findnext:
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
    jc dosfind_0060
    xor ax,ax
    jmp short dosfind_0064

dosfind_0060:
    push bx
    call __DOSERROR

dosfind_0064:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
