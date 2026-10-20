// Complete first six-function source-present candidate, D031..D2E8. No exact acceptance.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/background/background.hpp"

void near background_pixel_di(void)
{
    _AX = BG_DI->x;
    _BX = BG_DI->y;
    asm {
        sar ax, 4
        mov cx, ax
        sar ax, 3
        and bx, 0FFE0h
        shl bx, 1
        add ax, bx
        shr bx, 2
        add bx, ax
        and cl, 7
        mov ax, 00C0h
        ror ax, cl
        mov es:[bx], ax
    }
}

void far background_velocity_reset(void)
{
    register background_particle_t near *particle;
    register int i;
    background_angle = 64;
    particle = background_particles;
    for(i = 0; i < BACKGROUND_CAPACITY; i++, particle++) {
        vector2(particle->vx, particle->vy, 64, particle->speed);
    }
}

void far background_chain1_init(void)
{
    register background_particle_t near *particle;
    register int i;
    background_angle = 64;
    particle = background_particles;
    for(i = 0; i < 48; i++, particle++) {
        particle->x = irand() % (640 * 16);
        particle->y = irand() % (400 * 16);
        particle->vx = 0;
        particle->vy = 16;
        particle->speed = 32;
        particle->sprite = 0x210E;
        if(irand() & 1) {
            particle->sprite += 0x0280;
        }
        particle->random_aux = irand() % 4000;
    }
}

// Custom register boundary: DS:DI is the particle, AX receives corrected y.
// BX/CX/DX/SI/DI/BP and ES remain unchanged. The compiler owns all
// prologue/epilogue generation; no ordinary C return-value ABI is introduced.
void near background_update_di(void)
{
    enum {
        PARTICLE_X = offsetof(background_particle_t, x),
        PARTICLE_Y = offsetof(background_particle_t, y),
        PARTICLE_VX = offsetof(background_particle_t, vx),
        PARTICLE_VY = offsetof(background_particle_t, vy),
        X_MIN = 0x0080, X_MAX = 0x2780, X_SPAN = 0x2700,
        Y_MIN = 0x00E0, Y_MAX = 0x1800, Y_SPAN = 0x1720
    };
    asm {
        mov ax, word ptr [di + PARTICLE_X]
        add ax, word ptr [di + PARTICLE_VX]
        cmp ax, X_MIN
        jae x_check_upper
        add ax, X_SPAN
        jmp x_store
    x_check_upper:
        cmp ax, X_MAX
        jbe x_store
        sub ax, X_SPAN
    x_store:
        mov word ptr [di + PARTICLE_X], ax
        mov ax, word ptr [di + PARTICLE_Y]
        add ax, word ptr [di + PARTICLE_VY]
        cmp ax, Y_MIN
        jae y_check_upper
        add ax, Y_SPAN
        jmp y_store
    y_check_upper:
        cmp ax, Y_MAX
        jbe y_store
        sub ax, Y_SPAN
    y_store:
        mov word ptr [di + PARTICLE_Y], ax
    }
}

// Complete semantic register implementation; original source spelling is unknown.
void far background_chain1_accelerate(void)
{
    enum {
        PARTICLE_X = offsetof(background_particle_t, x),
        PARTICLE_Y = offsetof(background_particle_t, y),
        PARTICLE_VX = offsetof(background_particle_t, vx),
        PARTICLE_VY = offsetof(background_particle_t, vy),
        PARTICLE_SPEED = offsetof(background_particle_t, speed),
        PARTICLE_SPRITE = offsetof(background_particle_t, sprite),
        PARTICLE_STRIDE = sizeof(background_particle_t),
        PARTICLE_COUNT = 48,
        RANDOM_PARTICLE_COUNT = 40,
        SPRITE_HEIGHT = 0,
        SPRITE_WIDTH = sizeof(sprite16_put_size.h),
        CLIP_LEFT = 0,
        CLIP_RIGHT = sizeof(sprite16_clip.left),
        SPRITE_WIDTH_WORDS = 1,
        SPRITE_ROWS = 3,
        SCREEN_RIGHT = 639,
        VRAM_SEGMENT = 0xA800,
        // Pascal pushes mode then color. This DWORD contains both WORD arguments.
        CALLBACK_SEGMENT = sizeof(unsigned int),
        ACCELERATION_LAST_FRAME = 128
    };
    // SI is internal traversal state; DS:DI and pixel ES are real helper inputs.
    // No stack frame, register-save, return, or private calling convention is authored.
    BG_GRAPHICS_BEGIN(3, 10);
    asm {
        mov byte ptr background_angle, 64
        mov di, offset background_particles
        xor si, si
    chain1_accelerate_accelerate_pixels:
        call far ptr irand
        and ax, 1
        add ax, word ptr [di + PARTICLE_VY]
        mov word ptr [di + PARTICLE_VY], ax
        mov byte ptr [di + PARTICLE_SPEED], al
        call near ptr background_update_di
        call near ptr background_pixel_di
        add di, PARTICLE_STRIDE
        inc si
        cmp si, BACKGROUND_PIXEL_COUNT
        jb chain1_accelerate_accelerate_pixels
        call far ptr grcg_off
        call far ptr egc_on
    chain1_accelerate_draw_sprites:
        call far ptr irand
        and ax, 1
        add ax, word ptr [di + PARTICLE_VY]
        mov word ptr [di + PARTICLE_VY], ax
        mov byte ptr [di + PARTICLE_SPEED], al
        call near ptr background_update_di
        mov ax, word ptr [di + PARTICLE_X]
        sar ax, 4
        push ax
        mov ax, word ptr [di + PARTICLE_Y]
        sar ax, 4
        push ax
        push word ptr [di + PARTICLE_SPRITE]
        call far ptr sprite16_put
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain1_accelerate_draw_sprites
    }
    if(round_frame > 128UL) {
        background_render = background_chain1_periodic;
    }
    egc_off();
}

