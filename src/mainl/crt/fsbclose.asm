; Complete original Borland filebuf::close(). Flush through virtual
; overflow(-1), close the real DOS handle, clear the filebuf state and
; return this only if both operations succeeded.
.8086
extrn _close:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@close$qv
@filebuf@close$qv proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+26h],-1
    jnz short check_open_state
    mov word ptr es:[bx+2ah],0
check_open_state:
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2ah],0
    jnz short close_live_file
    xor dx,dx
    xor ax,ax
    jmp near ptr done
close_live_file:
    mov word ptr [bp-2],0
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+12h]
    or ax,word ptr es:[bx+14h]
    jz short no_output_pending
    mov ax,word ptr es:[bx+12h]
    xor dx,dx
    sub ax,word ptr es:[bx+0eh]
    sbb dx,0
    jmp short have_pending
no_output_pending:
    xor ax,ax
have_pending:
    or ax,ax
    jz short close_dos_handle
    mov ax,-1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+18h]
    add sp,6
    cmp ax,-1
    jnz short flush_succeeded
    mov ax,1
    jmp short record_flush_status
flush_succeeded:
    xor ax,ax
record_flush_status:
    mov [bp-2],ax
close_dos_handle:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+26h]
    call _close
    pop cx
    mov [bp-4],ax
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+26h],-1
    mov word ptr es:[bx+2ah],0
    mov ax,[bp-2]
    or ax,[bp-4]
    jz short return_this
    xor dx,dx
    xor ax,ax
    jmp short done
return_this:
    mov dx,[bp+8]
    mov ax,[bp+6]
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@filebuf@close$qv endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
