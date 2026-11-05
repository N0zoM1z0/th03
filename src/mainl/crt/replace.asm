; Borland string::replace(unsigned, unsigned, const string&, unsigned, unsigned).
; Complete original C++ exception/RTTI machinery and bounded substring replacement.
; Four full original OMF segments: independent far exception helpers in
; _TEXT, typed exception tables and RTTI in CODE, a 30-byte message in DATA,
; and the complete replacement entry in _TEXTC.
.8086
extrn @$bdele$qnv:far,@__RefDestructorCount$qv:far
extrn @_ThrowException$qnvt1t1t1uiuiuinuc:far
extrn ___InitExceptBlocks:far,___ExitExceptBlocks:far
extrn @xmsg@$bctr$qmx6string:far,@xmsg@$bctr$qmx4xmsg:far
extrn @xmsg@$bdtr$qv:far,@string@$bctr$qnxc:far
extrn @string@$bdtr$qv:far,@string@clone$qv:far
extrn @TStringRef@splice$quiuinxcui:far

_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
_TEXTC ends
DGROUP group _BSS,_DATA

_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Compiler-generated no-op far exception cleanup thunk.
empty_unwind:
    push si
    push di
    pop di
    pop si
    retf

; Original typed Borland C++ exception class/catch descriptors in CODE.
; Their cross-segment far pointers select the actual native RTTI records.
exception_types:
    dd rtti_xalloc
    dd rtti_out_of_range
    dd rtti_length_error
    dw 0,0
    dd rtti_string
    dw 4,-4,0
    dd rtti_out_of_range
    dw 4,-8,0
    dd 0
    dd rtti_xmsg
    db 0,1,1,0,0,0,0,0,0,0

exception_block_list:
    dd exception_types
    dw -38,0
    dd 5
    dw offset _TEXT:rtti_string_ref
    dw 6,5,1
    dw offset _TEXT:exception_scope_entry

; The labels below also serve as the original internal exception table keys.
; Their offsets are part of the retained source-bound OMF frame.
rtti_string_ref equ exception_types+16
exception_scope_entry equ exception_types+40

; Shared far C++ copy-constructed error object used by exception recovery.
construct_exception_message:
    push bp
    mov bp,sp
    push si
    push di
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bctr$qmx4xmsg
    add sp,8
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
    pop di
    pop si
    pop bp
    retf

; Destruction callbacks for length_error, xalloc, and out_of_range RTTI.
destroy_length_error:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,word ptr [bp+6]
    or ax,word ptr [bp+8]
    je length_return_zero
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+0ah],1
    je length_skip_delete
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short length_return
length_skip_delete:
    jmp short length_return
length_return_zero:
    xor ax,ax
length_return:
    pop di
    pop si
    pop bp
    retf

destroy_xalloc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,word ptr [bp+6]
    or ax,word ptr [bp+8]
    je xalloc_return_zero
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+0ah],1
    je xalloc_skip_delete
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short xalloc_return
xalloc_skip_delete:
    jmp short xalloc_return
xalloc_return_zero:
    xor ax,ax
xalloc_return:
    pop di
    pop si
    pop bp
    retf

destroy_out_of_range:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,word ptr [bp+6]
    or ax,word ptr [bp+8]
    je range_return_zero
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    xor ax,ax
    push ax
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @xmsg@$bdtr$qv
    add sp,6
    test byte ptr [bp+0ah],1
    je range_skip_delete
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short range_return
range_skip_delete:
    jmp short range_return
range_return_zero:
    xor ax,ax
range_return:
    pop di
    pop si
    pop bp
    retf
_TEXT ends

_DATA segment word public 'DATA'
    ; String literal used to instantiate the original C++ out_of_range.
out_of_range_message db 'String reference out of range',0
_DATA ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@replace$quiuimx6stringuiui

@string@replace$quiuimx6stringuiui:
    push bp
    mov bp,sp
    sub sp,2eh
    push si
    push di

    ; Link the Borland exception context on the current stack frame.
    mov ax,seg empty_unwind
    mov bx,offset _TEXT:exception_block_list
    call ___InitExceptBlocks

    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx]
    mov ax,word ptr es:[bx+6]
    cmp ax,word ptr [bp+0ah]
    jae in_bounds

    ; Construct and throw string::out_of_range with original message.
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    mov ax,5
    push ax
    mov ax,seg _TEXT
    push ax
    mov ax,offset _TEXT:construct_exception_message
    push ax
    xor ax,ax
    push ax
    push ax
    mov word ptr [bp-1ah],6
    push ds
    mov ax,offset DGROUP:out_of_range_message
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    call @string@$bctr$qnxc
    add sp,8

    lea ax,[bp-4]
    push ss
    push ax
    push ss
    lea ax,[bp-8]
    push ax
    call @xmsg@$bctr$qmx6string
    add sp,8
    mov word ptr [bp-1ah],0eh
    mov ax,2
    push ax
    push ss
    lea ax,[bp-4]
    push ax
    call @string@$bdtr$qv
    add sp,6
    mov word ptr [bp-1ah],6
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    add word ptr es:[bx],1
    adc word ptr es:[bx+2],0
    lea ax,[bp-8]
    push ss
    push ax
    push cs
    mov ax,offset _TEXTC:rtti_out_of_range
    push ax
    call @_ThrowException$qnvt1t1t1uiuiuinuc
    add sp,1ah

