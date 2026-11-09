#include "src/main/enemy/expl.hpp"

// The original large collision routine counts hits and charges in distinct
// bounded levels. Keep all byte mutations and signed bonus arithmetic.
enum explosion_native_timing_t {
    EXPLOSION_HIT_PERIOD = 4,
    EXPLOSION_NONPELLET_CHARGE_MULTIPLIER = 3,
    EXPLOSION_CHAIN_FIRST_END = 4,
    EXPLOSION_CHAIN_SECOND_END = 10,
    EXPLOSION_CHAIN_THIRD_END = 20,
    EXPLOSION_BONUS_HALVE_THROUGH = 48,
    EXPLOSION_BONUS_DOUBLE_FROM = 96,
    EXPLOSION_SUBPIXEL_RADIUS_SCALE = 6,
    EXPLOSION_BLUE_SCORE = 40,
    EXPLOSION_RED_SCORE = 80,
    EXPLOSION_PELLET_SCORE = 1,
    EXPLOSION_BLUE_BONUS_BASE = 100,
    EXPLOSION_RED_BONUS_BASE = 444,
    EXPLOSION_BULLET_BONUS_PER_HIT = 16,
    EXPLOSION_PELLET_BONUS_PER_HIT = 2,
    EXPLOSION_PELLET_GAUGE_CHARGE = 4,
    EXPLOSION_FIREBALL_GAUGE_MULTIPLIER = 3,
    EXPLOSION_HITS_SATURATION = 255,
    EXPLOSION_CHAIN_INITIAL_CHARGE = 2,
    EXPLOSION_CHAIN_MIDDLE_CHARGE = 5,
    EXPLOSION_CHAIN_LATE_CHARGE = 2,
    EXPLOSION_CHAIN_EXATT_END_CHARGE = 2,
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
        EHA2_ENEMY = (EXPLOSION_NONPELLET_CHARGE_MULTIPLIER * EHA_ENEMY),
        EHA2_PELLET = EHA_PELLET,
        EHA2_FIREBALL_BLUE = (EXPLOSION_NONPELLET_CHARGE_MULTIPLIER * EHA_FIREBALL_BLUE),
        EHA2_FIREBALL_RED = (EXPLOSION_NONPELLET_CHARGE_MULTIPLIER * EHA_FIREBALL_RED),

        _against2_FORCE_UINT8 = 0xFF
    };
    uint8_t against2;

    if(explosion_hittest_against == EHA_PELLET) {
        against2 = EHA2_PELLET;
    } else {
        against2 = (EXPLOSION_NONPELLET_CHARGE_MULTIPLIER * explosion_hittest_against);
    }

    expl_p = efes;
    explosion_collision_in_last_hittest = false;

    // Full real Enemy/Fireball explosion carrier traversal. The for
    // header advances the original signed 16-bit index and near pointer
    // after every continue path and completed collision, matching the
    // original TC4 iterator order byte-for-byte (af996d).
    for(i = 0; i < EFE_COUNT; ++i, ++expl_p) {
        // State, player and byte-frame filters remain ordered short-circuit
        // guards. The byte phase stays a low-bit test: natural %4 changed
        // original TC4 CODE (af902c).
        if(expl_p->flag < EFF_EXPLOSION_IGNORING_ENEMIES) {
            continue;
        }
        if(explosion_hittest_against == EHA_ENEMY) {
            if(
                (expl_p->flag == EFF_EXPLOSION_IGNORING_ENEMIES) ||
                (expl_p->flag >= (
                    EFF_EXPLOSION_HITTING_ENEMIES +
                    (expl_p->explosion_max_enemy_hits_half * 2)
                ))
            ) {
                continue;
            }
        }
        if(expl_p->pid != hitbox.pid) {
            continue;
        }
        if(expl_p->frame & (EXPLOSION_HIT_PERIOD - 1)) {
            continue;
        }

        extent.v = (expl_p->size_pixels * EXPLOSION_SUBPIXEL_RADIUS_SCALE);
        x.v = (expl_p->center.x.v - extent.v);
        y.v = (expl_p->center.y.v - extent.v);
        if(hitbox.right.v < x.v) {
            continue;
        }
        if(hitbox.bottom.v < y.v) {
            continue;
        }

        extent.v <<= 1;

        x.v += extent.v;
        y.v += extent.v;
        if(hitbox.origin.topleft.x.v > x.v) {
            continue;
        }
        if(hitbox.origin.topleft.y.v > y.v) {
            continue;
        }

        explosion_collision_chain_slot = expl_p->chain_slot;
        if(explosion_hittest_against == EHA_ENEMY) {
            // Original byte flag postfix is CODE-visible. Prefix
            // ++expl_p->flag changed original TC4 instructions (af902d).
            expl_p->flag++;
        } else {
            hits = chains.hits[hitbox.pid][explosion_collision_chain_slot];
            // Preserve strict uint8 saturation <255; semantically
            // equivalent !=255 again changed CODE (af902b), so the
            // original full chain counter condition stays intact.
            if(hits < EXPLOSION_HITS_SATURATION) {
                hits++;
            }
            chains.hits[hitbox.pid][explosion_collision_chain_slot] = hits;

            if(against2 == EHA2_PELLET) {
                bonus = (hits * EXPLOSION_PELLET_BONUS_PER_HIT);
                score_add(EXPLOSION_PELLET_SCORE, hitbox.pid);
            } else if(against2 == EHA2_FIREBALL_BLUE) {
                bonus = (
                    EXPLOSION_BLUE_BONUS_BASE +
                    (hits * EXPLOSION_BULLET_BONUS_PER_HIT)
                );
                score_add(EXPLOSION_BLUE_SCORE, hitbox.pid);
            } else if(against2 == EHA2_FIREBALL_RED) {
                bonus = (
                    EXPLOSION_RED_BONUS_BASE +
                    (hits * EXPLOSION_BULLET_BONUS_PER_HIT)
                );
                score_add(EXPLOSION_RED_SCORE, hitbox.pid);
            }

            bonus += round_speed;
            if(round_speed <= EXPLOSION_BONUS_HALVE_THROUGH) {
                bonus >>= 1;
            } else if(round_speed >= EXPLOSION_BONUS_DOUBLE_FROM) {
                // Preserve original signed addition: <<=1 changes TC4's
                // full physical CODE (negative control af747c).
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
                gauge_avail_add(hitbox.pid, EXPLOSION_PELLET_GAUGE_CHARGE);
            } else {
                gauge_avail_add(
                    hitbox.pid, (against2 * EXPLOSION_FIREBALL_GAUGE_MULTIPLIER)
                );
            }

            if(hits < EXPLOSION_CHAIN_FIRST_END) {
                *charge_fireball_p += EXPLOSION_CHAIN_INITIAL_CHARGE;
            } else if(hits < EXPLOSION_CHAIN_SECOND_END) {
                *charge_fireball_p += EXPLOSION_CHAIN_MIDDLE_CHARGE;
            } else if(hits < EXPLOSION_CHAIN_THIRD_END) {
                *charge_fireball_p += EXPLOSION_CHAIN_LATE_CHARGE;
                chains.charge_exatt[hitbox.pid][
                    explosion_collision_chain_slot
                ]++;
            } else {
                chains.charge_exatt[hitbox.pid][
                    explosion_collision_chain_slot
                ] += EXPLOSION_CHAIN_EXATT_END_CHARGE;
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
