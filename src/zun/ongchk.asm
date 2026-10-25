; TH03 ZUN option -1: recovered ONGCHK FM/ADPCM probe.
; Original source and assembler identity are unknown.
; Initialized COM: 892 instruction bytes + 34 DATA bytes, with 42 trailing BSS bytes.
; No startup/runtime library, encoded instruction arrays or file padding.
;
; All routines are near, with shared success/failure tails. Port operations and
; DOS exit retain their literal widths and interrupt-state changes. Busy waits
; are intentionally unbounded except the 10000-poll write-ready timeout.
.8086
.model tiny
.code
org 100h
public start, probe_hardware, probe_type3, probe_type2, probe_found, probe_failed
public adpcm_check, adpcm_write, adpcm_read, adpcm_dummy_read, adpcm_compare, adpcm_register_write
public ram_pattern, port_override, probe_result
public fm_address_port, fm_data_port, adpcm_address_port, adpcm_data_port, has_board_rom, type2_first, ram_buffer

; The initial LODSB reads PSP:80h (the length byte), not just the tail text.
; Length 38h selects type 2 first. Length 20h makes the scan enter the text.
start:
    cld
    mov ax, cs
    mov ds, ax
    mov es, ax
    mov byte ptr type2_first, 0
    mov si, 080h

priority_scan:
    lodsb
    cmp al, 020h
    je short priority_scan
    cmp al, 038h
    jne short probe_start
    mov byte ptr type2_first, 1

probe_start:
    call probe_hardware
    mov ah, 04Ch
    mov al, byte ptr probe_result
    int 021h

; Result kinds: 0=none, 1=FM echo, 2/3=detector type, 4/5=type with RAM.
probe_hardware:
    cmp byte ptr type2_first, 1
    je short probe_type2_first
    call probe_type3
    jae short probe_adpcm

probe_type2_first:
    call probe_type2
    jae short probe_adpcm
    cmp byte ptr type2_first, 1
    jne short probe_fm_echo
    call probe_type3
    jae short probe_adpcm

probe_fm_echo:
    mov byte ptr probe_result, 1
    mov ah, 4
    mov dx, 088h
    cmp byte ptr port_override, 0FFh
    je short echo_next_pair
    mov dh, byte ptr port_override
    mov ah, 1

echo_next_pair:
    cli
    mov cx, 064h

echo_select_delay:
    loop echo_select_delay
    mov al, 0Bh
    out dx, al
    mov cx, 064h

echo_data_delay:
    loop echo_data_delay
    add dx, 2
    mov al, 0AAh
    out dx, al
    mov cx, 064h

echo_read_delay:
    loop echo_read_delay
    in al, dx
    sti
    sub dx, 2
    cmp al, 0AAh
    jne short echo_failed
    jmp near ptr probe_found

echo_failed:
    dec ah
    jne short echo_advance
    jmp near ptr probe_failed

echo_advance:
    add dx, 0100h
    jmp short echo_next_pair

probe_adpcm:
    cmp byte ptr probe_result, 2
    jb short probe_done
    call adpcm_check
    jb short probe_done
    add byte ptr probe_result, 2

probe_done:
    clc
    ret

; Type 3 requires the ROM version check and the A460h configuration port.
probe_type3:
    mov byte ptr probe_result, 3
    mov byte ptr has_board_rom, 0
    mov ax, 0FD80h
    mov es, ax
    cmp word ptr es:[2], 02A27h
    jne short probe_type3_config
    mov byte ptr has_board_rom, 1
    cmp byte ptr es:[4], 6
    jae short probe_type3_config
    jmp near ptr probe_failed

probe_type3_config:
    mov dx, 0A460h
    in al, dx
    cmp al, 0FFh
    jne short probe_type3_enable
    jmp near ptr probe_failed

probe_type3_enable:
    out 05Fh, al
    and al, 0FCh
    out dx, al
    mov ah, 2
    mov dx, 0188h
    cmp byte ptr port_override, 0FFh
    je short probe_type3_pair
    mov dh, byte ptr port_override
    mov ah, 1

probe_type3_pair:
    cli
    mov al, 0FFh
    mov cx, 064h

probe_type3_select_delay:
    loop probe_type3_select_delay
    out dx, al
    add dx, 2
    mov cx, 064h

