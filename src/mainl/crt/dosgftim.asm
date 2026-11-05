; Original Japanese Borland CRT member: dosgftim
; INT 21h AX=5700h reads DOS file date and time into far words.
; Full 8086 ABI and DOS carry/error behavior, no patched object bytes.
.8086
extrn __DOSERROR:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __dos_getftime

__dos_getftime:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,5700h
    mov bx,[bp+6]
    int 21h
    jnc dosgftim_branch_0015
    push ax
    call __DOSERROR
    jmp short dosgftim_branch_0023

dosgftim_branch_0015:
    les bx,[bp+8]
    mov es:[bx],dx
    les bx,[bp+12]
    mov es:[bx],cx
    xor ax,ax

dosgftim_branch_0023:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
