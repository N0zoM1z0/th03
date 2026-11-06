; Allocate 1024 bytes; preserve low-word end-pointer arithmetic and original ownership flag.
; Original Japanese Borland stbalc: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @$bnwa$qui:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@doallocate$qv
; Complete disjoint instruction chunks preserve original native field order.

org 12
    call @$bnwa$qui
    pop cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, word ptr [bp-2]
    jne short install_allocated_buffer
    mov ax, 0ffffh
    jmp short allocation_return
install_allocated_buffer:
    les bx, dword ptr [bp+6]
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr es:[bx+8], dx
    mov word ptr es:[bx+6], ax
    add ax, 0400h
    mov word ptr es:[bx+0ch], dx
    mov word ptr es:[bx+0ah], ax
    mov word ptr es:[bx+2], 1
    mov ax, 1
allocation_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 0
@streambuf@doallocate$qv label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, 0400h
    push ax
_TEXTA ends
end
