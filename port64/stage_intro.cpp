#include "stage_intro.hpp"
#include <algorithm>
#include <cstdio>
#include <stdexcept>

namespace th03 {
namespace {
// CP932 titles/names from src/mainl/data/root_strings.inl, in character order.
constexpr const char* titles[9]={
    "\x20\x20\x20\x96\xb2\x82\xc6\x93\x60\x93\x9d\x82\xf0\x95\xdb\x8e\xe7\x82\xb7\x82\xe9\x9b\xde\x8f\x97\x20\x20\x20",
    "\x20\x8b\x76\x89\x93\x82\xcc\x96\xb2\x82\xc9\x89\x5e\x96\xbd\x82\xf0\x94\x43\x82\xb9\x82\xe9\x90\xb8\x90\x5f\x20",
    "\x20\x20\x20\x96\x82\x96\x40\x82\xc6\x8d\x67\x96\xb2\x82\xa9\x82\xe7\x82\xc8\x82\xe9\x91\xb6\x8d\xdd\x20\x20\x20",
    "\x82\xcd\x82\xbd\x82\xe7\x82\xab\x82\xe0\x82\xcc\x82\xc5\x97\xf6\x82\xf0\x96\xb2\x8c\xa9\x82\xe9\x96\x82\x8f\x97",
    "\x20\x20\x20\x20\x20\x92\x65\x96\x8b\x82\xc9\x94\xfc\x82\xf0\x96\xb2\x82\xdd\x82\xe9\x95\x50\x20\x20\x20\x20\x20",
    "\x20\x20\x20\x20\x20\x96\xb2\x82\xf0\x8e\xb8\x82\xc1\x82\xbd\x8f\xad\x8f\x97\x91\x9b\x97\xec\x20\x20\x20\x20\x20",
    "\x20\x20\x81\x40\x81\x40\x81\x40\x96\xb2\x82\xf0\x92\x54\x82\xb7\x89\xc8\x8a\x77\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x81\x40\x20\x20\x8e\x9e\x82\xf0\x82\xa9\x82\xaf\x82\xe9\x96\xb2\x8c\xb6\x82\xcc\x8f\x5a\x90\x6c\x20\x20\x20\x20",
    "\x81\x40\x20\x20\x81\x40\x81\x40\x81\x40\x96\xb2\x8c\xb6\x93\x60\x90\xe0\x81\x40\x81\x40\x81\x40\x20\x20\x20\x20"
};
constexpr const char* names[9]={
    "\x20\x20\x20\x94\x8e\x97\xed\x81\x40\xe8\xcb\x96\xb2",
    "\x20\x20\x20\x20\x20\x96\xa3\x20\x96\x82",
    "\x20\x20\x96\xb6\x89\x4a\x81\x40\x96\x82\x97\x9d\x8d\xb9\x20",
    "\x81\x40\x81\x40\x83\x47\x83\x8c\x83\x93",
    "\x20\x20\x20\x20\x8f\xac\x93\x65\x95\x50",
    "\x83\x4a\x83\x69\x81\x45\x83\x41\x83\x69\x83\x78\x83\x89\x83\x8b",
    "\x81\x40\x92\xa9\x91\x71\x81\x40\x97\x9d\x8d\x81\x8e\x71",
    "\x20\x96\x6b\x94\x92\x89\xcd\x81\x40\x82\xbf\x82\xe4\x82\xe8",
    "\x20\x81\x40\x89\xaa\x8d\xe8\x81\x40\x96\xb2\x94\xfc"
};
}
StageIntro::StageIntro(const PfArchive& assets,const Font& font,Resident& resident) {
    if(!font.present())throw std::runtime_error("stage introduction requires --font-bmp FILE");
    if(resident.mode==Mode::story)resident.paletted[1]=resident.opponents.at(resident.stage);
    const auto opponent=character_id(resident.paletted[1]);
    unsigned background=1;
    bool number=false;
    if(resident.mode!=Mode::story)background=5;
    else if(opponent==7)background=3;
    else if(opponent==8)background=2;
    else if(resident.stage==6)background=4;
    else number=true;
    char filename[16];
    // stage_load first draws the blank, then overlays the stage background.
    picture(canvas_,decode_pi(assets.read("STNX0.PI")));
    std::snprintf(filename,sizeof(filename),"STNX%u.PI",background);
    const auto image=decode_pi(assets.read(filename));
    picture(canvas_,image);palette_=image.palette;
    for(unsigned p=0;p<2;++p) {
        const auto id=character_id(resident.paletted[p]);
        if(id>=9)throw std::runtime_error("invalid stage character");
        std::snprintf(filename,sizeof(filename),"%02uSL.CD2",id*2);
        Cdg(assets.read(filename)).put(canvas_,(resident.paletted[p]-1)&1,p ? 352 : 96,96,true,p!=0);
        font.text(canvas_,p ? 336 : 80,292,titles[id],15,2);
        font.text(canvas_,p ? 384 : 128,308,names[id],15,2);
    }
    if(number)Cdg(assets.read("ST.CD2")).put(canvas_,resident.stage+1,384,46);
    std::snprintf(filename,sizeof(filename),"%02uMM.M",opponent);
    music_=resident.stage==6 ? "DEC.M" : filename;
}
void StageIntro::tick(std::uint16_t input) {
    if(done_)return;
    ++age_;
    if(state_==State::black_in) {
        tone_=std::min(tone_+6,100);
        if(tone_==100) {state_=State::wait;wait_=0;}
    } else if(state_==State::wait) {
        ++wait_;
        if(wait_>96||(wait_>32&&input))state_=State::white_out;
    } else if(state_==State::white_out) {
        tone_=std::min(tone_+6,200);
        if(tone_==200) {canvas_=Canvas{};state_=State::white_in;}
    } else {
        tone_=std::max(tone_-6,100);
        if(tone_==100)done_=true;
    }
}
}
