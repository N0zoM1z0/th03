; Original Borland ostream_withassign default constructor, full RTTI/vtable.
; Actual 16-bit C++ base construction, reference tracking, adjustment thunk,
; typed RTTI and DATA vtable pointers. All references are symbolic relocations.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far
extrn @ostream@$bdtr$qv:far
extrn @ostream@$bctr$qv:far
extrn @ostream_withassign@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream_withassign@$bctr$qv
@ostream_withassign@$bctr$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short allocated
    mov ax,44
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short retain_count
allocated:
    cmp word ptr [bp+10],0
    jnz short construct_ostream
    mov ax,[bp+6]
    add ax,4
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],ax
    mov ax,[bp+6]
    add ax,4
    push word ptr [bp+8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
construct_ostream:
    mov ax,1
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @ostream@$bctr$qv
    add sp,6
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:ostream_withassign_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ostream_adjusted_thunk_ptr
retain_count:
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
@ostream_withassign@$bctr$qv endp

; Compiler-generated this-adjustment destructor thunk at CODE+131.
ostream_destructor_thunk:
    mov bx,sp
    add word ptr ss:[bx+4],-4
    jmp @ostream_withassign@$bdtr$qv

; Source-typed Borland C++ RTTI including actual inherited-class records.
rtti_ostream_withassign:
    dw 44,3,38,2,127,58,70
    dw 0,0,0,0,0,0
    dw 3,2
    dd @ostream_withassign@$bdtr$qv
    dw 5,82
    db 'ostream_withassign',0,0
    dd rtti_ostream
    dw 0,3,0,0
    dd rtti_ios
    dw 0,13,0,0,0,0
rtti_ios:
    dw 40,3,38,0,115,42,46
    dw 0,0,0,0,0,0
    dw 1,1
    dd @ios@$bdtr$qv
    dw 5,50
    db 'ios',0
    dw 0,0,0,0,0,0
rtti_ostream:
    dw 44,3,38,2,127,46,50
    dw 0,0,0,0,0,0
    dw 2,1
    dd @ostream@$bdtr$qv
    dw 5,62
    db 'ostream',0
    dw 0,0
    dd rtti_ios
    dw 0,7,0,0,0,0
_TEXTA ends

_DATA segment word public 'DATA'
    dd rtti_ostream_withassign
    dd 0
ostream_withassign_vtable_marker label word
    dd @ostream_withassign@$bdtr$qv
    dw 4,8
ostream_adjusted_thunk_ptr label word
    dd ostream_destructor_thunk
_DATA ends
end
