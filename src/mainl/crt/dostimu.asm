; Original Borland 16-bit DOS packed date/time to UTC seconds.
; Includes leap-year correction, timezone offset and native DST check.
.8086
extrn __ISDST:near
extrn __daylight:word
extrn __timezone:dword
extrn __monthDay:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __DOSTIMETOU
__DOSTIMETOU proc near
    push bp
    mov bp,sp
    sub sp,0ch
    push si
    push di
    mov dx,word ptr DGROUP:__timezone+2
    mov ax,word ptr DGROUP:__timezone
    mov [bp-8],dx
    mov [bp-0ah],ax
    mov ax,word ptr DGROUP:__daylight
    mov [bp-0ch],ax
    mov cx,[bp+4]
    mov dx,[bp+6]
    mov si,cx
    mov di,dx
    mov bx,1e0h
    and bx,dx
    mov cl,5
    shr bx,cl
    and dx,1fh
    mov cx,0fe00h
    and cx,di
    shr cx,1
    xchg cl,ch
    test cl,3
    jnz short have_month
    cmp bl,2
    jbe short have_month
    inc dx
have_month:
    shl bx,1
    mov bx,word ptr __monthDay[bx-2]
    add bx,dx
    dec bx
    mov [bp-4],bx
    add cl,0ah
    mov [bp-6],cx
    mov ax,cx
    inc ax
    shr ax,1
    shr ax,1
    add bx,ax
    mov ax,16dh
    mul cx
    add bx,ax
    mov ax,0a8c0h
    mul bx
    shl ax,1
    rcl dx,1
    xchg si,ax
    mov bx,dx
    push ax
    mov cl,3
    shr ax,cl
    mov byte ptr [bp-2],ah
    mov byte ptr [bp-1],0
    dec cx
    shr al,cl
    mov cx,3ch
    xchg al,cl
    mul ah
    add ax,cx
    mov cl,3ch
    mul cx
    pop cx
    and cx,1fh
    shl cx,1
    add ax,cx
    adc dl,dh
    add ax,si
    adc dx,bx
    add ax,[bp-0ah]
    adc dx,[bp-8]
    cmp word ptr [bp-0ch],0
    jz short done_timezone
    push ax
    push dx
    push word ptr [bp-2]
    push word ptr [bp-4]
    xor ax,ax
    push ax
    push word ptr [bp-6]
    call __ISDST
    or ax,ax
    jz short no_dst
    mov ax,0e10h
    jmp short have_dst
no_dst:
    xor ax,ax
have_dst:
    mov si,ax
    pop dx
    pop ax
    sub ax,si
    sbb dx,0
done_timezone:
    pop di
    pop si
    mov sp,bp
    pop bp
    ret 4
__DOSTIMETOU endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
