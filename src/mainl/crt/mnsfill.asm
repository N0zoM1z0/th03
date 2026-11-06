; Original Japanese Borland mnsfill: complete native stream member.
; Preserve 16-bit near/far/Pascal ABI, original callbacks and unchecked behavior.
.8086
extrn @$bnew$qui:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @setfill$qi
; Native source chunks retain original logical FIXUPP chronology.

org 110
    mov word ptr es:[bx],offset _TEXTA:manipulator_apply
    mov ax, word ptr [bp-2]
    mov word ptr es:[bx+4], ax
manip_constructed:
    mov dx, word ptr [bp-4]
    mov ax, word ptr [bp-6]
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 104
    mov word ptr es:[bx+2],seg manipulator_apply

org 85
    call @$bnew$qui
    pop cx
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
manip_storage_ready:
    or ax, dx
    je short manip_constructed
    les bx, dword ptr [bp-6]

org 0
manipulator_apply label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov al, byte ptr [bp+0ah]
    mov byte ptr [bp-1], al
    les bx, dword ptr [bp+6]
    add bx, 018h
    mov word ptr [bp-4], bx
    mov al, byte ptr es:[bx]
    mov al, byte ptr [bp-1]
    cbw
    mov word ptr es:[bx], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
@setfill$qi label far
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-2], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, word ptr [bp-4]
    je short manip_allocate
    mov ax, word ptr [bp-6]
    jmp short manip_storage_ready
manip_allocate:
    mov ax, 6
    push ax
_TEXTA ends
end
