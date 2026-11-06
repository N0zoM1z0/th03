; Original Japanese Borland spawnlp: complete native runtime/process member.
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
public _spawnlp
; Original statement chunks preserve native relocation chronology.

org 74
invalid_mode:
    mov word ptr DGROUP:_errno, EINVAL
    mov ax, 0ffffh
process_return:
    pop di
    pop si
    pop bp
    retf

org 66
    call __LoadProg
    add sp, 010h
    jmp short process_return

org 62
    mov ax,offset __exec
load_dispatch:
    push ax

org 38
    mov ax,offset __spawn
    jmp short load_dispatch
exec_overlay:
    mov ax, 1
    push ax
    xor ax, ax
    push ax
    push ax
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]

org 0
_spawnlp label far
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
    mov ax, 1
    push ax
    xor ax, ax
    push ax
    push ax
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
end
