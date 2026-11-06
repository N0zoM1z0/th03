; Shared signal runtime: complete original CODE/DATA/BSS, ABI and ordered fields.
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
DGROUP group _BSS,_DATA
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _raise,_signal

; Hardware-facing interrupt trampoline; saves all registers then IRET.
; Preserve original interrupt frames, far cdecl APIs and unchecked handler state.
; Ordinary spans preserve native record chronology; all initialized bytes are written once.
; Bind real code labels before scheduling their instruction spans.
org 0
divide_interrupt label near
org 41
divide_check_default label near
org 61
divide_exit_default label near
org 71
divide_dispatch label near
org 102
divide_return label near
org 114
overflow_interrupt label near
org 155
overflow_check_default label near
org 175
overflow_exit_default label near
org 185
overflow_dispatch label near
org 216
overflow_return label near
org 228
break_interrupt label near
org 271
break_check_default label near
org 291
break_exit_default label near
org 301
break_dispatch label near
org 340
break_return label near
org 355
signal_index label near
org 362
index_next label near
org 379
index_advance label near
org 388
index_done label near
org 392
_signal label far
org 424
signal_registered label near
org 455
signal_valid label near
org 530
break_vector_saved label near
org 548
install_break_vector label near
org 556
break_vector_number label near
org 561
check_floating_signal label near
org 597
set_signal_vector label near
org 606
previous_handler label near
org 612
signal_done label near
org 618
_raise label far
org 647
raise_valid label near
org 677
raise_check_default label near
org 703
raise_break_default label near
org 712
raise_exit_default label near
org 724
raise_dispatch label near
org 761
raise_success label near
org 763
raise_done label near

; Original CODE 0..8.
org 0
    push ax
    push bx
    push cx
    push dx
    push es
    push ds
    push si
    push di
    push bp

; Original CODE 9..18.
org 9
    mov bp,seg DGROUP
    mov ds, bp
    mov bp, sp
    sub sp, 4

; Original CODE 19..22.
org 19
    mov dx, word ptr [signal_handlers+10]