in_bounds:
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx]
    cmp word ptr es:[bx],1
    jbe have_unique_ref
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @string@clone$qv
    pop cx
    pop cx
    jmp short have_unique_ref
have_unique_ref:
    ; Clamp first source slice offset to source length. Original Borland
    ; implementation selects one of two *stack word addresses* and then
    ; dereferences the selected SS:offset, preserving 16-bit semantics.
    les bx,dword ptr [bp+0eh]
    les bx,dword ptr es:[bx]
    mov ax,word ptr es:[bx+6]
    mov word ptr [bp-28h],ax
    mov ax,word ptr [bp+12h]
    cmp ax,word ptr [bp-28h]
    jae first_slice_limit
    mov dx,ss
    lea ax,[bp+12h]
    jmp short first_slice_address
first_slice_limit:
    mov dx,ss
    lea ax,[bp-28h]
first_slice_address:
    mov bx,ax
    mov es,dx
    mov cx,word ptr es:[bx]
    ; Clamp second bound against the available source characters.
    les bx,dword ptr [bp+0eh]
    les bx,dword ptr es:[bx]
    mov ax,word ptr es:[bx+6]
    sub ax,cx
    mov word ptr [bp-2ch],ax
    cmp ax,word ptr [bp+14h]
    jae second_slice_limit
    mov dx,ss
    lea ax,[bp-2ch]
    jmp short second_slice_address
second_slice_limit:
    mov dx,ss
    lea ax,[bp+14h]
second_slice_address:
    mov bx,ax
    mov es,dx
    mov ax,word ptr es:[bx]
    mov word ptr [bp-2ah],ax
    push ax
    les bx,dword ptr [bp+0eh]
    les bx,dword ptr es:[bx]
    mov ax,word ptr es:[bx+2]
    add ax,cx
    push word ptr es:[bx+4]
    push ax
    ; Clip the removed destination span to the remaining length.
    les bx,dword ptr [bp+6]
    les bx,dword ptr es:[bx]
    mov ax,word ptr es:[bx+6]
    sub ax,word ptr [bp+0ah]
    mov word ptr [bp-2eh],ax
    mov ax,word ptr [bp+0ch]
    cmp ax,word ptr [bp-2eh]
    jae clamp_remove_end
    mov dx,ss
    lea ax,[bp+0ch]
    jmp short got_remove_bound
clamp_remove_end:
    mov dx,ss
    lea ax,[bp-2eh]
got_remove_bound:
    mov bx,ax
    mov es,dx
    push word ptr es:[bx]
    push word ptr [bp+0ah]
    les bx,dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call @TStringRef@splice$quiuinxcui
    add sp,0eh
    mov dx,word ptr [bp+8]
    mov ax,word ptr [bp+6]
    push dx
    push ax
    push word ptr [bp-26h]
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Exact typed C++ RTTI. Data below is not executable x86 instructions.
rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0
    dw 0,0,0,0,0,0
rtti_string:
    dw 4,3,38,-1,3,46,50
    dw 0,0,0,0,0,0,1,1
    dd @string@$bdtr$qv
    dw 5,54
    db 'string',0
    db 0
    dw 0,0,0,0,0,0
rtti_length_error:
    dw 4,3,38,-1,7,58,70
    dw 0,0,0,0,0,0,2,2
    dd destroy_length_error
    dw 5,74
    db 'string::lengtherror',0
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0
rtti_xalloc:
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2
    dd destroy_xalloc
    dw 5,62
    db 'xalloc',0
    db 0
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0
rtti_out_of_range:
    dw 4,3,38,-1,7,58,70
    dw 0,0,0,0,0,0,2,2
    dd destroy_out_of_range
    dw 5,74
    db 'string::outofrange',0
    db 0 ; Original Borland RTTI alignment after odd-sized class name
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0
_TEXTC ends
end
