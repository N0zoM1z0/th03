; Original Japanese Borland cibmcrsr: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __video:byte
extrn __IBM_VIDEOINT:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___ibm_setcursortype
; Complete disjoint instruction chunks follow original OMF field chronology.

org 17
    cmp byte ptr DGROUP:__video+8, 7
    jne short cursor_normal_color
    mov dl, 0bh
    mov bl, 0ch
    jmp short cursor_bios
cursor_hidden:
    mov dl, 020h
    mov bl, 0
    jmp short cursor_bios

org 36
cursor_solid:
    cmp byte ptr DGROUP:__video+9, 02bh
    jne short cursor_solid_normal
    mov dl, 0
    mov bl, 8
    jmp short cursor_bios
cursor_solid_normal:
    mov dl, 0

org 51
    cmp byte ptr DGROUP:__video+8, 7
    jne short cursor_end_seven
    mov al, 0ch
    jmp short cursor_set_end
cursor_normal_color:
    mov dl, 6

org 64
    cmp byte ptr DGROUP:__video+9, 02bh
    jne short cursor_end_seven
    mov al, 0
    jmp short cursor_set_end
cursor_end_seven:
    mov al, 7
cursor_set_end:
    mov bl, al
cursor_bios:
    mov ch, dl
    mov cl, bl
    mov ah, 1

org 85
    call __IBM_VIDEOINT
    pop di
    pop si
    pop bp
    retf

org 0
___ibm_setcursortype label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, ax
    je short cursor_hidden
    cmp ax, 1
    je short cursor_solid
_TEXT ends
end
