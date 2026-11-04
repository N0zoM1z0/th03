; Original Japanese PC-98 serial communication driver and ISR.
; Natural 16-bit 8086 interrupts, polling, buffer rings and ports.
; Ten original API functions; no target machine CODE byte arrays.
.8086
extrn _getvect:far,_setvect:far,___nec_delay:far
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _pc98cominit,_pc98comterm,_pc98comsend,_pc98comrecv,_pc98comgetstat,_pc98comsetstat,_pc98comchkbuf,_pc98comsendbreak,_pc98comreset,_pc98comcheckbaud

; Original serial I/O interrupt handler.
serial_interrupt_receive:
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
    in al, 35h
    out 5fh, al
    and al, 0fah
    out 35h, al
    in al, 32h
    out 5fh, al
    out 5fh, al
    mov dh, al
    test al, 2
    jne loc_0025
    jmp near ptr loc_00d7
loc_0025:
    in al, 30h
    sti
    mov dl, al
    test dh, 38h
    je loc_0038
    mov al, byte ptr DGROUP:serial_state_47
    out 32h, al
    out 5fh, al
    out 5fh, al
loc_0038:
    test dh, 40h
    je loc_0045
    mov byte ptr DGROUP:serial_state_43, 1
    jmp near ptr loc_00d7
loc_0045:
    cli
    xor al, al
    xchg byte ptr DGROUP:serial_state_43, al
    mov byte ptr DGROUP:serial_state_44, al
    sti
    xor ax, ax
    cmp byte ptr DGROUP:serial_state_45, 0
    je loc_0073
    cmp dl, 11h
    je loc_0065
    cmp dl, 13h
    jne loc_0073
    inc al
loc_0065:
    mov byte ptr DGROUP:serial_state_38, al
    jmp short loc_00d7
    nop
loc_006b:
    mov byte ptr DGROUP:serial_state_19, 2
    jmp short loc_00d7
    nop
loc_0073:
    mov cx, word ptr DGROUP:serial_state_16
    cmp cx, word ptr DGROUP:serial_state_06
    jae loc_006b
    mov es, word ptr DGROUP:serial_state_00
    mov bx, word ptr DGROUP:serial_state_12
    mov word ptr es:[bx], dx
    inc bx
    inc bx
    inc cx
    mov word ptr DGROUP:serial_state_16, cx
    mov ax, word ptr DGROUP:serial_state_02
    cmp bx, word ptr DGROUP:serial_state_04
    je loc_0099
    xchg bx, ax
loc_0099:
    mov word ptr DGROUP:serial_state_12, ax
    cli
    cmp cx, word ptr DGROUP:serial_state_08
    jbe loc_00d7
    cmp byte ptr DGROUP:serial_state_18, 0
    jne loc_00d7
    cmp byte ptr DGROUP:serial_state_45, 0
    jne loc_00cf
    cmp byte ptr DGROUP:serial_state_46, 0
    jne loc_00ba
    jmp short loc_00d7
loc_00ba:
    mov al, byte ptr DGROUP:serial_state_47
    and al, 0dfh
    out 32h, al
    mov byte ptr DGROUP:serial_state_47, al
    out 5fh, al
    out 5fh, al
    mov al, 1
    mov byte ptr DGROUP:serial_state_18, al
    jmp short loc_00d7
loc_00cf:
    mov al, 1
    mov byte ptr DGROUP:serial_state_41, al
    mov byte ptr DGROUP:serial_state_42, al
loc_00d7:
    sti
    xor ax, ax
    cmp byte ptr DGROUP:serial_state_42, al
    je loc_013a
    test dh, 1
    je loc_013a
    cmp byte ptr DGROUP:serial_state_38, al
    jne loc_013a
    cmp byte ptr DGROUP:serial_state_41, al
    je loc_0100
    mov al, 13h
    out 30h, al
    xor al, al
    mov byte ptr DGROUP:serial_state_41, al
    inc ax
    mov byte ptr DGROUP:serial_state_18, al
    jmp short loc_013a
loc_0100:
    cmp byte ptr DGROUP:serial_state_40, al
    je loc_0114
    mov al, 11h
    out 30h, al
    xor al, al
    mov byte ptr DGROUP:serial_state_40, al
    mov byte ptr DGROUP:serial_state_18, al
    jmp short loc_013a
loc_0114:
    cmp word ptr DGROUP:serial_state_36, 0
    je loc_013a
    mov es, word ptr DGROUP:serial_state_20
    mov bx, word ptr DGROUP:serial_state_34
    mov al, byte ptr es:[bx]
    out 30h, al
    inc bx
    dec word ptr DGROUP:serial_state_36
    mov ax, word ptr DGROUP:serial_state_22
    cmp bx, word ptr DGROUP:serial_state_24
    je loc_0137
    xchg bx, ax
