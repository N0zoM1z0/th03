#include "src/main/enemy/expl.hpp"

#define chain_hits_inc_and_clamp(hits_new, pid, slot) \
    chains.hits[pid][slot]; \
    if(hits_new < 255) { \
        hits_new++; \
    } \
    chains.hits[pid][slot] = hits_new;

uint8_t far __cdecl explosions_hittest(void)
{
    efe_t near *expl_p;
    uint8_t near *charge_fireball_p;
    int i;
    Subpixel x;
    Subpixel y;
    union {
        Subpixel radius;
        Subpixel size;
    } u1;
    int bonus;
    unsigned int collision_count = 0;
    uint8_t hits;

    enum against2_t {
        EHA2_ENEMY = (3 * EHA_ENEMY),
        EHA2_PELLET = EHA_PELLET,
        EHA2_FIREBALL_BLUE = (3 * EHA_FIREBALL_BLUE),
        EHA2_FIREBALL_RED = (3 * EHA_FIREBALL_RED),

        _against2_FORCE_UINT8 = 0xFF
    };
    union {
        against2_t against2;
        uint8_t value;
    } ehm;

    if(explosion_hittest_against == EHA_PELLET) {
        ehm.value = 1;
    } else {
        ehm.value = (3 * explosion_hittest_against);
    }

    expl_p = efes;
    explosion_collision_in_last_hittest = false;

    for(i = 0; i < EFE_COUNT; (i++, expl_p++)) {
        if(expl_p->flag < EFF_EXPLOSION_IGNORING_ENEMIES) {
            continue;
        }

        if((explosion_hittest_against == EHA_ENEMY) && (
            (expl_p->flag == EFF_EXPLOSION_IGNORING_ENEMIES) ||
            (expl_p->flag >= (
                EFF_EXPLOSION_HITTING_ENEMIES +
                (expl_p->explosion_max_enemy_hits_half * 2)
            ))
        )) {
            continue;
        }

        if(expl_p->pid != hitbox.pid) {
            continue;
        }
        if((expl_p->frame & 3) != 0) {
            continue;
        }

        u1.radius.v = (expl_p->size_pixels * 6);
        x.v = (expl_p->center.x.v - u1.radius.v);
        y.v = (expl_p->center.y.v - u1.radius.v);
        if((hitbox.right.v < x.v) || (hitbox.bottom.v < y.v)) {
            continue;
        }

        u1.size.v <<= 1;

        x.v += u1.size.v;
        y.v += u1.size.v;
        if(
            (hitbox.origin.topleft.x.v > x.v) ||
            (hitbox.origin.topleft.y.v > y.v)
        ) {
            continue;
        }

        explosion_collision_chain_slot = expl_p->chain_slot;
        if(explosion_hittest_against == EHA_ENEMY) {
            expl_p->flag++;
        } else {
            hits = chain_hits_inc_and_clamp(
                hits, hitbox.pid, explosion_collision_chain_slot
            );

            if(ehm.against2 == EHA2_PELLET) {
                bonus = (hits * 2);
                score_add(1, hitbox.pid);
            } else if(ehm.against2 == EHA2_FIREBALL_BLUE) {
                bonus = (100 + (hits * 16));
                score_add(40, hitbox.pid);
            } else if(ehm.against2 == EHA2_FIREBALL_RED) {
                bonus = (444 + (hits * 16));
                score_add(80, hitbox.pid);
            }

            bonus += round_speed;
            if(round_speed <= 48) {
                bonus >>= 1;
            } else if(round_speed >= 96) {
                bonus += bonus;
            }

            #define pellet_and_fireball_val hits
            #define pellet_and_fireball_value_p charge_fireball_p
            pellet_and_fireball_value_p = (
                &chains.pellet_and_fireball_value[hitbox.pid][
                    explosion_collision_chain_slot
                ]
            );
            *pellet_and_fireball_value_p += ehm.value;
            pellet_and_fireball_val = *pellet_and_fireball_value_p;
            #undef pellet_and_fireball_value_p

            charge_fireball_p = &chains.charge_fireball[hitbox.pid][
                explosion_collision_chain_slot
            ];
            if(ehm.against2 == EHA2_PELLET) {
                gauge_avail_add(hitbox.pid, 4);
            } else {
                gauge_avail_add(hitbox.pid, (ehm.value * 3));
            }

            if(pellet_and_fireball_val < 4) {
                *charge_fireball_p += 2;
            } else if(pellet_and_fireball_val < 10) {
                *charge_fireball_p += 5;
            } else if(pellet_and_fireball_val < 20) {
                *charge_fireball_p += 2;
                chains.charge_exatt[hitbox.pid][
                    explosion_collision_chain_slot
                ]++;
            } else {
                chains.charge_exatt[hitbox.pid][
                    explosion_collision_chain_slot
                ] += 2;
            }

            bonus = combo_add(
                hitbox.pid, explosion_collision_chain_slot, bonus
            );
            fire_point_based_boss_attack_or_panic(bonus, hitbox.pid);
            explosion_collision_chain_slot_fire_charged_fireball(
                hitbox.pid, expl_p
            );
            #undef pellet_and_fireball_val
        }

        collision_count++;
        explosion_collision_in_last_hittest = true;
    }
    return collision_count;
}
