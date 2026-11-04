; Original Japanese PC-98 extended RS-232C communication driver.
; BIOS signature discovery, IRQ vectors and 10 far hardware APIs.
; Real symbolic 8086 source; ROM detection signature is DATA.
.8086
extrn _getvect:far,_setvect:far,___nec_delay:far,N_SCOPY@:near
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _pc98cominitx,_pc98comtermx,_pc98comsendx,_pc98comrecvx,_pc98comgetstatx,_pc98comsetstatx,_pc98comchkbufx,_pc98comsendbreakx,_pc98comresetx,_pc98comcheckbaudx
serial_bios_call:
    push bp
    mov bp, sp
    push si
    push di
    push ds
    push ax
    xor ax, ax
    mov ds, ax
    pop ax
    test byte ptr ds:[0501h],8
    jne loc_002b
    cmp word ptr [bp + 4], 0
    jne loc_001d
    int 19h
    jmp short loc_003c
loc_001d:
    cmp word ptr [bp + 4], 1
    jne loc_0027
    int 0d4h
    jmp short loc_003c
loc_0027:
    int 0d5h
    jmp short loc_003c
loc_002b:
    shl byte ptr [bp + 4], 1
    shl byte ptr [bp + 4], 1
    shl byte ptr [bp + 4], 1
    shl byte ptr [bp + 4], 1
    or ah, byte ptr [bp + 4]
    int 19h
loc_003c:
    pop ds
    pop di
    pop si
    pop bp
    ret 2
scan_bios_signature:
    push bp
    mov bp, sp
    sub sp, 0ah
    push si
    push di
    cmp byte ptr DGROUP:serial_config, 0
    je loc_0055
    jmp near ptr loc_0181
loc_0055:
    push ds
    push ds
    pop es
    mov ax, 0fd80h
    mov ds, ax
    mov word ptr [bp - 2], ax
    mov word ptr [bp - 6], ax
    cld
    xor si, si
loc_0066:
    cmp si, 3000h
    jae loc_0082
    mov di, offset serial_bios_signature
    mov cx, 5
    repe cmpsb
    jne loc_0066
    mov si, word ptr [si - 7]
    mov dx, word ptr [si + 18h]
    mov ax, word ptr [si + 32h]
    jmp short loc_00fd
    nop
loc_0082:
    xor si, si
loc_0084:
    cmp si, 3000h
    jae loc_00aa
    mov di, offset serial_signature_probe_di
    mov cx, 4
    repe cmpsb
    jne loc_0084
    mov dx, word ptr [si]
loc_0096:
    cmp si, 3000h
    jae loc_00aa
    mov di, offset serial_signature_probe_lo
    mov cx, 4
    repe cmpsb
    jne loc_0096
    mov ax, word ptr [si]
    jmp short loc_00fd
loc_00aa:
    xor si, si
loc_00ac:
    cmp si, 3000h
    jae loc_00c5
    mov di, offset serial_signature_probe_hi
    cmpsb
    jne loc_00ac
    cmpsb
    jne loc_00ac
    mov si, word ptr [si]
    mov dx, word ptr [si + 30h]
    mov ax, word ptr [si + 64h]
    jmp short loc_00fd
loc_00c5:
    mov ax, 0fd60h
    mov ds, ax
    xor si, si
loc_00cc:
    cmp si, 3000h
    jae loc_010a
    mov di, offset serial_signature_probe_tail
    cmpsb
    jne loc_00cc
    inc si
    inc si
    mov cx, 4
    repe cmpsb
    jne loc_00cc
    mov si, word ptr [si - 6]
    mov ax, 0fd80h
    mov ds, ax
    mov ax, word ptr [si + 32h]
    mov word ptr [bp - 2], ax
    mov ax, word ptr [si + 66h]
    mov word ptr [bp - 6], ax
    mov dx, word ptr [si + 30h]
    mov ax, word ptr [si + 64h]
    jmp short loc_00fd
loc_00fd:
    pop ds
    mov word ptr [bp - 4], dx
    mov word ptr [bp - 8], ax
    mov byte ptr [bp - 9], 0
    jmp short loc_010f
loc_010a:
    pop ds
    mov byte ptr [bp - 9], 1
loc_010f:
    mov ax, 0ch
    push ax
    call _getvect
    pop cx
    mov word ptr DGROUP:serial_runtime_64, dx
    mov word ptr DGROUP:serial_runtime_62, ax
    mov ax, 19h
    push ax
    call _getvect
    pop cx
    mov word ptr DGROUP:serial_runtime_68, dx
    mov word ptr DGROUP:serial_runtime_66, ax
    cmp byte ptr [bp - 9], 0
    je loc_015b
    cmp word ptr DGROUP:serial_runtime_64, 0fd80h
    jne loc_0147
    cmp word ptr DGROUP:serial_runtime_68, 0fd80h
    je loc_017c
