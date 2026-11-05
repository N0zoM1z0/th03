; Original ios(streambuf far*) constructor with complete typed Borland
; ios RTTI, a real DATA-backed vtable and exact 40-byte object ABI.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@init$qn9streambuf:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@$bctr$qn9streambuf
@ios@$bctr$qn9streambuf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short initialize_ios_object
    mov ax,28h
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short update_constructor_reference
initialize_ios_object:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:ios_vtable
    mov word ptr es:[bx+24h],0
    mov word ptr es:[bx+22h],0
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push bx
    call @ios@init$qn9streambuf
    add sp,8
update_constructor_reference:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
@ios@$bctr$qn9streambuf endp

; The actual 54-byte Borland C++ type descriptor for ios, CODE+99.
rtti_ios:
    dw 40,3,38,0,115,42,46
    dw 0,0,0,0,0,0
    dw 1,1
    dd @ios@$bdtr$qv
    dw 5,50
    db 'ios',0
    dw 0,0,0,0,0,0
_TEXTA ends
_DATA segment word public 'DATA'
    dd rtti_ios
    dd 0
ios_vtable label word
    dd @ios@$bdtr$qv
_DATA ends
end