loc_0137:
    mov word ptr DGROUP:serial_state_34, ax
loc_013a:
    cli
    mov al, 1
    out 37h, al
    out 5fh, al
    xor ax, ax
    cmp byte ptr DGROUP:serial_state_41, al
    jne loc_015b
    cmp byte ptr DGROUP:serial_state_40, al
    jne loc_015b
    cmp word ptr DGROUP:serial_state_36, ax
    je loc_0161
    cmp byte ptr DGROUP:serial_state_38, al
    jne loc_0161
loc_015b:
    mov al, 5
    out 37h, al
    mov al, 1
loc_0161:
    mov byte ptr DGROUP:serial_state_42, al
    mov al, 20h
    out 0, al
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
loc_0172:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 4]
    mov bx, dx
    mov ax, word ptr [bx + 2]
    mov word ptr [bx + 0ch], ax
    mov word ptr [bx + 0eh], ax
    mov word ptr [bx + 10h], 0
    mov byte ptr [bx + 12h], 0
    mov byte ptr [bx + 13h], 0
    pop di
    pop si
    pop bp
    ret 2

; Original serial I/O interrupt handler.
serial_interrupt_transmit:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov cx, word ptr [bp + 6]
    mov bx, cx
    mov ax, word ptr [bp + 4]
    mov word ptr [bx + 6], ax
    cwd
    sub ax, dx
    sar ax, 1
    push ax
    mov ax, word ptr [bp + 4]
    mov bx, 4
    cwd
    idiv bx
    mov word ptr [bp - 2], ax
    pop dx
    add dx, ax
    mov bx, cx
    mov word ptr [bx + 8], dx
    mov word ptr [bx + 0ah], ax
    push bx
    call loc_0172
    pop di
    pop si
    mov sp, bp
    pop bp
    ret 4

; Original selected PC-98 serial API at CODE+468.
_pc98cominit:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    xor ax, ax
    mov es, ax
    test byte ptr es:[501h], 80h
    je loc_01ec
    mov al, 1
    jmp short loc_01ee
loc_01ec:
    mov al, 0
loc_01ee:
    mov byte ptr [bp - 1], al
    les bx,dword ptr [bp + 6]
    cmp word ptr es:[bx], 16h
    jae loc_0224
    cmp byte ptr es:[bx + 2], 3
    ja loc_0224
    cmp byte ptr es:[bx + 3], 2
    ja loc_0224
    cmp byte ptr es:[bx + 4], 2
    ja loc_0224
    cmp byte ptr es:[bx + 5], 2
    ja loc_0224
    cmp word ptr es:[bx + 6], 2
    jb loc_0224
    cmp word ptr es:[bx + 0ch], 1
    jae loc_022a
loc_0224:
    mov ax, 0ffffh
    jmp near ptr loc_0395
loc_022a:
    les bx,dword ptr [bp + 6]
    mov al, byte ptr es:[bx + 2]
    mov ah, 0
    mov bx, ax
    mov al, byte ptr DGROUP:pc98_mode_controls[bx]
    mov bx, word ptr [bp + 6]
    mov dl, byte ptr es:[bx + 3]
    mov dh, 0
    mov bx, dx
    or al, byte ptr DGROUP:pc98_speed_options[bx]
    mov bx, word ptr [bp + 6]
    mov dl, byte ptr es:[bx + 4]
    mov dh, 0
    mov bx, dx
    or al, byte ptr DGROUP:pc98_speed_selector[bx]
    mov byte ptr [bp - 2], al
    mov al, byte ptr [bp - 1]
    cbw
    push ax
    mov ax, 16h
    pop dx
    imul dx
    mov bx, word ptr [bp + 6]
    mov dx, word ptr es:[bx]
    add dx, dx
    add ax, dx
    mov bx, ax
    mov ax, word ptr DGROUP:pc98_baud_divisors[bx]
    mov word ptr [bp - 4], ax
    mov bx, word ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ah]
    mov word ptr DGROUP:serial_state_00, ax
    mov ax, word ptr es:[bx + 10h]
    mov word ptr DGROUP:serial_state_20, ax
    mov ax, word ptr es:[bx + 8]
    mov word ptr DGROUP:serial_state_02, ax
    mov ax, word ptr es:[bx + 0eh]
    mov word ptr DGROUP:serial_state_22, ax
    add bx, 6
    mov word ptr [bp - 6], bx
    mov ax, word ptr es:[bx]
    shr ax, 1
    add ax, ax
    add ax, word ptr DGROUP:serial_state_02
    mov word ptr DGROUP:serial_state_04, ax
    mov bx, word ptr [bp + 6]
    mov ax, word ptr es:[bx + 0ch]
    add ax, word ptr DGROUP:serial_state_22
    mov word ptr DGROUP:serial_state_24, ax
    mov ax,offset DGROUP:serial_state_00
    push ax
    mov bx, word ptr [bp - 6]
    mov ax, word ptr es:[bx]
    shr ax, 1
    push ax
    call serial_interrupt_transmit
    mov ax,offset DGROUP:serial_state_20
    push ax
    les bx,dword ptr [bp + 6]
    push word ptr es:[bx + 0ch]
    call serial_interrupt_transmit
    mov byte ptr DGROUP:serial_state_43, 0
    mov byte ptr DGROUP:serial_state_44, 0
    mov byte ptr DGROUP:serial_state_42, 0
    mov byte ptr DGROUP:serial_state_40, 0
    mov byte ptr DGROUP:serial_state_41, 0
    mov byte ptr DGROUP:serial_state_45, 0
    mov byte ptr DGROUP:serial_state_46, 0
    les bx,dword ptr [bp + 6]
    cmp byte ptr es:[bx + 5], 1
    jne loc_030b
    mov byte ptr DGROUP:serial_state_45, 1
    jmp short loc_031a
