// MAINL cutscene owner, specialized for GAME=3 from the frozen ReC98 source.
// Preserve declaration/function order, near Pascal ABI, page changes, and unchecked
// allocation/script reads. Decoded candidate scope: 095F:0B3E, 3195 bytes.
// Source ownership is not exact-byte proof; the three PI call operands remain open.

#pragma option -zPgroup_01

#include <stddef.h>
#include "compat/rec98/game/cutscene.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"
#include "compat/rec98/th02/v_colors.hpp"
#include "compat/rec98/th02/hardware/frmdelay.h"
#include "compat/rec98/th03/hardware/input.h"
#include "compat/rec98/th03/formats/pi.hpp"

#define key_det input_sp
#include "compat/rec98/th01/hardware/grppsafx.h"
#include "compat/rec98/th03/snd/snd.h"
#include "src/mainl/cutscene/cutscene.hpp"

static const screen_y_t CUTSCENE_PIC_TOP = 64;
static const int CUTSCENE_PIC_SLOT = 0;

static const screen_x_t BOX_LEFT = 80;
static const screen_y_t BOX_TOP = 320;
static const pixel_t BOX_W = 480;
static const pixel_t BOX_H = (GLYPH_H * 4);

static const vram_byte_amount_t BOX_VRAM_W = (BOX_W / BYTE_DOTS);
static const screen_x_t BOX_RIGHT = (BOX_LEFT + BOX_W);
static const screen_y_t BOX_BOTTOM = (BOX_TOP + BOX_H);

static const shiftjis_ank_amount_t NAME_LEN = 6;
static const shiftjis_kanji_amount_t NAME_KANJI_LEN = (
	NAME_LEN / sizeof(shiftjis_kanji_t)
);

static const pixel_t NAME_W = ((NAME_LEN * GLYPH_HALF_W) + GLYPH_FULL_W);

static const int TEXT_INTERVAL_DEFAULT = ((GAME == 5) ? 2 : 1);

extern unsigned char far *script;

#define script_p script

extern Planar<dots16_t> far *box_bg;

extern bool fast_forward;

extern screen_point_t cursor;

extern int text_interval;
extern vc_t text_col;
extern uint8_t text_fx;

#pragma option -a2

#define box_wait_animate(frames_to_wait) { \
	input_wait_for_change(frames_to_wait); \
}

// Preserve original allocation size and B/R/G/E word-interleaved snapshots.
void near box_bg_allocate_and_snap(void);
void near box_bg_free(void);

inline void cutscene_input_sense(void) {
	input_mode_interface();
}

// The old script is freed first; allocation/read/close failures are unchecked.
bool16 pascal near cutscene_script_load(const char* fn)
{
	cutscene_script_free();

	if(!file_ropen(fn)) {
		return true;
	}
	size_t size = file_size();
	script = reinterpret_cast<unsigned char far *>(hmem_allocbyte(size));
	file_read(script_p, size);
	file_close();
	return false;
}

void near cutscene_script_free(void)
{
	if(script) {
		HMem<unsigned char>::free(script);
		script = nullptr;
	}
}

#define egc_start_copy	near egc_start_copy
#include "src/mainl/cutscene/egc_start_copy.inl"
#undef egc_start_copy

void pascal near pic_copy_to_other(screen_x_t left, vram_y_t top)
{
	vram_offset_t vo = vram_offset_shift(left, top);
	pixel_t y;
	vram_byte_amount_t vram_x;

	egc_start_copy();

	y = 0;
	while(y < CUTSCENE_PIC_H) {
		vram_x = 0;
		while(vram_x < CUTSCENE_PIC_VRAM_W) {
			egc_temp_t tmp;

			graph_accesspage(0);	tmp = egc_chunk(vo);
			graph_accesspage(1);	egc_chunk(vo) = tmp;

			vram_x += EGC_REGISTER_SIZE;
			vo += EGC_REGISTER_SIZE;
		}
		y++;
		vo += (ROW_SIZE - CUTSCENE_PIC_VRAM_W);
	}
	egc_off();

	graph_accesspage(0);
}

