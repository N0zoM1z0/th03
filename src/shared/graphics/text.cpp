#pragma option -zCSHARED

#include <mbctype.h>
#include <mbstring.h>
#include "compat/rec98/planar.h"
#include "compat/rec98/libs/master.lib/pc98_gfx.hpp"
#include "compat/rec98/th01/hardware/grppsafx.h"

#include "src/shared/graphics/text_glyph.inl"

void DEFCONV graph_putsa_fx(
	screen_x_t left, vram_y_t top, int16_t col_and_fx, const shiftjis_t *str
)
{
	jis_t codepoint;
	dots_t(GLYPH_FULL_W) glyph_row;
	dots8_t far *vram;
	int fullwidth;
	int first_bit;
	int weight = (col_and_fx >> 4) & 3;
	pixel_t spacing = (col_and_fx >> 6) & 7;
	pixel_t line;
	dot_rect_t(GLYPH_FULL_W, GLYPH_H) glyph;
	register dots_t(GLYPH_FULL_W) glyph_row_tmp;

	grcg_setcolor(GC_RMW, (col_and_fx & (COLOR_COUNT - 1)));
	outportb(0x68, 0xB); // CG ROM dot access

	while(str[0]) {
		set_vram_ptr(vram, first_bit, left, top);
		get_glyph(glyph, codepoint, fullwidth, str, left, line);

		for(line = 0; line < GLYPH_H; line++) {
			apply_weight(glyph_row, glyph[line], glyph_row_tmp, weight);
			put_row_and_advance(vram, glyph_row, first_bit);
		}
		advance_left(left, fullwidth, spacing);
	}

	outportb(0x68, 0xA); // CG ROM code access
	grcg_off();
}
