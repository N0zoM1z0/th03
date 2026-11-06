; Original Japanese Borland fsattch: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @ios@clear$qi:far
extrn @ios@setstate$qi:far
extrn @filebuf@attach$qi:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @fstreambase@attach$qi
; Complete disjoint instruction chunks preserve original native field order.

org 70
    call @ios@clear$qi
cleanup_ios_argument:
    add sp, 6
    pop di
    pop si
    pop bp
    retf

org 43
    call @filebuf@attach$qi
    add sp, 6
    or ax, dx
    je short attach_failed
    xor ax, ax
    jmp short clear_attach_state
attach_failed:
    mov ax, 4
clear_attach_state:
    push ax
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]

org 23
    call @ios@setstate$qi
    jmp short cleanup_ios_argument
attach_file_buffer:
    push word ptr [bp+0ah]
    mov ax, word ptr [bp+6]
    add ax, 4
    push word ptr [bp+8]
    push ax

org 0
@fstreambase@attach$qi label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+6]
    cmp word ptr es:[bx+02eh], 0
    je short attach_file_buffer
    mov ax, 2
    push ax
    push es
    push word ptr es:[bx]
_TEXTA ends
end
