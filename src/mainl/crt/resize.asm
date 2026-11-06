; Original Japanese Borland string resize through original clone and splice.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn @string@clone$qv:far
extrn @TStringRef@splice$quiuinxcui:far
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
public @string@resize$qui
; Native instruction chunks retain original FIXUPP enumeration.

org 113
resize_splice:
    call @TStringRef@splice$quiuinxcui
    add sp, 0eh
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 26
    call @string@clone$qv
    pop cx
    pop cx
    jmp short resize_storage_ready
resize_storage_ready:
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov ax, word ptr es:[bx+6]
    cmp ax, word ptr [bp+0ah]
    jae short resize_shrink
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov dx, es
    mov cx, bx
    mov ax, word ptr [bp+0ah]
    sub ax, word ptr es:[bx+6]
    push ax
    xor ax, ax
    push ax
    push ax
    push ax
    push word ptr es:[bx+6]
    push dx
    push bx
    jmp short resize_splice
resize_shrink:
    xor ax, ax
    push ax
    push ax
    push ax
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    mov word ptr [bp-2], es
    mov word ptr [bp-4], bx
    mov ax, word ptr es:[bx+6]
    sub ax, word ptr [bp+0ah]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp-2]
    push bx

org 0
@string@resize$qui proc far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    les bx, dword ptr [bp+6]
    les bx, dword ptr es:[bx]
    cmp word ptr es:[bx], 1
    jbe short resize_storage_ready
    push word ptr [bp+8]
    push word ptr [bp+6]
@string@resize$qui endp
_TEXTC ends
end
