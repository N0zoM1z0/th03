; Original Japanese Borland spawnl: complete native runtime/process member.
; Original ABI, argument traversal, callbacks and unchecked behavior are retained.
.8086
include crt_errno.inc
extrn __exec:near
extrn __spawn:near
extrn __LoadProg:near
extrn _errno:word
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _spawnl
; Original statement chunks preserve native relocation chronology.

org 68
invalid_mode:
    mov word ptr DGROUP:_errno, EINVAL
    mov ax, 0ffffh
process_return:
    pop di
    pop si
    pop bp
    retf

org 60
    call __LoadProg
    add sp, 010h
    jmp short process_return

org 56
    mov ax,offset __exec
load_dispatch:
    push ax

org 35
    mov ax,offset __spawn
    jmp short load_dispatch
exec_overlay:
    xor ax, ax
    push ax
    push ax
    push ax
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]

org 0
_spawnl label far
    push bp
    mov bp, sp
    push si
    push di
    mov ax, word ptr [bp+6]
    or ax, ax
    je short spawn_wait
    cmp ax, 2
    je short exec_overlay
    jmp short invalid_mode
spawn_wait:
    xor ax, ax
    push ax
    push ax
    push ax
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
end
