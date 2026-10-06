// TH03 OP Music Room bounded include; complete carrier reviewed separately.
void pascal near polygon_build(
	screen_point_t near* points,
	screen_x_t center_x,
	space_changing_pixel_t center_y,
	pixel_t radius,
	int point_count,
	unsigned char plus_angle
)
{
	int i;

	// ZUN bloat: center_y.pixel = center_y.sp.to_pixel();
	center_y.sp.v >>= SUBPIXEL_BITS;

	for(i = 0; i < point_count; i++) {
		unsigned char point_angle = (((i << 8) / point_count) + plus_angle);
		points[i].x = polar_x(center_x, radius, point_angle);
		points[i].y = polar_y(center_y.pixel, radius, point_angle);
	}
	points[i].x = points[0].x;
	points[i].y = points[0].y;
}

#define polygon_init(i, center_y, velocity_x) { \
	center[i].x = (irand() % RES_X); \
	center[i].y.v = center_y; \
	velocity[i].x = velocity_x; \
	if(velocity[i].x == 0) { \
		velocity[i].x = 1; \
	} \
	velocity[i].y.v = (to_sp(2.0f) + TO_SP(irand() & 3)); \
	angle[i] = irand(); \
	angle_speed[i] = (0x04 - (irand() & 0x07)); \
	if(angle_speed[i] == 0x00) { \
		angle_speed[i] = 0x04; \
	} \
}

inline int polygon_vertex_count(int polygon_index) {
	return ((polygon_index / 4) + 3);
}

void near polygons_update_and_render(void)
{
	int i;
	if(!polygons_initialized) {
		for(i = 0; i < POLYGONS_RENDERED; i++) {
			polygon_init(i, (irand() % to_sp(RES_Y)), (4 - (irand() & 7)));
		}

		// ZUN quirk: This is never reset.
		polygons_initialized = true;
	}
	for(i = 0; i < POLYGONS_RENDERED; i++) {
		polygon_build(
			points,
			center[i].x,
			reinterpret_cast<space_changing_pixel_t &>(center[i].y),
			(((i & 3) * 16) + 64),
			polygon_vertex_count(i),
			angle[i]
		);
		center[i].x += velocity[i].x;
		center[i].y.v += velocity[i].y.v;
		angle[i] += angle_speed[i];
		if((center[i].x <= 0) || (center[i].x >= (RES_X - 1))) {
			velocity[i].x *= -1;
		}

		// Original reset is -100 pixels; actual TH03 radii range from 64 to 112.
		if(center[i].y >= to_sp(RES_Y + 100.0f)) {
			polygon_init(i, to_sp(-100.0f), (8 - (irand() & 15)));
		}

		grcg_polygon_c(points, polygon_vertex_count(i));
	}
}

// ZUN bloat
#define frame_delay frame_delay_2

void near music_update_render_and_flip(void)
{
	nopoly_B_put();

	// Original GRCG arguments restrict the requested operation to the B plane.
	grcg_setcolor((GC_RMW | GC_B), 0xF);
	polygons_update_and_render();
	grcg_off();

	graph_showpage(music_page_accessed);
	music_page_accessed = (1 - music_page_accessed);
	graph_accesspage(music_page_accessed);

	// Original ordering: flip pages, then call the external frame delay.
	frame_delay(1);
}