void pascal near pic_put_both_masked(
	screen_x_t left, vram_y_t top, int quarter, int mask_id
)
{
	enum {
		TEMP_ROW = RES_Y,
	};

	vram_word_amount_t vram_word;
	vram_offset_t vo_temp;
	pi_buffer_p_t row_p;

	pi_buffer_p_init_quarter(row_p, CUTSCENE_PIC_SLOT, quarter);

	graph_showpage(1);
	vram_offset_t vo = vram_offset_shift(left, top);
	graph_accesspage(0);
	for(pixel_t y = 0; y < CUTSCENE_PIC_H; y++) {

		graph_pack_put_8_noclip(0, TEMP_ROW, row_p, CUTSCENE_PIC_W);
		egc_start_copy();
		egc_setup_copy_masked(PI_MASKS[mask_id][y % PI_MASK_COUNT]);
		vo_temp = vram_offset_shift(0, TEMP_ROW);
		vram_word = 0;
		while(vram_word < (CUTSCENE_PIC_W / EGC_REGISTER_DOTS)) {
			egc_chunk(vo) = egc_chunk(vo_temp);
			vram_word++;
			vo += EGC_REGISTER_SIZE;
			vo_temp += EGC_REGISTER_SIZE;
		}
		egc_off();

		vo += (ROW_SIZE - CUTSCENE_PIC_VRAM_W);
		pi_buffer_p_offset(row_p, PI_W, 0);
		pi_buffer_p_normalize(row_p);
	}
	graph_showpage(0);
	pic_copy_to_other(left, top);
}

#define box_bg_snap_func(p, vo) { \
	(&box_bg->B)[p++] = VRAM_CHUNK(B, vo, 16); \
	(&box_bg->B)[p++] = VRAM_CHUNK(R, vo, 16); \
	(&box_bg->B)[p++] = VRAM_CHUNK(G, vo, 16); \
	(&box_bg->B)[p++] = VRAM_CHUNK(E, vo, 16); \
}

#define box_bg_put_func(p, vo) { \
	VRAM_CHUNK(B, vo, 16) = (&box_bg->B)[p++]; \
	VRAM_CHUNK(R, vo, 16) = (&box_bg->B)[p++]; \
	VRAM_CHUNK(G, vo, 16) = (&box_bg->B)[p++]; \
	VRAM_CHUNK(E, vo, 16) = (&box_bg->B)[p++]; \
}

#define box_bg_loop(func)   \
	size_t p; \
	vram_y_t src_y; \
	screen_x_t src_x; \
	pixel_t dst_y; \
	vram_byte_amount_t dst_byte; \
	vram_offset_t vo; \
	\
	p = 0; \
	src_y = BOX_TOP; \
	dst_y = 0; \
	while(dst_y < BOX_H) { \
		src_x = BOX_LEFT; \
		dst_byte = 0; \
		while(dst_byte < BOX_VRAM_W) { \
			vo = vram_offset_shift(src_x, src_y); \
			func(p, vo); \
			dst_byte += static_cast<vram_byte_amount_t>(sizeof(dots16_t)); \
			src_x += 16; \
		} \
		dst_y++; \
		src_y++; \
	}

void near box_bg_allocate_and_snap(void)
{
	box_bg_free();
	graph_accesspage(0);
	box_bg = HMem< Planar<dots16_t> >::alloc(
		((BOX_VRAM_W * BOX_H) / sizeof(dots16_t))
	);
	box_bg_loop(box_bg_snap_func);
}

void near box_bg_free(void)
{
	if(box_bg) {
		HMem< Planar<dots16_t> >::free(box_bg);
		box_bg = nullptr;
	}
}

void near box_bg_put(void)
{
	box_bg_loop(box_bg_put_func);
}

#undef extern
#include "src/mainl/cutscene/script.inl"

void near cursor_advance_and_animate(void)
{
	cursor.x += GLYPH_FULL_W;
	if(cursor.x >= BOX_RIGHT) {
		cursor.y += GLYPH_H;
		cursor.x = (BOX_LEFT + NAME_W);

		if(cursor.y >= BOX_BOTTOM) {

			if(!fast_forward) {
				box_wait_animate(0);
			}

			cursor.x = BOX_LEFT;
			cursor.y = BOX_TOP;

			graph_accesspage(1);	box_bg_put();
			graph_accesspage(0);	box_bg_put();
		}
	}
}

