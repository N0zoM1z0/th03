#include "score_menu.hpp"
#include <algorithm>
#include <cstdio>
#include <stdexcept>

namespace th03 {
namespace {
constexpr const char* character_names[]={
    "\x20\x20\x4e\x6f\x20\x45\x6e\x74\x72\x79\x21\x20",
    "\x81\x40\x81\x40\xe8\xcb\x96\xb2\x81\x40\x81\x40",
    "\x81\x40\x81\x40\x96\xa3\x96\x82\x81\x40\x81\x40",
    "\x20\x81\x40\x96\x82\x97\x9d\x8d\xb9\x81\x40\x20",
    "\x20\x81\x40\x83\x47\x83\x8c\x83\x93\x81\x40\x20",
    "\x20\x81\x40\x8f\xac\x93\x65\x95\x50\x81\x40\x20",
    "\x20\x81\x40\x20\x83\x4a\x83\x69\x20\x20\x20\x20",
    "\x20\x81\x40\x97\x9d\x8d\x81\x8e\x71\x20\x20\x20",
    "\x20\x81\x40\x82\xbf\x82\xe4\x82\xe8\x81\x40\x20",
    "\x20\x81\x40\x20\x96\xb2\x94\xfc\x81\x40\x20\x20"
};
int name_left(std::uint8_t cursor) {return 72+(7-int(cursor))*24;}
}
ScoreMenu::ScoreMenu(const PfArchive& assets,const Font& font,ScoreFile& file,const Resident& resident):
    font_(font),file_(file),resident_(resident),seed_(resident.seed),normal_(assets.read("REGI2.BFT")),highlight_(assets.read("REGI1.BFT")) {
    if(!font.present())throw std::runtime_error("score menu requires --font-bmp FILE");
    sounds.push_back({SceneSound::Kind::load,"SCORE.M",0});sounds.push_back({SceneSound::Kind::control,{},0});
    section=file_.load(resident.options.rank,seed_,resident);
    if(resident.stage!=255)place=section.insert(resident);
    const auto image=decode_pi(assets.read("REGIB.PI"));picture(canvas_,image);palette_=image.palette;
    char filename[16];std::snprintf(filename,sizeof(filename),"RFT%u.CDG",unsigned(resident.options.rank));
    Cdg(assets.read(filename)).put(canvas_,0,320,312);
    normal_.apply_palette(palette_);highlight_.apply_palette(palette_);
    background_=canvas_;rows();
    if(place>=0) {
        background_=canvas_;
        for(unsigned code=0;code<48;++code)sprite(64+int(code%16)*32,320+int(code/16)*24,code,false);
    }
}
void ScoreMenu::sprite(int x,int y,unsigned code,bool bright) {
    const auto& font=bright ? highlight_ : normal_;
    // SUPER_PUT shifts the unsigned WORD x before adding y*80. The last
    // name-entry preview inherits a negative x after cursor255 and therefore
    // lands elsewhere in visible VRAM rather than clipping offscreen.
    const auto origin=std::uint16_t(y*80+(std::uint16_t(x)>>3));
    for(unsigned row=0;row<font.height;++row)for(unsigned column=0;column<font.width;++column) {
        const auto color=font.pixel(code,column,row);if(!color)continue;
        const auto at=unsigned(std::uint16_t(origin+row*80))*8+unsigned(x&7)+column;
        if(at<canvas_.pixels.size())canvas_.pixels[at]=color;
    }
}
void ScoreMenu::glyph(int x,int y,unsigned code,bool bright) {
    sprite(x,y,code,bright);
    if(code%16==14)sprite(x+32,y,code+1,bright);
}
void ScoreMenu::alphabet(unsigned code,bool bright) {glyph(64+int(code%16)*32,320+int(code/16)*24,code,bright);}
void ScoreMenu::unput(std::uint8_t cursor) {
    const auto origin=std::uint16_t((104+place*20)*80+(name_left(cursor)>>3));
    for(unsigned y=0;y<32;++y)for(unsigned x=0;x<32;++x) {
        const unsigned at=unsigned(std::uint16_t(origin+y*80))*8+x;
        if(at<canvas_.pixels.size())canvas_.pixels[at]=background_.pixels[at];
    }
}
void ScoreMenu::row(unsigned index) {
    const bool bright=place<0||place==int(index);const int y=104+int(index)*20;int x=24;
    if(index==9) {glyph(x-8,y,33,bright);glyph(x+8,y,32,bright);}else glyph(x,y,33+index,bright);
    x+=48;
    for(int c=7;c>=0;--c,x+=24) {
        const unsigned code=section.bytes[ScoreSection::names+index*8+unsigned(c)];
        if(code!=regi::space)glyph(x,y,code,bright);
    }
    x+=16;bool leading=true;
    for(int c=9;c>=0;--c,x+=16) {
        const unsigned code=section.bytes[ScoreSection::scores+index*10+unsigned(c)];
        if(code!=regi::zero)leading=false;
        if(!leading)glyph(x,y,code,bright);
    }
    x+=16;
    font_.text(canvas_,x,y+8,character_names[section.bytes[ScoreSection::characters+index]],bright ? 15 : 4,2);
    x+=112;glyph(x,y,section.bytes[ScoreSection::stages+index],bright);
}
void ScoreMenu::rows() {canvas_=background_;for(unsigned index=0;index<10;++index)row(index);}
void ScoreMenu::edit(std::uint16_t input) {
    if(name.tick(input,section,unsigned(place))) {
        for(unsigned i=0;i<name.old_count;++i)alphabet(name.old_letters[i],false);
        for(unsigned i=0;i<name.erase_count;++i)unput(name.erased[i]);
        alphabet(name.letter,true);row(unsigned(place));
        if(name.letter%16!=14)glyph(name_left(name.cursor),104+place*20,name.letter,false);
    }
    if(name.done) {state_=State::name_finish;wait_=1;}
}
void ScoreMenu::tick(std::uint16_t input,std::optional<unsigned> volume) {
    if(done())return;
    if(state_==State::volume_wait) {if(!volume||*volume==255){sounds.push_back({SceneSound::Kind::control,{},0x100});state_=State::done;}return;}
    if(state_==State::fade_in||state_==State::fade_out) {
        if(--wait_)return;
        if(state_==State::fade_in) {
            tone_=std::min(tone_+6,100);wait_=2;
            if(tone_<100)return;
            state_=place<0 ? State::release : State::name;
        } else {
            tone_=std::max(tone_-6,0);wait_=2;
            if(!tone_) {
                file_.save(section,resident_.options.rank,seed_,resident_);state_=State::done;
                if(!resident_.credits||resident_.stage==99) {
                    if(volume&&*volume!=255)state_=State::volume_wait;
                    else sounds.push_back({SceneSound::Kind::control,{},0x100});
                }
            }
            return;
        }
    }
    if(state_==State::name) {edit(input);return;}
    if(state_==State::name_finish) {
        section.default_name(unsigned(place),character_id(resident_.paletted[0]));rows();state_=State::release;
    }
    if(state_==State::release) {if(input)return;state_=State::press;}
    if(state_==State::press&&input) {if(!resident_.credits||resident_.stage==99)sounds.push_back({SceneSound::Kind::control,{},0x210});state_=State::fade_out;wait_=3;}
}
ContinueMenu::ContinueMenu(const PfArchive& assets,const Font& font,Resident& resident):
    assets_(assets),font_(font),resident_(resident),choices_(assets.read("CONTI.CD2")) {
    resident.scores={};
    const auto image=decode_pi(assets.read(resident.credits ? "CONTI.PI" : "OVER.PI"));picture(canvas_,image);palette_=image.palette;
    if(!resident.credits) {selected=false;state_=State::done;return;}
    choices();credits();
}
void ContinueMenu::choices() {choices_.put(canvas_,2-unsigned(selected)*2,192,272,false);choices_.put(canvas_,unsigned(selected)*2+1,352,272,false);}
void ContinueMenu::credits() {
    const char digit=char('0'+resident_.credits);font_.text(canvas_,576,371,std::string_view(&digit,1),15,2);
}
void ContinueMenu::tick(std::uint16_t input) {
    if(done())return;
    if(state_==State::fade_in||state_==State::fade_out) {
        if(--wait_)return;
        if(state_==State::fade_in) {tone_=std::min(tone_+6,100);wait_=1;if(tone_<100)return;state_=State::input;}
        else {
            tone_=std::max(tone_-6,0);wait_=1;
            if(!tone_) {
                const auto image=decode_pi(assets_.read("OVER.PI"));canvas_=Canvas{};picture(canvas_,image);palette_=image.palette;
                sounds.push_back({SceneSound::Kind::control,{},0x100});--resident_.stage;resident_.lives=2;state_=State::done;
            }
            return;
        }
    }
    if(input&(left|right)) {if(!held_) {selected=!selected;choices();}held_=true;}else held_=false;
    if(input&(ok|shot)) {
        if(selected) {--resident_.credits;canvas_.fill(576,371,592,387,0);credits();}
        sounds.push_back({SceneSound::Kind::control,{},0x203});state_=State::fade_out;wait_=2;
    } else if(input&cancel) {selected=false;sounds.push_back({SceneSound::Kind::control,{},0x203});state_=State::fade_out;wait_=2;}
}
GameOver::GameOver(const PfArchive& assets) {
    const auto image=decode_pi(assets.read("OVER.PI"));picture(canvas_,image);palette_=image.palette;
}
void GameOver::tick() {
    if(done()||--wait_)return;
    if(state_==State::fade_in) {tone_=std::min(tone_+6,100);wait_=1;if(tone_==100) {state_=State::hold;wait_=64;}}
    else if(state_==State::hold) {state_=State::fade_out;wait_=2;}
    else {tone_=std::max(tone_-6,0);wait_=1;if(!tone_)state_=State::done;}
}
}
