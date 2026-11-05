; Original Borland istream() default constructor. Construct ios base
; when not already supplied, install both typed vtable pointers and
; maintain original global destructor count/adjusting destructor thunk.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far
extrn @istream@$bdtr$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @istream@$bctr$qv
@istream@$bctr$qv proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short object_exists
    mov ax,46
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
    add ax,6
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],ax
    mov ax,[bp+6]
    add ax,6
    push word ptr [bp+8]
    push ax
    call @ios@$bctr$qv
    pop cx
    pop cx
base_initialized:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:istream_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:istream_adjusted_thunk_marker
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+4],0
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
@istream@$bctr$qv endp

assume cs:nothing
istream_adjusted_destructor:
    mov bx,sp
    add word ptr ss:[bx+4],-6
    jmp far ptr @istream@$bdtr$qv

; The original full C++ class RTTI descriptors, not anonymous padding.
rtti_istream:
    dw 46,3,38,2,127,46,50
    dw 0,0,0,0,0,0
    dw 2,1
    dd @istream@$bdtr$qv
    dw 5,62
    db 'istream',0
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
    dd rtti_istream
    dd 0
istream_vtable_marker label word
    dd @istream@$bdtr$qv
    dw 6,8
istream_adjusted_thunk_marker label word
    dd istream_adjusted_destructor
_DATA ends
end
