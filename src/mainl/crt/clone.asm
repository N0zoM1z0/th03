; Full original Japanese Borland string::clone with three typed RTTI.
; Native 8086 far copy-on-write, reference counts and exception state.
; All typed C++ RTTI/exception control fields are dw/dd symbolic source.
.8086
extrn @$bnew$qui:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @TStringRef@$bctr$qnxcuit1uiui:far
extrn @TStringRef@$bdtr$qv:far
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

; Real native original BCC CODE1 statement/fixup order.

org 39
    dw offset _TEXT:clone_exception_header

org 5

clone_exception_header:
    dd rtti_TStringRef_pointer
    dw 8327
    dw -4
    dw 0
    dw 0
    dw 0

clone_exception_state:
    dw 0
    dw 0
    dw -34
    dw 0
    dw 5
    dw 0
    dw -1
    dw 6
    dw 5
    dw 0

org 0

clone_empty_unwind:
    push si
    push di
    pop di
    pop si
    retf
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@clone$qv

; Real native original BCC CODE4 statement/fixup order.

org 221
    dd rtti_TReference
    dw 0
    dw 3
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0

rtti_TReference:
    dw 2
    dw 3
    dw 26
    dw -1
    dw 1
    dw 38
    dw 42
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    db 'TReference',0,0
    dw 0
    dw 0
    dw 0
    dw 0

org 201
    dd @TStringRef@$bdtr$qv
    dw 5
    dw 66
    db 'TStringRef',0,0

org 154
    dd rtti_TStringRef
    db 'TStringRef *',0

rtti_TStringRef:
    dw 12
    dw 3
    dw 38
    dw -1
    dw 7
    dw 50
    dw 62
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 0
    dw 1
    dw 1

org 137
    call ___ExitExceptBlocks
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

rtti_TStringRef_pointer:
    dw 4
    dw 8336
    dw 10

org 95
    call @__RefDestructorCount$qv
    mov bx,ax
    mov es,dx
    sub word ptr es:[bx],1
    sbb word ptr es:[bx+2],0
    mov word ptr [bp-22],6

plus_4_branch_0076:
    mov dx,[bp-2]
    mov ax,[bp-4]
    les bx,[bp+6]
    mov es:[bx+2],dx
    mov es:[bx],ax
    push word ptr [bp-34]

org 87
    call @TStringRef@$bctr$qnxcuit1uiui
    add sp,18

org 32
    call @$bnew$qui
    pop cx
    mov [bp-2],dx
    mov [bp-4],ax
    or ax,dx
    jz plus_4_branch_0076
    mov word ptr [bp-22],14
    xor ax,ax
    push ax
    push ax
    push ax
    push ax
    les bx,[bp+6]
    les bx,es:[bx]
    mov [bp-36],es
    mov [bp-38],bx
    push word ptr es:[bx+6]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push dx
    push word ptr [bp-4]

org 14
    call ___InitExceptBlocks
    les bx,[bp+6]
    les bx,es:[bx]
    dec word ptr es:[bx]
    mov ax,12
    push ax

org 11
    mov bx,offset _TEXT:clone_exception_state

org 8
    mov ax,seg _TEXT

org 0

@string@clone$qv:
    push bp
    mov bp,sp
    sub sp,38
    push si
    push di
_TEXTC ends
end
