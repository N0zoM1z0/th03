; DOS AH=47 current directory, with optional allocation and an explicit drive.
.8086
extrn _malloc:far,_errno:word,_strcpy:far,_strlen:far
ERANGE equ 34
ENOMEM equ 8
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __getdcwd
__getdcwd proc far
    push bp
    mov bp,sp
    sub sp,72
    push si
    push di
    ; 70-byte unchecked local path and a WORD drive number.
    mov ax,[bp+6]
    mov [bp-2],ax
    or ax,ax
    jne drive_selected
    mov ah,19h
    int 21h
    mov ah,0
    inc ax
    mov [bp-2],ax
 drive_selected:
    mov al,[bp-2]
    add al,40h
    mov [bp-72],al
    mov byte ptr [bp-71],':'
    mov byte ptr [bp-70],'\'
    push ds
    mov ax,ss
    mov ds,ax
    lea si,[bp-69]
    mov ah,47h
    mov dl,[bp-2]
    int 21h
    pop ds
    jc directory_failed
    push ss
    lea ax,[bp-72]
    push ax
    call _strlen
    pop cx
    pop cx
    cmp ax,[bp+12]
    jb directory_fits
    mov word ptr DGROUP:_errno,ERANGE
    jmp short directory_failed
 directory_fits:
    mov ax,[bp+8]
    or ax,[bp+10]
    jne copy_directory
    push word ptr [bp+12]
    call _malloc
    pop cx
    mov [bp+10],dx
    mov [bp+8],ax
    or ax,dx
    jne copy_directory
    mov word ptr DGROUP:_errno,ENOMEM
 directory_failed:
    xor dx,dx
    xor ax,ax
    jmp short directory_done
 copy_directory:
    push ss
    lea ax,[bp-72]
    push ax
    push word ptr [bp+10]
    push word ptr [bp+8]
    call _strcpy
    add sp,8
    mov dx,[bp+10]
    mov ax,[bp+8]
 directory_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__getdcwd endp
_TEXT ends
end
