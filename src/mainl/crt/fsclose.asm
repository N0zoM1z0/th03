; Original Japanese Borland fsclose: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @ios@clear$qi:far
extrn @ios@setstate$qi:far
extrn @filebuf@close$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @fstreambase@close$qv
; Complete disjoint instruction chunks preserve original native field order.

org 54
    call @ios@setstate$qi
cleanup_ios_argument:
    add sp, 6
    pop di
    pop si
    pop bp
    retf

org 36
    call @ios@clear$qi
    jmp short cleanup_ios_argument
file_buffer_close_failed:
    mov ax, 2
    push ax
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]

org 15
    call @filebuf@close$qv
    pop cx
    pop cx
    or ax, dx
    je short file_buffer_close_failed
    xor ax, ax
    push ax
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]

org 0
@fstreambase@close$qv label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    add ax, 4
    push word ptr [bp+8]
    push ax
_TEXTA ends
end
