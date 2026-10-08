; Complete low-level PC-98 intro display primitives; these two original
; near Pascal helpers occupy 155 consecutive bytes in PLAYER_M_TEXT.
; The original TASM includes two forced-width AND CX instructions; we
; retain their exact instruction encoding but no full game byte carriers.
.386
main_01 group PLAYER_M_TEXT
PLAYER_M_TEXT segment byte public 'CODE' use16
assume cs:PLAYER_M_TEXT
public HUD_START_SPRITE_STRIP_PUT
HUD_START_SPRITE_STRIP_PUT proc near
    push bp
    mov bp, sp
    push si
    push di
    push ds
    mov ax, 0A800h
    mov es, ax
    mov cx, [bp+0Ah]
    db 081h, 0E1h, 007h, 000h ; AND CX,0007h, original nonshort width
    mov ax, [bp+0Ah]
    mov bx, [bp+8]
    sar ax, 3
    shl bx, 6
    db 01h, 0D8h ; ADD AX,BX, original reg/rm opcode orientation
    shr bx, 2
    db 01h, 0D8h ; ADD AX,BX, original reg/rm opcode orientation
    db 089h, 0C7h ; MOV DI,AX, original rm/reg opcode orientation
    mov bx, [bp+6]
    shl bx, 1
    add bx, 11FCh
    mov ax, [bx]
    mov ds, ax
    assume ds:nothing
    mov ax, [bp+4]
    shl ax, 2
    add ax, 80h
    db 089h, 0C6h ; MOV SI,AX, original rm/reg opcode orientation
    mov bx, 4
hud_intro_strip_loop:
    cmp word ptr [bp+0Ah], 0
    jl short hud_intro_strip_skip
    cmp word ptr [bp+0Ah], 270h
    jge short hud_intro_strip_done
    db 030h, 0E4h ; XOR AH,AH, original rm/reg opcode orientation
    mov al, [si]
    ror ax, cl
    mov es:[di], ax
hud_intro_strip_skip:
    inc si
    inc di
    add word ptr [bp+0Ah], 8
    dec bx
    jnz short hud_intro_strip_loop
hud_intro_strip_done:
    pop ds
    pop di
    pop si
    pop bp
    ret 8
HUD_START_SPRITE_STRIP_PUT endp

public HUD_START_PARTICLE_PIXEL_PUT
HUD_START_PARTICLE_PIXEL_PUT proc near
    push bp
    mov bp, sp
    push di
    mov ax, [bp+6]
    mov bx, [bp+4]
    sar ax, 7
    shr bx, 5
    shl bx, 6
    db 01h, 0D8h ; ADD AX,BX, original reg/rm opcode orientation
    shr bx, 2
    db 01h, 0D8h ; ADD AX,BX, original reg/rm opcode orientation
    db 089h, 0C7h ; MOV DI,AX, original rm/reg opcode orientation
    mov cx, [bp+6]
    shr cx, 4
    db 081h, 0E1h, 007h, 000h ; AND CX,0007h, original nonshort width
    mov bx, 0C0h
    ror bx, cl
    mov es:[di], bx
    pop di
    pop bp
    ret 4
HUD_START_PARTICLE_PIXEL_PUT endp
PLAYER_M_TEXT ends
end
