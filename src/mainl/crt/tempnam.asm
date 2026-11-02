; Original DOS far-cdecl tempnam: four candidate directories,
; environment path, drive/DBCS separator normalization, real TMP
; prefix, stpcpy/strlen allocation and DOS attribute uniqueness.
; Original near __MKNAME takes the real suffix number; all original
; far CRT imported calls and data references remain symbolic.
; Disjoint authentic 8086 source blocks preserve descending OMF.
.8086
extrn __MKNAME:near
extrn _strlen:far
extrn __stpcpy:far
extrn _strchr:far
extrn _free:far
extrn _getenv:far
extrn _malloc:far
extrn __dos_getfileattr:far
extrn ___path_issbcs:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
tempnam_prefix db 'TMP',0
tempnam_empty_four db 0
tempnam_empty_five db 0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _tempnam
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 016Eh
    call _free
    pop cx
    pop cx
tempnam_next_directory:
    inc word ptr [bp-2]
    cmp word ptr [bp-2], 4
    jge short tempnam_none_left
    jmp near ptr tempnam_path_loop
tempnam_none_left:
    xor dx, dx
    xor ax, ax
tempnam_at_185:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0142h
    call __dos_getfileattr
    add sp, 8
    mov word ptr [bp-010h], ax
    or ax, ax
    je short tempnam_increase_filename
    cmp word ptr [bp-010h], 2
    jne short tempnam_at_168
    mov dx, word ptr [bp-0ch]
    mov ax, word ptr [bp-0eh]
    jmp short tempnam_at_185
tempnam_increase_filename:
    inc word ptr [bp-014h]
tempnam_at_162:
    cmp word ptr [bp-014h], -1
    jne short tempnam_try_filename
tempnam_at_168:
    push word ptr [bp-0ch]
    push word ptr [bp-0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0134h
    call __MKNAME
    push ss
    lea ax, [bp-012h]
    push ax
    push word ptr [bp-0ch]
    push word ptr [bp-0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0108h
    call ___path_issbcs
    add sp, 8
    or ax, ax
    jne short tempnam_next_number
tempnam_at_114:
    les bx, dword ptr [bp-0ah]
    mov byte ptr es:[bx], 05ch
    inc word ptr [bp-0ah]
tempnam_next_number:
    mov word ptr [bp-014h], 0
    jmp short tempnam_at_162
tempnam_try_filename:
    push word ptr [bp-8]
    push word ptr [bp-0ah]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp-014h]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0CAh
    call __stpcpy
    add sp, 8
    mov word ptr [bp-8], dx
    mov word ptr [bp-0ah], ax
    cmp dx, word ptr [bp-0ch]
    jne short tempnam_at_0e2
    cmp ax, word ptr [bp-0eh]
    je short tempnam_next_number
tempnam_at_0e2:
    les bx, dword ptr [bp-0ah]
    cmp byte ptr es:[bx-1], 02fh
    je short tempnam_append_separator
    cmp byte ptr es:[bx-1], 05ch
    je short tempnam_append_separator
    cmp byte ptr es:[bx-1], 03ah
    jne short tempnam_at_114
tempnam_append_separator:
    mov ax, word ptr [bp-0ah]
    dec ax
    push word ptr [bp-8]
    push ax
    push word ptr [bp-0ch]
    push word ptr [bp-0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0ABh
    call _malloc
    pop cx
    mov word ptr [bp-0ch], dx
    mov word ptr [bp-0eh], ax
    or ax, dx
    jne short tempnam_copy_directory
    jmp near ptr tempnam_next_directory
tempnam_copy_directory:
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp-0ch]
    push word ptr [bp-0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 09Dh
    call _strlen
    pop cx
    pop cx
    pop dx
    add dx, ax
    add dx, 8
    push dx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 08Fh
    call _strlen
    pop cx
    pop cx
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 05Fh
    mov word ptr [bp-018h],offset DGROUP:tempnam_empty_five
    mov word ptr [bp-2], 0
tempnam_path_loop:
    mov bx, word ptr [bp-2]
    mov cl, 2
    shl bx, cl
    lea ax, [bp-024h]
    add bx, ax
    mov dx, word ptr ss:[bx+2]
    mov ax, word ptr ss:[bx]
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, dx
    jne short tempnam_test_path
    jmp near ptr tempnam_next_directory
tempnam_test_path:
    push word ptr [bp-4]
    push word ptr [bp-6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 057h
    mov word ptr [bp-01ch],offset DGROUP:tempnam_empty_four
    mov word ptr [bp-016h], ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 03Bh
    call _getenv
    pop cx
    pop cx
    mov word ptr [bp-022h], dx
    mov word ptr [bp-024h], ax
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-01eh], dx
    mov word ptr [bp-020h], ax
    mov word ptr [bp-01ah], ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 037h
    mov ax,offset DGROUP:tempnam_prefix
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 027h
    call _strchr
    add sp, 6
    or ax, dx
    je short tempnam_select_environment
    jmp near ptr tempnam_none_left
tempnam_select_environment:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0Eh
    call _strlen
    pop cx
    pop cx
    cmp ax, 5
    jbe short tempnam_at_01d
    jmp near ptr tempnam_none_left
tempnam_at_01d:
    mov ax, 02eh
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_tempnam label far
    push bp
    mov bp, sp
    sub sp, 024h
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
_TEXT ends
end
