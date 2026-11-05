; Original Japanese Borland large-model DOS path compositor (__makepath).
; Maintains far string/drive/extension pointers and the Japanese SBCS
; predicate when recognizing a trailing directory slash.
.8086
extrn _strlen:far,__stpcpy:far,___path_issbcs:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __makepath
__makepath proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+10]
    or ax,[bp+12]
    jz short drive_done
    les bx,dword ptr [bp+10]
    cmp byte ptr es:[bx],0
    jz short drive_done
    mov al,byte ptr es:[bx]
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],al
    inc word ptr [bp+6]
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],':'
    inc word ptr [bp+6]
drive_done:
    mov ax,[bp+14]
    or ax,[bp+16]
    jz short directory_done
    les bx,dword ptr [bp+14]
    cmp byte ptr es:[bx],0
    jz short directory_done
    push word ptr [bp+16]
    push bx
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __stpcpy
    add sp,8
    mov [bp+8],dx
    mov [bp+6],ax
    les bx,dword ptr [bp+6]
    cmp byte ptr es:[bx-1],5ch
    jz short check_last_dir_char
    cmp byte ptr es:[bx-1],2fh
    jnz short add_backslash
check_last_dir_char:
    push word ptr [bp+16]
    push word ptr [bp+14]
    call _strlen
    pop cx
    pop cx
    add ax,[bp+14]
    dec ax
    push word ptr [bp+16]
    push ax
    push word ptr [bp+16]
    push word ptr [bp+14]
    call ___path_issbcs
    add sp,8
    or ax,ax
    jnz short directory_done
add_backslash:
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],5ch
    inc word ptr [bp+6]
directory_done:
    mov ax,[bp+18]
    or ax,[bp+20]
    jz short base_done
    push word ptr [bp+20]
    push word ptr [bp+18]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __stpcpy
    add sp,8
    mov [bp+8],dx
    mov [bp+6],ax
base_done:
    mov ax,[bp+22]
    or ax,[bp+24]
    jz short extension_done
    les bx,dword ptr [bp+22]
    cmp byte ptr es:[bx],0
    jz short extension_done
    cmp byte ptr es:[bx],'.'
    jz short append_extension
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],'.'
    inc word ptr [bp+6]
append_extension:
    push word ptr [bp+24]
    push word ptr [bp+22]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __stpcpy
    add sp,8
    mov [bp+8],dx
    mov [bp+6],ax
extension_done:
    les bx,dword ptr [bp+6]
    mov byte ptr es:[bx],0
    pop di
    pop si
    pop bp
    retf
__makepath endp
_TEXT ends
end
