; Original DOS Borland large-model file open translation unit.
; Private near DOS Create and zero-length truncate routines precede
; public far-cdecl _open: input mode, DOS flags, errno translation,
; original umask, IOCTL, descriptor table and process-exit cleanup.
; Keep the far __rtl_open/close/chmod and near __IOERROR real calls.
; No embedded opcode arrays, post-link patches or artificial filler.
.8086
extrn _errno:word
extrn __doserrno:word
extrn __rtl_chmod:far
extrn __rtl_close:far
extrn _ioctl:far
extrn __rtl_open:far
extrn __IOERROR:near
extrn __openfd:word
extrn __fmode:word
extrn __notUmask:word
extrn __exitopen:word
extrn __xclose:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
dos_create_with_attr proc near
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov cx, word ptr [bp+4]
    mov ah, 03ch
    lds dx, dword ptr [bp+6]
    int 021h
    pop ds
    jb short ioerror_create
    jmp short return_dos_create
ioerror_create:
    push ax
    call __IOERROR
return_dos_create:
    pop di
    pop si
    pop bp
    ret 6
dos_create_with_attr endp
dos_zero_length_file proc near
    push bp
    mov bp, sp
    push si
    push di
    mov bx, word ptr [bp+4]
    sub cx, cx
    sub dx, dx
    mov ah, 040h
    int 021h
    pop di
    pop si
    pop bp
    ret 2
dos_zero_length_file endp
public _open
_open proc far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    test byte ptr [bp+0bh], 0c0h
    jne short load_errno_before_open
    mov ax,word ptr DGROUP:__fmode
    and ax, 0c000h
    or word ptr [bp+0ah], ax
load_errno_before_open:
    mov ax,word ptr DGROUP:_errno
    mov word ptr [bp-6], ax
    xor ax, ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_chmod
    add sp, 6
    mov word ptr [bp-2], ax
    mov ax, word ptr [bp-6]
    mov word ptr DGROUP:_errno,ax
    test byte ptr [bp+0bh], 1
    jne short apply_umask
    jmp near ptr open_desired_access
apply_umask:
    mov ax,word ptr DGROUP:__notUmask
    and word ptr [bp+0ch], ax
    mov ax, word ptr [bp+0ch]
    test ax, 0180h
    jne short check_initial_open
    mov ax, 1
    push ax
    call __IOERROR
check_initial_open:
    cmp word ptr [bp-2], -1
    jne short try_create_if_missing
    cmp word ptr DGROUP:__doserrno,2
    je short select_file_create_mode
    push word ptr DGROUP:__doserrno
    jmp short open_at_0d3
select_file_create_mode:
    test byte ptr [bp+0ch], 080h
    je short open_at_0a7
    xor ax, ax
    jmp short fallback_existing_mode
open_at_0a7:
    mov ax, 1
fallback_existing_mode:
    mov word ptr [bp-2], ax
    test byte ptr [bp+0ah], 0f0h
    je short create_with_initial_mode
    push word ptr [bp+8]
    push word ptr [bp+6]
    xor ax, ax
    push ax
    call dos_create_with_attr
    mov word ptr [bp-8], ax
    or ax, ax
    jge short chmod_after_create
    jmp near ptr return_open_result
try_create_if_missing:
    test byte ptr [bp+0bh], 4
    je short open_desired_access
    mov ax, 050h
    push ax
open_at_0d3:
    call __IOERROR
    jmp near ptr open_done
chmod_after_create:
    push word ptr [bp-8]
    call __rtl_close
    pop cx
    jmp short open_desired_access
create_with_initial_mode:
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp-2]
    call dos_create_with_attr
    mov word ptr [bp-8], ax
    or ax, ax
    jl short open_at_0fa
    jmp near ptr check_open_status
open_at_0fa:
    jmp near ptr return_open_result
open_desired_access:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_open
    add sp, 6
    mov word ptr [bp-8], ax
    or ax, ax
    jl short check_open_status
    xor ax, ax
    push ax
    push word ptr [bp-8]
    call _ioctl
    pop cx
    pop cx
    mov word ptr [bp-4], ax
    test al, 080h
    je short after_ioctl
    or word ptr [bp+0ah], 02000h
    test byte ptr [bp+0bh], 080h
    je short apply_open_flags
    and ax, 0ffh
    or ax, 020h
    xor dx, dx
    push dx
    push ax
    mov ax, 1
    push ax
    push word ptr [bp-8]
    call _ioctl
    add sp, 8
    jmp short apply_open_flags
after_ioctl:
    test byte ptr [bp+0bh], 2
    je short apply_open_flags
    push word ptr [bp-8]
    call dos_zero_length_file
apply_open_flags:
    test byte ptr [bp-2], 1
    je short check_open_status
    test byte ptr [bp+0bh], 1
    je short check_open_status
    test byte ptr [bp+0ah], 0f0h
    je short check_open_status
    mov ax, 1
    push ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __rtl_chmod
    add sp, 8
check_open_status:
    cmp word ptr [bp-8], 0
    jl short return_open_result
    mov word ptr DGROUP:__exitopen+2,seg __xclose
    mov word ptr DGROUP:__exitopen,offset __xclose
    test byte ptr [bp+0bh], 3
    je short open_at_19d
    mov ax, 01000h
    jmp short open_at_19f
open_at_19d:
    xor ax, ax
open_at_19f:
    mov dx, word ptr [bp+0ah]
    and dx, 0f8ffh
    or ax, dx
    push ax
    test byte ptr [bp-2], 1
    je short open_at_1b3
    xor ax, ax
    jmp short open_at_1b6
open_at_1b3:
    mov ax, 0100h
open_at_1b6:
    pop dx
    or dx, ax
    mov bx, word ptr [bp-8]
    add bx, bx
    mov word ptr DGROUP:[bx+__openfd],dx
return_open_result:
    mov ax, word ptr [bp-8]
open_done:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_open endp
_TEXT ends
end