script_ret_t pascal near script_op(unsigned char c)
{

	int i;
	int p1;
	int p2;

	char fn[PF_FN_LEN + 3];

	c = tolower(c);
	switch(c) {
	case 'n':
		cursor.y += GLYPH_H;
		cursor.x = BOX_LEFT;
		if(cursor.y < BOX_BOTTOM) {
			break;
		}

	case 's':
		c = *script_p;
		if(c != '-') {
			script_param_read_number_first(p1, 0);
			if(!fast_forward) {
				box_wait_animate(p1);
			}
		} else {
			script_p++;
		}
		cursor.x = BOX_LEFT;
		cursor.y = BOX_TOP;

		graph_accesspage(1);	box_bg_put();
		graph_accesspage(0);	box_bg_put();
		break;

	case 'c':
		script_param_read_number_first(p1, V_WHITE);
		text_col = p1;
		break;

	case 'b':
		script_param_read_number_first(p1, WEIGHT_BOLD);
		switch(p1) {
		case WEIGHT_NORMAL:	text_fx = FX_WEIGHT_NORMAL;	break;
		case WEIGHT_HEAVY: 	text_fx = FX_WEIGHT_HEAVY; 	break;
		case WEIGHT_BOLD:  	text_fx = FX_WEIGHT_BOLD;  	break;
		case WEIGHT_BLACK: 	text_fx = FX_WEIGHT_BLACK; 	break;
		}
		break;

	case 'w':
		c = tolower(*script_p);
		if((c == 'o') || (c == 'i')) {
			script_op_fade(c, palette_white_in, palette_white_out, p1);
		} else {
			script_param_number_default = 64;
			if(c != 'm') {
				if(c == 'k') {
					script_p++;
				}
				script_param_read_number_first(p1);
				if(!fast_forward) {
					if(c != 'k')  {
						frame_delay(p1);
					} else {
						input_wait_for_ok(p1);
					}
				}
			} else {
				script_p++;
				c = *script_p;
				if(c == 'k') {
					script_p++;
				}
				script_param_read_number_first(p1);
				script_param_read_number_second(p2);
				if(!fast_forward) {

					if(c != 'k')  {
						snd_delay_until_measure(p1, p2);
					} else {
						input_wait_for_ok_or_measure(p1, p2);
					}
				}
			}
		}
		break;

	case 'v':
		if(*script_p != 'p') {
			script_param_read_number_first(p1, TEXT_INTERVAL_DEFAULT);
			text_interval = p1;
		} else {
			script_p++;
			script_param_read_number_first(p1, 0);
			graph_showpage(p1);
		}
		break;

	case 't':
		script_param_read_number_first(p1, 100);
		if(!fast_forward) {
			frame_delay(1);
		}
		palette_settone(p1);
		break;

	case 'f':
		c = *script_p;
		if(c != 'm') {
			if((c == 'i') || (c == 'o')) {
				script_op_fade(c, palette_black_in, palette_black_out, p1);
			}
		} else {
			script_p++;
			script_param_read_number_first(p1, 1);

			snd_kaja_interrupt((KAJA_SONG_FADE << 8) + p1);

			return CONTINUE;
		}
		break;

	// Keep both gaiji calls and their differing IDs. CF depends on the parser path
	// and 16-bit pointer wrap, not simply whether a numeric argument was present.
	case 'g':
		if((GAME == 5) || (*script_p != 'a')) {
			script_op_shake(fast_forward, p2, p1);
		} else {
			script_p++;
			script_param_read_number_first(p1, 0);

			graph_accesspage(1);

			graph_gaiji_putc(cursor.x, cursor.y, (p1 - 1), text_col);

			graph_accesspage(0);

			graph_gaiji_putc(cursor.x, cursor.y, p1, text_col);

			cursor_advance_and_animate();
		}
		return CONTINUE;

	case 'k':

		script_param_read_number_first(p1, 0);
		if(!fast_forward) {

			box_wait_animate((GAME >= 4) ? p1 : 0);
		}
		return CONTINUE;

	case '@':
		graph_accesspage(1);	graph_clear();
		graph_accesspage(0);	graph_clear();

		break;

	case 'p':
		c = *script_p;
		script_p++;

		if((c == '=') || (c == '@')) {
			graph_accesspage(1);
			if(c == '=') {
				pi_palette_apply(CUTSCENE_PIC_SLOT);
			}
			pi_put_8(0, 0, CUTSCENE_PIC_SLOT);
			graph_copy_page(0);
			graph_accesspage(0);
			box_bg_allocate_and_snap();
		} else if(c == '-') {
			pi_free(CUTSCENE_PIC_SLOT);
			return CONTINUE;
		} else if(c == 'p') {
			pi_palette_apply(CUTSCENE_PIC_SLOT);
			return CONTINUE;
		} else if(c != ',') {
			script_p--;
		} else {
			script_param_read_fn(fn, p1, c);
			pi_load(CUTSCENE_PIC_SLOT, fn);
		}
		break;

	case '=':
		script_param_number_default = PI_QUARTER_COUNT;
		c = *script_p;

		if(c != '=') {
			script_param_read_number_first(p1);

			graph_showpage(1);
			graph_accesspage(0);
			if(p1 < PI_QUARTER_COUNT) {
				pi_put_quarter_8(
					CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, CUTSCENE_PIC_SLOT, p1
				);
			} else {
				grcg_setcolor(GC_RMW, 0);
				grcg_boxfill_8(
					CUTSCENE_PIC_LEFT,
					CUTSCENE_PIC_TOP,
					(CUTSCENE_PIC_LEFT + CUTSCENE_PIC_W - 1),
					(CUTSCENE_PIC_TOP  + CUTSCENE_PIC_H - 1)
				);
				grcg_off();
			}
		} else {
			script_p++;
			script_param_read_number_first(p1);
			script_param_number_default = 1;
			script_param_read_number_second(p2);
			for(i = 0; i < PI_MASK_COUNT; i++) {
				pic_put_both_masked(CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, p1, i);
				if(!fast_forward) {
					frame_delay(p2);
				}
			}

			graph_showpage(1);
			graph_accesspage(0);

			pi_put_quarter_8(
				CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP, CUTSCENE_PIC_SLOT, p1
			);
		}
		graph_showpage(0);
		static_assert(CUTSCENE_PIC_W == PI_QUARTER_W);
		static_assert(CUTSCENE_PIC_H == PI_QUARTER_H);
		pic_copy_to_other(CUTSCENE_PIC_LEFT, CUTSCENE_PIC_TOP);
		break;

	case 'm':

		script_op_bgm(true, c, fn, p1);
		break;

	case 'e':
		script_param_read_number_first(p1);
		snd_se_play_force(p1);
		break;

	case '$':
		return STOP;
	}
	return CONTINUE;
}

