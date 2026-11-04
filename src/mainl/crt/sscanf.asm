; Original Borland scan-string callback and far scanf/vsscanf wrappers.
.8086
extrn __scanner:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
scan_char_get:
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+4]
    mov dx,word ptr es:[bx+2]
    mov si,word ptr es:[bx]
    inc word ptr es:[bx]
    mov es,dx
    mov dl,byte ptr es:[si]
    mov al,dl
    or al,al
    jne got_char
    mov ax,-1
    jmp short done_get
got_char:
    mov al,dl
    mov ah,0
done_get:
    pop di
    pop si
    pop bp
    ret
scan_char_unget:
    push bp
    mov bp,sp
    push si
    push di
    les bx,dword ptr [bp+6]
    dec word ptr es:[bx]
    pop di
    pop si
    pop bp
    ret
public _sscanf,_vsscanf
_sscanf proc far
    push bp
    mov bp,sp
    push si
    push di
    push ss
    lea ax,[bp+14]
    push ax
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp+6]
    push ax
    mov ax,offset scan_char_unget
    push ax
    mov ax,offset scan_char_get
    push ax
    call __scanner
    add sp,16
    pop di
    pop si
    pop bp
    retf
_sscanf endp
_vsscanf proc far
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+16]
    push word ptr [bp+14]
    push word ptr [bp+12]
    push word ptr [bp+10]
    push ss
    lea ax,[bp+6]
    push ax
    mov ax,offset scan_char_unget
    push ax
    mov ax,offset scan_char_get
    push ax
    call __scanner
    add sp,16
    pop di
    pop si
    pop bp
    retf
_vsscanf endp
_TEXT ends
end
