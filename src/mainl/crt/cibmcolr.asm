; Original IBM conio text color and attributes, six FAR public entrypoints.
; Use the real Borland __video text-mode state rather than hardware stubs.
.8086
extrn __video:byte
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public ___ibm_textcolor,___ibm_textbackground,___ibm_textattr
public ___ibm_highvideo,___ibm_lowvideo,___ibm_normvideo
___ibm_textcolor proc far
    push bp
    mov bp,sp
    push si
    push di
    cmp byte ptr DGROUP:__video+0dh,0
    je short standard_color
    mov ax,0f0h
    jmp short have_color_mask
standard_color:
    mov ax,70h
have_color_mask:
    mov bx,ax
    mov ax,word ptr DGROUP:__video+4
    and ax,bx
    mov dx,bx
    not dx
    and dx,[bp+6]
    or ax,dx
    mov word ptr DGROUP:__video+4,ax
    pop di
    pop si
    pop bp
    retf
___ibm_textcolor endp

___ibm_textbackground proc far
    push bp
    mov bp,sp
    sub sp,4
    push si
    push di
    cmp byte ptr DGROUP:__video+0dh,0
    je short background_normal
    mov al,0fh
    jmp short background_mask_ready
background_normal:
    mov al,8fh
background_mask_ready:
    mov byte ptr [bp-1],al
    mov ax,[bp+6]
    mov cl,4
    shl ax,cl
    mov dl,byte ptr [bp-1]
    mov dh,0
    mov [bp-4],dx
    not dx
    and ax,dx
    mov dx,[bp-4]
    and dx,word ptr DGROUP:__video+4
    or ax,dx
    mov word ptr DGROUP:__video+4,ax
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___ibm_textbackground endp

___ibm_textattr proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+6]
    test dh,1
    je short store_attr
    or dx,80h
store_attr:
    mov word ptr DGROUP:__video+4,dx
    pop di
    pop si
    pop bp
    retf
___ibm_textattr endp

___ibm_highvideo proc far
    push si
    push di
    or word ptr DGROUP:__video+4,8
    pop di
    pop si
    retf
___ibm_highvideo endp

___ibm_lowvideo proc far
    push si
    push di
    and word ptr DGROUP:__video+4,0fff7h
    pop di
    pop si
    retf
___ibm_lowvideo endp

___ibm_normvideo proc far
    push si
    push di
    mov ax,word ptr DGROUP:__video+6
    mov word ptr DGROUP:__video+4,ax
    pop di
    pop si
    retf
___ibm_normvideo endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
