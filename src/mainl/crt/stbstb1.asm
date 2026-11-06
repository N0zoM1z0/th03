; Original Japanese Borland stbstb1: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setb$qnct1i:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @streambuf@setbuf$qncii
; Complete disjoint instruction chunks preserve original native field order.

org 61
    call @streambuf@setp$qnct1
    add sp, 01ah
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf

org 30
    call @streambuf@setb$qnct1i
    mov ax, word ptr [bp+0ah]
    add ax, word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push ax
    mov ax, word ptr [bp+0ah]
    add ax, word ptr [bp+010h]
    push word ptr [bp+0ch]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]

org 0
@streambuf@setbuf$qncii label far
    push bp
    mov bp, sp
    push si
    push di
    xor ax, ax
    push ax
    mov ax, word ptr [bp+0ah]
    add ax, word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXTA ends
end