#define cmt_bg_blit_planar(cmt_bg_p, vo, x, dst, dst_p, src, src_p) \
	size_t cmt_bg_p = 0; \
	screen_y_t y; \
	for(y = CMT_TITLE_TOP; y < CMT_TITLE_BOTTOM; y++) { \
		for(x = CMT_TITLE_LEFT; x < CMT_TITLE_RIGHT; x += 32) { \
			vo = vram_offset_shift(x, y); \
			*(dots32_t *)(dst[0] + dst_p) = *(dots32_t *)(src[0] + src_p); \
			*(dots32_t *)(dst[1] + dst_p) = *(dots32_t *)(src[1] + src_p); \
			*(dots32_t *)(dst[2] + dst_p) = *(dots32_t *)(src[2] + src_p); \
			*(dots32_t *)(dst[3] + dst_p) = *(dots32_t *)(src[3] + src_p); \
			cmt_bg_p += sizeof(dots32_t); \
		} \
	} \
	for(y = CMT_COMMENT_TOP; y < CMT_COMMENT_BOTTOM; y++) { \
		for(x = CMT_COMMENT_LEFT; x < CMT_COMMENT_RIGHT; x += 32) { \
			vo = vram_offset_shift(x, y); \
			*(dots32_t *)(dst[0] + dst_p) = *(dots32_t *)(src[0] + src_p); \
			*(dots32_t *)(dst[1] + dst_p) = *(dots32_t *)(src[1] + src_p); \
			*(dots32_t *)(dst[2] + dst_p) = *(dots32_t *)(src[2] + src_p); \
			*(dots32_t *)(dst[3] + dst_p) = *(dots32_t *)(src[3] + src_p); \
			cmt_bg_p += sizeof(dots32_t); \
		} \
	}

void near cmt_bg_snap(void)
{
	screen_x_t x;
	vram_offset_t vo;
	for(int i = 0; i < PLANE_COUNT; i++) {
		cmt_bg[i] = HMem<dots8_t>::alloc(
			(GLYPH_H * CMT_LINE_VRAM_W) + (CMT_COMMENT_H * CMT_LINE_VRAM_W)
		);
	}
	cmt_bg_blit_planar(cmt_bg_p, vo, x, cmt_bg, cmt_bg_p, VRAM_PLANE, vo);
}

void pascal near cmt_load(int track)
{
	file_ropen("MUSIC.TXT");
	file_seek((track * int(sizeof(cmt))), SEEK_SET);
	file_read(cmt, sizeof(cmt));
	file_close();
	for(int i = 0; i < CMT_LINES; i++) {
		cmt[i].c[CMT_LINE_LENGTH] = '\0';
	}
}

// ZUN bloat: TH05 has the most straightforward version of this code.
#define cmt_put_macro(fx) \
	graph_putsa_fx( \
		CMT_TITLE_LEFT, CMT_TITLE_TOP, (COL_CMT_TRACK | fx), cmt[0].c \
	); \
	for(int line = 1; line < CMT_LINES; line++) { \
		if((GAME >= 4) && (cmt[line].c[0] == ';')) { \
			continue; \
		} \
		graph_putsa_fx( \
			CMT_COMMENT_LEFT, \
			((line + ((CMT_COMMENT_TOP - 1) / GLYPH_H)) * GLYPH_H), \
			(COL_CMT_COMMENT | fx), \
			cmt[line].c \
		); \
	}

void near cmt_bg_free(void)
{
	HMem<dots8_t>::free(cmt_bg.B);
	HMem<dots8_t>::free(cmt_bg.R);
	HMem<dots8_t>::free(cmt_bg.G);
	HMem<dots8_t>::free(cmt_bg.E);
}

void near cmt_unput(void)
{
	screen_x_t x;
	vram_offset_t vo;
	cmt_bg_blit_planar(cmt_bg_p, vo, x, VRAM_PLANE, vo, cmt_bg, cmt_bg_p);
}

void pascal near cmt_load_unput_and_put(int track)
{
	// ZUN bloat: This function is called once per VRAM page, but we only need
	// to load the track once.
	cmt_load(track);

	nopoly_B_put();
	cmt_unput();
	cmt_put_macro(FX_WEIGHT_HEAVY);

	// Recapture all 32000 B-plane bytes after each page's comment draw.
	// Equality of physical pages is not established by the reply fixture.
	for(vram_offset_t p = 0; p < PLANE_SIZE; p += int(sizeof(dots32_t))) {
		*reinterpret_cast<dots32_t *>(nopoly_B + p) = VRAM_CHUNK(B, p, 32);
	}
}

// Input wrappers
// --------------
#define key_det input_sp

