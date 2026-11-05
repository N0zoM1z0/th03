; Complete original Borland strstreambuf::init(char*,int,char*).
; Maintains far buffer extents, growth mode flags, setb/setp/setg and
; the original unchecked 16-bit near/far pointer arithmetic.
.8086
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
extrn @streambuf@setb$qnct1i:far
extrn _strlen:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@init$qncit1
@strstreambuf@init$qncit1 proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2eh],0
    cmp word ptr [bp+14],0
    jnz short check_growth_mode
    push word ptr [bp+12]
    push word ptr [bp+10]
    call _strlen
    pop cx
    pop cx
    mov [bp+14],ax
    jmp short configure_extent
check_growth_mode:
    cmp word ptr [bp+14],0
    jnl short configure_extent
    mov word ptr [bp+14],7fffh
    les bx,dword ptr [bp+6]
    or word ptr es:[bx+2eh],4
configure_extent:
    xor ax,ax
    push ax
    mov ax,[bp+10]
    add ax,[bp+14]
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setb$qnct1i
    add sp,14
    mov ax,[bp+16]
    or ax,[bp+18]
    jz short no_output_ptr
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+0ch]
    push word ptr es:[bx+0ah]
    push word ptr [bp+18]
    push word ptr [bp+16]
    push word ptr [bp+8]
    push bx
    call @streambuf@setp$qnct1
    add sp,12
    mov ax,[bp+10]
    add ax,[bp+14]
    cmp ax,[bp+16]
    jnc short use_output_extent
    mov dx,[bp+12]
    mov ax,[bp+10]
    add ax,[bp+14]
    jmp short choose_get_end
use_output_extent:
    mov dx,[bp+18]
    mov ax,[bp+16]
choose_get_end:
    push dx
    push ax
    jmp short configure_get_area
no_output_ptr:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+0ch]
    push word ptr es:[bx+0ah]
configure_get_area:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,16
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+28h],0
    mov word ptr es:[bx+26h],0
    mov word ptr es:[bx+2ch],0
    mov word ptr es:[bx+2ah],0
    pop di
    pop si
    pop bp
    retf
@strstreambuf@init$qncit1 endp
_TEXTA ends
end