probe_type3_read_delay:
    loop probe_type3_read_delay
    in al, dx
    sti
    sub dx, 2
    dec al
    jne short probe_type3_next
    add dx, 4
    in al, dx
    mov bl, al
    add dx, 2
    in al, dx
    sub dx, 6
    and al, bl
    inc al
    je short probe_type3_commit

probe_type3_next:
    dec ah
    jne short probe_type3_advance
    jmp near ptr probe_failed

probe_type3_advance:
    inc dh
    jmp short probe_type3_pair

probe_type3_commit:
    push dx
    mov dx, 0A460h
    cli
    in al, dx
    out 05Fh, al
    and al, 0FCh
    or al, 1
    out dx, al
    mov dx, 0A66Eh
    in al, dx
    out 05Fh, al
    and al, 0FEh
    out dx, al
    cmp byte ptr has_board_rom, 0
    je short probe_type3_commit_done
    mov al, 1
    out 06Eh, al

probe_type3_commit_done:
    sti
    pop dx
    jmp short probe_found

; Type 2 tolerates the older ROM and scans four FM address-port banks.
probe_type2:
    mov byte ptr probe_result, 2
    mov byte ptr has_board_rom, 0
    mov ax, 0FD80h
    mov es, ax
    cmp word ptr es:[2], 02A27h
    jne short probe_type2_config
    mov byte ptr has_board_rom, 1
    cmp byte ptr es:[4], 6
    jb short probe_type2_pairs

probe_type2_config:
    mov dx, 0A460h
    in al, dx
    cmp al, 0FFh
    je short probe_type2_pairs
    out 05Fh, al
    and al, 0FCh
    out dx, al

probe_type2_pairs:
    mov ah, 4
    mov dx, 088h
    cmp byte ptr port_override, 0FFh
    je short probe_type2_pair
    mov dh, byte ptr port_override
    mov ah, 1

probe_type2_pair:
    cli
    mov al, 0FFh
    mov cx, 064h

probe_type2_select_delay:
    loop probe_type2_select_delay
    out dx, al
    add dx, 2
    mov cx, 064h

probe_type2_read_delay:
    loop probe_type2_read_delay
    in al, dx
    sti
    sub dx, 2
    dec al
    jne short probe_type2_next
    add dx, 4
    in al, dx
    mov bl, al
    add dx, 2
    in al, dx
    sub dx, 6
    and al, bl
    inc al
    jne short probe_found

probe_type2_next:
    dec ah
    je short probe_failed
    add dx, 0100h
    jmp short probe_type2_pair

; Shared tail: the selected pair expands to four adjacent WORD port values.
probe_found:
    mov word ptr fm_address_port, dx
    add dx, 2
    mov word ptr fm_data_port, dx
    add dx, 2
    mov word ptr adpcm_address_port, dx
    add dx, 2
    mov word ptr adpcm_data_port, dx
    clc
    ret

probe_failed:
    mov byte ptr probe_result, 0
    stc
    ret

; Test the fixed 32-byte pattern after selecting CS for both source and buffer.
; A mismatch or write-ready timeout returns carry; successful compare clears it.
adpcm_check:
    mov ax, cs
    mov ds, ax
    mov es, ax
    call adpcm_write
    jb short adpcm_failed
    call adpcm_read
    call adpcm_compare
    je short adpcm_passed

adpcm_failed:
    stc
    ret

adpcm_passed:
    clc
    ret

; DH is a register index and DL its data for adpcm_register_write.
; Preserve each reset edge and the distinct operand orders of the exchanges.
adpcm_write:
    mov dx, 1
    call adpcm_register_write
    mov dx, 01017h
    call adpcm_register_write
    mov dx, 01080h
    call adpcm_register_write
    mov dx, 060h
    call adpcm_register_write
    mov dx, 0102h
    call adpcm_register_write
    mov dx, 0CFFh
    call adpcm_register_write
    inc dh
    call adpcm_register_write
    mov bx, 01FFFh
    mov dh, 2
    mov dl, bl
    call adpcm_register_write
    inc dh
    mov dl, bh
    call adpcm_register_write
    mov dx, 04FFh
    call adpcm_register_write
    inc dh
    call adpcm_register_write
    mov si, offset ram_pattern
    mov cx, 020h
    mov dx, word ptr adpcm_address_port
    mov bx, word ptr adpcm_data_port

write_byte:
    cli
    in al, dx

