; Original Japanese Borland validate: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __video:byte
extrn ___get_screen_height:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __VALIDATEXY
; Complete disjoint instruction chunks follow original OMF field chronology.

org 42
    call ___get_screen_height
    cmp ax, word ptr [bp+4]
    jl short rectangle_invalid
    mov ax, 1
    jmp short validate_return
rectangle_invalid:
    xor ax, ax
validate_return:
    pop di
    pop si
    pop bp
    ret 8

org 33
    mov al, byte ptr DGROUP:__video+10
    mov ah, 0
    cmp ax, cx
    jl short rectangle_invalid

org 0
__VALIDATEXY label near
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp+0ah]
    mov bx, word ptr [bp+8]
    mov cx, word ptr [bp+6]
    cmp dx, cx
    jg short rectangle_invalid
    cmp bx, word ptr [bp+4]
    jg short rectangle_invalid
    cmp dx, 1
    jl short rectangle_invalid
    cmp bx, 1
    jl short rectangle_invalid
_TEXT ends
end
