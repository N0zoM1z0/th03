; Canonicalize a DOS path in a161-byte temporary allocation. All pointer
; increments retain the original16-bit offset-only behavior and unchecked copy.
.8086
extrn __ctype:byte,_toupper:far,__getdcwd:far,__dos_getdrive:far
extrn _free:far,_malloc:far,_realloc:far,_strcpy:far,_strlen:far
extrn ___path_isdbcsleadbyte:far,___path_issbcs:far
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
is_separator proc near
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+4]
    cmp ax,'\'
    je separator_true
    cmp ax,'/'
    jne separator_false
separator_true:
    mov ax,1
    jmp short separator_done
separator_false:
    xor ax,ax
separator_done:
    pop di
    pop si
    pop bp
    ret 2
is_separator endp
; near callee-pop8: candidate character pointer, followed by string start.
is_sbcs_separator proc near
    push bp
    mov bp,sp
    push si
    push di
    les bx,[bp+4]
    mov al,es:[bx]
    mov ah,0
    push ax
    call is_separator
    or ax,ax
    je sbcs_separator_false
    push word ptr [bp+6]
    push word ptr [bp+4]
    push word ptr [bp+10]
    push word ptr [bp+8]
    call ___path_issbcs
    add sp,8
    or ax,ax
    je sbcs_separator_false
    mov ax,1
    jmp short sbcs_separator_done
sbcs_separator_false:
    xor ax,ax
sbcs_separator_done:
    pop di
    pop si
    pop bp
    ret 8
