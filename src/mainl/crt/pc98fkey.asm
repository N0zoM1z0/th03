; Original NEC PC-98 function-key display and state CRT member (80 CODE bytes).
; Native BIOS INT DCh and the actual five-byte escape control sequence;
; no opaque executable target data or binary patch.
.8086
_TEXT segment byte public 'CODE'
_TEXT ends
_DATA segment word public 'DATA'
_DATA ends
_BSS segment word public 'BSS'
_BSS ends
DGROUP group _DATA,_BSS
_TEXT segment byte public 'CODE'
assume cs:_TEXT,ds:DGROUP
public _pc98fkeyon,_pc98fkeyoff,_pc98fkeychk
pc98_write_control:
    push bp
    mov bp,sp
    push si
    push di
    mov bx,offset _TEXT:pc98_control_string
    mov cl,16
    xor ah,ah
    jmp short pc98_read_control
pc98_control_string:
    db 27,'[','>','1',0
pc98_write_next:
    int 0DCh
    inc bx
pc98_read_control:
    mov dl,byte ptr cs:[bx]
    or dl,dl
    jnz pc98_write_next
    mov dl,[bp+4]
    int 0DCh
    pop di
    pop si
    pop bp
    ret 2
_pc98fkeyon:
    push si
    push di
    mov al,06Ch
    push ax
    call pc98_write_control
    pop di
    pop si
    retf
_pc98fkeyoff:
    push si
    push di
    mov al,068h
    push ax
    call pc98_write_control
    pop di
    pop si
    retf
_pc98fkeychk:
    push si
    push di
    xor ax,ax
    mov es,ax
    mov al,byte ptr es:[0711h]
    cmp al,1
    sbb ax,ax
    inc ax
    pop di
    pop si
    retf
_TEXT ends
end
