; Original Borland istream(streambuf*) large-model C++ constructor.
; Real base construction, this-adjustor destructor thunk, full typed RTTI
; and DATA-resident vtable pointers. All 16-bit OMF references symbolic.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn @ios@$bdtr$qv:far
extrn @ios@$bctr$qv:far
extrn @ios@init$qn9streambuf:far
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
public @istream@$bctr$qn9streambuf
@istream@$bctr$qn9streambuf proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz short memory_ready
    mov ax,46
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz short increment_count
memory_ready:
    cmp word ptr [bp+10],0
    jnz short base_constructed
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
base_constructed:
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+2],offset DGROUP:istream_vtable_marker
    mov bx,word ptr es:[bx]
    mov word ptr es:[bx],offset DGROUP:istream_adjusted_thunk_ptr
    push word ptr [bp+14]
    push word ptr [bp+12]
    les bx,dword ptr [bp+6]
    push es
    push word ptr es:[bx]
    call @ios@init$qn9streambuf
    add sp,8
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx+4],0
increment_count:
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
@istream@$bctr$qn9streambuf endp

; The real far thunk at CODE+143 adjusts the ios base pointer by four.
assume cs:nothing
istream_destructor_thunk:
    mov bx,sp
    add word ptr ss:[bx+4],-6
    jmp far ptr @istream@$bdtr$qv

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
istream_adjusted_thunk_ptr label word
    dd istream_destructor_thunk
_DATA ends
end
