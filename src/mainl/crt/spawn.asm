; Original Borland DOS spawn core, including the 4-byte CODE-resident
; saved SS:SP during INT 21h/4B00h program execution.
.8086
extrn __IOERROR:near
extrn __psp:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; These are live CODE-resident stack registers, not anonymous padding.
spawn_saved_sp dw ?
spawn_saved_ss dw ?

public __spawn
__spawn proc near
    push bp
    mov bp,sp
    sub sp,2eh
    push si
    push ds
    push di
    push es
    push ss
    pop es
    mov ax,[bp+0ch]
    mov dx,[bp+0eh]
    mov cl,4
    shr ax,cl
    add ax,dx
    mov [bp-0eh],ax
    push ds
    lds si,dword ptr [bp+8]
    mov [bp-0ch],si
    mov [bp-0ah],ds
    mov ax,2901h
    lea di,[bp-2eh]
    mov [bp-8],di
    mov [bp-6],es
    inc si
    int 21h
scan_command_delimiter:
    mov al,[si]
    cmp al,20h
    je short parse_second_command
    cmp al,9
    je short parse_second_command
    cmp al,0dh
    je short parse_second_command
    inc si
    jmp short scan_command_delimiter
parse_second_command:
    mov ax,2901h
    lea di,[bp-1eh]
    mov [bp-4],di
    mov [bp-2],es
    int 21h
    pop ds
    push ds
    push es
    mov es,word ptr __psp
    lds si,dword ptr [bp+4]
    mov di,80h
    mov cx,7fh
    cld
copy_psp_command_tail:
    lodsb
    test al,al
    je short terminate_psp_tail
    stosb
    loop copy_psp_command_tail
    mov al,0
terminate_psp_tail:
    stosb
    pop es
    pop ds
    push bp
    push ds
    lea bx,[bp-0eh]
    mov ds,word ptr __psp
    mov dx,80h
    mov ax,4b00h
    push word ptr ss:[2eh]
    push word ptr ss:[30h]
    mov word ptr cs:spawn_saved_ss,ss
    mov word ptr cs:spawn_saved_sp,sp
    int 21h
    cli
    mov ss,word ptr cs:spawn_saved_ss
    mov sp,word ptr cs:spawn_saved_sp
    sti
    pop word ptr ss:[30h]
    pop word ptr ss:[2eh]
    pop ds
    pop bp
    jae short child_succeeded
    push ax
    call __IOERROR
    jmp short return_child_status
child_succeeded:
    mov ah,4dh
    int 21h
return_child_status:
    pop es
    pop di
    pop ds
    pop si
    mov sp,bp
    pop bp
    ret
__spawn endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
