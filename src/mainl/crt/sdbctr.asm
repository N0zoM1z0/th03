; Borland stdiobuf(FILE*) complete far constructor, RTTI and virtual table.
; Natural 8086 instructions, symbolic far callbacks and typed C++ descriptors.
.8086
extrn @$bnew$qui:far,@$bnwa$qui:far,@__RefDestructorCount$qv:far
extrn @streambuf@$bctr$qv:far,@streambuf@$bdtr$qv:far
extrn @streambuf@setbuf$qnci:far,@streambuf@do_sgetn$qnci:far
extrn @streambuf@do_sputn$qnxci:far,@streambuf@seekpos$qli:far
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far
extrn @streambuf@setb$qnct1i:far,@streambuf@doallocate$qv:far
extrn @stdiobuf@$bdtr$qv:far,@stdiobuf@overflow$qi:far
extrn @stdiobuf@pbackfail$qi:far,@stdiobuf@sync$qv:far
extrn @stdiobuf@seekoff$ql12ios@seek_diri:far
extrn @stdiobuf@underflow$qv:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA

_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @stdiobuf@$bctr$qn4FILE

@stdiobuf@$bctr$qn4FILE:
    push bp
    mov bp,sp
    sub sp,8
    push si
    push di
    mov ax,word ptr [bp+6]
    or ax,word ptr [bp+8]
    jne have_this
    mov ax,2ch
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp+8],dx
    mov word ptr [bp+6],ax
    or ax,dx
    jne have_this
    jmp near ptr count_and_return

have_this:
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@$bctr$qv
    pop cx
    pop cx

    ; Replace the streambuf virtual methods and attach caller's FILE*.
    les bx,dword ptr [bp+6]
    mov word ptr es:[bx],offset DGROUP:stdiobuf_virtual_methods
    mov dx,word ptr [bp+0ch]
    mov ax,word ptr [bp+0ah]
    mov word ptr es:[bx+28h],dx
    mov word ptr es:[bx+26h],ax

    ; 516-byte put/get area, with a four-byte front reserve.
    mov ax,204h
    push ax
    call @$bnwa$qui
    pop cx
    mov word ptr [bp-2],dx
    mov word ptr [bp-4],ax
    or ax,word ptr [bp-2]
    je count_and_return
    mov ax,1
    push ax
    mov ax,word ptr [bp-4]
    add ax,204h
    push dx
    push ax
    push dx
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setb$qnct1i
    mov ax,word ptr [bp-4]
    add ax,4
    mov word ptr [bp-6],ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setp$qnct1
    mov ax,word ptr [bp-4]
    add ax,4
    mov word ptr [bp-8],ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push ax
    push word ptr [bp-2]
    push word ptr [bp-4]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @streambuf@setg$qnct1t1
    add sp,2ah

count_and_return:
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Non-executable typed Borland C++ RTTI for stdiobuf and base streambuf.
stdiobuf_class_rtti:
    dw 44,3,38,0,119,48,60
    dw 0,0,0,0,0,0,2,2
    dd @stdiobuf@$bdtr$qv
    dw 5,64
    db 'stdiobuf',0
    db 0 ; Borland RTTI field alignment within the class descriptor
    dd streambuf_class_rtti
    dw 0,3,0,0,0,0,0,0
streambuf_class_rtti:
    dw 38,3,38,0,115,48,52
    dw 0,0,0,0,0,0,1,1
    dd @streambuf@$bdtr$qv
    dw 5,56
    db 'streambuf',0
    dw 0,0,0,0,0,0
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; C++ virtual table: one far class descriptor plus eleven methods.
    dd stdiobuf_class_rtti
    dw 0,0
stdiobuf_virtual_methods:
    dd @stdiobuf@$bdtr$qv
    dd @streambuf@setbuf$qnci
    dd @streambuf@do_sgetn$qnci
    dd @stdiobuf@underflow$qv
    dd @stdiobuf@pbackfail$qi
    dd @streambuf@do_sputn$qnxci
    dd @stdiobuf@overflow$qi
    dd @stdiobuf@seekoff$ql12ios@seek_diri
    dd @streambuf@seekpos$qli
    dd @stdiobuf@sync$qv
    dd @streambuf@doallocate$qv
_DATA ends
end