loc_030b:
    les bx,dword ptr [bp + 6]
    cmp byte ptr es:[bx + 5], 2
    jne loc_031a
    mov byte ptr DGROUP:serial_state_46, 1
loc_031a:
    mov ax, 0ch
    push ax
    call _getvect
    pop cx
    mov word ptr DGROUP:serial_state_52, dx
    mov word ptr DGROUP:serial_state_50, ax
    mov ax,seg serial_interrupt_receive
    push ax
    mov ax,offset serial_interrupt_receive
    push ax
    mov ax, 0ch
    push ax
    call _setvect
    add sp, 6
    jmp short loc_0348
loc_0341:
    out 32h, al
    out 5fh, al
    out 5fh, al
    ret
loc_0348:
    pushf
    cli
    mov cx, word ptr [bp - 4]
    mov al, 0b6h
    out 77h, al
    mov al, cl
    out 75h, al
    mov al, ch
    out 75h, al
    mov al, 0
    call loc_0341
    call loc_0341
    call loc_0341
    mov al, 40h
    call loc_0341
    mov al, byte ptr [bp - 2]
    call loc_0341
    mov al, 37h
    call loc_0341
    mov byte ptr DGROUP:serial_state_47, al
    in al, 35h
    out 5fh, al
    mov byte ptr DGROUP:serial_state_49, al
    and al, 0fdh
    or al, 5
    out 35h, al
    in al, 2
    mov byte ptr DGROUP:serial_state_48, al
    and al, 0efh
    out 2, al
    mov byte ptr DGROUP:pc98_mode_bytes, 1
    popf
    xor ax, ax
loc_0395:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original selected PC-98 serial API at CODE+923.
_pc98comterm:
    push si
    push di
    cmp byte ptr DGROUP:pc98_mode_bytes, 0
    jne loc_03a9
    mov ax, 100h
    jmp short loc_03e3
loc_03a9:
    pushf
    cli
    in al, 2
    mov ah, byte ptr DGROUP:serial_state_48
    and ax, 0ffefh
    or al, ah
    out 2, al
    in al, 35h
    out 5fh, al
    mov ah, byte ptr DGROUP:serial_state_49
    and ax, 0fff8h
    or al, ah
    out 35h, al
    popf
    push word ptr DGROUP:serial_state_52
    push word ptr DGROUP:serial_state_50
    mov ax, 0ch
    push ax
    call _setvect
    add sp, 6
    mov byte ptr DGROUP:pc98_mode_bytes, 0
    xor ax, ax
loc_03e3:
    pop di
    pop si
    retf

; Original selected PC-98 serial API at CODE+998.
_pc98comsend:
    push bp
    mov bp, sp
    push si
    push di
    pushf
    cli
    mov ax, 0ff00h
    mov cx, word ptr DGROUP:serial_state_36
    cmp cx, word ptr DGROUP:serial_state_26
    jae loc_0426
    mov al, byte ptr [bp + 6]
    mov es, word ptr DGROUP:serial_state_20
    mov bx, word ptr DGROUP:serial_state_32
    mov byte ptr es:[bx], al
    inc bx
    inc cx
    mov word ptr DGROUP:serial_state_36, cx
    mov ax, word ptr DGROUP:serial_state_22
    cmp bx, word ptr DGROUP:serial_state_24
    je loc_0418
    xchg bx, ax
