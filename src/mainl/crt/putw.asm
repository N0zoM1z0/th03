; Original Borland putw(FILE FAR*): two independent stdio byte writes,
; retaining actual FILE fast-buffer cursors and FAR fputc fallbacks.
.8086
extrn __fputc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _putw
_putw proc far
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+8]
    inc word ptr es:[bx]
    jge short low_fallback
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov al,byte ptr [bp+6]
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
    jmp short check_low
low_fallback:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fputc
    add sp,6
check_low:
    cmp ax,-1
    jz short write_failure
    les bx,dword ptr [bp+8]
    inc word ptr es:[bx]
    jge short high_fallback
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov al,byte ptr [bp+7]
    mov es,dx
    mov byte ptr es:[si],al
    mov ah,0
    jmp short check_high
high_fallback:
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+7]
    call __fputc
    add sp,6
check_high:
    cmp ax,-1
    jz short write_failure
    mov ax,[bp+6]
    jmp short done
write_failure:
    mov ax,-1
done:
    pop di
    pop si
    pop bp
    retf
_putw endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
