; Original Japanese NEC PC-98 serial communications BIOS bridge.
; The operation selects hardware BIOS INT 19h/D4h/D5h or the firmware
; serial-vector restoration path, retaining the original far buffer ABI.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
DGROUP group _BSS,_DATA
_BSS segment word public 'BSS'
_BSS ends
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public __necpc_bios_serialcom
__necpc_bios_serialcom proc far
    push bp
    mov bp,sp
    push si
    push di
    push ds
    lds si,dword ptr [bp+10]
    mov ah,[bp+6]
    cmp ah,3
    jz short serial_query_data
    cmp ah,5
    jz short serial_query_value
    cmp ah,1
    jna short configure_port
    jmp near ptr invoke_service
serial_query_data:
    les di,dword ptr [si+0ch]
    mov al,byte ptr es:[di]
    jmp short invoke_service
    nop ; original Borland instruction boundary after query shortcut
serial_query_value:
    mov al,byte ptr [si+4]
    cmp al,0ffh
    jnz short invoke_service
    mov al,15h
    jmp short invoke_service
    nop ; original Borland boundary following default parameter
configure_port:
    cmp word ptr [bp+8],1
    jz short serial_parameters
    push ds
    push si
    mov ax,0a000h
    mov ds,ax
    mov si,03feeh
    test byte ptr [si],10h
    jnz short install_firmware_vector
    mov ah,0ffh
    pop si
    pop ds
    jmp near ptr service_done
install_firmware_vector:
    mov ax,0d080h
    mov ds,ax
    mov si,6
    xor ax,ax
    mov es,ax
    mov di,0350h
    cmp word ptr [bp+8],3
    jnz short copy_vector
    add si,4
    add di,4
copy_vector:
    movsw
    mov ax,0d000h
    stosw
    pop si
    pop ds
serial_parameters:
    mov ah,[bp+6]
    mov al,[si]
    cmp al,0ffh
    jnz short select_speed
    mov al,4
select_speed:
    mov ch,[si+2]
    cmp ch,0ffh
    jnz short set_speed_flag
    mov ch,48h
set_speed_flag:
    or ch,2
    mov cl,[si+4]
    cmp cl,0ffh
    jnz short select_format
    mov cl,15h
select_format:
    mov bh,[si+6]
    mov bl,[si+8]
    mov dx,[si+10]
    les di,dword ptr [si+12]
invoke_service:
    push ds
    push si
    cmp word ptr [bp+8],1
    jnz short try_int_d4
    int 19h
    jmp short after_serial_int
try_int_d4:
    cmp word ptr [bp+8],2
    jnz short call_int_d5
    int 0d4h
    jmp short after_serial_int
call_int_d5:
    int 0d5h
after_serial_int:
    pop si
    pop ds
    mov bl,[bp+6]
    cmp bl,2
    jz short save_result_count
    cmp bl,4
    jz short save_result_far
    cmp bl,6
    jz short save_result_far
    jmp short service_done
save_result_count:
    mov [si+10],cx
    jmp short service_done
save_result_far:
    les di,dword ptr [si+12]
    xchg cl,ch
    mov word ptr es:[di],cx
service_done:
    mov al,ah
    xor ah,ah
    pop ds
    pop di
    pop si
    pop bp
    retf
__necpc_bios_serialcom endp
_TEXT ends
end