// Same game-specific branches as in the TH03/TH04/TH05 cutscene system, but
// with a different, much smaller effect here.
//
// The native caller waits for supplied input to clear. Hardware key filtering
// and polling duration remain external to the Music Room fixture.
inline void music_input_sense(void) {
	input_mode_interface();
}
// --------------


void MUSICROOM_DISTANCE musicroom_menu(void)
{
	enum {
		SEL_QUIT = (TRACK_COUNT + 1),
	};


	// ZUN bloat: The call site would have been a better place for this.
	for(int i = 0; i < CDG_SLOT_COUNT; i++) {
		cdg_free(i);
	}
	super_free();
	text_clear();

	music_page_accessed = 1;

	palette_settone(0);
	graph_showpage(0);

	// ZUN bloat: We copy page 1 to page 0 below anyway. The hardware palette
	// is also entirely black, so no one will ever see a difference.
	graph_accesspage(0);
	graph_clear();

	graph_accesspage(1);

	pi_fullres_load_palette_apply_put_free(0, "op3.pi");

	music_sel = track_playing;

	// ZUN bloat: We copy pages below anyway, this doesn't need to be blitted
	// to both.
	tracklist_put_both(music_sel);
	graph_copy_page(0);

	graph_accesspage(1);
	graph_showpage(0);

	nopoly_B_snap();

	cmt_bg_snap();
	graph_accesspage(1);	cmt_load_unput_and_put(track_playing);
	graph_accesspage(0);	cmt_load_unput_and_put(track_playing);

	palette_100();

	while(1) {
		// In TH05, this loop also ignores any ← or → inputs while ↑ or ↓ are
		// held, and vice versa.
		// ZUN bloat: None of this `goto` business would have been necessary if
		// the loop clearly defined its update and render steps. Especially
		// since it does want to render the polygon animation every frame.
		while(1) {
			music_input_sense();
			if(!key_det) {
				break;
			}
			music_update_render_and_flip();
		}
controls:
		// ZUN bloat: We already did that for this frame if we came from above,
		// but not if we came from the `goto` below.
		music_input_sense();

		if(key_det & INPUT_UP) {
			track_put_both(music_sel, COL_TRACKLIST);
			if(music_sel > 0) {
				music_sel--;
			} else {
				music_sel = SEL_QUIT;
			}

			// Skip over the empty line
			if(music_sel == TRACK_COUNT) {
				music_sel--;
			}

			track_put_both(music_sel, COL_TRACKLIST_SELECTED);
		}
		if(key_det & INPUT_DOWN) {
			track_put_both(music_sel, COL_TRACKLIST);
			if(music_sel < SEL_QUIT) {
				music_sel++;
			} else {
				music_sel = 0;
			}

			// Skip over the empty line
			if(music_sel == TRACK_COUNT) {
				music_sel++;
			}

			track_put_both(music_sel, COL_TRACKLIST_SELECTED);
		}
	skip_processing_of_left_and_right:
		if(key_det & INPUT_SHOT || key_det & INPUT_OK) {
			if(music_sel != SEL_QUIT) {
				// Original ordering stops the previous song before loading.
				snd_kaja_func(KAJA_SONG_STOP, 0);
				snd_load(MUSIC_FILES[music_sel], SND_LOAD_SONG);
				snd_kaja_func(KAJA_SONG_PLAY, 0);
				track_playing = music_sel;
				cmt_load_unput_and_put(music_sel);
				music_update_render_and_flip();
				cmt_load_unput_and_put(music_sel);
			} else {
				break;
			}
		}
		if(key_det & INPUT_CANCEL) {
			break;
		}
		if(!key_det) {
			music_update_render_and_flip();
			goto controls;
		}
	};

	// Wait until the player released the key that broke out of the loop
	while(1) {
		music_input_sense();
		if(!key_det) {
			break;
		}
		music_update_render_and_flip();
	}

	nopoly_B_free();
	cmt_bg_free();
	graph_showpage(0);

	graph_accesspage(0);
	graph_clear();

	graph_accesspage(1);


	graph_accesspage(0);
}
