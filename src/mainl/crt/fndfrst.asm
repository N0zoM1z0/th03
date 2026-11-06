; Original Japanese Borland find_first_of with original start check and far strpbrk.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
extrn @strpbrk$qncnxc:far
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
public @string@find_first_of$xqmx6stringui
; Native instruction chunks retain original FIXUPP enumeration.

org 134
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 88
    call @strpbrk$qncnxc
    add sp, 8
    mov word ptr [bp-022h], dx
    mov word ptr [bp-024h], ax
    or ax, word ptr [bp-022h]
    je short first_not_found
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr [bp-024h]
    xor dx, dx
    sub ax, word ptr es:[bx+2]
    sbb dx, 0
    jmp short first_result_ready
first_not_found:
    mov ax, 0ffffh
first_result_ready:
    push ax
    push word ptr [bp-01eh]

org 14
    call ___InitExceptBlocks
    mov ax, word ptr [bp+0eh]
    mov word ptr [bp-020h], ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp-020h]
    jbe short first_start_invalid
    mov ax, 1
    jmp short first_start_checked
first_start_invalid:
    xor ax, ax
first_start_checked:
    or ax, ax
    jne short first_search
    mov ax, 0ffffh
    jmp short first_result_ready
first_search:
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
@string@find_first_of$xqmx6stringui proc far
    push bp
    mov bp, sp
    sub sp, 024h
    push si
    push di
@string@find_first_of$xqmx6stringui endp
_TEXTC ends
end
