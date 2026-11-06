; Original Japanese Borland find_first_not_of with original strspn and length comparison.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn _strspn:far
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
public @string@find_first_not_of$xqmx6stringui
; Native instruction chunks retain original FIXUPP enumeration.

org 102
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 66
    call _strspn
    add sp, 8
    mov dx, ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    cmp word ptr es:[bx+6], dx
    jne short first_not_of_found
first_not_of_not_found:
    mov ax, 0ffffh
    jmp short first_not_of_result_ready
first_not_of_found:
    mov ax, dx
    add ax, word ptr [bp+0eh]
first_not_of_result_ready:
    push ax
    push word ptr [bp-01eh]

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+0eh]
    jbe short first_not_of_not_found
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    push word ptr es:[bx+4]
    push word ptr es:[bx+2]
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+2]
    add ax, word ptr [bp+0eh]
    push word ptr es:[bx+4]
    push ax

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@string@find_first_not_of$xqmx6stringui proc far
    push bp
    mov bp, sp
    sub sp, 01eh
    push si
    push di
@string@find_first_not_of$xqmx6stringui endp
_TEXTC ends
end