loc_0147:
    cmp word ptr DGROUP:serial_runtime_64, 0fd60h
    jne loc_0157
    cmp word ptr DGROUP:serial_runtime_68, 0fd60h
    je loc_017c
loc_0157:
    xor ax, ax
    jmp short loc_0184
loc_015b:
    push word ptr [bp - 2]
    push word ptr [bp - 4]
    mov ax, 0ch
    push ax
    call _setvect
    push word ptr [bp - 6]
    push word ptr [bp - 8]
    mov ax, 19h
    push ax
    call _setvect
    add sp, 0ch
loc_017c:
    mov byte ptr DGROUP:serial_config, 1
loc_0181:
    mov ax, 1
loc_0184:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
original_vector_mode:
    push si
    push di
    cmp byte ptr DGROUP:serial_config, 0
    je loc_01bd
    push word ptr DGROUP:serial_runtime_64
    push word ptr DGROUP:serial_runtime_62
    mov ax, 0ch
    push ax
    call _setvect
    push word ptr DGROUP:serial_runtime_68
    push word ptr DGROUP:serial_runtime_66
    mov ax, 19h
    push ax
    call _setvect
    add sp, 0ch
    mov byte ptr DGROUP:serial_config, 0
loc_01bd:
    pop di
    pop si
    ret
install_external_vector:
    push bp
    mov bp, sp
    sub sp, 6
    push si
    push di
    cmp byte ptr DGROUP:serial_vector_installed, 0
    je loc_01d2
    jmp short loc_024e
    nop
loc_01d2:
    mov word ptr [bp - 2], 0c000h
    jmp short loc_0258
    nop
loc_01da:
    mov ax, word ptr [bp - 2]
    mov word ptr [bp - 4], ax
    mov word ptr [bp - 6], 800h
    les bx, dword ptr [bp - 6]
    cmp byte ptr es:[bx], 2
    jne loc_0253
    cmp word ptr es:[bx + 4], 0d4h
    jne loc_0253
    cmp word ptr es:[bx + 8], 0d5h
    jne loc_0253
    mov ax, 0d4h
    push ax
    call _getvect
    pop cx
    mov word ptr DGROUP:serial_runtime_56, dx
    mov word ptr DGROUP:serial_runtime_54, ax
    mov ax, 0d5h
    push ax
    call _getvect
    pop cx
    mov word ptr DGROUP:serial_runtime_60, dx
    mov word ptr DGROUP:serial_runtime_58, ax
    push word ptr [bp - 2]
    les bx, dword ptr [bp - 6]
    push word ptr es:[bx + 6]
    mov ax, 0d4h
    push ax
    call _setvect
    push word ptr [bp - 2]
    les bx, dword ptr [bp - 6]
    push word ptr es:[bx + 0ah]
    mov ax, 0d5h
    push ax
    call _setvect
    add sp, 0ch
    mov byte ptr DGROUP:serial_vector_installed, 1
loc_024e:
    mov ax, 1
    jmp short loc_0264
loc_0253:
    add word ptr [bp - 2], 400h
loc_0258:
    cmp word ptr [bp - 2], 0e000h
    jae loc_0262
    jmp near ptr loc_01da
loc_0262:
    xor ax, ax
loc_0264:
    pop di
    pop si
    mov sp, bp
    pop bp
    ret
release_external_vector:
    push si
    push di
    cmp byte ptr DGROUP:serial_vector_installed, 0
    je loc_029d
    push word ptr DGROUP:serial_runtime_56
    push word ptr DGROUP:serial_runtime_54
    mov ax, 0d4h
    push ax
    call _setvect
    push word ptr DGROUP:serial_runtime_60
    push word ptr DGROUP:serial_runtime_58
    mov ax, 0d5h
    push ax
    call _setvect
    add sp, 0ch
    mov byte ptr DGROUP:serial_vector_installed, 0
loc_029d:
    pop di
    pop si
    ret

; Original far extended serial API CODE+672.
_pc98cominitx:
    push bp
    mov bp, sp
    sub sp, 8
    push si
    push di
    xor ax, ax
    mov es, ax
    mov al, byte ptr es:[501h]
    and al, 8
    mov byte ptr [bp - 3], al
    cmp word ptr [bp + 6], 3
    jb loc_02be
    jmp near ptr loc_0372
loc_02be:
    cmp byte ptr [bp - 3], 0
    jne loc_02e4
    cmp word ptr [bp + 6], 1
    jb loc_02d4
    call install_external_vector
    or ax, ax
    jne loc_02e4
    jmp near ptr loc_0372
