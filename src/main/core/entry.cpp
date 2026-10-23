// Candidate for MAIN load 96E6..9778; existing strings/storage stay external.
#pragma codeseg PLAYFLD_TEXT main_01
#include "src/main/core/entry.hpp"
// MAIN_EXEC returns far but shares the caller's MAIN_01 code frame.
#pragma samecodeseg main_exec

void far cdecl main(void)
{
    register int outcome;
    game_init_main(main_archive_name);
    if(cfg_load_resident_ptr()) {
        snd_midi_active = 0;
        if(resident->bgm_mode != SND_BGM_OFF) {
            snd_determine_mode();
        }
        gaiji_backup();
        gaiji_entry_bfnt(main_gaiji_font);
        stage_setup();
        main_background_init();
        for(;;) {
            PaletteTone = 100;
            palette_show();
            outcome = round_loop();
            resident->rand = round_frame;
            if(outcome != 1) {
                break;
            }
            round_start_next();
        }
        enemy_formations_free();
        snd_kaja_func(KAJA_SONG_STOP, 0);
        if(outcome == 0) {
            main_exec(main_op_name);
        } else {
            resident->story_stage++;
            main_exec(main_ending_name);
        }
    }
}
