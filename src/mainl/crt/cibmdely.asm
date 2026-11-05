; Borland IBM-compatible conio delay: native PIT counter capture,
; runtime calibration and original six-byte CRT INITDATA registration.
.8086
extrn ___conio_type:word
extrn N_LXMUL@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
_INIT_ segment word public 'INITDATA'
_INIT_ ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP

pit_io_sync proc near
    push si
    push di
    pop di
    pop si
    ret
pit_io_sync endp

read_ibm_pit_count proc near
    push si
    push di
    pushf
    cli
    mov al,0
    out 43h,al
    call near ptr pit_io_sync
    in al,40h
    mov bl,al
    call near ptr pit_io_sync
    in al,40h
    mov bh,al
    not bx
    popf
    mov ax,bx
    pop di
    pop si
    ret
read_ibm_pit_count endp

init_ibm_pit_calibration proc far
    push bp
    mov bp,sp
    sub sp,2
    push si
    push di
    cmp word ptr DGROUP:___conio_type,1
    jne short init_done
    mov word ptr [bp-2],0
sample_pit:
    call near ptr read_ibm_pit_count
    test al,1
    jne short test_attempt_limit
    mov word ptr DGROUP:pit_calibration_hi,0
    mov word ptr DGROUP:pit_calibration_lo,04a9h
    jmp short init_done
test_attempt_limit:
    inc word ptr [bp-2]
    cmp word ptr [bp-2],64h
    jl short sample_pit
init_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
init_ibm_pit_calibration endp

public ___ibm_delay
___ibm_delay proc far
    push bp
    mov bp,sp
    sub sp,6
    push si
    push di
    call near ptr read_ibm_pit_count
    mov word ptr [bp-6],ax
    xor dx,dx
    mov bx,[bp+6]
    xor cx,cx
    push ax
    push dx
    mov dx,word ptr DGROUP:pit_calibration_hi
    mov ax,word ptr DGROUP:pit_calibration_lo
    call N_LXMUL@
    pop bx
    pop cx
    add cx,ax
    adc bx,dx
    mov word ptr [bp-2],bx
    mov word ptr [bp-4],cx
    jmp short check_remaining_time
handle_timer_rollover:
    cmp bx,word ptr [bp-6]
    jae short save_new_time
    cmp word ptr [bp-2],1
    ja short decrease_target
    jb short delay_done
    cmp word ptr [bp-4],0
    jb short delay_done
decrease_target:
    dec word ptr [bp-2]
save_new_time:
    mov word ptr [bp-6],bx
check_remaining_time:
    call near ptr read_ibm_pit_count
    mov bx,ax
    xor dx,dx
    cmp dx,word ptr [bp-2]
    jb short handle_timer_rollover
    jne short delay_done
    cmp ax,word ptr [bp-4]
    jb short handle_timer_rollover
delay_done:
    pop di
    pop si
    mov sp,bp
    pop bp
    retf
___ibm_delay endp
_TEXT ends

_DATA segment word public 'DATA'
pit_calibration_lo dw 0952h
pit_calibration_hi dw 0
_DATA ends

_INIT_ segment word public 'INITDATA'
    dw 1001h
    dd init_ibm_pit_calibration
_INIT_ ends
end
