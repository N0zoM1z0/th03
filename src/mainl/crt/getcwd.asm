; Original Borland large-model current-directory fetch, far buffer and errno.
; The original 68-byte temporary stack buffer retains the drive prefix.
.8086
extrn _getcurdir:far,_getdisk:far,_strcpy:far,_strlen:far,_errno:word,_malloc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getcwd
_getcwd proc far
    push bp
    mov bp,sp
    sub sp,68
    push si
    push di
    call _getdisk
    add al,'A'
    mov byte ptr [bp-68],al
    mov byte ptr [bp-67],':'
    mov byte ptr [bp-66],'\'
    push ss
    lea ax,[bp-65]
    push ax
    xor ax,ax
    push ax
    call _getcurdir
    add sp,6
    cmp ax,-1
    je failed
    push ss
    lea ax,[bp-68]
    push ax
    call _strlen
    pop cx
    pop cx
    cmp ax,[bp+10]
    jb enough_space
    mov word ptr DGROUP:_errno,34
    jmp short failed
enough_space:
    mov ax,[bp+6]
    or ax,[bp+8]
    jne copy_path
    push word ptr [bp+10]
    call _malloc
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jne copy_path
    mov word ptr DGROUP:_errno,8
failed:
    xor dx,dx
    xor ax,ax
    jmp short result
copy_path:
    push ss
    lea ax,[bp-68]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call _strcpy
    add sp,8
    mov dx,[bp+8]
    mov ax,[bp+6]
result:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_getcwd endp
_TEXT ends
end
