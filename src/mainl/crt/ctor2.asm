; Original Japanese Borland string copy constructor: optional storage allocation and reference counting.
; Two CODE segments retain local unwind/cleanup, typed RTTI and the far API.
.8086
extrn @$bnew$qui:far
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
include string_xmsg_rtti.inl
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
include string_xmsg_unwind.inl
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@$bctr$qmx6string
STRING_BODY_SIZE equ 111
STRING_THROW_RTTI 6,<'xalloc'>,8

; Original statement/fixup chronology; each bounded instruction appears once.

org 94
    call ___ExitExceptBlocks
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 73
copy_construct_count:
    call @__RefDestructorCount$qv
    mov bx, ax
    mov es, dx
    add word ptr es:[bx], 1
    adc word ptr es:[bx+2], 0
    push word ptr [bp-01eh]

org 31
    call @$bnew$qui
    pop cx
    mov word ptr [bp+8], dx
    mov word ptr [bp+6], ax
    or ax, dx
    je short copy_construct_count
copy_construct_reference:
    les bx, dword ptr [bp+0ah]
    mov dx, word ptr es:[bx+2]
    mov ax, word ptr es:[bx]
    les bx, dword ptr [bp+6]
    mov word ptr es:[bx+2], dx
    mov word ptr es:[bx], ax
    les bx, dword ptr es:[bx]
    inc word ptr es:[bx]

org 14
    call ___InitExceptBlocks
    mov ax, word ptr [bp+6]
    or ax, word ptr [bp+8]
    jne short copy_construct_reference
    mov ax, 4
    push ax

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@$bctr$qmx6string proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@$bctr$qmx6string endp
_TEXTC ends
end
