; Original Japanese Borland ostfloat: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
.8087
EMUL
extrn @ostream@outstr$qnxct1:far
extrn __REALCVT:near
extrn FIDRQQ:far
extrn FIWRQQ:far
extrn __turboFloat:byte
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
_TEXT ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
float_positive_prefix db '+',0
_DATA ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @ostream@$blsh$qg
; Native source chunks retain original logical FIXUPP chronology.

org 145
    call @ostream@outstr$qnxct1
    add sp, 0ch
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 125
    call __REALCVT
    push word ptr [bp-2]
    push word ptr [bp-4]
    push ss
    lea ax, [bp-042h]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 92
    mov word ptr [bp-4],offset DGROUP:float_positive_prefix
float_convert:
    push ss
    lea ax, [bp+0ah]
    push ax
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    push word ptr es:[bx+014h]
    push ss
    lea ax, [bp-042h]
    push ax
    push dx
    mov al, 0
    push ax
    mov ax, 8
    push ax

org 68
    fwait
    mov ax, word ptr [bp-6]
    sahf
    ja short float_convert
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+011h], 4
    je short float_convert
    mov word ptr [bp-2], ds

org 64
    fstsw word ptr [bp-6]

org 61
    fcompp

org 58
    fldz

org 54
    fld tbyte ptr [bp+0ah]

org 0
@ostream@$blsh$qg label far
    push bp
    mov bp, sp
    sub sp, 042h
    push si
    push di
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+011h], 010h
    je short float_check_scientific
    mov dl, 066h
    jmp short float_format_ready
float_check_scientific:
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx]
    test byte ptr es:[bx+011h], 8
    je short float_general
    mov dl, 065h
    jmp short float_format_ready
float_general:
    mov dl, 067h
float_format_ready:
    mov word ptr [bp-2], 0
    mov word ptr [bp-4], 0
_TEXT ends
end
