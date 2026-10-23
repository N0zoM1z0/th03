// Real-mode VRAM helpers. TC4 emits their Pascal frames and saves SI/DI.
void near pascal hud_start_sprite_strip_put(int x, int y, int pattern, int column)
{
    asm {
        push ds
        mov ax, 0A800h
        mov es, ax
        mov cx, x
        and cx, 7
        mov ax, x
        mov bx, y
        sar ax, 3
        shl bx, 6
        add ax, bx
        shr bx, 2
        add ax, bx
        mov di, ax
        mov bx, pattern
        shl bx, 1
        add bx, offset super_patdata
        mov ax, [bx]
        mov ds, ax
        mov ax, column
        shl ax, 2
        add ax, 80h
        mov si, ax
        mov bx, 4
    strip_loop:
        cmp x, 0
        jl strip_skip
        cmp x, 270h
        jge strip_done
        xor ah, ah
        mov al, [si]
        ror ax, cl
        mov es:[di], ax
    strip_skip:
        inc si
        inc di
        add x, 8
        dec bx
        jnz strip_loop
    strip_done:
        pop ds
    }
}

void near pascal hud_start_particle_pixel_put(int x, int y)
{
    asm {
        mov ax, x
        mov bx, y
        sar ax, 7
        shr bx, 5
        shl bx, 6
        add ax, bx
        shr bx, 2
        add ax, bx
        mov di, ax
        mov cx, x
        shr cx, 4
        and cx, 7
        mov bx, 0C0h
        ror bx, cl
        mov es:[di], bx
    }
}
