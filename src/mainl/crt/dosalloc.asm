; Original Japanese Borland CRT member: dosalloc
; INT 21h AH=48h allocates DOS memory and preserves max-free error.
; Full 8086 ABI and DOS carry/error behavior, no patched object bytes.
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
public __dos_allocmem

__dos_allocmem:
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+6]
    mov ah,48h
    int 21h
    jnc dosalloc_branch_001c
    mov cx,bx
    les bx,[bp+8]
    mov es:[bx],cx
    push ax
    call __DOSERROR
    jmp short dosalloc_branch_0024

dosalloc_branch_001c:
    les bx,[bp+8]
    mov es:[bx],ax
    xor ax,ax

dosalloc_branch_0024:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