loc_0418:
    mov word ptr DGROUP:serial_state_32, ax
    mov al, 5
    out 37h, al
    mov ax, 1
    mov byte ptr DGROUP:serial_state_42, al
    dec ax
loc_0426:
    popf
    pop di
    pop si
    pop bp
    retf

; Original selected PC-98 serial API at CODE+1067.
_pc98comrecv:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov word ptr [bp - 2], 0fe00h
    mov es, word ptr DGROUP:serial_state_00
    pushf
    cli
    mov cx, word ptr DGROUP:serial_state_16
    jcxz loc_04ae
    mov bx, word ptr DGROUP:serial_state_14
    mov ax, word ptr es:[bx]
    mov dx, bx
    les bx,dword ptr [bp + 6]
    mov byte ptr es:[bx], al
    mov byte ptr [bp - 2], ah
    mov byte ptr [bp - 1], 0
    inc dx
    inc dx
    dec cx
    mov ax, word ptr DGROUP:serial_state_02
    cmp dx, word ptr DGROUP:serial_state_04
    je loc_0467
    xchg dx, ax
loc_0467:
    mov word ptr DGROUP:serial_state_14, ax
    mov word ptr DGROUP:serial_state_16, cx
    cmp byte ptr DGROUP:serial_state_18, 0
    je loc_04ae
    cmp cx, word ptr DGROUP:serial_state_10
    ja loc_04ae
    cmp byte ptr DGROUP:serial_state_45, 0
    jne loc_04a0
    cmp byte ptr DGROUP:serial_state_46, 0
    jne loc_048b
    jmp short loc_04ae
loc_048b:
    mov al, byte ptr DGROUP:serial_state_47
    or al, 20h
    out 32h, al
    mov byte ptr DGROUP:serial_state_47, al
    out 5fh, al
    out 5fh, al
    xor al, al
    mov byte ptr DGROUP:serial_state_18, al
    jmp short loc_04ae
loc_04a0:
    mov al, 1
    mov byte ptr DGROUP:serial_state_40, al
    mov byte ptr DGROUP:serial_state_42, al
    mov al, 5
    out 37h, al
    out 5fh, al
loc_04ae:
    popf
    mov ax, word ptr [bp - 2]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original selected PC-98 serial API at CODE+1208.
_pc98comgetstat:
    push bp
    mov bp, sp
    push si
    push di
    pushf
    cli
    in al, 32h
    out 5fh, al
    out 5fh, al
    mov ah, al
    in al, 33h
    out 5fh, al
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    xor ax, ax
    xchg byte ptr DGROUP:serial_state_19, ah
    popf
    pop di
    pop si
    pop bp
    retf

; Original selected PC-98 serial API at CODE+1244.
_pc98comsetstat:
    push bp
    mov bp, sp
    push si
    push di
    pushf
    cli
    mov al, byte ptr [bp + 6]
    mov byte ptr DGROUP:serial_state_47, al
    call loc_0341
    popf
    xor ax, ax
    pop di
    pop si
    pop bp
    retf

; Original selected PC-98 serial API at CODE+1267.
_pc98comchkbuf:
    push bp
    mov bp, sp
    push si
    push di
    pushf
    cli
    mov ax, word ptr DGROUP:serial_state_16
    mov dx, word ptr DGROUP:serial_state_36
    mov cl, byte ptr DGROUP:serial_state_18
    mov ch, byte ptr DGROUP:serial_state_38
    popf
    les bx,dword ptr [bp + 6]
    mov word ptr es:[bx], ax
    mov word ptr es:[bx + 4], dx
    xor ax, ax
    xchg al, ch
    mov word ptr es:[bx + 2], cx
    mov word ptr es:[bx + 6], ax
    xor ax, ax
    xchg byte ptr DGROUP:serial_state_19, ah
    pop di
    pop si
    pop bp
    retf

; Original selected PC-98 serial API at CODE+1322.
_pc98comsendbreak:
    push si
    push di
    pushf
    cli
    mov al, byte ptr DGROUP:serial_state_47
    or al, 8
    mov byte ptr DGROUP:serial_state_47, al
    call loc_0341
    popf
    mov ax, 12ch
    push ax
    call ___nec_delay
    pop cx
    pushf
    cli
    mov al, byte ptr DGROUP:serial_state_47
    and al, 0f7h
    mov byte ptr DGROUP:serial_state_47, al
    call loc_0341
    popf
    xor ax, ax
    pop di
    pop si
    retf

