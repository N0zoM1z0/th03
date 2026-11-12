#include "round.hpp"
#include <algorithm>

namespace th03 {
void Round::begin_pause(const Resident& resident) {
    if(resident.cpu[0]&&resident.cpu[1]) {
        pause=Pause::fade;pause_fade_frame=0;palette_tone=100;
    } else {
        sounds.push_back(255);sounds.push_back(21);pause=Pause::release;
    }
}
bool Round::pause_tick(std::uint16_t input) {
    switch(pause) {
    case Pause::none:return false;
    case Pause::fade:
        if(pause_fade_frame++)palette_tone=std::max<std::int16_t>(0,std::int16_t(palette_tone-6));
        if(!palette_tone) {quit_requested=true;pause=Pause::none;}
        break;
    case Pause::release:
        if(!input)pause=Pause::command;
        break;
    case Pause::command:
        if(input&q) {quit_requested=true;pause=Pause::none;}
        else if(input&cancel)pause=Pause::resume_release;
        break;
    case Pause::resume_release:
        if(!input)pause=Pause::resume_finish;
        break;
    case Pause::resume_finish:
        sounds.push_back(255);sounds.push_back(21);pause=Pause::none;
        break;
    }
    return pause!=Pause::none;
}
void Round::warning_text_put(unsigned pid,std::uint16_t attribute) {
    auto& text=warning_text.at(pid);
    text.attribute=attribute;text.boss=gauge_next[pid]==5;
    text.level=text.boss ? boss_level : gauge_levels[pid];text.visible=true;
}
void Round::prepare_warning_portraits() {
    for(unsigned pid=0;pid<2;++pid) {
        warning_portrait[pid]=warning[pid]==1;
        if(warning_portrait[pid])warning[pid]=2;
    }
}
bool Round::begin_warning_flash() {
    if(warning[0]!=2&&warning[1]!=2)return false;
    sounds.push_back(255);sounds.push_back(19);
    for(unsigned pid=0;pid<2;++pid)if(warning[pid]==2) {
        warning[pid]=3;warning_text_put(pid,0xe1);
    }
    warning_flash_frame=0;
    return true;
}
bool Round::warning_flash_tick() {
    if(warning_flash_frame>=27)return false;
    palette_tone=std::int16_t(100+(warning_flash_frame&1)*50);
    ++warning_flash_frame;
    return warning_flash_frame<27;
}
void Round::warning_update(unsigned pid) {
    auto& flag=warning.at(pid);const auto attacked=pid^1;
    const auto restore=[&] {std::copy_n(palette_backup.begin()+attacked*3,3,palette.begin()+attacked*3);};
    auto& brightness=warning_brightness[pid];auto& fading=warning_fading_out[pid];
    if(flag>=3) {
        if(flag==3)brightness=0;
        if(flag<33) {
            brightness=std::uint8_t(brightness+(flag<18 ? 13 : -13));
            ++flag;
            std::uint16_t attribute=1;
            if(flag&1) {
                attribute=gauge_next[pid]==1 ? 0xa1 : gauge_next[pid]==3 ? 0x61 : 0x41;
                restore();
            } else {
                if(gauge_next[pid]==1)palette[attacked*3+2]=120;
                else if(gauge_next[pid]==3)palette[attacked*3]=palette[attacked*3+2]=120;
                else palette[attacked*3]=120;
            }
            warning_text_put(pid,attribute);
        } else {
            warning_text[pid].visible=false;restore();flag=0;
            gauge_flags[pid]=gauge_next[pid];brightness=fading=0;
        }
    }
    // The completion call starts the active pulse immediately.
    if(gauge_flags[pid]) {
        brightness=std::uint8_t(brightness+(fading ? -4 : 4));
        if(!fading&&brightness>=144)fading=1;
        else if(fading&&brightness==0)fading=0;
        palette[attacked*3]=brightness;
    }
}
}