write_wait_idle:
    in al, dx
    or al, al
    js short write_wait_idle
    mov al, 8
    out dx, al
    push cx
    mov cx, 064h

write_select_delay:
    loop write_select_delay
    pop cx
    xchg bx, dx
    lodsb
    out dx, al
    sti
    xchg dx, bx
    push cx
    mov cx, 02710h
    in al, dx

write_wait_ready:
    in al, dx
    test al, 8
    jne short write_ready
    loop write_wait_ready
    pop cx
    stc
    ret

write_ready:
    pop cx
    in al, dx

write_wait_complete:
    in al, dx
    test al, al
    jns short write_complete
    in al, dx
    jmp short write_wait_complete

write_complete:
    mov al, 010h
    cli
    out dx, al
    push cx
    mov cx, 064h

write_reset_delay:
    loop write_reset_delay
    pop cx
    xchg dx, bx
    mov al, 080h
    out dx, al
    sti
    xchg dx, bx
    loop write_byte
    mov dx, 01000h
    call adpcm_register_write
    mov dx, 01080h
    call adpcm_register_write
    mov dx, 1
    call adpcm_register_write
    clc
    ret

; Two actual dummy reads precede the 32 bytes stored through ES:DI.
adpcm_read:
    mov dx, 1
    call adpcm_register_write
    mov dx, 01000h
    call adpcm_register_write
    mov dx, 01080h
    call adpcm_register_write
    mov dx, 020h
    call adpcm_register_write
    mov dx, 0102h
    call adpcm_register_write
    mov dx, 0CFFh
    call adpcm_register_write
    inc dh
    call adpcm_register_write
    mov bx, 01FFFh
    mov dh, 2
    mov dl, bl
    call adpcm_register_write
    mov dh, 3
    mov dl, bh
    call adpcm_register_write
    mov dx, 04FFh
    call adpcm_register_write
    inc dh
    call adpcm_register_write
    call adpcm_dummy_read
    call adpcm_dummy_read
    mov cx, 020h
    mov di, offset ram_buffer

read_byte:
    mov dx, word ptr adpcm_address_port
    cli

read_wait_idle:
    in al, dx
    test al, al
    js short read_wait_idle
    mov al, 8
    out dx, al
    in al, dx

read_wait_ready:
    in al, dx
    test al, 8
    je short read_wait_ready
    in al, dx

read_wait_data_idle:
    in al, dx
    or al, al
    js short read_wait_data_idle
    mov dx, word ptr adpcm_data_port
    in al, dx
    sti
    stosb
    mov dx, 01080h
    call adpcm_register_write
    loop read_byte
    mov dx, 1
    call adpcm_register_write
    ret

adpcm_dummy_read:
    cli
    mov dx, word ptr adpcm_address_port

dummy_wait_idle:
    in al, dx
    test al, al
    js short dummy_wait_idle
    mov al, 8
    out dx, al
    push cx
    mov cx, 064h

dummy_select_delay:
    loop dummy_select_delay
    pop cx
    mov dx, word ptr adpcm_data_port
    in al, dx
    sti
    mov dx, 01080h
    call adpcm_register_write
    ret

adpcm_compare:
    mov si, offset ram_pattern
    mov di, offset ram_buffer
    mov cx, 020h
    repe cmpsb
    ret

; Preserve AX/BX/DX/CX and incoming FLAGS across the atomic register write.
adpcm_register_write:
    push ax
    push bx
    push dx
    mov bx, dx
    mov dx, word ptr adpcm_address_port
    pushf
    cli
    in al, dx

register_wait_idle:
    in al, dx
    or al, al
    js short register_wait_idle
    mov al, bh
    out dx, al
    push cx
    mov cx, 064h

register_select_delay:
    loop register_select_delay
    pop cx
    mov dx, word ptr adpcm_data_port
    mov al, bl
    out dx, al
    popf
    pop dx
    pop bx
    pop ax
    ret

; Initialized DATA: a meaningful hardware RAM test pattern and mutable defaults.
ram_pattern db "*+=-PMD ADPCM RAM Check Data-=+*"
port_override db 0FFh
probe_result db 0
; Uninitialized work area follows the file image; TLINK does not file-back it.
.data?
fm_address_port dw ?
fm_data_port dw ?
adpcm_address_port dw ?
adpcm_data_port dw ?
has_board_rom db ?
type2_first db ?
ram_buffer db 32 dup (?)
end start
