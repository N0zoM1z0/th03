; Original Japanese Borland xxas: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
SS_DESTRUCTOR_COUNT equ 10h
SS_EXCEPTION_LIST equ 14h
; SEG DGROUP supplies saved DS in the registration frame at +0Eh.
extrn __ExceptionHandler:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public @__RefDestructorCount$qv
public @__RefExceptionList$qv
public ___InitExceptBlocks
public ___ExitExceptBlocks
; Original statement chunks preserve native relocation chronology.

org 0
@__RefDestructorCount$qv label far
    mov dx, ss
    mov ax,SS_DESTRUCTOR_COUNT
    retf
@__RefExceptionList$qv label far
    mov dx, ss
    mov ax,SS_EXCEPTION_LIST
    retf
___InitExceptBlocks label far
    mov es, ax
    mov dx, bx
    mov cx, bp
    mov bx, word ptr es:[bx+4]
    add bx, cx
    mov word ptr ss:[bx+6], dx
    mov word ptr ss:[bx+8], ax
    mov ax, sp
    add ax, 4
    mov word ptr ss:[bx+0ah], ax

org 41
    mov ax,seg DGROUP
    mov word ptr ss:[bx+0eh], ax
    mov word ptr ss:[bx+010h], si

org 52
    mov word ptr ss:[bx+2],offset __ExceptionHandler

org 58
    mov word ptr ss:[bx+4],seg __ExceptionHandler
    mov word ptr ss:[bx+0ch], 0
    mov word ptr ss:[bx+012h], 0
    push bx
    push cs
    call near ptr @__RefDestructorCount$qv
    pop bx
    xchg bx, ax
    mov es, dx
    mov cx, word ptr es:[bx]
    mov dx, word ptr es:[bx+2]
    mov bx, ax
    mov word ptr ss:[bx+01ah], cx
    mov word ptr ss:[bx+01ch], dx
    push bx
    push cs
    call near ptr @__RefExceptionList$qv
    pop bx
    xchg bx, ax
    mov es, dx
    mov cx, word ptr es:[bx]
    mov word ptr es:[bx], ax
    mov bx, ax
    mov word ptr ss:[bx], cx
    retf
___ExitExceptBlocks label far
    push bp
    mov bp, sp
    push cs
    call near ptr @__RefExceptionList$qv
    mov bx, word ptr [bp+6]
    xchg bx, ax
    mov es, dx
    mov word ptr es:[bx], ax
    pop bp
    retf 2
_TEXT ends
end