loc_02d4:
    cmp word ptr [bp + 6], 0
    jne loc_02e4
    call scan_bios_signature
    or ax, ax
    jne loc_02e4
    jmp near ptr loc_0372
loc_02e4:
    les bx, dword ptr [bp + 8]
    cmp byte ptr es:[bx + 2], 3
    jbe loc_02f1
    jmp near ptr loc_0372
loc_02f1:
    cmp byte ptr es:[bx + 3], 2
    jbe loc_02fb
    jmp short loc_0372
    nop
loc_02fb:
    cmp byte ptr es:[bx + 4], 2
    ja loc_0372
    cmp byte ptr es:[bx + 5], 2
    jae loc_0372
    les bx, dword ptr [bp + 8]
    mov al, byte ptr es:[bx + 2]
    mov ah, 0
    mov bx, ax
    mov al, byte ptr DGROUP:serial_port_modes[bx]
    mov bx, word ptr [bp + 8]
    mov dl, byte ptr es:[bx + 3]
    mov dh, 0
    mov bx, dx
    or al, byte ptr DGROUP:serial_port_rates[bx]
    mov bx, word ptr [bp + 8]
    mov dl, byte ptr es:[bx + 4]
    mov dh, 0
    mov bx, dx
    or al, byte ptr DGROUP:serial_port_speeds[bx]
    mov byte ptr [bp - 1], al
    cmp word ptr [bp + 6], 0
    jne loc_0351
    mov bx, word ptr [bp + 8]
    cmp word ptr es:[bx], 8
    ja loc_0372
    les bx, dword ptr [bp + 8]
    mov al, byte ptr es:[bx]
    mov byte ptr [bp - 2], al
loc_0351:
    or byte ptr [bp - 1], 2
    cmp byte ptr [bp - 3], 0
    je loc_0360
    mov ax, 1ah
    jmp short loc_0363
loc_0360:
    mov ax, 16h
loc_0363:
    mov word ptr [bp - 8], ax
    les bx, dword ptr [bp + 8]
    mov ax, word ptr es:[bx + 6]
    cmp ax, word ptr [bp - 8]
    jae loc_0377
loc_0372:
    mov ax, 0ffffh
    jmp short loc_03b1
loc_0377:
    push ds
    lds si, dword ptr [bp + 8]
    mov cl, 37h
    mov ch, byte ptr [bp - 1]
    mov bl, 0
    mov bh, 0
    mov dx, word ptr [si + 6]
    sub dx, word ptr [bp - 8]
    les di, dword ptr [si + 8]
    mov al, byte ptr [bp - 2]
    xor ah, ah
    cmp byte ptr [si + 5], 1
    jne loc_039a
    inc ah
loc_039a:
    pop ds
    push word ptr [bp + 6]
    call serial_bios_call
    mov al, 0
    mov word ptr [bp - 6], ax
    mov bx, word ptr [bp + 6]
    mov byte ptr DGROUP:serial_active[bx], 1
    mov ax, word ptr [bp - 6]
loc_03b1:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original far extended serial API CODE+951.
_pc98comtermx:
    push bp
    mov bp, sp
    push si
    push di
    mov bx, word ptr [bp + 6]
    cmp byte ptr DGROUP:serial_active[bx], 0
    jne loc_03cb
    mov ax, 100h
    jmp short loc_03f9
loc_03cb:
    mov ax, 540h
    push word ptr [bp + 6]
    call serial_bios_call
    mov bx, word ptr [bp + 6]
    mov byte ptr DGROUP:serial_active[bx], 0
    cmp byte ptr DGROUP:serial_software_mode, 0
    jne loc_03ed
    cmp byte ptr DGROUP:serial_board_detected, 0
    jne loc_03ed
    call release_external_vector
loc_03ed:
    cmp byte ptr DGROUP:serial_active, 0
    jne loc_03f7
    call original_vector_mode
loc_03f7:
    xor ax, ax
