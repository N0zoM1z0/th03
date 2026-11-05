; Japanese PC-98 direct text-VRAM access and character output CRT.
; Original zero-initialized BSS records the active plane cursor, while the
; real __video/__wgarbage/___row/___col imports retain their DOS ABI.
.8086
extrn __wgarbage:word,__video:byte,___col:word,___row:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
cursor_vram_offset dw ?
cursor_vram_segment dw ?
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

public __NEC_RESET_VRAM_ACCESS
__NEC_RESET_VRAM_ACCESS proc near
    push si
    push di
    mov word ptr DGROUP:cursor_vram_segment,0
    pop di
    pop si
    ret
__NEC_RESET_VRAM_ACCESS endp

public __NEC_START_VRAM_ACCESS
__NEC_START_VRAM_ACCESS proc near
    push si
    push di
    cmp word ptr DGROUP:cursor_vram_segment,0
    jnz short start_done
    mov al,byte ptr ___row
    mov ah,byte ptr __video+10
    mul ah
    add ax,word ptr ___col
    shl ax,1
    les bx,dword ptr __video+16
    add bx,ax
    mov word ptr DGROUP:cursor_vram_offset,bx
    mov word ptr DGROUP:cursor_vram_segment,es
    cmp word ptr __wgarbage,0
    jz short start_done
    cmp word ptr ___col,0
    jz short start_done
    mov ax,word ptr es:[bx-2]
    or ah,ah
    jz short start_done
    test ax,8080h
    jnz short start_done
    cmp al,9
    jb short clear_prev
    cmp al,12
    jb short start_done
clear_prev:
    mov ax,20h
    mov word ptr es:[bx-2],ax
start_done:
    pop di
    pop si
    ret
__NEC_START_VRAM_ACCESS endp

public __NEC_END_VRAM_ACCESS
__NEC_END_VRAM_ACCESS proc near
    push si
    push di
    cmp word ptr DGROUP:cursor_vram_segment,0
    jz short end_done
    cmp word ptr __wgarbage,0
    jz short reset_access
    mov al,byte ptr ___col
    cmp al,byte ptr __video+10
    jnc short reset_access
    les bx,dword ptr DGROUP:cursor_vram_offset
    mov ax,word ptr es:[bx]
    or ah,ah
    jz short reset_access
    test ax,8080h
    jz short reset_access
    and al,7fh
    cmp al,9
    jb short clear_current
    cmp al,12
    jb short reset_access
clear_current:
    mov ax,20h
    mov word ptr es:[bx],ax
reset_access:
    mov word ptr DGROUP:cursor_vram_segment,0
end_done:
    pop di
    pop si
    ret
__NEC_END_VRAM_ACCESS endp

public __NEC_OUTPUT_CHAR
__NEC_OUTPUT_CHAR proc near
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr DGROUP:cursor_vram_offset
    mov dx,word ptr __video+4
    mov ax,[bp+4]
    or ah,ah
    jz short one_cell
    cmp al,80h
    adc al,61h
    jc short converted_lead
    sub al,0a2h
converted_lead:
    rcl ah,1
    and ah,7fh
    add ax,0ff21h
    xchg al,ah
    cmp al,9
    jb short first_cell
    cmp al,12
    jb short one_cell
first_cell:
    mov word ptr es:[bx],ax
    mov word ptr es:[bx+2000h],dx
    inc word ptr ___col
    inc bx
    inc bx
    or ax,8080h
one_cell:
    mov word ptr es:[bx],ax
    mov word ptr es:[bx+2000h],dx
    inc word ptr ___col
    inc bx
    inc bx
    mov word ptr DGROUP:cursor_vram_offset,bx
    pop di
    pop si
    pop bp
    ret 2
__NEC_OUTPUT_CHAR endp
_TEXT ends
end
