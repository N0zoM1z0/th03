; DOS large-model far cdecl memcpy, with no generated memory-access traps.
; Arguments: destination far [BP+6], source far [BP+10], count WORD [BP+14].
; Returns the original destination in DX:AX, preserving incoming DS/SI/DI.
; The copy executes forward, including the original odd trailing byte.
.8086
_TEXT segment byte public 'CODE'
assume cs:_TEXT
public _memcpy
_memcpy proc far
    push bp
    mov bp,sp
    push si
    push di

    mov dx,ds
    les di,dword ptr [bp+6]
    lds si,dword ptr [bp+10]
    mov cx,[bp+14]
    shr cx,1
    cld
    rep movsw
    jnc short copy_finished
    movsb
copy_finished:
    mov ds,dx
    mov dx,[bp+8]
    mov ax,[bp+6]
    pop di
    pop si
    pop bp
    retf
_memcpy endp
_TEXT ends

; Declare DGROUP before the empty segments. TASM otherwise reverses the
; original BSS/DATA GRPDEF membership and loses the empty BSS MAP owner.
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
end
