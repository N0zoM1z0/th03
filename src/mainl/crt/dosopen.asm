; Original Japanese Borland dosopen: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
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
public __dos_open
; Complete disjoint instruction chunks preserve original native field order.

org 51
    call __DOSERROR
dos_open_return:
    pop di
    pop si
    pop bp
    retf

org 0
__dos_open label far
    push bp
    mov bp, sp
    push si
    push di
    mov cl, byte ptr [bp+0ah]
    mov al, 1
    test cl, 2
    jne short combine_sharing_flags
    mov al, 2
    test cl, 4
    jne short combine_sharing_flags
    mov al, 0
combine_sharing_flags:
    and cl, 0f0h
    or al, cl
    mov ah, 03dh
    push ds
    lds dx, dword ptr [bp+6]
    int 021h
    pop ds
    jb short dos_open_error
    les bx, dword ptr [bp+0ch]
    mov word ptr es:[bx], ax
    xor ax, ax
    jmp short dos_open_return
dos_open_error:
    push ax
_TEXT ends
end
