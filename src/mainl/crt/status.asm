; Original Japanese Borland TRegexp status read with original read-and-clear side effect.
; Retain distinct CODE owners, literal ordered fields and unchecked behavior.
.8086
extrn @__RefDestructorCount$qv:far
extrn ___InitExceptBlocks:far
extrn ___ExitExceptBlocks:far
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
public @TRegexp@status$qv
; Native instruction chunks retain original FIXUPP enumeration.

org 43
    call ___ExitExceptBlocks
    pop ax
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 14
    call ___InitExceptBlocks
    les bx, dword ptr [bp+6]
    add bx, 4
    mov word ptr [bp-022h], bx
    mov ax, word ptr es:[bx]
    mov word ptr [bp-020h], ax
    mov word ptr es:[bx], 0
    push ax
    push word ptr [bp-01eh]

org 11
    mov bx,offset _TEXT:string_exception_frame

org 8
    mov ax,seg string_exception_unwind

org 0
@TRegexp@status$qv proc far
    push bp
    mov bp, sp
    sub sp, 022h
    push si
    push di
@TRegexp@status$qv endp
_TEXTC ends
end
