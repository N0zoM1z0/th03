; Far cdecl DOS resize(segment, paragraphs). Return FFFF on success, otherwise
; DOS's maximum available paragraph count. Error reporting must preserve BX;
; a failure reporting BX=FFFF therefore collides with the success sentinel.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
extrn __IOERROR:near
public _setblock
_setblock proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ah,4Ah
    mov bx,[bp+8]
    mov es,[bp+6]
    int 21h
    jc resize_failed
    mov ax,-1
    jmp short resize_done
resize_failed:
    push bx
    push ax
    call __IOERROR
    pop ax
resize_done:
    pop di
    pop si
    pop bp
    retf
_setblock endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
end
