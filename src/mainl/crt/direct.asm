; Original Borland DOS directory search subsystem.
; _opendir: far path allocation/normalization, DBCS last separator
; and DOS *.* pattern, findfirst handle lifetime and DIR allocation.
; _rewinddir resets native find-first state and DOS cursor flags.
; _readdir calls DOS findnext and returns directory entry storage.
; _closedir frees the far path/name buffers and DIR handle.
; Two real original DATA strings encode backslash-star-dot-star-NUL
; and star-dot-star-NUL. Original 20 OMF FIXUPPs are descending.
; Every code interval below has real instructions, at exactly its
; original coordinate; ORG does not add executable bytes or padding.
.8086
extrn __dos_findfirst:far
extrn __dos_findnext:far
extrn _errno:word
extrn _free:far
extrn _malloc:far
extrn _strcat:far
extrn _strcpy:far
extrn _strlen:far
extrn ___path_issbcs:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
dir_pattern_with_slash db 5Ch,2Ah,2Eh,2Ah,0
dir_pattern_without_slash db 2Ah,2Eh,2Ah,0
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public _opendir,_rewinddir,_readdir,_closedir
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01F7h
    call _free
    add sp, 8
    xor ax, ax
closedir_return:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01ECh
    call _free
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01D1h
closedir_invalid:
    mov word ptr DGROUP:_errno,6
    mov ax, 0ffffh
    jmp short closedir_return
closedir_release_entries:
    les bx, dword ptr [bp+6]
    mov byte ptr es:[bx+030h], 0
    push word ptr es:[bx+02dh]
    push word ptr es:[bx+02bh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01BAh
_closedir label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    je short closedir_invalid
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx+030h], 0ddh
    je short closedir_release_entries
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0194h
    call __dos_findnext
    pop cx
    pop cx
    or ax, ax
    je short readdir_found_entry
readdir_failure:
    xor dx, dx
    xor ax, ax
    jmp short readdir_return
readdir_found_entry:
    les bx, dword ptr [bp+6]
    mov byte ptr es:[bx+02fh], 0
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    add ax, 01eh
readdir_return:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 017Eh
    mov word ptr DGROUP:_errno,6
    jmp short readdir_failure
readdir_new_search:
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx+02fh], 0
    jne short readdir_found_entry
    push word ptr [bp+8]
    push bx
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 016Fh
_readdir label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx+030h], 0ddh
    je short readdir_new_search
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 015Bh
    call __dos_findfirst
    add sp, 0ah
    les bx, dword ptr [bp+6]
    mov byte ptr es:[bx+02fh], 1
dir_at_16b:
    pop di
    pop si
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0137h
_rewinddir label far
    push bp
    mov bp, sp
    push si
    push di
    les bx, dword ptr [bp+6]
    cmp byte ptr es:[bx+030h], 0ddh
    jne short dir_at_16b
    push word ptr [bp+8]
    push word ptr [bp+6]
    mov ax, 017h
    push ax
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+02dh]
    push word ptr es:[bx+02bh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0102h
    call _free
    add sp, 8
opendir_failure:
    xor dx, dx
    xor ax, ax
    jmp short opendir_return
opendir_store_handle:
    les bx, dword ptr [bp-8]
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    mov word ptr es:[bx+02dh], dx
    mov word ptr es:[bx+02bh], ax
    mov byte ptr es:[bx+02fh], 1
    mov byte ptr es:[bx+030h], 0ddh
    mov dx, word ptr [bp-6]
    mov ax, word ptr [bp-8]
opendir_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0F7h
    call _free
    push word ptr [bp-6]
    push word ptr [bp-8]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0E5h
    call __dos_findfirst
    add sp, 0ah
    or ax, ax
    je short opendir_store_handle
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0CCh
    call _free
    pop cx
    pop cx
    jmp short opendir_failure
opendir_handle_initialized:
    push word ptr [bp-6]
    push word ptr [bp-8]
    mov ax, 017h
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0C0h
    mov word ptr DGROUP:_errno,8
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0B0h
    call _malloc
    pop cx
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    or ax, dx
    jne short opendir_handle_initialized
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A4h
    call _strcat
    add sp, 8
    mov ax, 031h
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 09Ah
    mov ax,offset DGROUP:dir_pattern_without_slash
dir_at_09d:
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 094h
    mov ax,offset DGROUP:dir_pattern_with_slash
    jmp short dir_at_09d
opendir_append_default_pattern:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 087h
    call ___path_issbcs
    add sp, 8
    or ax, ax
    jne short opendir_append_default_pattern
opendir_append_pattern:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 041h
    call _strcpy
    add sp, 8
    mov ax, word ptr [bp-0ah]
    dec word ptr [bp-0ah]
    or ax, ax
    je short opendir_append_default_pattern
    les bx, dword ptr [bp-4]
    add bx, word ptr [bp-0ah]
    cmp byte ptr es:[bx], 03ah
    je short opendir_preserve_last_separator
    mov bx, word ptr [bp-4]
    add bx, word ptr [bp-0ah]
    cmp byte ptr es:[bx], 05ch
    je short opendir_preserve_last_separator
    mov bx, word ptr [bp-4]
    add bx, word ptr [bp-0ah]
    cmp byte ptr es:[bx], 02fh
    jne short opendir_append_pattern
opendir_preserve_last_separator:
    mov ax, word ptr [bp-4]
    add ax, word ptr [bp-0ah]
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02Ch
    mov word ptr DGROUP:_errno,8
    jmp near ptr opendir_failure
opendir_alloc_success:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 01Ch
    call _malloc
    pop cx
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    jne short opendir_alloc_success
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0Eh
    call _strlen
    pop cx
    pop cx
    mov word ptr [bp-0ah], ax
    add ax, 5
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
_opendir label far
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
_TEXT ends
end
