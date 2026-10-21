; Near callee-pop error helpers. Nonnegative inputs are DOS errors, negative
; inputs are negated System V errno values. Signed INT_MIN stays negative.
.8086
include crt_errno.inc
_TEXT segment byte public 'CODE'
assume cs:_TEXT, ds:DGROUP
public __IOERROR, __DOSERROR
__IOERROR proc near
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
system_error:
    neg dx
    cmp dx,__sys_nerr
    jg invalid_error
    mov __doserrno,-1
save_errno:
    mov _errno,dx
    mov ax,-1
    pop di
    pop si
    pop bp
    ret 2
__IOERROR endp
__DOSERROR proc near
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
__DOSERROR endp
_TEXT ends
_DATA segment word public 'DATA'
; External errno words belong to DGROUP, never the current CODE segment.
extrn _errno:word, __sys_nerr:word
public __doserrno, __dosErrorToSV
__doserrno dw 0
__dosErrorToSV label byte
include dos_error_map.inc
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
