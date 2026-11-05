; Original Borland ostream() default constructor. Construct ios base
; when not already supplied, install both typed vtable pointers and
; maintain original global destructor count/adjusting destructor thunk.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far
extrn @ostream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @ostream@$bctr$qv
@ostream@$bctr$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short object_exists
    mov ax,44
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short update_count
object_exists:
    cmp word ptr [bp+10],0
    jnz short base_initialized
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
base_initialized:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:ostream_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:ostream_adjusted_thunk_marker
update_count:
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
@ostream@$bctr$qv endp

assume cs:nothing
ostream_adjusted_destructor:
    mov bx,sp
    add word ptr ss:[bx+4],-4
    jmp far ptr @ostream@$bdtr$qv

; The original full C++ class RTTI descriptors, not anonymous padding.
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
    dd rtti_ostream
    dd 0
ostream_vtable_marker label word
    dd @ostream@$bdtr$qv
    dw 4,8
ostream_adjusted_thunk_marker label word
    dd ostream_adjusted_destructor
_DATA ends
end
