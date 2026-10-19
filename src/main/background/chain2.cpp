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

void far background_chain2_accelerate(void)
{
    register unsigned int i;
    BG_GRAPHICS_BEGIN(8, 13);
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
            ((i < 40) ? (irand() & 1) : 0) +
            static_cast<unsigned int>(BG_DI->vy)
        ));
        background_update_di();
        sprite16_put_noclip(BG_DI->x >> 4, BG_DI->y >> 4, BG_DI->sprite);
        BG_NEXT(i);
    } while(i < 50);
    if(round_frame > 144UL) {
        background_render = background_chain2_periodic;
    }
    egc_off();
}

void far background_chain2_periodic(void)
{
    register unsigned int i;
    int frame;
    // Deliberate uninitialized-local hypothesis; see the proposal review.
    unsigned char changed;
#include "src/main/background/phase.inl"
    BG_START(i);
    do {
        background_update_di();
        if(changed) {
            vector2(BG_DI->vx, BG_DI->vy, background_angle, BG_DI->speed);
        }
        BG_NEXT(i);
    } while(i < 50);
    BG_GRAPHICS_BEGIN(8, 13);
    BG_START(i);
    do {
        background_pixel_di();
        BG_NEXT(i);
    } while(i < BACKGROUND_PIXEL_COUNT);
    grcg_off();
    egc_on();
    do {
        sprite16_put_noclip(
            BG_DI->x >> 4, BG_DI->y >> 4, BG_DI->sprite + ((i < 40) ? 0U :
                (((static_cast<unsigned int>(frame) & 31U) >> 3) * 2U))
        );
        BG_NEXT(i);
    } while(i < 50);
    egc_off();
}
