; Original Japanese Borland string copy: clamp requested count and preserve original count-plus-one memcpy.
; Two CODE segments retain local unwind/cleanup, typed RTTI and the far API.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _memcpy:far
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
public @string@copy$qncuiui
STRING_BODY_SIZE equ 103
STRING_THROW_RTTI 4,<'string::outofrange'>,20

; Original statement/fixup chronology; each bounded instruction appears once.

org 91
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 76
    call _memcpy
    add sp, 0ah
    mov ax, word ptr [bp+0eh]
    push ax
    push word ptr [bp-01eh]

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    sub ax, word ptr [bp+010h]
    cmp ax, word ptr [bp+0eh]
    jae short copy_count_ready
    mov ax, word ptr es:[bx+6]
    sub ax, word ptr [bp+010h]
    mov word ptr [bp+0eh], ax
copy_count_ready:
    mov ax, word ptr [bp+0eh]
    inc ax
    push ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    add ax, word ptr [bp+010h]
    push word ptr es:[bx+4]
    push ax
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@copy$qncuiui proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@copy$qncuiui endp
_TEXTC ends
end
