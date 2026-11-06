; Original Japanese Borland const string comparison with original case-selection global.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strcmp:far
extrn _stricmp:far
extrn @string@case_sensitive:word
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
public @string@compare$xqmx6string
; Native instruction chunks retain original FIXUPP enumeration.

org 101
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 89
    call _stricmp
compare_finish:
    add sp, 8
    push ax
    push word ptr [bp-01eh]

org 54
    call _strcmp
    jmp short compare_finish
compare_ignore_case:
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 19
    cmp word ptr DGROUP:@string@case_sensitive, 0
    je short compare_ignore_case
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]

org 14
    call ___InitExceptBlocks

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@compare$xqmx6string proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@compare$xqmx6string endp
_TEXTC ends
end
