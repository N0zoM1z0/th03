; Original Japanese Borland spawnle: complete native runtime/process member.
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
public _spawnle
; Original statement chunks preserve native relocation chronology.

org 112
invalid_mode:
    mov word ptr DGROUP:_errno, EINVAL
    mov ax, 0ffffh
process_return:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

org 104
    call __LoadProg
    add sp, 010h
    jmp short process_return

org 100
    mov ax,offset __exec
load_dispatch:
    push ax

org 71
    mov ax,offset __spawn
    jmp short load_dispatch
exec_overlay:
    xor ax, ax
    push ax
    les bx, dword ptr [bp-4]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]

org 0
_spawnle label far
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    lea ax, [bp+0ch]
    mov word ptr [bp-2], ss
    mov word ptr [bp-4], ax
scan_argument_end:
    les bx, dword ptr [bp-4]
    add word ptr [bp-4], 4
    mov ax, word ptr es:[bx]
    or ax, word ptr es:[bx+2]
    jne short scan_argument_end
    mov ax, word ptr [bp+6]
    or ax, ax
    je short spawn_wait
    cmp ax, 2
    je short exec_overlay
    jmp short invalid_mode
spawn_wait:
    xor ax, ax
    push ax
    les bx, dword ptr [bp-4]
    push word ptr es:[bx+2]
    push word ptr es:[bx]
    push ss
    lea ax, [bp+0ch]
    push ax
    push word ptr [bp+0ah]
    push word ptr [bp+8]
_TEXT ends
end
