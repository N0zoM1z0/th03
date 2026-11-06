; Original Japanese Borland TRegexp text assignment with original pattern deletion and generation.
; Preserve both native CODE segments, control metadata, far ABI and literal fields.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
extrn @TRegexp@gen_pattern$qnxc:far
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
public @TRegexp@$basg$qnxc
STRING_BODY_SIZE equ 78
STRING_THROW_RTTI 6,<'xalloc'>,8
; Native statement chunks preserve complete original ordered FIXUPPs.

org 65
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 46
    call @TRegexp@gen_pattern$qnxc
    add sp, 0ch
    mov dx, word ptr [bp+8]
    mov ax, word ptr [bp+6]
    push dx
    push ax
    push word ptr [bp-01eh]

org 29
    call @$bdele$qnv
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@TRegexp@$basg$qnxc proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@TRegexp@$basg$qnxc endp
_TEXTC ends
end
