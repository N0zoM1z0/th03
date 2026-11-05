; Original strstreambuf::doallocate() virtual implementation. Uses the
; original far callback if installed, otherwise new[], registers an owned
; buffer and NUL-terminates it. Return values and unchecked allocation are
; exactly those from the 16-bit Borland ABI.
.8086
extrn @$bnwa$qui:far
extrn @streambuf@setb$qnct1i:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@doallocate$qv
@strstreambuf@doallocate$qv proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+30h],0
    jz short use_default_size
    mov ax,word ptr es:[bx+30h]
    jmp short selected_size
use_default_size:
    mov ax,16
selected_size:
    mov [bp-2],ax
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+26h]
    or ax,word ptr es:[bx+28h]
    jz short use_array_new
    mov ax,[bp-2]
    cwd
    push dx
    push ax
    call dword ptr es:[bx+26h]
    pop cx
    pop cx
    jmp short allocated
use_array_new:
    push word ptr [bp-2]
    call @$bnwa$qui
    pop cx
allocated:
    mov [bp-4],dx
    mov [bp-6],ax
    mov ax,[bp-6]
    or ax,[bp-4]
    jnz short install_buffer
    mov ax,-1
    jmp short done
install_buffer:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+30h],0
    xor ax,ax
    push ax
    mov ax,[bp-6]
    add ax,[bp-2]
    push word ptr [bp-4]
    push ax
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+8]
    push bx
    call @streambuf@setb$qnct1i
    add sp,0eh
    les bx,dword ptr [bp-6]
    mov byte ptr es:[bx],0
    mov ax,1
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@strstreambuf@doallocate$qv endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
