; Original Japanese Borland C++ regular expression class implementation.
; Full constructors, destructor, clone/copy_pattern, gen_pattern, typed RTTI.
; The named 2-byte DATA maxpat and two genuine CODE segments are preserved.
.8086
extrn @$bnew$qui:far
extrn @$bnwa$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
extrn _memcpy:far
extrn @makepat$qnxcnucui:far
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
exception_noop:
    push si
    push di
    pop di
    pop si
    retf

; Two original compiler exception frame chains in CODE, not opcodes.
regexp_copy_exception_frame:
    dd rtti_xalloc
    dd 0
regexp_copy_exception_state:
    dd regexp_copy_exception_frame
    dw -30
regexp_gen_exception_frame:
    dd rtti_xalloc
    dd 0
regexp_gen_exception_state:
    dd regexp_gen_exception_frame
    dw -30

; Original non-exported destruction helper used by exception unwind.

regexp_destroy_xalloc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jz branch_1_0068
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
    test byte ptr [bp+10],1
    jz branch_1_0066
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx
    jmp short branch_1_006a

branch_1_0066:
    jmp short branch_1_006a

branch_1_0068:
    xor ax,ax

branch_1_006a:
    pop di
    pop si
    pop bp
    retf
_TEXT ends

_DATA segment word public 'DATA'
assume ds:DGROUP
public @TRegexp@maxpat
@TRegexp@maxpat dw 128
_DATA ends

_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @TRegexp@$bctr$qnxc,@TRegexp@$bctr$qmx7TRegexp
public @TRegexp@$bdtr$qv,@TRegexp@copy_pattern$qmx7TRegexp
public @TRegexp@gen_pattern$qnxc

@TRegexp@$bctr$qnxc:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_4_0021
    mov ax,6
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_4_0035

branch_4_0021:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    ; TASM rewrites local far CALL as PUSH CS + near CALL (one byte shorter).
    ; Preserve the original direct CALL FAR immediate opcode and let OMF
    ; relocate the naturally declared far function pointer.
    db 09ah
    dd @TRegexp@gen_pattern$qnxc
    add sp,8

branch_4_0035:
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

@TRegexp@$bctr$qmx7TRegexp:
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    or ax,[bp+8]
    jnz branch_4_0072
    mov ax,6
    push ax
    call @$bnew$qui
    pop cx
    mov [bp+8],dx
    mov [bp+6],ax
    or ax,dx
    jz branch_4_0086

branch_4_0072:
    push word ptr [bp+12]
    push word ptr [bp+10]
    push word ptr [bp+8]
    push word ptr [bp+6]
    db 09ah
    dd @TRegexp@copy_pattern$qmx7TRegexp
    add sp,8

branch_4_0086:
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

@TRegexp@$bdtr$qv:
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
    jz branch_4_00e5
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call @$bdele$qnv
    pop cx
    pop cx
    test byte ptr [bp+10],1
    jz branch_4_00e5
    push word ptr [bp+8]
    push word ptr [bp+6]
    call @$bdele$qnv
    pop cx
    pop cx

branch_4_00e5:
    pop di
    pop si
    pop bp
    retf

@TRegexp@copy_pattern$qmx7TRegexp:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:regexp_copy_exception_state
    call ___InitExceptBlocks
    mov ax,128
    push ax
    call @$bnwa$qui
    pop cx
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov ax,128
    push ax
    les bx,[bp+10]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    les bx,[bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    call _memcpy
    add sp,10
    les bx,[bp+10]
    mov ax,es:[bx+4]
    les bx,[bp+6]
    mov es:[bx+4],ax
    push word ptr [bp-30]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

@TRegexp@gen_pattern$qnxc:
    push bp
    mov bp,sp
    sub sp,30
    push si
    push di
    mov ax,seg _TEXT
    mov bx,offset _TEXT:regexp_gen_exception_state
    call ___InitExceptBlocks
    mov ax,128
    push ax
    call @$bnwa$qui
    pop cx
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax
    mov ax,128
    push ax
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push word ptr [bp+12]
    push word ptr [bp+10]
    call @makepat$qnxcnucui
    add sp,10
    les bx,[bp+6]
    mov es:[bx+4],ax
    push word ptr [bp-30]
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

; Typed original Borland exception RTTI at _TEXTC+417.
rtti_xalloc:
    dw 6,3,38,-1,7,46,58
    dw 0,0,0,0,0,0,2,2
    dd regexp_destroy_xalloc
    dw 5,62
    db 'xalloc',0
    db 0
    dd rtti_xmsg
    dw 0,3,0,0,0,0,0,0
rtti_xmsg:
    dw 4,3,38,-1,3,44,48
    dw 0,0,0,0,0,0,1,1
    dd @xmsg@$bdtr$qv
    dw 5,52
    db 'xmsg',0
    db 0
    dw 0,0,0,0,0,0
_TEXTC ends
end
