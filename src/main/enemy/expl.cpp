#include "src/main/enemy/expl.hpp"

// The original large collision routine counts hits and charges in distinct
// bounded levels. Keep all byte mutations and signed bonus arithmetic.
enum explosion_native_timing_t {
    EXPLOSION_HIT_PERIOD = 4,
    EXPLOSION_CHAIN_FIRST_END = 4,
    EXPLOSION_CHAIN_SECOND_END = 10,
    EXPLOSION_CHAIN_THIRD_END = 20,
    EXPLOSION_BONUS_HALVE_THROUGH = 48,
    EXPLOSION_BONUS_DOUBLE_FROM = 96,
};

uint8_t far __cdecl explosions_hittest(void)
{
    efe_t near *expl_p;
    uint8_t near *charge_fireball_p;
    int i;
    Subpixel x;
    Subpixel y;
    // The same two-byte value is first a radius, then doubled to diameter.
    Subpixel extent;
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
    uint8_t against2;

    if(explosion_hittest_against == EHA_PELLET) {
        against2 = EHA2_PELLET;
    } else {
        against2 = (3 * explosion_hittest_against);
    }

    expl_p = efes;
    explosion_collision_in_last_hittest = false;

    for(i = 0; i < EFE_COUNT; (++i, expl_p++)) {
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
        if(expl_p->frame & (EXPLOSION_HIT_PERIOD - 1)) {
            continue;
        }

        extent.v = (expl_p->size_pixels * 6);
        x.v = (expl_p->center.x.v - extent.v);
        y.v = (expl_p->center.y.v - extent.v);
        if((hitbox.right.v < x.v) || (hitbox.bottom.v < y.v)) {
            continue;
        }

        extent.v <<= 1;

        x.v += extent.v;
        y.v += extent.v;
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
            hits = chains.hits[hitbox.pid][explosion_collision_chain_slot];
            if(hits < 255) {
                hits++;
            }
            chains.hits[hitbox.pid][explosion_collision_chain_slot] = hits;

            if(against2 == EHA2_PELLET) {
                bonus = (hits * 2);
                score_add(1, hitbox.pid);
            } else if(against2 == EHA2_FIREBALL_BLUE) {
                bonus = (100 + (hits * 16));
                score_add(40, hitbox.pid);
            } else if(against2 == EHA2_FIREBALL_RED) {
                bonus = (444 + (hits * 16));
                score_add(80, hitbox.pid);
            }

            bonus += round_speed;
            if(round_speed <= EXPLOSION_BONUS_HALVE_THROUGH) {
                bonus >>= 1;
            } else if(round_speed >= EXPLOSION_BONUS_DOUBLE_FROM) {
                // Preserve original signed addition: <<=1 changes TC4's
            // actual full physical CODE (negative control af747c).
            bonus += bonus;
            }

            charge_fireball_p = (
                &chains.pellet_and_fireball_value[hitbox.pid][
                    explosion_collision_chain_slot
                ]
            );
            *charge_fireball_p += against2;
            hits = *charge_fireball_p;

            charge_fireball_p = &chains.charge_fireball[hitbox.pid][
                explosion_collision_chain_slot
            ];
            if(against2 == EHA2_PELLET) {
                gauge_avail_add(hitbox.pid, 4);
            } else {
                gauge_avail_add(hitbox.pid, (against2 * 3));
            }

            if(hits < EXPLOSION_CHAIN_FIRST_END) {
                *charge_fireball_p += 2;
            } else if(hits < EXPLOSION_CHAIN_SECOND_END) {
                *charge_fireball_p += 5;
            } else if(hits < EXPLOSION_CHAIN_THIRD_END) {
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
        }

        ++collision_count;
        explosion_collision_in_last_hittest = true;
    }
    return collision_count;
}
