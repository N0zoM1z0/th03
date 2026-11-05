; Complete original strstreambuf::underflow. This is not a wrapper: the
; far get/put regions, streambuf::setg adjustment and EOF paths are real.
.8086
extrn @streambuf@setg$qnct1t1:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @strstreambuf@underflow$qv
@strstreambuf@underflow$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+22h]
    cmp ax,word ptr es:[bx+1eh]
    jna short check_base
    jmp near ptr return_character
check_base:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+6]
    or ax,word ptr es:[bx+8]
    jnz short check_allocation
    jmp near ptr return_eof
check_allocation:
    cmp word ptr es:[bx+4],0
    jz short check_put_area
    jmp near ptr return_eof
check_put_area:
    mov ax,word ptr es:[bx+12h]
    cmp ax,word ptr es:[bx+0eh]
    jna short return_eof
    mov ax,word ptr es:[bx+1eh]
    or ax,word ptr es:[bx+20h]
    jz short restore_beginning
    mov ax,word ptr es:[bx+1eh]
    cmp ax,word ptr es:[bx+0eh]
    jnc short advance_get_area
restore_beginning:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+14h]
    push word ptr es:[bx+12h]
    push word ptr es:[bx+10h]
    push word ptr es:[bx+0eh]
    push word ptr es:[bx+8]
    push word ptr es:[bx+6]
    push word ptr [bp+8]
    push bx
    call @streambuf@setg$qnct1t1
    add sp,16
    jmp short return_character
advance_get_area:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+1eh]
    cmp ax,word ptr es:[bx+12h]
    jnc short return_eof
    push word ptr es:[bx+14h]
    push word ptr es:[bx+12h]
    push word ptr es:[bx+20h]
    push word ptr es:[bx+1eh]
    push word ptr es:[bx+1ch]
    push word ptr es:[bx+1ah]
    push word ptr [bp+8]
    push bx
    call @streambuf@setg$qnct1t1
    add sp,16
return_character:
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx+1eh]
    mov al,byte ptr es:[bx]
    mov ah,0
    jmp short return_value
return_eof:
    mov ax,0ffffh
return_value:
    pop di
    pop si
    pop bp
    retf
@strstreambuf@underflow$qv endp
_TEXTA ends
end
