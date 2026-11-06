; Original Japanese Borland tmpfile: complete file/stream native member.
; Preserve original near/far cleanup, widths and ordered relocation chronology.
.8086
include stdio_tmp.inc
extrn _fopen:far
extrn __TMPNAM:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_DATA segment word public 'DATA'
temporary_open_mode db 'w+b',0
_DATA ends
_BSS segment word public 'BSS'
public __tmpnum
__tmpnum dw ?
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _tmpfile
; Complete disjoint instruction chunks preserve original native field order.

org 56
    mov ax, word ptr DGROUP:__tmpnum
    mov word ptr es:[bx+FILE_TMPNUM], ax
tmpfile_return:
    mov dx, word ptr [bp-2]
    mov ax, word ptr [bp-4]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 35
    call _fopen
    add sp, 8
    mov word ptr [bp-2], dx
    mov word ptr [bp-4], ax
    or ax, dx
    je short tmpfile_return
    les bx, dword ptr [bp-4]

org 27
    mov ax,offset DGROUP:temporary_open_mode
    push ax
    push dx
    push word ptr [bp-8]

org 17
    call __TMPNAM
    mov word ptr [bp-6], dx
    mov word ptr [bp-8], ax
    push ds

org 13
    mov ax,offset DGROUP:__tmpnum
    push ax

org 0
_tmpfile label far
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    xor ax, ax
    push ax
    push ax
    push ds
_TEXT ends
end
