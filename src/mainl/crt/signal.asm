; Original Borland large-model signal subsystem: interrupt entry stubs,
; DOS interrupt vector registration, signal handler dispatch, raise/exit.
; Full original 16-bit CODE with named DATA and BSS, never byte arrays.
.8086
extrn __exit:far,__abort:far,_errno:word,_getvect:far,_setvect:far,___SignalPtr:dword
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _signal,_raise

; Hardware-facing interrupt trampoline; saves all registers then IRET.
signal_interrupt_0:
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
    mov ds, bp
    mov bp, sp
    sub sp, 4
    mov dx, word ptr [signal_handlers+10]
    mov ax, word ptr [signal_handlers+8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne loc_0029
    cmp ax, 1
    je loc_0066
loc_0029:
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je loc_003d
    cmp word ptr [bp - 2], -1
    jne loc_0047
    cmp word ptr [bp - 4], -1
    jne loc_0047
loc_003d:
    mov ax, 1
    push ax
    call __exit
    pop cx
loc_0047:
    mov word ptr [signal_handlers+10], 0
    mov word ptr [signal_handlers+8], 0
    push ss
    lea ax, [bp]
    push ax
    mov ax, 7fh
    push ax
    mov ax, 8
    push ax
    call dword ptr [bp - 4]
    add sp, 8
loc_0066:
    mov sp, bp
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

; Hardware-facing interrupt trampoline; saves all registers then IRET.
signal_interrupt_1:
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
    mov ds, bp
    mov bp, sp
    sub sp, 4
    mov dx, word ptr [signal_handlers+10]
    mov ax, word ptr [signal_handlers+8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne loc_009b
    cmp ax, 1
    je loc_00d8
loc_009b:
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je loc_00af
    cmp word ptr [bp - 2], -1
    jne loc_00b9
    cmp word ptr [bp - 4], -1
    jne loc_00b9
loc_00af:
    mov ax, 1
    push ax
    call __exit
    pop cx
loc_00b9:
    mov word ptr [signal_handlers+10], 0
    mov word ptr [signal_handlers+8], 0
    push ss
    lea ax, [bp]
    push ax
    mov ax, 7eh
    push ax
    mov ax, 8
    push ax
    call dword ptr [bp - 4]
    add sp, 8
loc_00d8:
    mov sp, bp
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

; Hardware-facing interrupt trampoline; saves all registers then IRET.
signal_interrupt_2:
    push ax
    push cx
    push dx
    push bx
    push sp
    push bp
    push si
    push di
    push ds
    push es
    mov bp,seg DGROUP
    mov ds, bp
    mov bp, sp
    sub sp, 4
    pushf
    mov dx, word ptr [signal_handlers+2]
    mov ax, word ptr [signal_handlers]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne loc_010f
    cmp ax, 1
    je loc_0154
loc_010f:
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je loc_0123
    cmp word ptr [bp - 2], -1
    jne loc_012d
    cmp word ptr [bp - 4], -1
    jne loc_012d
loc_0123:
    mov ax, 1
    push ax
    call __exit
    pop cx
loc_012d:
    mov word ptr [signal_handlers+2], 0
    mov word ptr [signal_handlers], 0
    push word ptr [saved_interrupt_vector+2]
    push word ptr [saved_interrupt_vector]
    mov ax, 23h
    push ax
    call _setvect
    mov ax, 2
    push ax
    call dword ptr [bp - 4]
    add sp, 8
loc_0154:
    popf
    clc
    mov sp, bp
    pop es
    pop ds
    pop di
    pop si
    pop bp
    pop bx
    pop bx
    pop dx
    pop cx
    pop ax
    retf
loc_0163:
    push bp
    mov bp, sp
    push si
    push di
    xor dx, dx
loc_016a:
    mov bx, dx
    mov al, byte ptr [bx+signal_interrupt_numbers]
    mov ah, 0
    cmp ax, word ptr [bp + 6]
    jne loc_017b
    mov ax, dx
    jmp short loc_0184
loc_017b:
    inc dx
    cmp dx, 6
    jl loc_016a
    mov ax, 0ffffh
loc_0184:
    pop di
    pop si
    pop bp
    retf

; Exported Borland far signal API.
_signal:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    cmp byte ptr [signal_armed], 0
    jne loc_01a8
    mov word ptr DGROUP:___SignalPtr+2,seg _signal
    mov word ptr DGROUP:___SignalPtr,offset _signal
    mov byte ptr [signal_armed], 1
loc_01a8:
    push word ptr [bp + 6]
    push cs
    call loc_0163
    pop cx
    mov word ptr [bp - 2], ax
    cmp ax, 0ffffh
    jne loc_01c7
    mov word ptr DGROUP:_errno,13h
    mov dx, 0ffffh
    mov ax, 0ffffh
    jmp near ptr loc_0264
loc_01c7:
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl
    mov dx, word ptr [bx+signal_handlers+2]
    mov ax, word ptr [bx+signal_handlers]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    mov bx, word ptr [bp - 2]
    shl bx, cl
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]
    mov word ptr [bx+signal_handlers+2], dx
    mov word ptr [bx+signal_handlers], ax
    cmp word ptr [bp + 6], 2
    jne loc_0231
    cmp byte ptr [signal_installed], 0
    jne loc_0212
    mov ax, 23h
    push ax
    call _getvect
    pop cx
    mov word ptr [saved_interrupt_vector+2], dx
    mov word ptr [saved_interrupt_vector], ax
    mov byte ptr [signal_installed], 1
loc_0212:
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    jne loc_0224
    push word ptr [saved_interrupt_vector+2]
    push word ptr [saved_interrupt_vector]
    jmp short loc_022c
loc_0224:
    mov ax,seg signal_interrupt_0
    push ax
    mov ax,offset signal_interrupt_2
    push ax
loc_022c:
    mov ax, 23h
    jmp short loc_0255
loc_0231:
    cmp word ptr [bp + 6], 8
    jne loc_025e
    mov ax,seg signal_interrupt_0
    push ax
    mov ax,offset signal_interrupt_0
    push ax
    xor ax, ax
    push ax
    call _setvect
    add sp, 6
    mov ax,seg signal_interrupt_0
    push ax
    mov ax,offset signal_interrupt_1
    push ax
    mov ax, 4
loc_0255:
    push ax
    call _setvect
    add sp, 6
loc_025e:
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
loc_0264:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Exported Borland far signal API.
_raise:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push word ptr [bp + 6]
    push cs
    call loc_0163
    pop cx
    mov word ptr [bp - 2], ax
    cmp ax, 0ffffh
    jne loc_0287
    mov ax, 1
    jmp short loc_02fb
loc_0287:
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl
    mov dx, word ptr [bx+signal_handlers+2]
    mov ax, word ptr [bx+signal_handlers]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or dx, dx
    jne loc_02a5
    cmp ax, 1
    je loc_02f9
loc_02a5:
    mov ax, word ptr [bp - 6]
    or ax, word ptr [bp - 4]
    jne loc_02d4
    mov ax, word ptr [bp + 6]
    cmp ax, 2
    je loc_02bf
    cmp ax, 16h
    jne loc_02c8
    call __abort
loc_02bf:
    xor ax, ax
    int 23h
    mov ax, 4c03h
    int 21h
loc_02c8:
    mov ax, 1
    push ax
    call __exit
    pop cx
    jmp short loc_02f9
loc_02d4:
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl
    mov word ptr [bx+signal_handlers+2], 0
    mov word ptr [bx+signal_handlers], 0
    mov bx, word ptr [bp - 2]
    mov al, byte ptr [bx+signal_interrupt_numbers+6]
    mov ah, 0
    push ax
    push word ptr [bp + 6]
    call dword ptr [bp - 6]
    pop cx
    pop cx
loc_02f9:
    xor ax, ax
loc_02fb:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends

; Active vector setup and six signal handler slots; original static 38 bytes.
_DATA segment word public 'DATA'
signal_installed db 0
signal_armed db 0
signal_handlers dw 0,0,0,0,0,0,0,0,0,0,0,0
signal_interrupt_numbers db 2,4,8,11,15,22,0,21
signal_os_state dw 0b8ch,0
_DATA ends
_BSS segment word public 'BSS'
saved_interrupt_vector dd ?
_BSS ends
end
