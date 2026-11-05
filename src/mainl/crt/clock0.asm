; Original Borland clock() using native __ftime and 32-bit N_LXMUL@
; with initialized six-byte BSS baseline and original CRT INITDATA hook.
.8086
extrn __ftime:far
extrn N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _clock
_clock proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    push ss
    lea ax,[bp-0ah]
    push ax
    call __ftime
    pop cx
    pop cx
    mov cx,[bp-8]
    mov bx,[bp-0ah]
    sub bx,word ptr DGROUP:clock_base_seconds
    sbb cx,word ptr DGROUP:clock_base_seconds+2
    xor dx,dx
    mov ax,1000
    call N_LXMUL@
    push ax
    mov ax,[bp-6]
    sub ax,word ptr DGROUP:clock_base_millis
    push dx
    cwd
    mov bx,dx
    pop dx
    mov cx,ax
    pop ax
    add ax,cx
    adc dx,bx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_clock endp

; Private real CRT INITDATA hook, original CODE+68.
clock_base_initializer proc far
    push bp
    mov bp,sp
    sub sp,0ah
    push si
    push di
    push ss
    lea ax,[bp-0ah]
    push ax
    call __ftime
    pop cx
    pop cx
    mov dx,[bp-8]
    mov ax,[bp-0ah]
    mov word ptr DGROUP:clock_base_seconds+2,dx
    mov word ptr DGROUP:clock_base_seconds,ax
    mov ax,[bp-6]
    mov word ptr DGROUP:clock_base_millis,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
clock_base_initializer endp
_TEXT ends

_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
clock_base_seconds dd ?
clock_base_millis dw ?
_BSS ends
_INIT_ segment word public 'INITDATA'
    dw 1f01h
    dd clock_base_initializer
_INIT_ ends
end