void near cutscene_animate(void)
{
	extern ShiftJISKanji near CUTSCENE_KANJI[];

	unsigned char c;
	uint8_t speedup_cycle;

	ShiftJISKanji& kanji = *CUTSCENE_KANJI;

	cursor.x = BOX_LEFT;
	cursor.y = BOX_TOP;
	text_interval = TEXT_INTERVAL_DEFAULT;
	text_col = V_WHITE;
	text_fx = FX_WEIGHT_BOLD;

	speedup_cycle = 0;

	box_bg_allocate_and_snap();

	fast_forward = false;

	while(1) {
		cutscene_input_sense();
		if(key_det & INPUT_CANCEL) {
			fast_forward = true;
		} else {
			fast_forward = false;
		}

		// NUL is skipped as a control byte, not an EOF marker. Only the stop opcode exits.
		c = *(script_p++);
		if(str_sep_control_or_space(c)) {
			continue;
		}

		if(c == '\\') {
			c = *(script_p++);
			if(script_op(c) == STOP) {
				break;
			}
			continue;
		}

		kanji.byte[0] = c;
		c = *script_p;
		kanji.byte[1] = c;
		script_p++;

		graph_accesspage(1);
		graph_putsa_fx(cursor.x, cursor.y, (text_col | text_fx), kanji.byte);
		graph_accesspage(0);
		graph_putsa_fx(cursor.x, cursor.y, (text_col | text_fx), kanji.byte);
		cursor_advance_and_animate();

		if(fast_forward) {
			continue;
		}
		if(key_det == INPUT_NONE) {
			frame_delay(text_interval);
		} else {
			int speedup_interval = (text_interval / 3);
			if((speedup_cycle & 1) || speedup_interval) {
				if(speedup_interval == 0) {
					speedup_interval++;
				}
				frame_delay(speedup_interval);
			}
			speedup_cycle++;
		}
	}
	box_bg_put();
	box_bg_free();
}
