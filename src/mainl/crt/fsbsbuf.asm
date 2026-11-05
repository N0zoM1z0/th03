; Original filebuf::setbuf(char far *buffer, int length).
; Rejects replacing a live attached buffer, derives the get/put offset,
; then uses the true streambuf setb/setp/setg interfaces.
.8086
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
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
public @filebuf@setbuf$qnci
@filebuf@setbuf$qnci proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov dx,[bp+14]
    les bx,dword ptr [bp+6]
    cmp word ptr es:[bx+2ah],0
    jz short check_input
    mov ax,word ptr es:[bx+6]
    or ax,word ptr es:[bx+8]
    jz short check_input
    xor dx,dx
    xor ax,ax
    jmp near ptr done
check_input:
    mov ax,[bp+10]
    or ax,[bp+12]
    jz short no_buffer
    or dx,dx
    jle short no_buffer
    cmp dx,8
    jle short small_buffer
    mov ax,4
    jmp short selected_offset
small_buffer:
    mov ax,1
selected_offset:
    mov [bp-2],ax
    jmp short install_ranges
no_buffer:
    xor ax,ax
    mov [bp-2],ax
    mov dx,ax
    mov word ptr [bp+12],0
    mov word ptr [bp+10],0
install_ranges:
    xor ax,ax
    push ax
    mov ax,[bp+10]
    add ax,dx
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setb$qnct1i
    mov ax,[bp+10]
    add ax,[bp-2]
    mov [bp-4],ax
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setp$qnct1
    mov ax,[bp+10]
    add ax,[bp-2]
    mov [bp-6],ax
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,2ah
    mov dx,[bp+8]
    mov ax,[bp+6]
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@filebuf@setbuf$qnci endp
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
end
