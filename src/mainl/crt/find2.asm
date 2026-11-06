; Original Japanese Borland TRegexp match with original result-length output.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn @matchs$qnxcnxucnnc:far
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
include string_unwind_only.inl
_TEXT ends
_TEXTC segment byte public 'CODE'
assume cs:_TEXTC,ds:DGROUP
public @TRegexp@find$xqmx6stringnuiui
; Native instruction chunks retain original FIXUPP enumeration.

org 51
    call @matchs$qnxcnxucnnc
    add sp, 0ch
    mov word ptr [bp-0ah], dx
    mov word ptr [bp-0ch], ax
    or ax, word ptr [bp-0ah]
    je short regexp_not_found
    mov ax, word ptr [bp-0ch]
    xor dx, dx
    sub ax, word ptr [bp-4]
    sbb dx, 0
    inc ax
    les bx, dword ptr [bp+0eh]
    mov word ptr es:[bx], ax
    mov ax, word ptr [bp-4]
    xor dx, dx
    sub ax, word ptr [bp-8]
    sbb dx, 0
    jmp short regexp_find_return
regexp_not_found:
    les bx, dword ptr [bp+0eh]
    mov word ptr es:[bx], 0
    mov ax, 0ffffh
regexp_find_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 0
@TRegexp@find$xqmx6stringnuiui proc far
    push bp
    mov bp, sp
    sub sp, 0ch
    push si
    push di
    les bx, dword ptr [bp+0ah]
    les bx, dword ptr es:[bx]
    mov dx, word ptr es:[bx+4]
    mov ax, word ptr es:[bx+2]
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    push ss
    lea ax, [bp-4]
    push ax
    les bx, dword ptr [bp+6]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    mov ax, word ptr [bp-8]
    add ax, word ptr [bp+012h]
    push dx
    push ax
@TRegexp@find$xqmx6stringnuiui endp
_TEXTC ends
end
