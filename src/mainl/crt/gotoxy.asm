; Complete original Borland Japanese CRT gotoxy ABI and control flow.
.8086
extrn __video:byte
extrn __GOTOXY:far
extrn ___get_windowy2:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _gotoxy
_gotoxy proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    mov al,byte ptr DGROUP:__video
    mov ah,0
    add ax,[bp+6]
    dec ax
    mov [bp-2],ax
    mov al,byte ptr DGROUP:__video+1
    mov ah,0
    mov [bp-6],ax
    add ax,[bp+8]
    dec ax
    mov [bp-4],ax
    mov ax,[bp-6]
    cmp ax,[bp-4]
    jg short done
    call ___get_windowy2
    cmp ax,[bp-4]
    jl short done
    mov al,byte ptr DGROUP:__video
    mov ah,0
    cmp ax,[bp-2]
    jg short done
    mov al,byte ptr DGROUP:__video+2
    mov ah,0
    cmp ax,[bp-2]
    jl short done
    push word ptr [bp-2]
    push word ptr [bp-4]
    call __GOTOXY
done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
_gotoxy endp
_TEXT ends
end
