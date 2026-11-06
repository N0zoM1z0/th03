; Original Japanese Borland fstrrchr: complete native CRT member.
; Preserve far interfaces, original unchecked arithmetic and ordered relocations.
.8086
extrn __fstrlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fstrrchr
; Complete disjoint instruction chunks preserve original OMF field chronology.

org 14
    call __fstrlen
    pop cx
    pop cx
    inc ax
    mov cx, ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short test_search_count
scan_previous_byte:
    dec word ptr [bp-4]
    les bx, dword ptr [bp-4]
    mov al, byte ptr es:[bx]
    cmp al, byte ptr [bp+0ah]
    jne short decrement_search_count
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    jmp short last_character_return
decrement_search_count:
    dec cx
test_search_count:
    or cx, cx
    jne short scan_previous_byte
    xor dx, dx
    xor ax, ax
last_character_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 0
__fstrrchr label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
