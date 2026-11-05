; Complete NEC PC-98 BIOS disk driver call (original Japanese Borland CRT).
; Performs authentic INT 1Bh transfer and conditionally copies firmware
; disk-parameter vectors from physical memory for the original commands.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __necpc_bios_disk
__necpc_bios_disk proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    mov ah,byte ptr [bp+6]
    lds di,dword ptr [bp+8]
    mov dx,word ptr [di]
    mov al,byte ptr [di+2]
    cmp dl,50h
    jnz short command_ready
    cmp ah,8dh
    jnz short command_ready
    and ah,7fh
command_ready:
    or ax,dx
    mov bx,word ptr [di+8]
    cmp byte ptr [di],80h
    jz short long_disk_sector
    mov ch,byte ptr [di+0ah]
    mov cl,byte ptr [di+6]
    jmp short sector_ready
long_disk_sector:
    mov cx,word ptr [di+6]
    cmp byte ptr [bp+6],8dh
    jz short long_sector_cylinder
    cmp byte ptr [bp+6],0dh
    jnz short sector_ready
long_sector_cylinder:
    mov bh,bl
sector_ready:
    mov dh,byte ptr [di+4]
    mov dl,byte ptr [di+0ch]
    cmp byte ptr [bp+4],8
    jnz short drive_number_ready
    xor dl,dl
drive_number_ready:
    push bp
    les bp,dword ptr [di+10h]
    int 1bh
    pop bp
    mov al,0
    jnc short transfer_succeeded
    mov al,0ffh
transfer_succeeded:
    xchg ah,al
    push ax
    push di
    push ds
    pop es
    mov di,offset DGROUP:disk_command_ids
    push cx
    mov cx,8
    mov al,byte ptr [bp+6]
    repne scasb
    pop cx
    pop bx
    jnz short disk_done
    cmp al,0ah
    jz short copy_param_block
    cmp byte ptr [bx],50h
    jz short disk_done
    cmp byte ptr [bx],80h
    jz short disk_done
copy_param_block:
    mov cx,8
    mov si,05d0h
    cmp byte ptr [bx],70h
    jz short copy_disk_params
    mov cx,4
    mov ax,word ptr [bx+2]
    shl ax,1
    shl ax,1
    shl ax,1
    add ax,0564h
    mov si,ax
copy_disk_params:
    les di,dword ptr [bx+14h]
    xor ax,ax
    mov ds,ax
    rep movsw
disk_done:
    pop ax
    pop ds
    pop di
    pop si
    pop bp
    retf
__necpc_bios_disk endp
_TEXT ends
_DATA segment word public 'DATA'
; BIOS command classes for DOS disk parameter-update decisions.
disk_command_ids db 06h,05h,10h,01h,0ah,09h,0ch,02h
_DATA ends
end
