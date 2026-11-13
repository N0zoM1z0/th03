#include "round.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
int pixel(int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);}
int screen_x(const Round& round,int x,unsigned pid) {return 16+int(pid)*320+pixel(x)+round.fg_shift[pid];}
void advance(Point& p,Point v) {p.x=motion::wrap(int(p.x)+v.x);p.y=motion::wrap(int(p.y)+v.y);}
bool outside(Point p) {return p.x<=-512||p.x>=5120||p.y<=-512||p.y>=6400;}
void color(Round& round,unsigned pid,int red,int green,int blue) {
    round.palette[pid*3]=std::uint8_t(red);round.palette[pid*3+1]=std::uint8_t(green);round.palette[pid*3+2]=std::uint8_t(blue);
}
void gray(Round& round,unsigned pid,int value) {color(round,pid,value,value,value);}
void restore(Round& round,unsigned pid) {std::copy_n(round.palette_backup.begin()+pid*3,3,round.palette.begin()+pid*3);}
}
void Round::set_palette(const Palette& colors) {palette=palette_backup=colors;palette_initialized=true;}
void Round::effect_add(Point center,unsigned pid,Effect type) {
    effect_cursor=std::uint8_t((effect_cursor+1)%12);auto& effect=effects[effect_cursor];
    effect.kind=type==Effect::axis ? 2 : 1;effect.age=0;
    effect.center={std::int16_t(screen_x(*this,center.x,pid)),std::int16_t(pixel(center.y)+16)};
    effect.radius=type==Effect::explosion ? 8 : type==Effect::center ? 136 : 162;
    effect.radius_delta=type==Effect::explosion ? 8 : type==Effect::center ? -8 : -10;
    if(type==Effect::axis)effect.angle=std::uint8_t(random.ring());
}
void Round::update_effects() {
    for(auto& effect:effects)if(effect.kind) {
        ++effect.age;if(effect.age>16)effect.kind=0;
        effect.radius=std::uint8_t(effect.radius+effect.radius_delta);
    }
}
void Round::prepare_effects_render() {
    for(unsigned i=0;i<effects.size();++i)if(effects[i].kind&&effects[i].kind!=1)
        effects[i].angle=std::uint8_t(effects[i].angle+((i&1) ? -8 : 8));
}
void Round::player_bomb(unsigned pid,Resident& resident) {
    auto& p=players[pid];if(bomb_flags[pid]||p.hyper_active)return;
    if(p.bombs) {bomb_flags[pid]=1;--p.bombs;p.invincibility=180;}
    else {
        if(p.gauge_avail<4080)return;
        damage_all[pid]=1;sounds.push_back(7);p.hyper_active=p.paletted;effect_add(p.center,pid,Effect::explosion);
    }
    if(!pid&&resident.skill)--resident.skill;
}
void Bombs::update(Round& round,unsigned pid) {
    auto& flag=round.bomb_flags[pid];if(!flag)return;
    const auto character=character_id(round.players[pid].paletted);
    if(flag==1) {
        flag=2;frame[pid]=0;round.sounds.push_back(character==3 ? 17 : 18);
        if(character==0)for(auto& p:reimu[pid])p.active=0;
        else if(character==1)for(auto& p:mima[pid])p.sprite=0;
        else if(character==3)for(auto& p:ellen[pid])p.center.x=19999;
    }
    ++frame[pid];
    if(character==0) {
        for(auto& p:reimu[pid])if(p.active) {
            p.center.y=motion::wrap(int(p.center.y)+p.velocity_y);
            if(p.center.y<=-128) {p.center.y=6144;p.velocity_y=motion::wrap(int(p.velocity_y)+8);}
        }
    } else if(character==1) {
        const int i=frame[pid]/8-1;
        if(i<8&&!(frame[pid]%8)) {
            auto& p=mima[pid][unsigned(i)];p.x=std::int16_t(round.random.ring()%4608);p.sprite=std::uint16_t((i/3)*2+pid*40+0x1c);
        }
    } else if(character==3)for(auto& p:ellen[pid]) {
        if(p.center.x!=9999) {
            if(p.center.x==19999)continue;
            advance(p.center,p.velocity);if(!outside(p.center))continue;
        }
        p.center={2304,2944};const auto v=motion::polar(std::uint8_t(round.random.ring()),224);p.velocity={v.x,v.y};
    }
    if(frame[pid]>=180) {flag=0;restore(round,pid);}
}
std::uint8_t Bombs::palette_stack_byte(const Round& r,unsigned pid,std::uint8_t incoming) const {
    if(!r.bomb_flags[pid])return incoming;
    // The two far Bomb callbacks reuse [caller SP-8]. Kotohime's color is
    // [BP-2]; other characters leave these specific locals in that byte.
    const unsigned f=frame[pid];
    const auto fade=std::uint8_t(255-f*8);
    switch(character_id(r.players[pid].paletted)) {
    case 0:if(f>=112)return fade;if(f>=64)return std::uint8_t(f%8);break;
    case 1:return f<=80 ? std::uint8_t(-int(f)*3) : f<144 ? std::uint8_t(f%8) : fade;
    case 2:if(f<64)return std::uint8_t(-int(f)*4);if(f>=128)return fade;break;
    case 3:if(f>=64&&f<128)return std::uint8_t(r.fg_shift[pid]);break;
    case 4:if(f<64)return std::uint8_t(f*3);if(f>=128)return std::uint8_t(incoming*2);break;
    case 5:if(f<64)return std::uint8_t(64-f);if(f>=128)return std::uint8_t(fade*2);break;
    case 6:if(f<64)return std::uint8_t(f*4);if(f>=128)return std::uint8_t(fade*2);break;
    case 7:if(f<64)return std::uint8_t(255-f*4);if(f>=144)return std::uint8_t(fade*2);break;
    case 8:if(f<=64)return std::uint8_t(16+pid*320);break;
    }
    return incoming;
}
void Bombs::prepare_render(Round& r,unsigned pid,std::optional<std::uint8_t> stack_color) {
    if(!r.bomb_flags[pid])return;
    const int f=frame[pid];const unsigned character=character_id(r.players[pid].paletted);
    const auto effect=[&](int x,int y,Effect type=Effect::explosion) {r.effect_add({motion::wrap(x),motion::wrap(y)},pid,type);};
    const auto shake=[&] {r.fg_shift[pid]=(f&3)<2 ? 4 : -4;};
    const auto fade=[&] {r.fg_shift[pid]=0;const auto value=std::uint8_t(255-f*8);color(r,pid,value*2,value*2,value);};
    switch(character) {
    case 0:
        if(f<64) {
            if(f<32) {
                auto& p=reimu[pid][f];p.active=1;p.velocity_y=std::int16_t(-96-(r.random.ring()&127));
                p.center={std::int16_t(r.random.ring()%4608),6144};
            }
            color(r,pid,f*4,f*3,f*3);
        } else if(f<112) {
            if(f&1)r.sounds.push_back(16);
            r.palette_tone=f<=96 ? std::int16_t((f%2)*80+100) : 100;shake();
        } else {r.fg_shift[pid]=0;gray(r,pid,255-f*8);}
        return;
    case 1:
        if(f<=80)gray(r,pid,-int(f)*3);
        else if(f<144) {
            if(!(f%2))r.sounds.push_back(16);
            color(r,pid,(f%2) ? 0 : 100,0,0);if(!(f%8))effect(2304,2944);shake();
        } else {r.fg_shift[pid]=0;gray(r,pid,255-f*8);}
        return;
    case 2:
        if(f<64)gray(r,pid,-int(f)*4);
        else if(f<128) {
            if(f&1)r.sounds.push_back(16);
            shake();
            if(!(f%8)) {
                marisa_point={std::int16_t(r.random.ring()%4608),std::int16_t(r.random.ring()%5888)};
                effect(marisa_point.x,marisa_point.y);
                marisa_point={std::int16_t(screen_x(r,marisa_point.x,pid)),std::int16_t(pixel(marisa_point.y)+16)};
            }
            marisa_draw_point[pid]=marisa_point;
        } else {r.fg_shift[pid]=0;gray(r,pid,255-f*8);}
        return;
    case 3:
        if(f<64) {color(r,pid,f*4,f*2,f*2);ellen_spawn_count=0;}
        else if(f<128) {
            if(f&1) {r.sounds.push_back(10);color(r,pid,255,128,128);}else color(r,pid,0,0,32);
            shake();
            if(!(f%4)) {
                effect(2304,2944);
                if(ellen_spawn_count<8)ellen[pid][unsigned(ellen_spawn_count++)].center.x=9999;
            }
        } else {r.fg_shift[pid]=0;const auto value=std::uint8_t(255-f*8);color(r,pid,value*2,value,value);}
        return;
    case 4:
        if(f<64) {
            color(r,pid,f*3+64,f*3+32,f*3);
            if(!(f%8)) {kotohime_y=motion::wrap(int(f)*92+92);effect(4536-int(f)*72,kotohime_y);}
        } else if(f<128) {
            shake();if((f&3)<2) {r.sounds.push_back(10);r.palette_tone=170;}else r.palette_tone=100;
            if(!(f%8)) {for(int x=0;x<=4608;x+=1536)effect(x,kotohime_y);kotohime_y=motion::wrap(int(kotohime_y)-736);}
        } else {
            if(!stack_color)throw std::runtime_error("Kotohime Bomb fade needs the render caller's stack color");
            r.palette_tone=100;r.fg_shift[pid]=0;color(r,pid,*stack_color*2,*stack_color*2,255-f*8);
        }
        return;
    case 5:
        if(f<64) {gray(r,pid,64-f);if(!(f%8))effect(2304,2944,Effect::center);kana_angle=0;}
        else if(f<128) {
            shake();if((f&3)<2) {r.sounds.push_back(10);gray(r,pid,160);}else gray(r,pid,0);
            if(!(f%4)) {
                const auto circle=[&] {const auto v=motion::polar(kana_angle,144);effect((144+v.x)*16,(184+v.y)*16);};
                circle();kana_angle=std::uint8_t(128-kana_angle);circle();kana_angle=std::uint8_t(128-kana_angle+16);
            }
        } else fade();
        return;
    case 6:
        if(f<64) {gray(r,pid,f*4);rikako_line_offset=0;}
        else if(f<128) {
            shake();rikako_draw_offset[pid]=rikako_line_offset;
            rikako_line_offset=motion::wrap(int(rikako_line_offset)+65);if(rikako_line_offset>=1152)rikako_line_offset=0;
            if(!(f%8))for(int x=r.random.ring()&1023;x<=4608;x+=1536)effect(x,5888);
            if(!(f%4))r.sounds.push_back(5);
        } else fade();
        return;
    case 7:
        if(f<64) {gray(r,pid,255-f*4);if(!(f%8))effect(2304,2944,Effect::center);}
        else if(f<144) {
            shake();r.palette_tone=(f&3)<2 ? 60 : 120;
            if(!(f%16)) {
                r.sounds.push_back(10);const int distance=(int(f)-64)*32;
                effect(2304-distance,2944,Effect::axis);effect(2304+distance,2944,Effect::axis);
                effect(2304,2944-distance,Effect::axis);effect(2304,2944+distance,Effect::axis);
            }
        } else {r.palette_tone=100;fade();}
        return;
    case 8:
        if(f<=64)gray(r,pid,f*4);
        else if(f<144) {
            if(!(f%8)) {r.sounds.push_back(5);r.palette_tone=140;effect(2304,2944,Effect::axis);}else r.palette_tone=60;
            shake();
        } else {r.palette_tone=100;r.fg_shift[pid]=0;gray(r,pid,255-f*8);}
        return;
    }
}
}