; Original CODE 23..64.
org 23
    mov ax, word ptr [signal_handlers+8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne divide_check_default
    cmp ax, word ptr 1
    je divide_return
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je divide_exit_default
    cmp word ptr [bp - 2], -1
    jne divide_dispatch
    cmp word ptr [bp - 4], -1
    jne divide_dispatch
    mov ax, 1
    push ax

; Original CODE 71..76.
org 71
    mov word ptr [signal_handlers+10], 0

; Original CODE 77..122.
org 77
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
    push ax
    push bx
    push cx
    push dx
    push es
    push ds
    push si
    push di
    push bp

; Original CODE 123..132.
org 123
    mov bp,seg DGROUP
    mov ds, bp
    mov bp, sp
    sub sp, 4

; Original CODE 133..136.
org 133
    mov dx, word ptr [signal_handlers+10]

; Original CODE 137..178.
org 137
    mov ax, word ptr [signal_handlers+8]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne overflow_check_default
    cmp ax, word ptr 1
    je overflow_return
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je overflow_exit_default
    cmp word ptr [bp - 2], -1
    jne overflow_dispatch
    cmp word ptr [bp - 4], -1
    jne overflow_dispatch
    mov ax, 1
    push ax

; Original CODE 185..190.
org 185
    mov word ptr [signal_handlers+10], 0

; Original CODE 191..237.
org 191
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

; Original CODE 238..248.
org 238
    mov bp,seg DGROUP
    mov ds, bp
    mov bp, sp
    sub sp, 4
    pushf

; Original CODE 249..252.
org 249
    mov dx, word ptr [signal_handlers+2]

; Original CODE 253..294.
org 253
    mov ax, word ptr [signal_handlers]
    mov word ptr [bp - 2], dx
    mov word ptr [bp - 4], ax
    or dx, dx
    jne break_check_default
    cmp ax, word ptr 1
    je break_return
    mov ax, word ptr [bp - 4]
    or ax, word ptr [bp - 2]
    je break_exit_default
    cmp word ptr [bp - 2], -1
    jne break_dispatch
    cmp word ptr [bp - 4], -1
    jne break_dispatch
    mov ax, 1
    push ax

; Original CODE 301..306.
org 301
    mov word ptr [signal_handlers+2], 0

; Original CODE 307..312.
org 307
    mov word ptr [signal_handlers], 0

; Original CODE 364..399.
org 364
    mov al, byte ptr [bx+signal_interrupt_numbers]
    mov ah, 0
    cmp ax, word ptr [bp + 6]
    jne index_advance
    mov ax, dx
    jmp short index_done
    inc dx
    cmp dx, 6
    jl index_next
    mov ax, 0ffffh
    pop di
    pop si
    pop bp
    retf
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di

; Original CODE 400..406.
org 400
    cmp byte ptr [signal_armed], 0
    jne signal_registered

; Original CODE 419..439.
org 419
    mov byte ptr [signal_armed], 1
    push word ptr [bp + 6]
    push cs
    call signal_index
    pop cx
    mov word ptr [bp - 2], ax
    cmp ax, word ptr 0ffffh
    jne signal_valid

; Original CODE 462..465.
org 462
    mov dx, word ptr [bx+signal_handlers+2]

; Original CODE 466..486.
org 466
    mov ax, word ptr [bx+signal_handlers]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    mov bx, word ptr [bp - 2]
    shl bx, cl
    mov dx, word ptr [bp + 0ah]
    mov ax, word ptr [bp + 8]

; Original CODE 65..70.
org 65
    call __exit
    pop cx

; Original CODE 179..184.
org 179
    call __exit
    pop cx

; Original CODE 295..300.
org 295
    call __exit
    pop cx

; Original CODE 313..316.
org 313
    push word ptr [saved_interrupt_vector+2]

; Original CODE 317..324.
org 317
    push word ptr [saved_interrupt_vector]
    mov ax, 23h
    push ax

; Original CODE 325..363.
org 325
    call _setvect
    mov ax, 2
    push ax
    call dword ptr [bp - 4]
    add sp, 8
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
    push bp
    mov bp, sp
    push si
    push di
    xor dx, dx
    mov bx, dx

; Original CODE 407..412.
org 407
    mov word ptr DGROUP:___SignalPtr+2,seg _signal

; Original CODE 413..418.
org 413
    mov word ptr DGROUP:___SignalPtr,offset _signal

; Original CODE 440..461.
org 440
    mov word ptr DGROUP:_errno,13h
    mov dx, 0ffffh
    mov ax, 0ffffh
    jmp near ptr signal_done
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl

; Original CODE 512..517.
org 512
    call _getvect
    pop cx

; Original CODE 518..521.
org 518
    mov word ptr [saved_interrupt_vector+2], dx

; Original CODE 522..524.
org 522
    mov word ptr [saved_interrupt_vector], ax

; Original CODE 538..541.
org 538
    push word ptr [saved_interrupt_vector+2]

; Original CODE 542..547.
org 542
    push word ptr [saved_interrupt_vector]
    jmp short break_vector_number

; Original CODE 578..585.
org 578
    call _setvect
    add sp, 6

; Original CODE 598..653.
org 598
    call _setvect
    add sp, 6
    mov dx, word ptr [bp - 4]
    mov ax, word ptr [bp - 6]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    push word ptr [bp + 6]
    push cs
    call signal_index
    pop cx
    mov word ptr [bp - 2], ax
    cmp ax, word ptr 0ffffh
    jne raise_valid
    mov ax, 1
    jmp short raise_done
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl

; Original CODE 698..715.
org 698
    call __abort
    xor ax, ax
    int 23h
    mov ax, 4c03h
    int 21h
    mov ax, 1
    push ax

; Original CODE 716..730.
org 716
    call __exit
    pop cx
    jmp short raise_success
    mov bx, word ptr [bp - 2]
    mov cl, 2
    shl bx, cl

; Original CODE 487..490.
org 487
    mov word ptr [bx+signal_handlers+2], dx

; Original CODE 491..500.
org 491
    mov word ptr [bx+signal_handlers], ax
    cmp word ptr [bp + 6], 2
    jne check_floating_signal

; Original CODE 501..511.
org 501
    cmp byte ptr [signal_installed], 0
    jne break_vector_saved
    mov ax, 23h
    push ax

; Original CODE 525..537.
org 525
    mov byte ptr [signal_installed], 1
    mov ax, word ptr [bp + 8]
    or ax, word ptr [bp + 0ah]
    jne install_break_vector

; Original CODE 548..551.
org 548
    mov ax,seg divide_interrupt
    push ax

; Original CODE 552..566.
org 552
    mov ax,offset break_interrupt
    push ax
    mov ax, 23h
    jmp short set_signal_vector
    cmp word ptr [bp + 6], 8
    jne previous_handler

; Original CODE 567..570.
org 567
    mov ax,seg divide_interrupt
    push ax

; Original CODE 571..577.
org 571
    mov ax,offset divide_interrupt
    push ax
    xor ax, ax
    push ax

; Original CODE 586..589.
org 586
    mov ax,seg divide_interrupt
    push ax

; Original CODE 590..597.
org 590
    mov ax,offset overflow_interrupt
    push ax
    mov ax, 4
    push ax

; Original CODE 654..657.
org 654
    mov dx, word ptr [bx+signal_handlers+2]

; Original CODE 658..697.
org 658
    mov ax, word ptr [bx+signal_handlers]
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 6], ax
    or dx, dx
    jne raise_check_default
    cmp ax, word ptr 1
    je raise_success
    mov ax, word ptr [bp - 6]
    or ax, word ptr [bp - 4]
    jne raise_dispatch
    mov ax, word ptr [bp + 6]
    cmp ax, word ptr 2
    je raise_break_default
    cmp ax, word ptr 16h
    jne raise_exit_default

; Original CODE 731..736.
org 731
    mov word ptr [bx+signal_handlers+2], 0

; Original CODE 737..745.
org 737
    mov word ptr [bx+signal_handlers], 0
    mov bx, word ptr [bp - 2]

; Original CODE 746..768.
org 746
    mov al, byte ptr [bx+signal_interrupt_numbers+6]
    mov ah, 0
    push ax
    push word ptr [bp + 6]
    call dword ptr [bp - 6]
    pop cx
    pop cx
    xor ax, ax
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
