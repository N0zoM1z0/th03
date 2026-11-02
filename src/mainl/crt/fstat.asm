; Original Borland DOS large-model far-cdecl fstat. Use DOS INT 21h
; IOCTL and file-time calls, real __openfd binary/text attribute,
; far _filelength, near DOS timestamp and near error conversion.
; Preserve 16-bit stat-struct word layout written by REP-style STOSW.
.8086
extrn _filelength:far
extrn __IOERROR:near
extrn __DOSTIMETOU:near
extrn __openfd:byte
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _fstat
_fstat proc far
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    mov ax,04400h
    int 021h
    jae short check_device_class
    jmp short report_IO_error
check_device_class:
    sub si,si
    or dl,dl
    js short character_device
    or si,08100h
    and dx,03Fh
    mov di,dx
    mov bx,[bp+6]
    add bx,bx
    test byte ptr DGROUP:[bx+__openfd+1],1
    je short read_file_length
    or si,080h
read_file_length:
    mov bx,[bp+6]
    push bx
    call _filelength
    pop cx
    or dx,dx
    jl short file_length_error
    push dx
    push ax
    mov ax,05700h
    int 021h
    jb short no_file_time
    push dx
    push cx
    call __DOSTIMETOU
    xchg cx,ax
    jmp short fill_fstat_words
character_device:
    or si,02180h
    mov di,bx
    sub ax,ax
    push ax
    push ax
no_file_time:
    sub cx,cx
    mov dx,cx
fill_fstat_words:
    xchg di,ax
    les di,dword ptr [bp+8]
    cld
    stosw
    xchg bx,ax
    sub ax,ax
    stosw
    xchg si,ax
    stosw
    mov ax,1
    stosw
    xchg si,ax
    stosw
    stosw
    xchg bx,ax
    stosw
    pop ax
    stosw
    pop ax
    stosw
    xchg cx,ax
    stosw
    xchg dx,ax
    stosw
    xchg dx,ax
    stosw
    xchg dx,ax
    stosw
    xchg dx,ax
    stosw
    xchg dx,ax
    stosw
    xor ax,ax
    jmp short return_stat
file_length_error:
    mov ax,0ffffh
    jmp short return_stat
report_IO_error:
    push ax
    call __IOERROR
return_stat:
    pop di
    pop si
    pop bp
    retf
_fstat endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
end
