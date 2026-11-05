; stdiobuf::overflow(int) -- Borland C++ far member function.
; Preserve the original streambuf put-area rollover, EOF path, write failure
; handling, and the two far setp/setg callbacks without changing the ABI.
.8086
extrn @streambuf@setp$qnct1:far
extrn @streambuf@setg$qnct1t1:far
extrn __fputc:far

_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA

_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@overflow$qi

@stdiobuf@overflow$qi:
    push bp
    mov bp,sp
    sub sp,0ch
    push si
    push di

    ; Error bit in the FILE owned by this stdiobuf.
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx+26h]
    test byte ptr es:[bx+2],10h
    je check_buffer
    mov ax,0ffffh
    jmp failed_or_done

check_buffer:
    les bx,dword ptr [bp+6]
    mov ax,word ptr es:[bx+12h]
    or ax,word ptr es:[bx+14h]
    je no_pending
    mov ax,word ptr es:[bx+12h]
    xor dx,dx
    sub ax,word ptr es:[bx+0eh]
    sbb dx,0
    jmp short got_pending
no_pending:
    xor ax,ax
got_pending:
    mov word ptr [bp-6],ax
    cmp word ptr [bp-6],0
    jle maybe_new_char

    ; Flush each pending character through the stdio output buffer.
flush_loop:
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+10h]
    mov ax,word ptr es:[bx+0eh]
    mov word ptr [bp-2],dx
    mov word ptr [bp-4],ax
try_flush:
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx+26h]
    inc word ptr es:[bx]
    jge flush_fputc
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    les bx,dword ptr [bp-4]
    mov al,byte ptr es:[bx]
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
    jmp short flush_continue
flush_fputc:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+28h]
    push word ptr es:[bx+26h]
    les bx,dword ptr [bp-4]
    mov al,byte ptr es:[bx]
    push ax
    call __fputc
    add sp,6
flush_continue:
    inc word ptr [bp-4]
    dec word ptr [bp-6]
    jne try_flush

maybe_new_char:
    cmp word ptr [bp+0ah],-1
    je reset_stream
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx+26h]
    inc word ptr es:[bx]
    jge new_fputc
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov al,byte ptr [bp+0ah]
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
    jmp short reset_stream
new_fputc:
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+28h]
    push word ptr es:[bx+26h]
    push word ptr [bp+0ah]
    call __fputc
    add sp,6

reset_stream:
    ; Reinstall the streambuf get and put bounds relative to its base.
    les bx,dword ptr [bp+6]
    mov dx,word ptr es:[bx+8]
    mov ax,word ptr es:[bx+6]
    mov word ptr [bp-8],dx
    mov word ptr [bp-0ah],ax
    mov ax,word ptr es:[bx+0ah]
    xor dx,dx
    sub ax,word ptr es:[bx+6]
    sbb dx,0
    add ax,word ptr [bp-0ah]
    push word ptr [bp-8]
    push ax
    mov ax,word ptr [bp-0ah]
    add ax,4
    push word ptr [bp-8]
    push ax
    push word ptr [bp+8]
    push bx
    call @streambuf@setp$qnct1
    mov ax,word ptr [bp-0ah]
    add ax,4
    mov word ptr [bp-0ch],ax
    push word ptr [bp-8]
    push ax
    push word ptr [bp-8]
    push ax
    push word ptr [bp-8]
    push word ptr [bp-0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,1ch

    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx+26h]
    test byte ptr es:[bx+2],10h
    je succeeded
    mov ax,0ffffh
    jmp short failed_or_done
succeeded:
    mov ax,1
failed_or_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_TEXTA ends
end