; Original selected PC-98 serial API at CODE+1367.
_pc98comreset:
    push si
    push di
    pushf
    cli
    mov ax,offset DGROUP:serial_state_20
    push ax
    call loc_0172
    mov ax,offset DGROUP:serial_state_00
    push ax
    call loc_0172
    mov byte ptr DGROUP:serial_state_43, 0
    mov byte ptr DGROUP:serial_state_44, 0
    mov byte ptr DGROUP:serial_state_42, 0
    mov byte ptr DGROUP:serial_state_40, 0
    mov byte ptr DGROUP:serial_state_41, 0
    mov al, byte ptr DGROUP:serial_state_47
    call loc_0341
    popf
    xor ax, ax
    pop di
    pop si
    retf

; Original selected PC-98 serial API at CODE+1422.
_pc98comcheckbaud:
    push bp
    mov bp, sp
    push si
    push di
    mov dx, word ptr [bp + 6]
    mov bx, 7
    xor ax, ax
    mov es, ax
    test byte ptr es:[501h], 80h
    je loc_05a8
    mov bx, 8
loc_05a8:
    or dx, dx
    jl loc_05b5
    cmp dx, bx
    jg loc_05b5
    mov ax, 1
    jmp short loc_05b7
loc_05b5:
    xor ax, ax
loc_05b7:
    pop di
    pop si
    pop bp
    retf
_TEXT ends

; Original selected PC-98 serial mode / baud tables.
_DATA segment word public 'DATA'
pc98_mode_bytes db 0
pc98_mode_controls db 2,6,10,14
pc98_speed_selector db 0,48,16
pc98_speed_options db 64,128,192
pc98_baud_divisors label word
    dw 2048
    dw 1024
    dw 512
    dw 256
    dw 128
    dw 64
    dw 32
    dw 16
    dw 8
    dw 4
    dw 2
    dw 1664
    dw 832
    dw 416
    dw 208
    dw 104
    dw 52
    dw 26
    dw 13
    dw 6
    dw 3
    dw 2
_DATA ends

; Serial interrupt registers/ring state, actual uninitialized BSS.
_BSS segment word public 'BSS'
assume cs:nothing
serial_state_00:
    db 2 dup (?) ; original state bytes 0..1
serial_state_02:
    db 2 dup (?) ; original state bytes 2..3
serial_state_04:
    db 2 dup (?) ; original state bytes 4..5
serial_state_06:
    db 2 dup (?) ; original state bytes 6..7
serial_state_08:
    db 2 dup (?) ; original state bytes 8..9
serial_state_10:
    db 2 dup (?) ; original state bytes 10..11
serial_state_12:
    db 2 dup (?) ; original state bytes 12..13
serial_state_14:
    db 2 dup (?) ; original state bytes 14..15
serial_state_16:
    db 2 dup (?) ; original state bytes 16..17
serial_state_18:
    db 1 dup (?) ; original state bytes 18..18
serial_state_19:
    db 1 dup (?) ; original state bytes 19..19
serial_state_20:
    db 2 dup (?) ; original state bytes 20..21
serial_state_22:
    db 2 dup (?) ; original state bytes 22..23
serial_state_24:
    db 2 dup (?) ; original state bytes 24..25
serial_state_26:
    db 6 dup (?) ; original state bytes 26..31
serial_state_32:
    db 2 dup (?) ; original state bytes 32..33
serial_state_34:
    db 2 dup (?) ; original state bytes 34..35
serial_state_36:
    db 2 dup (?) ; original state bytes 36..37
serial_state_38:
    db 2 dup (?) ; original state bytes 38..39
serial_state_40:
    db 1 dup (?) ; original state bytes 40..40
serial_state_41:
    db 1 dup (?) ; original state bytes 41..41
serial_state_42:
    db 1 dup (?) ; original state bytes 42..42
serial_state_43:
    db 1 dup (?) ; original state bytes 43..43
serial_state_44:
    db 1 dup (?) ; original state bytes 44..44
serial_state_45:
    db 1 dup (?) ; original state bytes 45..45
serial_state_46:
    db 1 dup (?) ; original state bytes 46..46
serial_state_47:
    db 1 dup (?) ; original state bytes 47..47
serial_state_48:
    db 1 dup (?) ; original state bytes 48..48
serial_state_49:
    db 1 dup (?) ; original state bytes 49..49
serial_state_50:
    db 2 dup (?) ; original state bytes 50..51
serial_state_52:
    db 2 dup (?) ; original state bytes 52..53
_BSS ends
end
