; Original Japanese Borland TSubString indexed mutable access with range check and clone.
; Two CODE segments retain local unwind/cleanup, typed RTTI and the far API.
.8086
extrn @$bdele$qnv:far
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @xmsg@$bdtr$qv:far
extrn @string@clone$qv:far
extrn @TSubString@assert_element$xqui:far
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
public @TSubString@$bcall$qui
STRING_BODY_SIZE equ 117
STRING_THROW_RTTI 4,<'string::outofrange'>,20

; Original statement/fixup chronology; each bounded instruction appears once.

org 104
    call ___ExitExceptBlocks
    pop ax
    pop dx
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 61
    call @string@clone$qv
    pop cx
    pop cx
    jmp short substring_storage_ready
substring_storage_ready:
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    les bx, dword ptr es:[bx]
    mov dx, word ptr es:[bx+4]
    mov ax, word ptr es:[bx+2]
    les bx, dword ptr [bp+6]
    mov bx, word ptr es:[bx+4]
    add bx, word ptr [bp+0ah]
    add ax, bx
    push dx
    push ax
    push word ptr [bp-01eh]

org 28
    call @TSubString@assert_element$xqui
    add sp, 6
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    les bx, dword ptr es:[bx]
    cmp word ptr es:[bx], 1
    jbe short substring_storage_ready
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]

org 14
    call ___InitExceptBlocks
    push word ptr [bp+0ah]
    push word ptr [bp+8]
    push word ptr [bp+6]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@TSubString@$bcall$qui proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@TSubString@$bcall$qui endp
_TEXTC ends
end
