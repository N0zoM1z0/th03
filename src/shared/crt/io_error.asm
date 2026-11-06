; DOS/System V error conversion, retaining signed INT_MIN and callee cleanup.
; Source PUBLIC order intentionally crosses CODE, DATA, then CODE again.
.8086
include crt_errno.inc
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
extrn _errno:word, __sys_nerr:word
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __IOERROR
__IOERROR label near
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+4]
    or dx,dx
    jl system_error
    cmp dx,88
    jle map_dos_error
invalid_error:
    mov dx,87
map_dos_error:
    mov __doserrno,dx
    mov bx,dx
    mov al,__dosErrorToSV[bx]
    cbw
    mov dx,ax
    jmp short save_errno
org 43
    mov word ptr __doserrno,-1
org 35
system_error:
    neg dx
    cmp dx,__sys_nerr
    jg invalid_error
org 49
save_errno:
    mov _errno,dx
    mov ax,-1
    pop di
    pop si
    pop bp
    ret 2
_TEXT ends
_DATA segment word public 'DATA'
org 2
public __dosErrorToSV
__dosErrorToSV label byte
include dos_error_map.inc
org 0
public __doserrno
__doserrno dw 0
_DATA ends
_TEXT segment byte public 'CODE'
org 62
public __DOSERROR
__DOSERROR label near
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+4]
    call __IOERROR
    mov ax,[bp+4]
    pop di
    pop si
    pop bp
    ret 2
_TEXT ends
end
