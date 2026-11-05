; Borland DOS INT 24h critical-error bridge, original large-model CRT.
; The actual interrupt stack and both old/new callback conventions share
; the same 12-byte DGROUP state. This is not a DOS signal-emulation shim.
.8086
extrn _bdos:far,_setvect:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
; BSS-first group ordering is original; declare before BSS SEGDEF to retain
; Borland's 08ff03ff02 group member order under TASM50.
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

; INT 24h entry; temporarily set DS to CRT DGROUP before dereferencing
; the saved application callback. Preserve the interrupted register frame.
critical_error_interrupt proc far
    push ax
    push bx
    push cx
    push dx
    push es
    push ds
    push si
    push di
    push bp
    mov bp,seg DGROUP
    mov ds,bp
    mov bp,sp
    mov word ptr DGROUP:saved_interrupt_sp,sp
    cmp word ptr DGROUP:extended_callback_flag,0
    jz short standard_callback
    push word ptr [bp]
    push word ptr [bp+4]
    push word ptr [bp+2]
    push word ptr [bp+16]
    call dword ptr DGROUP:extended_callback
    add sp,8
    jmp short error_action_ready
standard_callback:
    push word ptr [bp+4]
    push word ptr [bp]
    push word ptr [bp+16]
    mov ax,[bp+2]
    and ax,0FFh
    push ax
    call dword ptr DGROUP:legacy_callback
    add sp,8
    mov [bp+16],ax
error_action_ready:
    pop bp
    pop di
    pop si
    pop ds
    pop es
    pop dx
    pop cx
    pop bx
    pop ax
    iret
critical_error_interrupt endp

; Register an original-style critical-error handler (two-word far callback).
public ___harderr
___harderr proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr DGROUP:legacy_callback+2,dx
    mov word ptr DGROUP:legacy_callback,ax
    mov word ptr DGROUP:extended_callback_flag,0
    mov ax,seg critical_error_interrupt
    push ax
    mov ax,offset critical_error_interrupt
    push ax
    mov ax,24h
    push ax
    call _setvect
    add sp,6
    pop di
    pop si
    pop bp
    retf
___harderr endp

; Register the extended-style handler; retains the original argument layout.
public __harderr
__harderr proc far
    push bp
    mov bp,sp
    push si
    push di
    mov dx,[bp+8]
    mov ax,[bp+6]
    mov word ptr DGROUP:extended_callback+2,dx
    mov word ptr DGROUP:extended_callback,ax
    mov word ptr DGROUP:extended_callback_flag,1
    mov ax,seg critical_error_interrupt
    push ax
    mov ax,offset critical_error_interrupt
    push ax
    mov ax,24h
    push ax
    call _setvect
    add sp,6
    pop di
    pop si
    pop bp
    retf
__harderr endp

; This exits the callback back through the saved hardware interrupt frame.
public __hardresume
__hardresume proc far
    push bp
    mov bp,sp
    push si
    push di
    mov ax,[bp+6]
    mov sp,word ptr DGROUP:saved_interrupt_sp
    pop bp
    pop di
    pop si
    pop ds
    pop es
    pop dx
    pop cx
    pop bx
    inc sp
    inc sp
    iret
    pop di
    pop si
    pop bp
    retf
__hardresume endp

; Return from a DOS critical error to the original caller and restore flags.
public __hardretn
__hardretn proc far
    push bp
    mov bp,sp
    push si
    push di
    xor ax,ax
    push ax
    push ax
    mov ax,54h
    push ax
    call _bdos
    add sp,6
    mov si,[bp+6]
    mov ax,word ptr DGROUP:saved_interrupt_sp
    add ax,18h
    mov sp,ax
    mov bp,ax
    pop ax
    cmp ah,38h
    jnc short flag_error
    cmp ah,0Fh
    jc short skip_update
    cmp ah,13h
    jna short set_failure
skip_update:
    cmp ah,16h
    jz short set_failure
    cmp ah,17h
    jz short set_failure
    cmp ah,23h
    jz short set_failure
    cmp ah,29h
    jnz short complete
set_failure:
    mov al,0FFh
    jmp short complete
flag_error:
    or byte ptr [bp+16h],1
    mov ax,si
complete:
    pop bx
    pop cx
    pop dx
    pop si
    pop di
    pop bp
    pop ds
    pop es
    iret
    pop di
    pop si
    pop bp
    retf
__hardretn endp
_TEXT ends
_BSS segment word public 'BSS'
saved_interrupt_sp dw ?
legacy_callback dd ?
extended_callback dd ?
extended_callback_flag dw ?
_BSS ends
end
