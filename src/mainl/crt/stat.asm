; Original Borland DOS large-model stat: private far path-delimiter
; helper and public far _stat. DOS FindFirst and DTA stack owner,
; fullpath/free lifetime, case/drive parsing, FILE attributes and
; local DOS timestamp conversion are preserved from real 8086 code.
; Four bytes of actual initialized DATA are named DOS path separators.
; No machine opcode arrays, synthetic filler or patched original OMF.
.8086
extrn __IOERROR:near
extrn __DOSTIMETOU:near
extrn _free:far
extrn __fullpath:far
extrn ___path_isdbcsleadbyte:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
stat_separators db 5Ch,2Fh,2Eh,0 ; DOS backslash,slash,dot,NUL
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
stat_find_delimiter proc far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    jmp short check_end_of_path
inspect_next_far_path_byte:
    les bx, dword ptr [bp-4]
    mov al, byte ptr es:[bx]
    push ax
    call ___path_isdbcsleadbyte
    pop cx
    or ax, ax
    je short scan_delimiter_set
    inc word ptr [bp-4]
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    jne short advance_path_character
    jmp short delimiter_missing
scan_delimiter_set:
    mov dx, word ptr [bp+0ch]
    mov ax, word ptr [bp+0ah]
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    jmp short check_delimiter_end
compare_path_delimiter:
    les bx, dword ptr [bp-4]
    mov al, byte ptr es:[bx]
    les bx, dword ptr [bp-8]
    cmp al, byte ptr es:[bx]
    je short found_delimiter
    inc word ptr [bp-8]
check_delimiter_end:
    les bx, dword ptr [bp-8]
    cmp byte ptr es:[bx], 0
    jne short compare_path_delimiter
found_delimiter:
    les bx, dword ptr [bp-8]
    cmp byte ptr es:[bx], 0
    je short advance_path_character
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    jmp short return_delimiter
advance_path_character:
    inc word ptr [bp-4]
check_end_of_path:
    les bx, dword ptr [bp-4]
    cmp byte ptr es:[bx], 0
    jne short inspect_next_far_path_byte
delimiter_missing:
    xor dx, dx
    xor ax, ax
return_delimiter:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
stat_find_delimiter endp
public _stat
_stat proc far
    push bp
    mov bp, sp
    sub sp, 036h
    push si
    push di
    push ds
    push ss
    pop ds
    lea dx, [bp-036h]
    mov ah, 01ah
    int 021h
    pop ds
    jb short stat_findfirst_error
    push ds
    lds dx, dword ptr [bp+6]
    mov cx, 016h
    mov ah, 04eh
    int 021h
    pop ds
    jb short stat_findfirst_error
    jmp near ptr stat_fill_information
stat_findfirst_error:
    mov word ptr [bp-2], ax
    push ds
    mov ax,offset DGROUP:stat_separators
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push cs
    call near ptr stat_find_delimiter
    add sp, 8
    or ax, dx
    jne short stat_resolve_far_path
    jmp near ptr stat_fail
stat_resolve_far_path:
    xor ax, ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ax
    push ax
    call __fullpath
    add sp, 0ah
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, dx
    jne short check_path_filename_suffix
    jmp short stat_fail
check_path_filename_suffix:
    les bx, dword ptr [bp-6]
    mov al, byte ptr es:[bx]
    cbw
    mov word ptr [bp-8], ax
    mov al, byte ptr es:[bx+3]
    cbw
    mov word ptr [bp-0ah], ax
    cmp word ptr [bp-0ah], 0
    jne short stat_findfirst_retry
    push dx
    push bx
    call _free
    pop cx
    pop cx
    cmp word ptr [bp-8], 061h
    jl short set_dir_entry_case
    cmp word ptr [bp-8], 07ah
    jg short set_dir_entry_case
    mov al, 061h
    jmp short set_drive_suffix
set_dir_entry_case:
    mov al, 041h
set_drive_suffix:
    mov dl, byte ptr [bp-8]
    sub dl, al
    mov byte ptr [bp-036h], dl
    mov word ptr [bp-020h], 0
    mov word ptr [bp-01eh], 021h
    mov word ptr [bp-01ah], 0
    mov word ptr [bp-01ch], 0
    mov si, 04140h
    jmp near ptr convert_dos_time
stat_findfirst_retry:
    push ds
    lds dx, dword ptr [bp-6]
    mov cx, 016h
    mov ah, 04eh
    int 021h
    pop ds
    pushf
    push word ptr [bp-4]
    push word ptr [bp-6]
    call _free
    pop cx
    pop cx
    popf
    jae short stat_fill_information
stat_fail:
    push word ptr [bp-2]
    call __IOERROR
    jmp near ptr stat_return
stat_fill_information:
    test byte ptr [bp-021h], 040h
    jne short check_directory_flag
    cmp byte ptr [bp-036h], 01ah
    jle short check_directory_flag
    xor ax, ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    push ax
    push ax
    call __fullpath
    add sp, 0ah
    mov word ptr [bp-4], dx
    mov word ptr [bp-6], ax
    or ax, dx
    je short check_directory_flag
    les bx, dword ptr [bp-6]
    cmp byte ptr es:[bx], 061h
    jl short stat_dos_attribute
    cmp byte ptr es:[bx], 07ah
    jg short stat_dos_attribute
    mov al, 061h
    jmp short stat_at_19e
stat_dos_attribute:
    mov al, 041h
stat_at_19e:
    les bx, dword ptr [bp-6]
    mov dl, byte ptr es:[bx]
    inc dl
    sub dl, al
    mov byte ptr [bp-036h], dl
    push word ptr [bp-4]
    push bx
    call _free
    pop cx
    pop cx
check_directory_flag:
    mov dl, byte ptr [bp-021h]
    sub si, si
    test dl, 040h
    jne short stat_directory_path
    or si, 0100h
    dec byte ptr [bp-036h]
    test dl, 010h
    jne short stat_file_mode_done
    or si, 08100h
    test dl, 1
    jne short convert_dos_time
    or si, 080h
    jmp short convert_dos_time
stat_file_mode_done:
    or si, 04040h
convert_dos_time:
    push word ptr [bp-01eh]
    push word ptr [bp-020h]
    call __DOSTIMETOU
    xchg cx, ax
    jmp short write_file_stat
stat_directory_path:
    mov word ptr [bp-036h], 0ffffh
    or si, 02180h
    sub cx, cx
    mov dx, cx
write_file_stat:
    les di, dword ptr [bp+0ah]
    cld
    mov al, byte ptr [bp-036h]
    cbw
    stosw
    xchg bx, ax
    sub ax, ax
    stosw
    xchg si, ax
    stosw
    mov ax, 1
    stosw
    xchg si, ax
    stosw
    stosw
    xchg bx, ax
    stosw
    mov ax, word ptr [bp-01ch]
    stosw
    mov ax, word ptr [bp-01ah]
    stosw
    xchg cx, ax
    stosw
    xchg dx, ax
    stosw
    xchg dx, ax
    stosw
    xchg dx, ax
    stosw
    xchg dx, ax
    stosw
    xchg dx, ax
    stosw
    xor ax, ax
stat_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_stat endp
_TEXT ends
end
