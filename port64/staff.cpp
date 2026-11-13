#include "staff.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
constexpr std::uint16_t flake_masks[4][8]={
    {0x003c,0x007e,0x00ff,0x00ff,0x00ff,0x00ff,0x007e,0x003c},
    {0,0x0018,0x003c,0x007e,0x007e,0x003c,0x0018,0},
    {0,0,0x0018,0x003c,0x003c,0x0018,0,0},
    {0,0,0,0x0018,0x0018,0,0,0}
};
constexpr std::uint16_t dissolve_masks[8][4]={
    {0xffff,0xffff,0xffff,0xffff},{0x2222,0x5555,0x8888,0x5555},
    {0xaaaa,0x5555,0xaaaa,0x5555},{0xeeee,0x5555,0xbbbb,0x5555},
    {0xeeee,0x7777,0xbbbb,0xdddd},{0xffff,0x5555,0xffff,0x5555},
    {0xffff,0xeeee,0xffff,0xbbbb},{0xffff,0x7777,0xffff,0xffff}
};
struct Segment {unsigned slot,enter_measure,leave_measure;};
constexpr Segment segments[]={{0,8,10},{1,16,20},{2,22,24},{3,32,34},
    {4,36,38},{11,42,44},{5,48,50},{6,54,56},{10,60,62}};
