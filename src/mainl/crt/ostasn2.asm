; Original Japanese Borland ostasn2: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
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
public @ostream_withassign@$basg$qn9streambuf
; Native source chunks retain original logical FIXUPP chronology.

org 18
    call @ios@init$qn9streambuf
    add sp, 8
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf

org 0
@ostream_withassign@$basg$qn9streambuf label far
    push bp
    mov bp, sp
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    les bx, dword ptr [bp+6]
    push es
    push word ptr es:[bx]
_TEXTA ends
end
