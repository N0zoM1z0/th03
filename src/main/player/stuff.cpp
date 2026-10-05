#pragma option -G

#include "compat/rec98/th03/resident.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "src/main/player/stuff.hpp"
#include "compat/rec98/th03/main/player/cpu.hpp"

void near story_skill_decrement(void);

void near pascal player_hittest(collmap_tile_amount_t hitbox_size)
{
	collmap_tile_amount_t tile_top;
	uint8_t tile_bottom;
	enum {
		CENTER_X = offsetof(player_stuff_t, center),
		CENTER_Y = CENTER_X + sizeof(Subpixel),
		INVINCIBILITY = offsetof(player_stuff_t, invincibility_time),
		HYPER = offsetof(player_stuff_t, hyper_active),
		IS_HIT = offsetof(player_stuff_t, is_hit),
		COLLISION_Y = offsetof(PlayfieldPoint, y),
		TILE_SHIFT = SUBPIXEL_BITS + COLLMAP_TILE_W_BITS,
		BYTE_SHIFT = TILE_SHIFT + 3,
	};
	// AX stores top/row; BX stores the bitmap pointer; CX stores mask/stride;
	// DX stores byte-column/bottom; DI stores the remaining width in tiles.
	// The bitmap is traversed in column-major order. Byte comparisons and
	// the original asymmetric clipping are retained explicitly.
	asm {
		mov si, player_cur;
		cmp byte ptr [si + INVINCIBILITY], 0;
		jne guard_exit;
		cmp byte ptr [si + HYPER], 0;
		je prepare_rectangle;
	guard_exit:
		jmp collision_done;
	prepare_rectangle:
		mov ax, hitbox_size;
		mov bx, ax;
		sar ax, 1;
		mov dx, [si + CENTER_X];
		sar dx, TILE_SHIFT;
		sub dx, ax;
		mov cx, [si + CENTER_Y];
		sar cx, TILE_SHIFT;
		sub cx, ax;
		add bx, cx;
		cmp cx, 0;
		jge clip_bottom;
		xor cx, cx;
		jmp rectangle_clipped;
	clip_bottom:
		cmp bx, COLLMAP_H;
		jl rectangle_clipped;
		mov bx, (COLLMAP_H - 1);
	rectangle_clipped:
		mov tile_bottom, bl;
		mov tile_top, cx;
		mov cx, dx;
		and cx, 7;
		sar dx, 3;
		mov di, hitbox_size;
		add di, cx;
		mov ch, 0FFh;
		shr ch, cl;
		mov bx, di;
		cmp bx, 8;
		jg initial_mask_ready;
		mov bh, 0FFh;
		mov cl, bl;
		shr bh, cl;
		xor ch, bh;
	initial_mask_ready:
		mov al, dl;
		mov bl, COLLMAP_H;
		mul bl;
		mov bx, offset collmap;
		add bx, ax;
		cmp pid.current, 1;
		jne bitmap_selected;
		add bx, COLLMAP_SIZE;
	bitmap_selected:
		add bx, tile_top;
		mov dh, tile_bottom;
		mov ax, tile_top;
	column_scan:
		cmp dl, COLLMAP_MEMORY_W;
		jge collision_done;
		or dl, dl;
		jl next_column;
		mov ah, al;
		mov cl, COLLMAP_H;
	row_scan:
		test byte ptr [bx], ch;
		je next_row;
		xor dh, dh;
		shl dx, BYTE_SHIFT;
		mov word ptr player_hittest_collision_top, dx;
		mov ah, 0;
		shl ax, TILE_SHIFT;
		mov word ptr [player_hittest_collision_top + COLLISION_Y], ax;
		mov byte ptr [si + IS_HIT], 1;
		jmp collision_done;
	next_row:
		inc bx;
		dec cl;
		inc ah;
		cmp ah, dh;
		jb row_scan;
	next_column:
		inc dl;
		mov ch, 0;
		add bx, cx;
		sub di, 8;
		mov ch, 0FFh;
		cmp di, 8;
		jae width_checked;
		mov cx, di;
		mov ch, 0FFh;
		shr ch, cl;
		not ch;
	width_checked:
		or di, di;
		jg column_scan;
	collision_done:
	}
}

shalfhearts_t near pascal players_hit_damage_update(
	player_stuff_t near& player_hit
)
{
	static_assert(PLAYER_COUNT == 2);
	shalfhearts_t damage;
	spid_t pid_other = (1 - pid.current);

	// ZUN bloat: Assign `player_hit.hit_damage_next` once.
	if(!player_hit.is_cpu) {
		damage = player_hit.hit_damage_next;
	} else {
		damage = player_hit.hit_damage_next;
		damage += cpu_hit_damage_additional;
	}

	player_hit.hit_damage_next = 3;
	if(players[pid_other].hit_damage_next > 3) {
		players[pid_other].hit_damage_next--;
	}

	if(((player_hit.halfhearts - damage) <= 0) && (player_hit.halfhearts > 1)) {
		damage = (player_hit.halfhearts - 1u);
	}
	story_skill_decrement();
	return damage;
}

void near story_skill_decrement(void)
{
	if((pid.current == 0) && (resident->skill > 0)) {
		resident->skill--;
	}
}