// Complete semantic register implementation; original source spelling is unknown.
void far background_chain1_periodic(void)
{
    int frame;
    // Intentionally retains the incoming local byte on 416 phase paths.
    // Compiler owns its allocation; any displacement change rejects this candidate.
    unsigned char changed;
    enum {
        PARTICLE_X = offsetof(background_particle_t, x),
        PARTICLE_Y = offsetof(background_particle_t, y),
        PARTICLE_VX = offsetof(background_particle_t, vx),
        PARTICLE_VY = offsetof(background_particle_t, vy),
        PARTICLE_SPEED = offsetof(background_particle_t, speed),
        PARTICLE_SPRITE = offsetof(background_particle_t, sprite),
        PARTICLE_STRIDE = sizeof(background_particle_t),
        PARTICLE_COUNT = 48,
        RANDOM_PARTICLE_COUNT = 40,
        SPRITE_HEIGHT = 0,
        SPRITE_WIDTH = sizeof(sprite16_put_size.h),
        CLIP_LEFT = 0,
        CLIP_RIGHT = sizeof(sprite16_clip.left),
        SPRITE_WIDTH_WORDS = 1,
        SPRITE_ROWS = 3,
        SCREEN_RIGHT = 639,
        VRAM_SEGMENT = 0xA800,
        // Pascal pushes mode then color. This DWORD contains both WORD arguments.
        CALLBACK_SEGMENT = sizeof(unsigned int),
        ACCELERATION_LAST_FRAME = 128
    };
    // SI is internal traversal state; DS:DI and pixel ES are real helper inputs.
    // No stack frame, register-save, return, or private calling convention is authored.
#include "src/main/background/phase.inl"
    asm {
        mov di, offset background_particles
        xor si, si
    chain1_periodic_update_particles:
        call near ptr background_update_di
        cmp changed, 0
        je chain1_periodic_next_update
        lea bx, [di + PARTICLE_VX]
        push ds
        push bx
        lea bx, [di + PARTICLE_VY]
        push ds
        push bx
        mov al, byte ptr background_angle
        mov ah, 0
        push ax
        mov al, byte ptr [di + PARTICLE_SPEED]
        push ax
        call far ptr vector2
    chain1_periodic_next_update:
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain1_periodic_update_particles
    }
    BG_GRAPHICS_BEGIN(3, 10);
    asm {
        mov di, offset background_particles
        xor si, si
    chain1_periodic_draw_pixels:
        call near ptr background_pixel_di
        add di, PARTICLE_STRIDE
        inc si
        cmp si, BACKGROUND_PIXEL_COUNT
        jb chain1_periodic_draw_pixels
        call far ptr grcg_off
        call far ptr egc_on
    chain1_periodic_draw_sprites:
        mov ax, word ptr [di + PARTICLE_X]
        sar ax, 4
        push ax
        mov ax, word ptr [di + PARTICLE_Y]
        sar ax, 4
        push ax
        push word ptr [di + PARTICLE_SPRITE]
        call far ptr sprite16_put_noclip
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain1_periodic_draw_sprites
        call far ptr egc_off
    }
}
