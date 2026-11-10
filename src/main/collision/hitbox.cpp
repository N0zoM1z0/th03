#pragma option -G

#include "src/main/collision/hitbox.hpp"
#include "compat/rec98/th03/main/defeat.hpp"
#include "compat/rec98/th03/main/hitcirc.hpp"
#include "compat/rec98/th03/main/round.hpp"
#include "compat/rec98/th03/main/enemy/efe.hpp"
#include "compat/rec98/th03/main/enemy/expl.hpp"
#include "compat/rec98/th03/main/player/bomb.hpp"
#include "compat/rec98/th03/main/player/ch_shot.hpp"
#include "compat/rec98/th03/main/player/shot.hpp"

// Original per-shot and alternate-frame Bomb damage are byte quantities.
// These source-only values generate no new DATA or hitbox state.
enum hitbox_native_damage_t {
    HITBOX_SHOTPAIR_DAMAGE = 2,
    HITBOX_SHOTPAIR_HALF_W = SHOTPAIR_W / 2,
    HITBOX_SHOTPAIR_HALF_H = SHOTPAIR_H / 2,
    HITBOX_BOMB_DAMAGE_PERIOD = 2,
};

uint8_t hitbox_hittest(void)
{
	shotpair_t near *p;
	playfield_subpixel_t center_x;
	int i;
	playfield_subpixel_t center_y;
	uint8_t damage = 0;

	// The screen-negative and defeat-banner terminal guards share the
	// same early return; neither condition may enter any hit-test list.
	if((hitbox.origin.center.y.v < 0) || (defeat_flag == DF_BANNER)) {
		return 0;
	}

	// Shot pairs
	// ----------

	ef_onehit = false;
	p = shotpairs;
	hitbox.right.v  = (hitbox.origin.center.x.v + hitbox.radius.x.v);
	hitbox.bottom.v = (hitbox.origin.center.y.v + hitbox.radius.y.v);
	hitbox.origin.topleft.x.v = (hitbox.origin.center.x.v - hitbox.radius.x.v);
	hitbox.origin.topleft.y.v = (hitbox.origin.center.y.v - hitbox.radius.y.v);
	hitcircles_enemy_add_do_not_randomly_center_within_hitbox = true;
	// This first-order physical shotpair scan has *two* compiler-sensitive
	// continues. An explicit while with both near-pointer/index updates
	// changes original CODE (native negative af901a), so keep for.
	for(i = 0; i < SHOTPAIR_COUNT; (++i, ++p)) {
		// The original `alive != true` must stay explicit: `!alive`
		// and `alive == false` changed original CODE (af901d/e).
		// Alive and owner checks are independently short-circuited:
		// a dead shot must not contribute to either player's hitbox.
		if(p->alive != true) {
			continue;
		}
		if(p->pid != hitbox.pid) {
			continue;
		}
		center_x = (p->topleft.x.v + to_sp(HITBOX_SHOTPAIR_HALF_W));
		center_y = (p->topleft.y.v + to_sp(HITBOX_SHOTPAIR_HALF_H));
		if(
			((center_x - to_sp(HITBOX_SHOTPAIR_HALF_W)) > hitbox.right.v) ||
			((center_x + to_sp(HITBOX_SHOTPAIR_HALF_W)) < hitbox.origin.topleft.x.v) ||
			(center_y < hitbox.origin.topleft.y.v) ||
			(center_y > hitbox.bottom.v)
		) {
			continue;
		}
		p->alive = false;
		// A named enum in `damage += enum_2` altered original byte CODE;
		// natural C++ `damage = damage + enum_2` is exact (af901g).
		damage = damage + HITBOX_SHOTPAIR_DAMAGE;
		hitcircles_enemy_add(center_x, center_y, hitbox.pid);
	}
	hitcircles_enemy_add_do_not_randomly_center_within_hitbox = false;
	// ----------

	// This flag bypasses only the original segmented explosion call.
	if(hitbox_hittest_skip_explosions == false) {
		/* TODO: Replace with the decompiled call
		 * 	damage += explosions_hittest();
		 * once the segmentation allows us to, if ever */
		asm { nop; push cs; call near ptr explosions_hittest; }
		damage += _AL;
	}

	// Keep the explicit two-player far-callback branches: the compact
	// indexed expression changed complete CODE (af998b).
	static_assert(PLAYER_COUNT == 2);
	// TC4 emits the original far callback sequence for explicit pid == 0.
	if(hitbox.pid == 0) {
		damage += chargeshot_hittest[0]();
	} else {
		damage += chargeshot_hittest[1]();
	}

	// This code never runs for fireballs, because they're always removed in
	// fireballs_update().
	// Bomb contact damages only when the selected player's bomb is
	// active AND the unsigned-word frame clock is on the even phase.
	// Keep both tests short-circuited before the byte-memory increment.
	if((bomb_flag[hitbox.pid] != BF_INACTIVE) &&
	   ((round_or_result_frame % HITBOX_BOMB_DAMAGE_PERIOD) == 0)) {
		// Original damage byte uses postfix, not prefix; changing it
		// generated 271 instead of 266 CODE bytes (af901h).
		damage++;
	}
	return damage;
}
