; Original Borland FAR string strncat; invokes native far strlen twice,
; clips source length, calls native overlap-safe far fmovmem, and NULs.
.8086
extrn __fmovmem:far
extrn __fstrlen:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __fstrncat
__fstrncat proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    push word ptr [bp+8]
    push word ptr [bp+6]
    call __fstrlen
    pop cx
    pop cx
    mov [bp-4],ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call __fstrlen
    pop cx
    pop cx
    mov [bp-2],ax
    cmp ax,[bp+0eh]
    jbe short length_clipped
    mov ax,[bp+0eh]
    mov [bp-2],ax
length_clipped:
    push word ptr [bp-2]
    mov ax,[bp+6]
    add ax,[bp-4]
    push word ptr [bp+8]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call __fmovmem
    add sp,0ah
    mov ax,[bp-4]
    add ax,[bp-2]
    les bx,dword ptr [bp+6]
    add bx,ax
    mov byte ptr es:[bx],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
__fstrncat endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
