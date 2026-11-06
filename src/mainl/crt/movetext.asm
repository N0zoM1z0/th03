; Original Japanese Borland movetext: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __video:byte
extrn __VALIDATEXY:near
extrn __MOVETEXT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _movetext
; Complete disjoint instruction chunks follow original OMF field chronology.

org 104
    call __MOVETEXT
movetext_return:
    pop di
    pop si
    pop bp
    retf

org 57
    call __VALIDATEXY
    or ax, ax
    jne short move_rectangle
invalid_rectangle:
    xor ax, ax
    jmp short movetext_return
move_rectangle:
    mov al, byte ptr [bp+6]
    add al, 0ffh
    push ax
    mov al, byte ptr [bp+8]
    add al, 0ffh
    push ax
    mov al, byte ptr [bp+0ah]
    add al, 0ffh
    push ax
    mov al, byte ptr [bp+0ch]
    add al, 0ffh
    push ax
    mov al, byte ptr [bp+0eh]
    add al, 0ffh
    push ax
    mov al, byte ptr [bp+010h]
    add al, 0ffh
    push ax

org 24
    call __VALIDATEXY
    or ax, ax
    je short invalid_rectangle
    push word ptr [bp+0eh]
    push word ptr [bp+010h]
    mov ax, word ptr [bp+0ah]
    sub ax, word ptr [bp+6]
    add ax, word ptr [bp+0eh]
    push ax
    mov ax, word ptr [bp+0ch]
    sub ax, word ptr [bp+8]
    add ax, word ptr [bp+010h]
    push ax

org 5
    cmp byte ptr DGROUP:__video+11, 0
    jne short invalid_rectangle
    push word ptr [bp+6]
    push word ptr [bp+8]
    push word ptr [bp+0ah]
    push word ptr [bp+0ch]

org 0
_movetext label far
    push bp
    mov bp, sp
    push si
    push di
_TEXT ends
end
