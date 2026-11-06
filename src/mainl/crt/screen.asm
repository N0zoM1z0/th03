; Original Japanese Borland screen: complete platform/runtime member.
; Preserve register ABI, interrupt behavior, storage and native relocation order.
.8086
extrn __MOVELINE:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __MOVETEXT
; Row direction preserves overlapping moves; original byte counters wrap.
; Complete disjoint instruction chunks follow original OMF field chronology.

org 85
    call __MOVELINE
    or ax, ax
    jne short advance_rows
    xor ax, ax
    jmp short move_return
advance_rows:
    mov al, byte ptr [bp-3]
    add byte ptr [bp+0ch], al
    add byte ptr [bp+4], al
test_rows_remaining:
    mov al, byte ptr [bp-2]
    dec byte ptr [bp-2]
    or al, al
    ja short move_next_line
    mov ax, 1
move_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 0ch

org 0
__MOVETEXT label near
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov al, byte ptr [bp+0ah]
    sub al, byte ptr [bp+0eh]
    inc al
    mov byte ptr [bp-1], al
    mov al, byte ptr [bp+8]
    sub al, byte ptr [bp+0ch]
    inc al
    mov byte ptr [bp-2], al
    mov byte ptr [bp-3], 1
    mov al, byte ptr [bp+0ch]
    cmp al, byte ptr [bp+4]
    jae short test_rows_remaining
    mov al, byte ptr [bp-2]
    add al, byte ptr [bp+0ch]
    add al, 0ffh
    mov byte ptr [bp+0ch], al
    mov al, byte ptr [bp-2]
    add al, byte ptr [bp+4]
    add al, 0ffh
    mov byte ptr [bp+4], al
    mov byte ptr [bp-3], 0ffh
    jmp short test_rows_remaining
move_next_line:
    push word ptr [bp+0eh]
    push word ptr [bp+0ch]
    push word ptr [bp+6]
    push word ptr [bp+4]
    push word ptr [bp-1]
_TEXT ends
end
