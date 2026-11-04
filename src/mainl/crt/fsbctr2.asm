; Original Japanese Borland C++ filebuf fsbctr2 complete far constructor.
; Native 8086 instruction semantics, heap allocation and filebuf vtable.
; Real symbolic CODE and typed RTTI, no copied executable CODE bytes.
.8086
extrn @$bnew$qui:far,@$bnwa$qui:far,@__RefDestructorCount$qv:far
extrn @streambuf@$bctr$qv:far,@streambuf@$bdtr$qv:far,@streambuf@do_sgetn$qnci:far
extrn @streambuf@pbackfail$qi:far,@streambuf@do_sputn$qnxci:far,@streambuf@seekpos$qli:far
extrn @streambuf@setp$qnct1:far,@streambuf@setg$qnct1t1:far,@streambuf@setb$qnct1i:far
extrn @streambuf@doallocate$qv:far,@filebuf@$bdtr$qv:far,@filebuf@overflow$qi:far
extrn @filebuf@underflow$qv:far,@filebuf@sync$qv:far,@filebuf@seekoff$ql12ios@seek_diri:far
extrn @filebuf@setbuf$qnci:far
_TEXTA segment byte public 'CODE'
_TEXTA ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXTA segment byte public 'CODE'
assume cs:_TEXTA,ds:DGROUP
public @filebuf@$bctr$qi

@filebuf@$bctr$qi:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    mov ax, word ptr [bp + 6]
    or ax, word ptr [bp + 8]
    jne filebuf_code_0027
    mov ax, 36h
    push ax
    call @$bnew$qui
    pop cx
    mov word ptr [bp + 8], dx
    mov word ptr [bp + 6], ax
    or ax, dx
    jne filebuf_code_0027
    jmp near ptr filebuf_code_00cc

filebuf_code_0027:
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@$bctr$qv
    pop cx
    pop cx
    les bx, dword ptr [bp + 6]
    mov word ptr es:[bx],offset DGROUP:filebuf_virtual_methods
    mov ax, word ptr [bp + 0ah]
    mov word ptr es:[bx + 26h], ax
    mov word ptr es:[bx + 2ah], 1
    mov word ptr es:[bx + 28h], 0
    mov word ptr es:[bx + 2eh], 0
    mov word ptr es:[bx + 2ch], 0
    mov ax, 204h
    push ax
    call @$bnwa$qui
    pop cx
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or ax, word ptr [bp - 2]
    je filebuf_code_00cc
    mov ax, 1
    push ax
    mov ax, word ptr [bp - 4]
    add ax, 204h
    push dx
    push ax
    push dx
    push word ptr [bp - 4]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setb$qnct1i
    mov ax, word ptr [bp - 4]
    add ax, 4
    mov word ptr [bp - 6], ax
    push word ptr [bp - 2]
    push ax
    push word ptr [bp - 2]
    push ax
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setp$qnct1
    mov ax, word ptr [bp - 4]
    add ax, 4
    mov word ptr [bp - 8], ax
    push word ptr [bp - 2]
    push ax
    push word ptr [bp - 2]
    push ax
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    push word ptr [bp + 8]
    push word ptr [bp + 6]
    call @streambuf@setg$qnct1t1
    add sp, 2ah

filebuf_code_00cc:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx + 2], 0
    mov dx, word ptr [bp + 8]
    mov ax, word ptr [bp + 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Non-executable Borland C++ class RTTI/destructor pointer table.
filebuf_meta_00ea:
    dw 54 ; typed RTTI descriptor
    dw 3 ; typed RTTI descriptor
    dw 38 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 119 ; typed RTTI descriptor
    dw 46 ; typed RTTI descriptor
    dw 58 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 2 ; typed RTTI descriptor
    dw 2 ; typed RTTI descriptor
    dd @filebuf@$bdtr$qv ; original native far class pointer
    dw 5 ; typed RTTI descriptor
    dw 62 ; typed RTTI descriptor
    db 'filebuf',0 ; actual native C++ class name
    dd filebuf_meta_012c ; original native far class pointer
    dw 0 ; typed RTTI descriptor
    dw 3 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
filebuf_meta_012c:
    dw 38 ; typed RTTI descriptor
    dw 3 ; typed RTTI descriptor
    dw 38 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 115 ; typed RTTI descriptor
    dw 48 ; typed RTTI descriptor
    dw 52 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 1 ; typed RTTI descriptor
    dw 1 ; typed RTTI descriptor
    dd @streambuf@$bdtr$qv ; original native far class pointer
    dw 5 ; typed RTTI descriptor
    dw 56 ; typed RTTI descriptor
    db 'streambuf',0 ; actual native C++ class name
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
    dw 0 ; typed RTTI descriptor
_TEXTA ends

_DATA segment word public 'DATA'
assume cs:nothing
; Original native filebuf class virtual dispatch table.
    dd filebuf_meta_00ea ; far virtual method or destructor
    dw 0 ; original vtable preamble
    dw 0 ; original vtable preamble
filebuf_virtual_methods:
    dd @filebuf@$bdtr$qv ; far virtual method or destructor
    dd @filebuf@setbuf$qnci ; far virtual method or destructor
    dd @streambuf@do_sgetn$qnci ; far virtual method or destructor
    dd @filebuf@underflow$qv ; far virtual method or destructor
    dd @streambuf@pbackfail$qi ; far virtual method or destructor
    dd @streambuf@do_sputn$qnxci ; far virtual method or destructor
    dd @filebuf@overflow$qi ; far virtual method or destructor
    dd @filebuf@seekoff$ql12ios@seek_diri ; far virtual method or destructor
    dd @streambuf@seekpos$qli ; far virtual method or destructor
    dd @filebuf@sync$qv ; far virtual method or destructor
    dd @streambuf@doallocate$qv ; far virtual method or destructor
_DATA ends
end
