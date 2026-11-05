; Original Borland istream_withassign destructor and full typed C++ RTTI.
; Actual 16-bit reference count, istream/ios base destruction and optional
; far deletion plus original local destructor-adjustment thunk and DATA table.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
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
public @istream_withassign@$bdtr$qv
@istream_withassign@$bdtr$qv proc far
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
    jz short destruction_done
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:istream_withassign_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:istream_adjusted_thunk_ptr
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @istream@$bdtr$qv
    add sp,6
    test byte ptr [bp+10],2
    jz short maybe_delete_object
    xor ax,ax
    push ax
    mov ax,[bp+6]
    add ax,6
    push word ptr [bp+8]
    push ax
    call @ios@$bdtr$qv
    add sp,6
maybe_delete_object:
    test byte ptr [bp+10],1
    jz short destruction_done
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
destruction_done:
    pop di
    pop si
    pop bp
    retf
@istream_withassign@$bdtr$qv endp

; CODE+115: real 12-byte this-adjusting destructor thunk for ios base.
assume cs:nothing
istream_destructor_thunk:
    mov bx,sp
    add word ptr ss:[bx+4],-6
    jmp far ptr @istream_withassign@$bdtr$qv

; Original typed C++ RTTI and genuine intra-segment inheritance pointers.
rtti_istream_withassign:
    dw 46,3,38,2,127,58,70
    dw 0,0,0,0,0,0
    dw 3,2
    dd @istream_withassign@$bdtr$qv
    dw 5,82
    db 'istream_withassign',0,0
    dd rtti_istream
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
_TEXTA ends

_DATA segment word public 'DATA'
    dd rtti_istream_withassign
    dd 0
istream_withassign_vtable_marker label word
    dd @istream_withassign@$bdtr$qv
    dw 6,8
istream_adjusted_thunk_ptr label word
    dd istream_destructor_thunk
_DATA ends
end