constexpr const char* names[]={
    "\x20\x20\x20\x94\x8e\x97\xed\x81\x40\xe8\xcb\x96\xb2",
    "\x20\x20\x20\x20\x20\x96\xa3\x20\x96\x82",
    "\x20\x20\x96\xb6\x89\x4a\x81\x40\x96\x82\x97\x9d\x8d\xb9\x20",
    "\x81\x40\x81\x40\x83\x47\x83\x8c\x83\x93",
    "\x20\x20\x20\x20\x8f\xac\x93\x65\x95\x50",
    "\x83\x4a\x83\x69\x81\x45\x83\x41\x83\x69\x83\x78\x83\x89\x83\x8b",
    "\x81\x40\x92\xa9\x91\x71\x81\x40\x97\x9d\x8d\x81\x8e\x71",
    "\x20\x96\x6b\x94\x92\x89\xcd\x81\x40\x82\xbf\x82\xe4\x82\xe8",
    "\x20\x81\x40\x89\xaa\x8d\xe8\x81\x40\x96\xb2\x94\xfc",
};
constexpr const char* ranks[]={
    "\x20\x20\x20\x82\x64\x82\x81\x82\x93\x82\x99",
    "\x20\x82\x6d\x82\x8f\x82\x92\x82\x8d\x82\x81\x82\x8c",
    "\x20\x20\x20\x82\x67\x82\x81\x82\x92\x82\x84",
    "\x82\x6b\x82\x95\x82\x8e\x82\x81\x82\x94\x82\x89\x82\x83",
};
constexpr const char* digits[]={
    "\x82\x4f",
    "\x82\x50",
    "\x82\x51",
    "\x82\x52",
    "\x82\x53",
    "\x82\x54",
    "\x82\x55",
    "\x82\x56",
    "\x82\x57",
    "\x82\x58",
};
}
void StaffSnow::update(std::int16_t frame) {
    const auto irand=[&] {return random_next(seed)&0x7fff;};
    for(unsigned i=0;i<limit;++i) {
        auto& f=flakes[i];
        if(!f.alive&&int(i*8)<=frame) {
            f.alive=true;
            if(i&3)f.position={std::int16_t(irand()%10112),0};
            else f.position={10112,std::int16_t(irand()%6272)};
            const auto angle=std::uint8_t(irand()%32+80);
            const auto length=std::int16_t(irand()%64+48);
            f.cel=std::uint16_t(irand()&3);
            f.velocity=motion::polar(angle,length);
        }
    }
    for(unsigned i=0;i<limit;++i) {
        auto& f=flakes[i];if(!f.alive)continue;
        f.position.x=motion::wrap(f.position.x+f.velocity.x);
        f.position.y=motion::wrap(f.position.y+f.velocity.y);
        if(f.position.x<=0)f.position.x=motion::wrap(f.position.x+10112);
        if(f.position.y>=6272)f.position.y=motion::wrap(f.position.y-6272);
    }
}
void StaffSnow::draw(Canvas& dest) const {
    for(unsigned i=0;i<limit;++i) {
        const auto& f=flakes[i];if(!f.alive)continue;
        const int left=f.position.x>>4,top=f.position.y>>4;
        const unsigned shift=left&7;
        const auto origin=std::uint16_t(top*80+(left>>3));
        for(unsigned y=0;y<8;++y) {
            const auto raw=flake_masks[f.cel][y];
            const auto bits=std::uint16_t((raw>>shift)|(std::uint32_t(raw)<<(16-shift)));
            for(unsigned x=0;x<16;++x)if(bits&(1u<<((x&8)+7-(x&7)))) {
                const auto at=unsigned(std::uint16_t(origin+y*80))*8+x;
                if(at<dest.pixels.size())dest.pixels[at]|=1;
            }
        }
    }
}
StaffVerdict::StaffVerdict(const Resident& resident):character(std::uint8_t(character_id(resident.paletted[0]))),rank(resident.options.rank),skill(resident.skill) {
    std::copy(resident.scores[0].begin(),resident.scores[0].end(),score.begin()+1);score[0]=std::uint8_t(3-resident.credits);
    if(score[7]==3)skill=std::uint8_t(skill+score[6]/2+2);
    if(score[7]==3||score[7]==4)skill=std::uint8_t(skill+score[6]/2+7);
    if(score[7]>=5)skill=std::uint8_t(skill+15);
    if(score[8])skill=100;
    if(skill>100)skill=100;
}
void StaffVerdict::draw(Canvas& dest,const Font& font) const {
    const auto number=[&](int x,int y,unsigned digit) {font.text(dest,x,y,digits[digit],15,2);};
    font.text(dest,352,174,names[character],15,2);font.text(dest,360,199,ranks[rank],15,2);
    int x=408;bool seen=false;
    for(int d=8;d>0;--d) {
        const auto digit=score[unsigned(d)];
        if(!seen&&digit) {x-=d*8;seen=true;}
        if(seen) {number(x,224,digit);x+=16;}
    }
    number(x,224,score[0]);number(408,248,score[0]);
    x=408;seen=false;
    if(skill/100) {x-=16;seen=true;number(x,291,skill/100);x+=16;}
    const unsigned tens=skill%100/10;
    if(tens&&!seen) {seen=true;x-=8;}
    if(seen) {number(x,291,tens);x+=16;}
    number(x,291,skill%10);font.text(dest,x+16,291,"\x93\x5f",15,2);
}
StaffRoll::StaffRoll(const PfArchive& assets,const Font& font,const Resident& resident,const Cutscene* previous):verdict(resident),assets_(assets),font_(font) {
    if(!font.present())throw std::runtime_error("Staff Roll requires --font-bmp FILE");
    snow.seed=resident.seed;
    if(previous) {pages=previous->pages;palette_=previous->palette();shown_page=previous->shown_page;tone=previous->tone;}
    sounds.push_back({SceneSound::Kind::control,{},0x210});
}
void StaffRoll::setup() {
    sounds.push_back({SceneSound::Kind::control,{},0x100});
    sounds.push_back({SceneSound::Kind::load,"ED.M",0});
    palette_=read_palette(assets_.read("EDBK1.RGB"));
    for(auto& page:pages) {page.fill(0,0,639,399,8);page.fill(8,8,631,391,0);}
    shown_page=1;back=0;
    const char* files[]={"STF1.CDG","STF11.CDG","STF3.CDG","STF4.CDG","STF5.CDG","STF6.CDG","STF7.CDG","STF8.CDG","STF9.CDG","STF10.CDG","STF2.CDG","STF12.CDG"};
    for(const auto file:files)pictures_.emplace_back(assets_.read(file));
    tone=100;state=State::sync;sounds.push_back({SceneSound::Kind::control,{},0});
}
void StaffRoll::clear_blue() {for(auto& pixel:pages[back].pixels)pixel&=14;}
void StaffRoll::clear_interior() {pages[back].fill(8,8,631,391,0);}
void StaffRoll::unput(int x,int y,unsigned slot) {
    const auto& image=pictures_.at(slot);
    const int left=(x-int(image.width)/2)/8*8,top=y+int(image.height)/2-2;
    for(int row=top;row<top+3;++row)for(int column=left;column<left+int(image.width/16)*16;++column)
        if(row>=0&&row<400&&column>=0&&column<640)pages[back].pixels[unsigned(row*640+column)]&=7;
}
void StaffRoll::dissolve(int x,int y,unsigned slot,int strength) {
    const auto& image=pictures_.at(slot);
    const int left=x-int(image.width)/2,top=y-int(image.height)/2;
    image.put(pages[back],0,left,top,alpha_enabled&&alpha_requested);
    strength&=7;if(!strength)return;
    const int aligned=left/8*8;
    for(int row=top;row<top+int(image.height);++row)for(int column=0;column<int(image.width/16)*16;++column) {
        const auto bits=dissolve_masks[strength][row&3];
        if(bits&(1u<<(((column&15)&8)+7-(column&7)))) {
            const int dx=aligned+column;
            if(dx>=0&&dx<640&&row>=0&&row<400)pages[back].pixels[unsigned(row*640+dx)]&=7;
        }
    }
}
void StaffRoll::enter() {
    clear_blue();if(frame>duration)return;
    const unsigned slot=segments[segment].slot;
    unput(320,centers[back],slot);
    if(centers[back]>center_limit)centers[back]=std::max(centers[back]-speed,center_limit);
    const int strength=std::max(7-frame/(duration/8),0);
    if(alpha_requested&&secondary_slot) {dissolve(504,200,secondary_slot,strength);alpha_enabled=true;}
    dissolve(320,centers[back],slot,strength);alpha_enabled=false;
}
void StaffRoll::leave() {
    clear_blue();if(frame>161)return;
    if(frame>=160) {clear_interior();return;}
    const unsigned slot=segments[segment].slot;
    unput(320,centers[back],slot);--centers[back];
    const int strength=std::min(int(frame)/20,7);
    if(alpha_requested&&secondary_slot) {dissolve(504,200,secondary_slot,strength);alpha_enabled=true;}
    dissolve(320,centers[back],slot,strength);alpha_enabled=false;
}
void StaffRoll::present(unsigned elapsed_refreshes) {
    snow.update(frame);snow.draw(pages[back]);
    if(auto_adjust&&elapsed_refreshes>1) {alpha_requested=false;snow.limit=50;auto_adjust=false;}
    shown_page=back;back=1-back;
}
bool StaffRoll::gate(unsigned target,std::optional<unsigned> measure) const {return measure ? *measure>=target&&frame>192 : frame>256;}
void StaffRoll::begin_segment() {
    frame=0;state=State::enter;
    if(segment==1) {speed=1;duration=161;auto_adjust=false;}
    else if(segment==2) {height_offset=32;center_limit=168;}
    else if(segment==3) {secondary_slot=7;center_limit=216;height_offset=-16;}
    else if(segment==4) {secondary_slot=0;center_limit=200;height_offset=0;}
    if(speed==2) {centers[back]=264;centers[back^1]=263;}
    else centers.fill(280-height_offset);
}
void StaffRoll::tick(std::uint16_t input,std::optional<unsigned> measure,unsigned elapsed_refreshes,std::optional<unsigned> volume) {
    if(done())return;
    if(state==State::black_out) {
        if(--wait_)return;
        // palette_black_out synchronizes once, then writes 100,94,...,4,0.
        tone=fade_tone_==0 ? 100 : std::max(tone-6,0);fade_tone_=1;wait_=4;
        if(!tone){if(volume&&*volume!=255)state=State::volume_wait;else setup();}
        return;
    }
    if(state==State::volume_wait) {if(!volume||*volume==255)setup();return;}
    if(state==State::sync) {state=State::initial;return;}
    if(state==State::initial||state==State::hold||state==State::gallery||state==State::verdict)clear_blue();
    if(state==State::enter) {
        enter();
        if(segment==3) {alpha_enabled=true;dissolve(320,secondary_y,2,0);alpha_enabled=false;}
    } else if(state==State::leave) {
        if(segment==3&&frame<=161)unput(320,secondary_y,2);
        leave();
        if(segment==3&&frame<=161) {
            const int strength=std::min((int(frame)-1)/20,7);
            if(back==0)--secondary_y;
            alpha_enabled=true;if(frame<160)dissolve(320,secondary_y,2,strength);else clear_interior();alpha_enabled=false;
        }
    } else if(state==State::clear)clear_interior();
    else if(state==State::gallery&&frame<=160) {
        dissolve(320,128,8,std::max(7-frame/20,0));dissolve(192,240,9,std::max(7-frame/20,0));
    }
    present(elapsed_refreshes);
    if(state==State::clear) {
        if(++clears_==2) {++segment;if(segment<9)begin_segment();else {state=State::gallery;frame=0;}}
        return;
    }
    frame=motion::wrap(frame+1);
    if(state==State::verdict) {
        if(fade_tone_) {tone=fade_tone_;if(frame&1&&!--fade_tone_)state=State::done;}
        else if(input&&frame>256) {sounds.push_back({SceneSound::Kind::control,{},0x208});fade_tone_=100;frame=0;}
        return;
    }
    const auto target=state==State::initial ? 4 : state==State::gallery ? 66 : state==State::enter ? segments[segment].enter_measure : segments[segment].leave_measure;
    if(!gate(target,measure))return;
    if(state==State::initial)begin_segment();
    else if(state==State::enter) {frame=0;state=segment==2 ? State::hold : State::leave;}
    else if(state==State::hold) {secondary_y=centers[back];++segment;begin_segment();}
    else if(state==State::leave) {state=State::clear;clears_=0;}
    else if(state==State::gallery) {
        verdict.draw(pages[back^1],font_);verdict.draw(pages[back],font_);frame=0;fade_tone_=0;state=State::verdict;
    }
}
}
