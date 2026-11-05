; Original Borland DOS absolute disk I/O for Japanese PC-98 MAINL CRT.
; INT 25h/26h use the real 16-bit large-model calling convention and
; the original DOS disk transfer descriptor / legacy short form selection.
.8086
extrn _getfat:far,_errno:word,N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
; Borland native GROUP has BSS first, DATA second, with a separate
; initialized 0ffffh last-drive word and uninitialized cached mode.
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
large_drive_mode dw ?
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Internal far ABI disk-format probe, called by pushing CS before near call.
absdisk_probe proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov dx,[bp+6]
    cmp dx,word ptr DGROUP:cached_drive
    jz short have_drive_mode
    mov word ptr DGROUP:cached_drive,dx
    push ss
    lea ax,[bp-6]
    push ax
    mov al,dl
    inc al
    push ax
    call _getfat
    add sp,6
    mov al,[bp-6]
    cbw
    cwd
    push ax
    mov ax,[bp-4]
    push dx
    xor dx,dx
    pop cx
    pop bx
    call N_LXMUL@
    or dx,dx
    jc short within_sector_limit
    ja short beyond_sector_limit
    cmp ax,0ffffh
    jna short within_sector_limit
beyond_sector_limit:
    mov ax,1
    jmp short save_mode
within_sector_limit:
    xor ax,ax
save_mode:
    mov word ptr DGROUP:large_drive_mode,ax
have_drive_mode:
    mov ax,word ptr DGROUP:large_drive_mode
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
absdisk_probe endp

public _absread
_absread proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    push word ptr [bp+6]
    push cs
    call near ptr absdisk_probe
    pop cx
    or ax,ax
    jz short legacy_read
    mov al,[bp+6]
    push ss
    pop ds
    sub sp,10
    mov bx,sp
    mov dx,[bp+10]
    mov word ptr [bx],dx
    mov dx,[bp+12]
    mov word ptr [bx+2],dx
    mov cx,[bp+8]
    mov [bx+4],cx
    mov dx,[bp+14]
    mov word ptr [bx+6],dx
    mov dx,[bp+16]
    mov word ptr [bx+8],dx
    mov cx,0ffffh
    int 25h
    sbb cx,cx
    add sp,10
    jmp short read_finish
legacy_read:
    mov al,[bp+6]
    mov cx,[bp+8]
    mov dx,[bp+10]
    lds bx,dword ptr [bp+14]
    int 25h
    sbb cx,cx
read_finish:
    pop bx
    pop ds
    jcxz short read_success
    mov word ptr _errno,ax
    mov ax,0ffffh
    jmp short read_exit
read_success:
    xor ax,ax
read_exit:
    pop di
    pop si
    pop bp
    retf
_absread endp

public _abswrite
_abswrite proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    push word ptr [bp+6]
    push cs
    call near ptr absdisk_probe
    pop cx
    or ax,ax
    jz short legacy_write
    mov al,[bp+6]
    push ss
    pop ds
    sub sp,10
    mov bx,sp
    mov dx,[bp+10]
    mov word ptr [bx],dx
    mov dx,[bp+12]
    mov word ptr [bx+2],dx
    mov cx,[bp+8]
    mov [bx+4],cx
    mov dx,[bp+14]
    mov word ptr [bx+6],dx
    mov dx,[bp+16]
    mov word ptr [bx+8],dx
    mov cx,0ffffh
    int 26h
    sbb cx,cx
    add sp,10
    jmp short write_finish
legacy_write:
    mov al,[bp+6]
    mov cx,[bp+8]
    mov dx,[bp+10]
    lds bx,dword ptr [bp+14]
    int 26h
    sbb cx,cx
write_finish:
    pop bx
    pop ds
    jcxz short write_success
    mov word ptr _errno,ax
    mov ax,0ffffh
    jmp short write_exit
write_success:
    xor ax,ax
write_exit:
    pop di
    pop si
    pop bp
    retf
_abswrite endp
_TEXT ends
_DATA segment word public 'DATA'
cached_drive dw 0ffffh
_DATA ends
end
