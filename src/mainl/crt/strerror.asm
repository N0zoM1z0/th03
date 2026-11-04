; Original Borland large-model error-message formatting.
; A near Pascal helper formats a system message into the shared buffer;
; the two exported far entry points select explicit/current errno.
.8086
extrn _sprintf:far,_errno:word,__sys_nerr:word,__sys_errlist:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
unknown_error db 'Unknown error',0
prefixed_error_format db '%s: %s',10,0
plain_error_format db '%s',10,0
_DATA ends
_BSS segment word public 'BSS'
message_buffer db 161 dup (?)
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

strerror_format proc near
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    mov dx,[bp+8]
    cmp dx,DGROUP:__sys_nerr
    jge unknown_message
    or dx,dx
    jl unknown_message
    mov bx,dx
    mov cl,2
    shl bx,cl
    mov dx,word ptr DGROUP:__sys_errlist[bx+2]
    mov ax,word ptr DGROUP:__sys_errlist[bx]
    mov [bp-2],dx
    mov [bp-4],ax
    jmp short check_prefix
unknown_message:
    mov [bp-2],ds
    mov word ptr [bp-4],offset DGROUP:unknown_error
check_prefix:
    mov ax,[bp+4]
    or ax,[bp+6]
    je no_prefix
    les bx,[bp+4]
    cmp byte ptr es:[bx],0
    je no_prefix
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+6]
    push bx
    push ds
    mov ax,offset DGROUP:prefixed_error_format
    push ax
    push ds
    mov ax,offset DGROUP:message_buffer
    push ax
    call _sprintf
    add sp,16
    jmp short formatted
no_prefix:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ds
    mov ax,offset DGROUP:plain_error_format
    push ax
    push ds
    mov ax,offset DGROUP:message_buffer
    push ax
    call _sprintf
    add sp,12
formatted:
    mov dx,ds
    mov ax,offset DGROUP:message_buffer
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 6
strerror_format endp

public __strerror,_strerror
__strerror proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr DGROUP:_errno
    push word ptr [bp+8]
    push word ptr [bp+6]
    call strerror_format
    pop di
    pop si
    pop bp
    retf
__strerror endp

_strerror proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+6]
    xor ax,ax
    push ax
    push ax
    call strerror_format
    pop di
    pop si
    pop bp
    retf
_strerror endp
_TEXT ends
end
