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

void far background_chain1_accelerate(void)
{
    register unsigned int i;
    BG_GRAPHICS_BEGIN(3, 10);
    background_angle = 64;
    BG_START(i);
    do {
        BG_DI->speed = (BG_DI->vy = static_cast<unsigned int>(
            (irand() & 1) + static_cast<unsigned int>(BG_DI->vy)
        ));
        background_update_di();
        background_pixel_di();
        BG_NEXT(i);
    } while(i < BACKGROUND_PIXEL_COUNT);
    grcg_off();
    egc_on();
    do {
        BG_DI->speed = (BG_DI->vy = static_cast<unsigned int>(
            (irand() & 1) + static_cast<unsigned int>(BG_DI->vy)
        ));
        background_update_di();
        sprite16_put(BG_DI->x >> 4, BG_DI->y >> 4, BG_DI->sprite);
        BG_NEXT(i);
    } while(i < 48);
    if(round_frame > 128UL) {
        background_render = background_chain1_periodic;
    }
    egc_off();
}

void far background_chain1_periodic(void)
{
    register unsigned int i;
    int frame;
    // Empirical TC4 hypothesis: intentionally not initialized on every path.
    // The later branch reads an indeterminate value in ordinary C++ semantics.
    // No manual frame/slot, volatile, static state or initialization is allowed.
    unsigned char changed;
#include "src/main/background/phase.inl"
    BG_START(i);
    do {
        background_update_di();
        if(changed) {
            vector2(BG_DI->vx, BG_DI->vy, background_angle, BG_DI->speed);
        }
        BG_NEXT(i);
    } while(i < 48);
    BG_GRAPHICS_BEGIN(3, 10);
    BG_START(i);
    do {
        background_pixel_di();
        BG_NEXT(i);
    } while(i < BACKGROUND_PIXEL_COUNT);
    grcg_off();
    egc_on();
    do {
        sprite16_put_noclip(BG_DI->x >> 4, BG_DI->y >> 4, BG_DI->sprite);
        BG_NEXT(i);
    } while(i < 48);
    egc_off();
}
