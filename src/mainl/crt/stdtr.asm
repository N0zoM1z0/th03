; Original Borland ios::~ios with true typed RTTI and global ios fmtflag
; DATA, user-count word, and real FAR virtual destructor vtable.
.8086
extrn @$bdele$qnv:far
extrn @$bdla$qnv:far
extrn @__RefDestructorCount$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ios@$bdtr$qv
@ios@$bdtr$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov ax,[bp+6]
    or ax,[bp+8]
    jz short ios_destructor_done
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:ios_vtable
    mov ax,word ptr es:[bx+22h]
    or ax,word ptr es:[bx+24h]
    jz short ios_skip_user_words
    push word ptr es:[bx+24h]
    push word ptr es:[bx+22h]
    call @$bdla$qnv
    pop cx
    pop cx
ios_skip_user_words:
    test byte ptr [bp+0ah],1
    jz short ios_destructor_done
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
ios_destructor_done:
    pop di
    pop si
    pop bp
    retf
@ios@$bdtr$qv endp

; 54-byte native Borland ios runtime type descriptor at CODE+87.
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
public @ios@basefield,@ios@adjustfield,@ios@floatfield
public @ios@nextbit,@ios@usercount
@ios@basefield   dd 70h
@ios@adjustfield dd 0eh
@ios@floatfield  dd 1800h
@ios@nextbit     dd 10h
@ios@usercount   dw 0
ios_rtti_pointer dd rtti_ios
ios_rtti_reserved dd 0
ios_vtable label word
    dd @ios@$bdtr$qv
_DATA ends
_BSS segment word public 'BSS'
public @ios@stdioflush
@ios@stdioflush dd ?
_BSS ends
end
