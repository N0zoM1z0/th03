; Original getw(FILE FAR *): two native stdio byte reads with
; direct FILE buffer fast paths, far fgetc fallbacks, and true EOF ABI.
.8086
extrn __fgetc:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _getw
_getw proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    les bx,dword ptr [bp+6]
    dec word ptr es:[bx]
    jl short low_fallback
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
    jmp short save_low
low_fallback:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fgetc
    pop cx
    pop cx
save_low:
    mov [bp-2],ax
    cmp ax,-1
    jz short done
    les bx,dword ptr [bp+6]
    dec word ptr es:[bx]
    jl short high_fallback
    mov dx,word ptr es:[bx+0eh]
    mov si,word ptr es:[bx+0ch]
    inc word ptr es:[bx+0ch]
    mov es,dx
    mov al,byte ptr es:[si]
    mov ah,0
    jmp short save_high
high_fallback:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fgetc
    pop cx
    pop cx
save_high:
    mov [bp-4],ax
    cmp ax,-1
    jnz short combine
    mov word ptr [bp-2],-1
    jmp short done
combine:
    mov al,byte ptr [bp-4]
    mov byte ptr [bp-1],al
done:
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_getw endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
