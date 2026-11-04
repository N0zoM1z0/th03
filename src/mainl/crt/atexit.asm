; Original Borland CRT atexit: up to 32 registered far shutdown callbacks.
; Preserve the original static count and uninitialized 128-byte callback table.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
public __atexitcnt
__atexitcnt dw 0
_DATA ends
_BSS segment word public 'BSS'
public __atexittbl
__atexittbl dd 32 dup (?)
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _atexit
_atexit proc far
    push bp
    mov bp,sp
    push si
    push di
    cmp word ptr DGROUP:__atexitcnt,32
    jne register_handler
    mov ax,1
    jmp short done
register_handler:
    mov bx,word ptr DGROUP:__atexitcnt
    mov cl,2
    shl bx,cl
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr DGROUP:__atexittbl[bx+2],dx
    mov word ptr DGROUP:__atexittbl[bx],ax
    inc word ptr DGROUP:__atexitcnt
    xor ax,ax
done:
    pop di
    pop si
    pop bp
    retf
_atexit endp
_TEXT ends
end
