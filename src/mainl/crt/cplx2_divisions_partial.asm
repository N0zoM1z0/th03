; PARTIAL LARGE-BOSS SOURCE: three complete FAR complex division
; implementations at original CODE offsets 0, 166, and 405.
; These 692 bytes are NOT the whole 5598-byte cplx2. Not source-linked.
; Rebuild/compare via scripts/probe_th03_cplx2_divisions_partial.py.
.8086
.8087
EMUL
extrn @norm$qm7complex:far
extrn @complex@$brmul$qm7complex:far
extrn @$bmul$qm7complext1:far
extrn @$bnew$qui:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @complex@$brdiv$qm7complex
@complex@$brdiv$qm7complex proc far
    push bp
    mov bp,sp
    sub sp,30h
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    call @norm$qm7complex
    fstp tbyte ptr [bp-0ah]
    push ss
    fwait
    mov dx,[bp+0ch]
    mov ax,[bp+0ah]
    mov [bp-0ch],dx
    mov [bp-0eh],ax
    les bx,dword ptr [bp-0eh]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-16h]
    fwait
    les bx,dword ptr [bp-0eh]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1eh]
    fld qword ptr [bp-1eh]
    fstp qword ptr [bp-30h]
    fld qword ptr [bp-16h]
    fstp qword ptr [bp-28h]
    fwait
    lea ax,[bp-30h]
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @complex@$brmul$qm7complex
    add sp,0ch
    les bx,dword ptr [bp+6]
    fld qword ptr es:[bx]
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    les bx,dword ptr [bp+6]
    fstp qword ptr es:[bx]
    add bx,8
    fwait
    mov [bp-20h],bx
    fld qword ptr es:[bx]
    fld tbyte ptr [bp-0ah]
    fdivp st(1),st(0)
    mov es,[bp+8]
    mov bx,[bp-20h]
    fstp qword ptr es:[bx]
    fwait
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@complex@$brdiv$qm7complex endp


; Second complete FAR division operator; returns a constructed complex
; through the hidden return-object pointer (or original far new[] path).
public @$bdiv$qm7complext1
@$bdiv$qm7complext1 proc far
    push bp
    mov bp,sp
    sub sp,58h
    push si
    push di
    push word ptr [bp+10h]
    push word ptr [bp+0eh]
    call @norm$qm7complex
    fstp qword ptr [bp-8]
    push ss
    fwait
    mov dx,[bp+10h]
    mov ax,[bp+0eh]
    mov [bp-0ah],dx
    mov [bp-0ch],ax
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-14h]
    fwait
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1ch]
    fld qword ptr [bp-1ch]
    fstp qword ptr [bp-48h]
    fld qword ptr [bp-14h]
    fstp qword ptr [bp-40h]
    fwait
    lea ax,[bp-48h]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push ss
    lea ax,[bp-58h]
    push ax
    call @$bmul$qm7complext1
    add sp,10h
    lea ax,[bp-58h]
    mov [bp-1eh],ss
    mov [bp-20h],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-22h],dx
    mov [bp-24h],ax
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx+8]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-2ch]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-34h]
    fwait
    mov [bp-36h],dx
    mov [bp-38h],ax
    or ax,[bp-36h]
    jz short allocate_complex_result
    mov ax,[bp-38h]
    jmp short have_complex_result
allocate_complex_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-36h],dx
    mov [bp-38h],ax
have_complex_result:
    or ax,dx
    jz short return_complex_result
    les bx,dword ptr [bp-38h]
    fld qword ptr [bp-34h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-2ch]
    fstp qword ptr es:[bx+8]
    fwait
return_complex_result:
    mov dx,[bp-36h]
    mov ax,[bp-38h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@$bdiv$qm7complext1 endp


; Third complete FAR division overload: scalar double over complex
; with real/imaginary temporaries, native x87 operations and allocation.
public @$bdiv$qdm7complex
@$bdiv$qdm7complex proc far
    push bp
    mov bp,sp
    sub sp,74h
    push si
    push di
    push word ptr [bp+14h]
    push word ptr [bp+12h]
    call @norm$qm7complex
    pop cx
    pop cx
    fstp qword ptr [bp-8]
    fwait
    mov dx,[bp+14h]
    mov ax,[bp+12h]
    mov [bp-0ah],dx
    mov [bp-0ch],ax
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx+8]
    fchs
    fstp qword ptr [bp-14h]
    fwait
    les bx,dword ptr [bp-0ch]
    fld qword ptr es:[bx]
    fstp qword ptr [bp-1ch]
    fld qword ptr [bp-1ch]
    fstp qword ptr [bp-64h]
    fld qword ptr [bp-14h]
    fstp qword ptr [bp-5ch]
    fwait
    lea ax,[bp-64h]
    mov [bp-1eh],ss
    mov [bp-20h],ax
    fld qword ptr [bp+0ah]
    fstp qword ptr [bp-28h]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx+8]
    fmul qword ptr [bp-28h]
    fstp qword ptr [bp-30h]
    fwait
    les bx,dword ptr [bp-20h]
    fld qword ptr es:[bx]
    fmul qword ptr [bp-28h]
    fstp qword ptr [bp-38h]
    fld qword ptr [bp-38h]
    fstp qword ptr [bp-74h]
    fld qword ptr [bp-30h]
    fstp qword ptr [bp-6ch]
    fwait
    lea ax,[bp-74h]
    mov [bp-3ah],ss
    mov [bp-3ch],ax
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov [bp-3eh],dx
    mov [bp-40h],ax
    les bx,dword ptr [bp-3ch]
    fld qword ptr es:[bx+8]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-48h]
    fwait
    les bx,dword ptr [bp-3ch]
    fld qword ptr es:[bx]
    fdiv qword ptr [bp-8]
    fstp qword ptr [bp-50h]
    fwait
    mov [bp-52h],dx
    mov [bp-54h],ax
    or ax,[bp-52h]
    jz short alloc_complex_division_result
    mov ax,[bp-54h]
    jmp short init_complex_division_result
alloc_complex_division_result:
    mov ax,16
    push ax
    call @$bnew$qui
    pop cx
    mov [bp-52h],dx
    mov [bp-54h],ax
init_complex_division_result:
    or ax,dx
    jz short scalar_division_return
    les bx,dword ptr [bp-54h]
    fld qword ptr [bp-50h]
    fstp qword ptr es:[bx]
    fld qword ptr [bp-48h]
    fstp qword ptr es:[bx+8]
    fwait
scalar_division_return:
    mov dx,[bp-52h]
    mov ax,[bp-54h]
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
@$bdiv$qdm7complex endp
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
end
