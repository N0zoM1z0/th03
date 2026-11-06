; Original Japanese Borland iostasn1: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @ios@init$qn9streambuf:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @iostream_withassign@$basg$qm3ios
; Complete disjoint instruction chunks preserve original native field order.

org 23
    call @ios@init$qn9streambuf
    add sp, 8
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf

org 0
@iostream_withassign@$basg$qm3ios label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+0ah]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]
_TEXTA ends
end