loc_03f9:
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1021.
_pc98comsendx:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 3
    mov al, byte ptr [bp + 8]
    push word ptr [bp + 6]
    call serial_bios_call
    mov al, 0
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1043.
_pc98comrecvx:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 4
    push word ptr [bp + 6]
    call serial_bios_call
    les bx, dword ptr [bp + 8]
    mov byte ptr es:[bx], ch
    mov al, cl
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1068.
_pc98comgetstatx:
    push bp
    mov bp, sp
    sub sp, 2
    push si
    push di
    mov ah, 6
    push word ptr [bp + 6]
    call serial_bios_call
    mov al, 0
    mov word ptr [bp - 2], ax
    les bx, dword ptr [bp + 8]
    mov word ptr es:[bx], cx
    mov ax, word ptr [bp - 2]
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original far extended serial API CODE+1104.
_pc98comsetstatx:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 5
    mov al, byte ptr [bp + 8]
    push word ptr [bp + 6]
    call serial_bios_call
    mov al, 0
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1126.
_pc98comchkbufx:
    push bp
    mov bp, sp
    push si
    push di
    mov ah, 2
    push word ptr [bp + 6]
    call serial_bios_call
    xor dx, dx
    les bx, dword ptr [bp + 8]
    mov word ptr es:[bx], cx
    mov word ptr es:[bx + 2], dx
    mov word ptr es:[bx + 4], dx
    mov word ptr es:[bx + 6], dx
    mov al, 0
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1165.
_pc98comsendbreakx:
    push bp
    mov bp, sp
    push si
    push di
    mov ax, 53fh
    push word ptr [bp + 6]
    call serial_bios_call
    mov ax, 12ch
    push ax
    call ___nec_delay
    pop cx
    mov ax, 537h
    push word ptr [bp + 6]
    call serial_bios_call
    pop di
    pop si
    pop bp
    retf

; Original far extended serial API CODE+1202.
_pc98comresetx:
    push bp
    mov bp, sp
    sub sp, 12h
    push si
    push di
    mov bx, word ptr [bp + 6]
    cmp byte ptr DGROUP:serial_active[bx], 0
    jne loc_04c9
    mov ax, 100h
    jmp short loc_04ee
loc_04c9:
    lea ax, [bp - 12h]
    push ss
    push ax
    mov ax, 12h
    imul word ptr [bp + 6]
    add ax, offset DGROUP:serial_runtime_00
    push ds
    push ax
    mov cx, 12h
    call N_SCOPY@
    push ss
    lea ax, [bp - 12h]
    push ax
    push word ptr [bp + 6]
    push cs
    call _pc98cominitx
    add sp, 6
loc_04ee:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf

; Original far extended serial API CODE+1268.
_pc98comcheckbaudx:
    push bp
    mov bp, sp
    sub sp, 4
    push si
    push di
    mov ax, word ptr [bp + 6]
    mov dx, word ptr [bp + 8]
    or ax, ax
    jne loc_0543
    mov cx, 7
    xor ax, ax
    mov es, ax
    test byte ptr es:[501h], 80h
    je loc_0539
    mov word ptr [bp - 2], 0f8e8h
    mov word ptr [bp - 4], 0
    les bx, dword ptr [bp - 4]
    cmp byte ptr es:[bx], 98h
    jne loc_0539
    cmp byte ptr es:[bx + 1], 21h
    jne loc_0539
    test byte ptr es:[bx + 2], 4
    je loc_0539
    mov cx, 8
loc_0539:
    or dx, dx
    jl loc_055b
    cmp dx, cx
    jg loc_055b
    jmp short loc_0556
loc_0543:
    cmp ax, 1
    je loc_054d
    cmp ax, 2
    jne loc_055f
loc_054d:
    or dx, dx
    jl loc_055b
    cmp dx, 7
    jg loc_055b
loc_0556:
    mov ax, 1
    jmp short loc_055d
loc_055b:
    xor ax, ax
loc_055d:
    jmp short loc_0561
loc_055f:
    xor ax, ax
loc_0561:
    pop di
    pop si
    mov sp, bp
    pop bp
    retf
_TEXT ends

_DATA segment word public 'DATA'
serial_active db 0
serial_software_mode db 0
serial_board_detected db 0
serial_vector_installed db 0
serial_config db 0
; Unaligned signed-byte BIOS/ROM signature used as a search pattern.
serial_bios_signature label byte
    db 51,255,185,30,0
serial_signature_probe_di label byte
    db 191,48,0,184
serial_signature_probe_lo label byte
    db 191,100,0,184
serial_signature_probe_hi label byte
    db 249,190
serial_signature_probe_tail label byte
    db 179,51,192,142,192
serial_port_modes db 0,4,8,12
serial_port_speeds db 0,48,16
serial_port_rates db 64,128,192
_DATA ends

; Original 70-byte uninitialized ring state and saved DOS interrupt vectors.
_BSS segment word public 'BSS'
assume cs:nothing
serial_runtime_00:
    db 54 dup (?)
serial_runtime_54:
    db 2 dup (?)
serial_runtime_56:
    db 2 dup (?)
serial_runtime_58:
    db 2 dup (?)
serial_runtime_60:
    db 2 dup (?)
serial_runtime_62:
    db 2 dup (?)
serial_runtime_64:
    db 2 dup (?)
serial_runtime_66:
    db 2 dup (?)
serial_runtime_68:
    db 2 dup (?)
_BSS ends
end
