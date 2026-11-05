; Original Borland streambuf::setb(char far *start, char far *end, int own).
; Releases the old owned buffer only when a distinct far buffer arrives,
; installs range pointers and computes the original unbuffered/own flags.
.8086
extrn @$bdla$qnv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@setb$qnct1i
@streambuf@setb$qnct1i proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2],0
    jz short set_buffer
    mov ax,word ptr es:[bx+6]
    or ax,word ptr es:[bx+8]
    jz short set_buffer
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    cmp dx,[bp+12]
    jnz short free_old_buffer
    cmp ax,[bp+10]
    jz short set_buffer
free_old_buffer:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    call @$bdla$qnv
    pop cx
    pop cx
set_buffer:
    les bx,dword ptr [bp+6]
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov word ptr es:[bx+8],dx
    mov word ptr es:[bx+6],ax
    or ax,[bp+12]
    jz short use_start_as_end
    mov ax,[bp+14]
    or ax,[bp+16]
    jz short use_start_as_end
    mov ax,[bp+14]
    cmp ax,[bp+10]
    jb short use_start_as_end
    mov dx,[bp+16]
    jmp short set_end
use_start_as_end:
    mov dx,[bp+12]
    mov ax,[bp+10]
set_end:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+0ch],dx
    mov word ptr es:[bx+0ah],ax
    push es
    push bx
    mov ax,[bp+10]
    or ax,[bp+12]
    jnz short buffer_present
    mov ax,1
    jmp short set_unbuffered
buffer_present:
    xor ax,ax
set_unbuffered:
    pop bx
    pop es
    mov word ptr es:[bx+4],ax
    cmp word ptr [bp+18],0
    jz short not_owned
    mov ax,[bp+10]
    or ax,[bp+12]
    jz short not_owned
    mov ax,1
    jmp short set_ownership
not_owned:
    xor ax,ax
set_ownership:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],ax
    pop di
    pop si
    pop bp
    retf
@streambuf@setb$qnct1i endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