is_sbcs_separator endp
public __fullpath
__fullpath proc far
    push bp
    mov bp,sp
    sub sp,18
    push si
    push di
    ; BP-4/-2 temporary, -8/-6 destination, -12/-10 source,
    ; -14 character, -16 drive letter, -18 one-based drive number.
    mov ax,161
    push ax
    call _malloc
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jne temporary_allocated
    jmp fullpath_failed
 temporary_allocated:
    mov dx,[bp+12]
    mov ax,[bp+10]
    mov [bp-10],dx
    mov [bp-12],ax
    les bx,[bp-12]
    mov al,es:[bx]
    cbw
    mov bx,ax
    test byte ptr DGROUP:__ctype[bx+1],0ch
    je default_drive
    mov bx,[bp-12]
    cmp byte ptr es:[bx+1],':'
    jne default_drive
    mov al,es:[bx]
    cbw
    mov [bp-16],ax
    push ax
    call _toupper
    pop cx
    add ax,-64
    mov [bp-18],ax
    add word ptr [bp-12],2
    jmp short drive_selected
 default_drive:
    push ss
    lea ax,[bp-18]
    push ax
    call __dos_getdrive
    pop cx
    pop cx
    mov ax,[bp-18]
    add ax,'A'
    dec ax
    mov [bp-16],ax
 drive_selected:
    les bx,[bp-12]
    mov al,es:[bx]
    cbw
    push ax
    call is_separator
    or ax,ax
    jne absolute_path
    mov ax,161
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp-18]
    call __getdcwd
    add sp,8
    or ax,dx
    jne directory_loaded
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _free
    pop cx
    pop cx
    jmp fullpath_failed
 directory_loaded:
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _strlen
    pop cx
    pop cx
    mov dx,[bp-2]
    add ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    push dx
    push word ptr [bp-4]
    dec ax
    push dx
    push ax
    call is_sbcs_separator
    or ax,ax
    jne append_input
    les bx,[bp-8]
    mov byte ptr es:[bx],'\'
    jmp short advance_prefix
 absolute_path:
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    les bx,[bp-8]
    mov al,[bp-16]
    mov es:[bx],al
    inc word ptr [bp-8]
    les bx,[bp-8]
    mov byte ptr es:[bx],':'
 advance_prefix:
    inc word ptr [bp-8]
 append_input:
    push word ptr [bp-10]
    push word ptr [bp-12]
    push word ptr [bp-6]
    push word ptr [bp-8]
    call _strcpy
    add sp,8
    mov dx,[bp-2]
    mov ax,[bp-4]
    mov [bp-6],dx
    mov [bp-8],ax
    mov [bp-10],dx
    mov [bp-12],ax
 scan_character:
    les bx,[bp-12]
    inc word ptr [bp-12]
    mov al,es:[bx]
    cbw
    mov [bp-14],ax
    or ax,ax
    je component_boundary
    push ax
    call is_separator
    or ax,ax
    jne component_boundary
    jmp copy_character
 component_boundary:
    les bx,[bp-8]
    cmp byte ptr es:[bx-1],'.'
    jne test_parent_component
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax,[bp-8]
    add ax,-2
    push word ptr [bp-6]
    push ax
    call is_sbcs_separator
    or ax,ax
    je test_parent_component
    sub word ptr [bp-8],2
    jmp short component_reduced
 test_parent_component:
    les bx,[bp-8]
    cmp byte ptr es:[bx-1],'.'
    jne component_reduced
    cmp byte ptr es:[bx-2],'.'
    jne component_reduced
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax,[bp-8]
    add ax,-3
    push word ptr [bp-6]
    push ax
    call is_sbcs_separator
    or ax,ax
    je component_reduced
    sub word ptr [bp-8],3
    les bx,[bp-8]
    cmp byte ptr es:[bx-1],':'
    jne retreat_component
    mov ax,[bp-8]
    dec ax
    push word ptr [bp-6]
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    call ___path_issbcs
    add sp,8
    or ax,ax
    je retreat_component
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _free
    pop cx
    pop cx
    jmp fullpath_failed
 retreat_component:
    push word ptr [bp-2]
    push word ptr [bp-4]
    dec word ptr [bp-8]
    mov ax,[bp-8]
    push word ptr [bp-6]
    push ax
    call is_sbcs_separator
    or ax,ax
    je retreat_component
 component_reduced:
    cmp word ptr [bp-14],0
    je terminate_path
    jmp copy_boundary
 terminate_path:
    push word ptr [bp-2]
    push word ptr [bp-4]
    mov ax,[bp-8]
    dec ax
    push word ptr [bp-6]
    push ax
    call is_sbcs_separator
    or ax,ax
    je test_drive_root
    dec word ptr [bp-8]
 test_drive_root:
    les bx,[bp-8]
    cmp byte ptr es:[bx-1],':'
    jne write_terminator
    mov ax,[bp-8]
    dec ax
    push word ptr [bp-6]
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    call ___path_issbcs
    add sp,8
    or ax,ax
    je write_terminator
    les bx,[bp-8]
    mov byte ptr es:[bx],'\'
    inc word ptr [bp-8]
 write_terminator:
    les bx,[bp-8]
    mov byte ptr es:[bx],0
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _strlen
    pop cx
    pop cx
    inc ax
    mov dx,ax
    mov ax,[bp+6]
    or ax,[bp+8]
    jne check_caller_size
    jmp resize_temporary
 check_caller_size:
    cmp dx,[bp+14]
    jbe copy_to_caller
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _free
    pop cx
    pop cx
 fullpath_failed:
    xor dx,dx
    xor ax,ax
    jmp short fullpath_done
 copy_boundary:
    les bx,[bp-8]
    mov al,[bp-14]
    mov es:[bx],al
    jmp short advance_destination
 copy_character:
    les bx,[bp-8]
    mov al,[bp-14]
    mov es:[bx],al
    inc word ptr [bp-8]
    push word ptr [bp-14]
    call ___path_isdbcsleadbyte
    pop cx
    or ax,ax
    jne copy_trail_if_present
    jmp scan_character
 copy_trail_if_present:
    les bx,[bp-12]
    cmp byte ptr es:[bx],0
    jne copy_trail
    jmp scan_character
 copy_trail:
    mov al,es:[bx]
    les bx,[bp-8]
    mov es:[bx],al
    inc word ptr [bp-12]
 advance_destination:
    inc word ptr [bp-8]
    jmp scan_character
 copy_to_caller:
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strcpy
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _free
    add sp,12
    mov dx,[bp+8]
    mov ax,[bp+6]
    jmp short fullpath_done
 resize_temporary:
    push dx
    push word ptr [bp-2]
    push word ptr [bp-4]
    call _realloc
    add sp,6
 fullpath_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__fullpath endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
