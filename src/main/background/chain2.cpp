// Complete second three-function source-present candidate, D2E8..D50E. No exact acceptance.
#pragma codeseg PLAYER_M_TEXT main_01
#include "src/main/background/background.hpp"

void far background_chain2_init(void)
{
    register background_particle_t near *particle;
    register int i;
    background_angle = 64;
    particle = background_particles;
    for(i = 0; i < 50; i++, particle++) {
        particle->x = irand() % (640 * 16);
        particle->y = irand() % (400 * 16);
        particle->vx = 0;
        particle->vy = 16;
        particle->speed = 16;
        if(i < 40) {
            particle->sprite = 0x233E;
        } else {
            particle->sprite = 0x20BE;
        }
    }
}

// Complete semantic register implementation; original source spelling is unknown.
void far background_chain2_accelerate(void)
{
    enum {
        PARTICLE_X = offsetof(background_particle_t, x),
        PARTICLE_Y = offsetof(background_particle_t, y),
        PARTICLE_VX = offsetof(background_particle_t, vx),
        PARTICLE_VY = offsetof(background_particle_t, vy),
        PARTICLE_SPEED = offsetof(background_particle_t, speed),
        PARTICLE_SPRITE = offsetof(background_particle_t, sprite),
        PARTICLE_STRIDE = sizeof(background_particle_t),
        PARTICLE_COUNT = 50,
        RANDOM_PARTICLE_COUNT = 40,
        SPRITE_HEIGHT = 0,
        SPRITE_WIDTH = sizeof(sprite16_put_size.h),
        CLIP_LEFT = 0,
        CLIP_RIGHT = sizeof(sprite16_clip.left),
        SPRITE_WIDTH_WORDS = 1,
        SPRITE_ROWS = 8,
        SCREEN_RIGHT = 639,
        VRAM_SEGMENT = 0xA800,
        // Pascal pushes mode then color. This DWORD contains both WORD arguments.
        CALLBACK_SEGMENT = sizeof(unsigned int),
        ACCELERATION_LAST_FRAME = 144
    };
    // SI is internal traversal state; DS:DI and pixel ES are real helper inputs.
    // No stack frame, register-save, return, or private calling convention is authored.
    BG_GRAPHICS_BEGIN(8, 13);
    asm {
        mov byte ptr background_angle, 64
        mov di, offset background_particles
        xor si, si
    chain2_accelerate_accelerate_pixels:
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
        jb chain2_accelerate_accelerate_pixels
        call far ptr grcg_off
        call far ptr egc_on
    chain2_accelerate_draw_sprites:
        xor ax, ax
        cmp si, RANDOM_PARTICLE_COUNT
        jae chain2_accelerate_velocity_ready
        call far ptr irand
        and ax, 1
    chain2_accelerate_velocity_ready:
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
        call far ptr sprite16_put_noclip
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain2_accelerate_draw_sprites
    }
    if(round_frame > 144UL) {
        background_render = background_chain2_periodic;
    }
    egc_off();
}

// Complete semantic register implementation; original source spelling is unknown.
void far background_chain2_periodic(void)
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
        PARTICLE_COUNT = 50,
        RANDOM_PARTICLE_COUNT = 40,
        SPRITE_HEIGHT = 0,
        SPRITE_WIDTH = sizeof(sprite16_put_size.h),
        CLIP_LEFT = 0,
        CLIP_RIGHT = sizeof(sprite16_clip.left),
        SPRITE_WIDTH_WORDS = 1,
        SPRITE_ROWS = 8,
        SCREEN_RIGHT = 639,
        VRAM_SEGMENT = 0xA800,
        // Pascal pushes mode then color. This DWORD contains both WORD arguments.
        CALLBACK_SEGMENT = sizeof(unsigned int),
        ACCELERATION_LAST_FRAME = 144
    };
    // SI is internal traversal state; DS:DI and pixel ES are real helper inputs.
    // No stack frame, register-save, return, or private calling convention is authored.
#include "src/main/background/phase.inl"
    asm {
        mov di, offset background_particles
        xor si, si
    chain2_periodic_update_particles:
        call near ptr background_update_di
        cmp changed, 0
        je chain2_periodic_next_update
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
    chain2_periodic_next_update:
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain2_periodic_update_particles
    }
    BG_GRAPHICS_BEGIN(8, 13);
    asm {
        mov di, offset background_particles
        xor si, si
    chain2_periodic_draw_pixels:
        call near ptr background_pixel_di
        add di, PARTICLE_STRIDE
        inc si
        cmp si, BACKGROUND_PIXEL_COUNT
        jb chain2_periodic_draw_pixels
        call far ptr grcg_off
        call far ptr egc_on
    chain2_periodic_draw_sprites:
        xor dx, dx
        cmp si, RANDOM_PARTICLE_COUNT
        jb chain2_periodic_sprite_delta_ready
        mov dx, frame
        and dx, 31
        shr dx, 3
        shl dx, 1
    chain2_periodic_sprite_delta_ready:
        mov ax, word ptr [di + PARTICLE_X]
        sar ax, 4
        push ax
        mov ax, word ptr [di + PARTICLE_Y]
        sar ax, 4
        push ax
        add dx, word ptr [di + PARTICLE_SPRITE]
        push dx
        call far ptr sprite16_put_noclip
        add di, PARTICLE_STRIDE
        inc si
        cmp si, PARTICLE_COUNT
        jb chain2_periodic_draw_sprites
        call far ptr egc_off
    }
}
