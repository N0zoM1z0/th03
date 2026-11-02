; Original Borland DOS __searchstr large-model far-cdecl path resolver.
; Three far parameters: file name, path/search list, output scratch buffer.
; Compose a CWD candidate, verify separators, append the file name,
; check access, walk semicolon-separated additional path entries,
; canonicalize an accessible candidate using original far __fullpath,
; copy its resolved text and free the original allocated temporary.
; Original unchecked pointer offsets, literal DOS separator string and
; eight external far CRT helper names/indices are preserved.
.8086
extrn __getdcwd:far
extrn _strcat:far
extrn _strcpy:far
extrn _strlen:far
extrn _free:far
extrn __fullpath:far
extrn __access:far
extrn ___path_issbcs:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
path_separator db 5Ch,0 ; DOS path separator and terminator
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
public __searchstr
; Intentionally source-order reversed code blocks: the original BCC
; wrote the ten far/data FIXUPP fields in descending CODE-site order.
; Every ORG below begins exactly at a real instruction/branch boundary.
; No ORG inserts alignment bytes or modifies original target binary.
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0134h
    call _free
    add sp, 0ch
return_from_path_search:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0129h
    call _strcpy
    push word ptr [bp-2]
    push word ptr [bp-4]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 010Bh
    call __fullpath
    add sp, 0ah
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    je short return_from_path_search
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 0A6h
    call __access
    add sp, 6
    or ax, ax
    je short canonicalize_accessible_path
    les bx, dword ptr [bp+0ah]
    cmp byte ptr es:[bx], 0
    jne short setup_next_path
    les bx, dword ptr [bp+0eh]
    mov byte ptr es:[bx], 0
    jmp short return_from_path_search
setup_next_path:
    xor dx, dx
    jmp short test_path_component_end
copy_path_component:
    les bx, dword ptr [bp+0eh]
    add bx, dx
    push es
    les si, dword ptr [bp+0ah]
    mov al, byte ptr es:[si]
    pop es
    mov byte ptr es:[bx], al
    inc word ptr [bp+0ah]
    inc dx
test_path_component_end:
    les bx, dword ptr [bp+0ah]
    cmp byte ptr es:[bx], 03bh
    je short finish_path_component
    cmp byte ptr es:[bx], 0
    jne short copy_path_component
finish_path_component:
    les bx, dword ptr [bp+0ah]
    cmp byte ptr es:[bx], 0
    jne short skip_component_semicolon
    jmp near ptr format_candidate_root
skip_component_semicolon:
    inc word ptr [bp+0ah]
    jmp near ptr format_candidate_root
canonicalize_accessible_path:
    mov ax, 050h
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    xor ax, ax
    push ax
    push ax
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 095h
    call _strcat
    add sp, 8
    xor ax, ax
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 081h
    call _strcat
    add sp, 8
append_original_filename:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 077h
    mov ax,offset DGROUP:path_separator
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 06Ah
    call ___path_issbcs
    add sp, 8
    or ax, ax
    jne short append_original_filename
append_dos_path_separator:
    push ds
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 02Bh
    call _strlen
    pop cx
    pop cx
    mov dx, ax
format_candidate_root:
    les bx, dword ptr [bp+0eh]
    add bx, dx
    mov byte ptr es:[bx], 0
    or dx, dx
    je short append_original_filename
    mov bx, dx
    add bx, word ptr [bp+0eh]
    mov bl, byte ptr es:[bx-1]
    mov al, bl
    cmp al, 05ch
    je short inspect_trailing_path_separator
    cmp bl, 02fh
    je short inspect_trailing_path_separator
    cmp bl, 03ah
    jne short append_dos_path_separator
inspect_trailing_path_separator:
    mov ax, word ptr [bp+0eh]
    add ax, dx
    dec ax
    push word ptr [bp+010h]
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 015h
    call __getdcwd
    add sp, 8
    or ax, dx
    jne short cwd_was_available
    xor dx, dx
    jmp short format_candidate_root
cwd_was_available:
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
_TEXT ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
org 00h
__searchstr label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, 050h
    push ax
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    xor ax, ax
    push ax
_TEXT ends
end
