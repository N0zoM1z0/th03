; Original Japanese Borland CRT member: dossftim
; INT 21h AX=5701h stores DOS file date and time words.
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
public __dos_setftime

__dos_setftime:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,5701h
    mov bx,[bp+6]
    mov cx,[bp+10]
    mov dx,[bp+8]
    int 21h
    jnc dossftim_branch_001b
    push ax
    call __DOSERROR
    jmp short dossftim_branch_001d

dossftim_branch_001b:
    xor ax,ax

dossftim_branch_001d:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
end
