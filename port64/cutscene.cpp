#include "cutscene.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
bool digit(unsigned c) {return c>='0'&&c<='9';}
bool separator(unsigned c) {return c<=32||c==127;}
unsigned lower(unsigned c) {return c>='A'&&c<='Z' ? c+32 : c;}
constexpr unsigned masks[4][4]={{0,0x1111,0,0x4444},{0x8888,0x1111,0x2222,0x4444},
                                    {0xaaaa,0x5555,0xaaaa,0x5555},{0xeeee,0x7777,0xbbbb,0xdddd}};
}
int ScriptCursor::first() {
    const auto a=take(),b=take(),c=take();
    const unsigned rewind=!digit(a) ? 3 : !digit(b) ? 2 : !digit(c) ? 1 : 0;
    // Two digits end with DEC(pointer), which retains the decimal ADD's CF;
    // three digits retain it directly. One/default use real pointer SUBs.
    carry=rewind<=1||at<rewind;at=std::uint16_t(at-rewind);
    if(rewind==3)return number_default;
    if(rewind==2)return a-'0';
    if(rewind==1)return (a-'0')*10+b-'0';
    return (a-'0')*100+(b-'0')*10+c-'0';
}
int ScriptCursor::second() {if(peek()!=',') {carry=peek()<',';return number_default;}take();return first();}
std::string ScriptCursor::filename() {
    std::string out;
    for(unsigned i=0;i<12;++i) {const auto c=take();if(separator(c))break;out+=char(c);}
    return out;
}
Cutscene::Cutscene(const PfArchive& assets,const Font& font,std::string filename,std::uint16_t input):Cutscene(assets,font,assets.read(std::move(filename)),input) {}
Cutscene::Cutscene(const PfArchive& assets,const Font& font,Bytes bytes,std::uint16_t input):script(std::move(bytes)),
    assets_(assets),font_(font),gaiji_(assets.read("MIKOFT.BFT")),box_(480*64) {
    if(!font.present())throw std::runtime_error("cutscene requires --font-bmp FILE");
    snapshot();pump(input);
}
void Cutscene::snapshot() {
    for(unsigned y=0;y<64;++y)std::copy_n(pages[0].pixels.begin()+(320+y)*640+80,480,box_.begin()+y*480);
}
void Cutscene::restore(unsigned page) {
    for(unsigned y=0;y<64;++y)std::copy_n(box_.begin()+y*480,480,pages[page].pixels.begin()+(320+y)*640+80);
}
void Cutscene::clear_text() {cursor={80,320};restore(1);restore(0);}
void Cutscene::quarter(unsigned id,std::optional<unsigned> mask) {
    if(id>=4) {pages[0].fill(160,64,479,263,0);}
    else {
        if(!picture_)throw std::runtime_error("cutscene quarter has no loaded PI");
        const unsigned sx=(id&1)*320,sy=(id>>1)*200;
        for(unsigned y=0;y<200;++y)for(unsigned x=0;x<320;++x) {
            if(mask&&!(masks[*mask][y%4]&(0x80u>>(x&7))))continue;
            const auto packed=picture_->pixels.at(((sy+y)*640+sx+x)/2);
            pages[0].put(160+int(x),64+int(y),std::uint8_t((x&1) ? packed&15 : packed>>4));
        }
    }
    for(unsigned y=64;y<264;++y)std::copy_n(pages[0].pixels.begin()+y*640+160,320,pages[1].pixels.begin()+y*640+160);
    shown_page=0;
}
void Cutscene::masked_step() {
    while(mask_step_<4) {
        quarter(mask_quarter_,mask_step_++);
        if(!fast_forward&&mask_delay_) {sleep(mask_delay_,After::mask);return;}
    }
    quarter(mask_quarter_);
}
void Cutscene::shake_step() {
    while(shake_step_<=shake_last_) {
        scroll=(shake_step_++&1) ? 4 : 396;
        if(!fast_forward) {sleep(1,After::shake);return;}
    }
    scroll=0;
}
void Cutscene::sleep(unsigned frames,After after) {
    if(!frames)return;
    wait=Wait::delay;ticks_=frames;after_=after;
}
bool Cutscene::wait_change(unsigned frames,std::uint16_t input,After after) {
    wait=input ? Wait::release : Wait::press;timeout_=frames==9999 ? 0 : frames;after_=after;return true;
}
void Cutscene::fade(int from,int to,int speed) {
    fade_value_=from;fade_target_=to;fade_step_=to>from ? 6 : -6;fade_speed_=speed;
    fade_sync_=true;wait=Wait::fade;ticks_=1;after_=After::none;
}
void Cutscene::complete_wait(std::uint16_t input) {
    const auto after=after_;wait=Wait::none;after_=After::none;
    if(after==After::clear||after==After::clear_glyph) {
        clear_text();if(after==After::clear_glyph)glyph_delay(input);
    } else if(after==After::tone)tone=pending_tone_;
    else if(after==After::mask)masked_step();
    else if(after==After::shake)shake_step();
    else if(after==After::speedup)++speedup_cycle;
}
void Cutscene::tick(std::uint16_t input) {
    if(stopped_)return;
    if(wait==Wait::release) {if(input)return;wait=Wait::press;return;}
    if(wait==Wait::press) {
        if(!input&&(!timeout_||--timeout_))return;
        complete_wait(input);
    } else if(wait==Wait::ok) {
        if(!(input&(ok|shot))&&--ticks_)return;
        complete_wait(input);
    } else if(wait==Wait::delay) {
        if(--ticks_)return;
        complete_wait(input);
    } else if(wait==Wait::fade) {
        if(--ticks_)return;
        if(fade_sync_) {fade_sync_=false;tone=fade_value_;}
        else {fade_value_+=fade_step_;tone=fade_value_;}
        if(fade_speed_<=0||(fade_step_>0 ? fade_value_>=fade_target_ : fade_value_<=fade_target_)) {
            tone=fade_target_;complete_wait(input);
        } else {ticks_=unsigned(fade_speed_);return;}
    }
    if(wait==Wait::none)pump(input);
}
void Cutscene::glyph_delay(std::uint16_t input) {
    if(fast_forward)return;
    if(!input)sleep(unsigned(interval));
    else {
        int frames=interval/3;
        if((speedup_cycle&1)||frames)sleep(unsigned(frames ? frames : 1),After::speedup);
        else ++speedup_cycle;
    }
}
bool Cutscene::advance_cursor(std::uint16_t input,bool glyph) {
    cursor.x+=16;
    if(cursor.x>=560) {
        cursor.y+=16;cursor.x=144;
        if(cursor.y>=384) {
            if(!fast_forward)return wait_change(0,input,glyph ? After::clear_glyph : After::clear);
            clear_text();
        }
    }
    return false;
}
void Cutscene::gaiji(unsigned page,std::uint16_t id,bool carry) {
    const auto jis=std::uint16_t(id+0x5680+unsigned(carry))&0xff7f;
    if((jis>>8)==0x56||(jis>>8)==0x57) {
        const unsigned code=((jis>>8)-0x56)*128+(jis&127);
        th03::gaiji(pages[page],gaiji_,code,cursor.x,cursor.y,std::uint8_t(color));
    } else {
        for(unsigned y=0;y<16;++y) {
            const auto row=font_.jis_row((((jis>>8)+0x20)<<8)|(jis&127),y);
            for(unsigned x=0;x<16;++x)if(row&(0x8000u>>x))pages[page].put(cursor.x+int(x),cursor.y+int(y),std::uint8_t(color));
        }
    }
}
void Cutscene::pump(std::uint16_t input) {
    while(wait==Wait::none&&!stopped_) {
        fast_forward=input&cancel;
        const auto c=script.take();
        if(separator(c))continue;
        if(c=='\\') {op(script.take(),input);continue;}
        const char glyph[]={char(c),char(script.take())};
        const auto effect=unsigned(weight)|((unsigned(color)>>4)&3);
        font_.text(pages[1],cursor.x,cursor.y,std::string_view(glyph,2),unsigned(color),effect);
        font_.text(pages[0],cursor.x,cursor.y,std::string_view(glyph,2),unsigned(color),effect);
        if(!advance_cursor(input,true))glyph_delay(input);
    }
}
void Cutscene::op(unsigned command,std::uint16_t input) {
    command=lower(command);
    switch(command) {
    case 'n':cursor.y+=16;cursor.x=80;if(cursor.y<384)break;[[fallthrough]];
    case 's': {
        if(script.peek()=='-')script.take();
        else {const auto frames=script.first(0);if(!fast_forward) {wait_change(unsigned(frames),input,After::clear);break;}}
        clear_text();break;
    }
    case 'c':color=std::uint8_t(script.first(15));break;
    case 'b': {const auto value=script.first(2);if(value<4)weight=value;break;}
    case 'w': {
        const auto kind=lower(script.peek());
        if(kind=='o'||kind=='i') {script.take();const auto speed=script.first(1);fade(kind=='i' ? 200 : 100,kind=='i' ? 100 : 200,speed);break;}
        script.number_default=64;
        bool key=kind=='k';
        if(kind=='m') {script.take();key=script.peek()=='k';if(key)script.take();}
        else if(key)script.take();
        auto frames=script.first();if(kind=='m')frames=script.second();
        if(fast_forward)break;
        if(key) {if(!(input&(ok|shot))&&frames) {wait=Wait::ok;ticks_=unsigned(frames);}}
        else sleep(unsigned(frames));
        break;
    }
    case 'v':if(script.peek()=='p') {script.take();shown_page=unsigned(script.first(0))&1;}else interval=script.first(1);break;
    case 't':pending_tone_=script.first(100);if(fast_forward)tone=pending_tone_;else sleep(1,After::tone);break;
    case 'f': {
        const auto kind=script.peek();
        if(kind=='m') {script.take();sounds.push_back({SceneSound::Kind::control,{},0x200+script.first(1)});}
        else if(kind=='i'||kind=='o') {script.take();const auto speed=script.first(1);fade(kind=='i' ? 0 : 100,kind=='i' ? 100 : 0,speed);}
        break;
    }
    case 'g':
        if(script.peek()=='a') {
            script.take();const auto id=script.first(0);gaiji(1,std::uint16_t(id-1),script.carry);gaiji(0,std::uint16_t(id),false);
            advance_cursor(input,false);
        } else {shake_last_=unsigned(script.first(8));shake_step_=0;shake_step();}
        break;
    case 'k':script.first(0);if(!fast_forward)wait_change(0,input,After::none);break;
    case '@':for(auto& page:pages)std::fill(page.pixels.begin(),page.pixels.end(),0);break;
    case 'p': {
        const auto kind=script.take();
        if(kind=='='||kind=='@') {
            if(!picture_)throw std::runtime_error("cutscene full picture has no loaded PI");
            if(kind=='=')palette_=picture_->palette;
            picture(pages[1],*picture_);pages[0]=pages[1];snapshot();
        } else if(kind=='-')picture_.reset();
        else if(kind=='p') {if(!picture_)throw std::runtime_error("cutscene palette has no loaded PI");palette_=picture_->palette;}
        else if(kind==',')picture_=decode_pi(assets_.read(script.filename()));
        else --script.at;
        break;
    }
    case '=':
        if(script.peek()=='=') {
            script.take();const auto id=unsigned(script.first(4));mask_quarter_=id<4 ? id : 0;
            script.number_default=1;mask_delay_=unsigned(script.second());mask_step_=0;masked_step();
        } else quarter(unsigned(script.first(4)));
        break;
    case 'm':
        if(script.peek()=='$') {script.take();sounds.push_back({SceneSound::Kind::control,{},0x100});}
        else if(script.peek()=='*') {script.take();sounds.push_back({SceneSound::Kind::control,{},0});}
        else if(script.peek()==',') {script.take();const auto file=script.filename();sounds.push_back({SceneSound::Kind::control,{},0x100});sounds.push_back({SceneSound::Kind::load,file,0});sounds.push_back({SceneSound::Kind::control,{},0});}
        break;
    case 'e':sounds.push_back({SceneSound::Kind::effect,{},script.first()});break;
    case '$':restore(0);stopped_=true;break;
    }
}
Frame Cutscene::render() const {
    if(!scroll)return pages[shown_page].frame(palette_,tone);
    Canvas display;
    for(unsigned y=0;y<400;++y)std::copy_n(pages[shown_page].pixels.begin()+((y+scroll)%400)*640,640,display.pixels.begin()+y*640);
    return display.frame(palette_,tone);
}
}
