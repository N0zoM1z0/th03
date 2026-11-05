; Original Japanese Borland stdiobuf::seekoff C++ stream boss.
; Preserve 16-bit far object layout, get/put buffer cursors, direct vtable
; sync, fseek/ftell and both streambuf setp/setg calling conventions.
.8086
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far
extrn _fseek:far,_ftell:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@seekoff$ql12ios@seek_diri
@stdiobuf@seekoff$ql12ios@seek_diri proc far
    push bp
    mov bp,sp
    sub sp,10
    push si
    push di
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+12h]
    or ax,word ptr es:[bx+14h]
    jz short no_output_pending
    mov ax,word ptr es:[bx+12h]
    xor dx,dx
    sub ax,word ptr es:[bx+0eh]
    sbb dx,0
    jmp short compare_output
no_output_pending:
    xor ax,ax
compare_output:
    or ax,ax
    jnz short sync_before_seek
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+22h]
    cmp ax,word ptr es:[bx+1eh]
    jna short no_get_pending
    xor dx,dx
    sub ax,word ptr es:[bx+1eh]
    sbb dx,0
    jmp short compare_get
no_get_pending:
    xor ax,ax
compare_get:
    or ax,ax
    jz short seek_with_offset
sync_before_seek:
    push word ptr [bp+8]
    push word ptr [bp+6]
    les bx,dword ptr [bp+6]
    mov bx,word ptr es:[bx]
    call dword ptr [bx+24h]
    pop cx
    pop cx
    cmp ax,0ffffh
    jnz short seek_with_offset
    mov dx,0ffffh
    mov ax,0ffffh
    jmp near ptr seek_return
seek_with_offset:
    cmp word ptr [bp+14],0
    jnz short origin_test_end
    mov word ptr [bp-2],0
    jmp short origin_ready
origin_test_end:
    cmp word ptr [bp+14],2
    jnz short origin_current
    mov word ptr [bp-2],2
    jmp short origin_ready
origin_current:
    mov word ptr [bp-2],1
origin_ready:
    push word ptr [bp-2]
    push word ptr [bp+12]
    push word ptr [bp+10]
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+28h]
    push word ptr es:[bx+26h]
    call _fseek
    add sp,10
    mov [bp-2],ax
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    mov [bp-4],dx
    mov [bp-6],ax
    cmp word ptr es:[bx+4],0
    jnz short test_seek_result
    or ax,[bp-4]
    jz short test_seek_result
    mov ax,[bp-6]
    add ax,4
    mov [bp-8],ax
    push dx
    push ax
    push dx
    push ax
    push word ptr [bp+8]
    push bx
    call @streambuf@setp$qnct1
    mov ax,[bp-6]
    add ax,4
    mov [bp-10],ax
    push word ptr [bp-4]
    push ax
    push word ptr [bp-4]
    push ax
    push word ptr [bp-4]
    push word ptr [bp-6]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,28
test_seek_result:
    cmp word ptr [bp-2],0
    jz short actual_file_offset
    mov dx,0ffffh
    mov ax,0ffffh
    jmp short seek_return
actual_file_offset:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+28h]
    push word ptr es:[bx+26h]
    call _ftell
    pop cx
    pop cx
seek_return:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@stdiobuf@seekoff$ql12ios@seek_diri endp
_TEXTA ends
end
