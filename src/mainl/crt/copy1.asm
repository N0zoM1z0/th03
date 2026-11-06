; Original Japanese Borland string prefix copy with original count-plus-one memcpy.
; Preserve both native CODE segments, control metadata, far ABI and literal fields.
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
public @string@copy$qncui
STRING_BODY_SIZE equ 89
STRING_THROW_RTTI 4,<'string::outofrange'>,20
; Native statement chunks preserve complete original ordered FIXUPPs.

org 77
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 62
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
    cmp ax, word ptr [bp+0eh]
    jae short copy_count_ready
    mov word ptr [bp+0eh], ax
copy_count_ready:
    mov ax, word ptr [bp+0eh]
    inc ax
    push ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@copy$qncui proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@copy$qncui endp
_TEXTC ends
end
