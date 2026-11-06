; Original Japanese Borland string regexp find with caller result-length reference.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @TRegexp@find$xqmx6stringnuiui:far
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
include string_empty_unwind.inl
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @string@find$xqmx7TRegexpnuiui
; Native instruction chunks retain original FIXUPP enumeration.

org 52
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 40
    call @TRegexp@find$xqmx6stringnuiui
    add sp, 0eh
    push ax
    push word ptr [bp-01eh]

org 14
    call ___InitExceptBlocks
    push word ptr [bp+012h]
    push word ptr [bp+010h]
    push word ptr [bp+0eh]
    push word ptr [bp+8]
    push word ptr [bp+6]
    push word ptr [bp+0ch]
    push word ptr [bp+0ah]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@find$xqmx7TRegexpnuiui proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@find$xqmx7TRegexpnuiui endp
_TEXTC ends
end
