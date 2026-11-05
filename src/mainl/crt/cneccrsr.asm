; Original Japanese Borland PC-98 cursor-shape controller. This member
; supports both NEC interrupt paths and direct hardware cursor I/O.
; The two ESC[>5 mode strings are actual initialized DATA, not CODE bytes.
.8086
extrn __video:byte
extrn ___nec_get_screen_height:far
extrn __NEC_VIDEOINT18:near,__NEC_VIDEOINTDC:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
; Original GROUP member order is BSS, DATA, not TASM's default.
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; Emit a zero-terminated far buffer through the original NEC video service.
video_escape proc near
    push bp
    mov bp,sp
    push si
    push di
    jmp short escaped_next
escaped_write:
    les bx,dword ptr [bp+4]
    mov dl,byte ptr es:[bx]
    mov cl,10h
    mov ah,0
    call __NEC_VIDEOINTDC
    inc word ptr [bp+4]
escaped_next:
    les bx,dword ptr [bp+4]
    cmp byte ptr es:[bx],0
    jne short escaped_write
    pop di
    pop si
    pop bp
    ret 4
video_escape endp

; Original direct PC-98 cursor parameter handshaking with interrupt flags
; saved and restored. Nothing here depends on a modern BIOS emulator shim.
cursor_direct proc near
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    mov es,ax
    pushf
    mov dx,[bp+4]
    mov ah,byte ptr es:[053bh]
    test dh,80h
    jnz short cursor_flag_ready
    or ah,80h
cursor_flag_ready:
    and dh,1fh
    shl dl,1
    shl dl,1
    shl dl,1
    or dl,3
    jmp short wait_port
pulse_port:
    out 5fh,al
    out 5fh,al
    ret
wait_port:
    sti
    call pulse_port
    cli
    in al,60h
    test al,4
    jz short wait_port
    call pulse_port
    mov al,4bh
    out 62h,al
    call pulse_port
    mov al,ah
    out 60h,al
    call pulse_port
    mov al,dh
    out 60h,al
    call pulse_port
    mov al,dl
    out 60h,al
    call pulse_port
    popf
    pop di
    pop si
    pop bp
    ret 2
cursor_direct endp

; INT 18h cursor mode: preserve height-bit meaning in AH=11h/12h.
cursor_interrupt proc near
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+4]
    and dh,7fh
    mov ax,1e80h
    call __NEC_VIDEOINT18
    mov ah,11h
    test byte ptr [bp+5],80h
    jz short int18_mode_ready
    mov ah,12h
int18_mode_ready:
    call __NEC_VIDEOINT18
    pop di
    pop si
    pop bp
    ret 2
cursor_interrupt endp

public ___nec_setcursortype
___nec_setcursortype proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    call ___nec_get_screen_height
    mov [bp-2],ax
    cmp word ptr [bp+6],0
    jnz short show_mode
    mov dx,ds
    mov ax,offset DGROUP:cursor_mode_on
    jmp short mode_text_ready
show_mode:
    mov dx,ds
    mov ax,offset DGROUP:cursor_mode_off
mode_text_ready:
    push dx
    push ax
    call video_escape
    cmp byte ptr DGROUP:__video+14,0
    jz short direct_mode
    cmp word ptr [bp+6],0
    jnz short interrupt_alt
    cmp word ptr [bp-2],25
    jng short interrupt_small
    mov ax,800bh
    jmp short interrupt_call
interrupt_small:
    mov ax,800eh
    jmp short interrupt_call
interrupt_alt:
    cmp word ptr [bp+6],3
    jnz short interrupt_other
    cmp word ptr [bp-2],25
    jng short interrupt_alt_small
    mov ax,090bh
    jmp short interrupt_call
interrupt_alt_small:
    mov ax,0b0eh
    jmp short interrupt_call
interrupt_other:
    cmp word ptr [bp-2],25
    jng short interrupt_other_small
    mov ax,000bh
    jmp short interrupt_call
interrupt_other_small:
    mov ax,000eh
interrupt_call:
    push ax
    call cursor_interrupt
    jmp short cursor_done
direct_mode:
    cmp word ptr [bp+6],0
    jnz short direct_alt
    cmp word ptr [bp-2],20
    jng short direct_small
    mov ax,800fh
    jmp short direct_call
direct_small:
    mov ax,8013h
    jmp short direct_call
direct_alt:
    cmp word ptr [bp+6],3
    jnz short direct_other
    cmp word ptr [bp-2],20
    jng short direct_alt_small
    mov ax,0c0fh
    jmp short direct_call
direct_alt_small:
    mov ax,0e13h
    jmp short direct_call
direct_other:
    cmp word ptr [bp-2],20
    jng short direct_other_small
    mov ax,000fh
    jmp short direct_call
direct_other_small:
    mov ax,0013h
direct_call:
    push ax
    call cursor_direct
cursor_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___nec_setcursortype endp
_TEXT ends

_DATA segment word public 'DATA'
cursor_mode_off db 1bh,'[>5l',0
cursor_mode_on db 1bh,'[>5h',0
_DATA ends
end
