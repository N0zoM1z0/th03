; Original Borland DOS text-stream Ctrl-Z ending management.
; Two private NEAR seek/read helpers, two public NEAR procedures.
.8086
extrn _lseek:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

seek_end_minus_one proc near
    push bp
    mov bp,sp
    push si
    push di
    mov bx,[bp+4]
    mov cx,-1
    mov dx,cx
    mov ax,4202h
    int 21h
    pop di
    pop si
    pop bp
    ret 2
seek_end_minus_one endp

read_byte_from_dos proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov byte ptr [bp-1],0
    push ds
    mov bx,[bp+4]
    mov cx,1
    push ss
    pop ds
    lea dx,[bp-1]
    mov ah,3fh
    int 21h
    pop ds
    mov al,[bp-1]
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 2
read_byte_from_dos endp

public __TRIMCTLZ
__TRIMCTLZ proc near
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+4]
    call seek_end_minus_one
    push dx
    push ax
    push word ptr [bp+4]
    call read_byte_from_dos
    cmp al,1ah
    jne short restore_original_position
    push word ptr [bp+4]
    call seek_end_minus_one
    mov bx,[bp+4]
    sub cx,cx
    sub dx,dx
    mov ah,40h
    int 21h
restore_original_position:
    mov bx,[bp+4]
    pop dx
    pop cx
    mov ax,4200h
    int 21h
    xor ax,ax
    push ax
    push ax
    push ax
    push word ptr [bp+4]
    call _lseek
    add sp,8
    pop di
    pop si
    pop bp
    ret 2
__TRIMCTLZ endp

public __APPENDCTLZ
__APPENDCTLZ proc near
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    mov byte ptr [bp-1],1ah
    push word ptr [bp+4]
    call seek_end_minus_one
    push word ptr [bp+4]
    call read_byte_from_dos
    cmp al,1ah
    je short done_append
    push ds
    mov bx,[bp+4]
    mov cx,1
    push ss
    pop ds
    lea dx,[bp-1]
    mov ah,40h
    int 21h
    pop ds
done_append:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 2
__APPENDCTLZ endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
