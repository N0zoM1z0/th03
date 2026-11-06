; Original Japanese Borland ostosfx: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
extrn @ostream@flush$qv:far
extrn _cout:byte
extrn _clog:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@do_osfx$qv
; Native source chunks retain original logical FIXUPP chronology.

org 66
    call @ostream@flush$qv
    add sp, 8
suffix_return:
    pop di
    pop si
    pop bp
    retf

org 62
    mov ax,offset DGROUP:_clog
    push ax

org 56
    call @ostream@flush$qv
    push ds

org 52
    mov ax,offset DGROUP:_cout
    push ax

org 31
    call @ostream@flush$qv
    pop cx
    pop cx
suffix_check_stdio:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+011h], 040h
    je short suffix_return
    push ds

org 0
@ostream@do_osfx$qv label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+0ah], 086h
    jne short suffix_check_stdio
    test byte ptr es:[bx+011h], 020h
    je short suffix_check_stdio
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
