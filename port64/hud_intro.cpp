#include "round.hpp"
#include "motion.hpp"

namespace th03 {
void HudIntro::update(RandomRing& random,Mode mode) {
    if(flag==1) {
        frame=0;
        int x=-288,y=84;
        for(unsigned i=0;i<16;++i,x+=8,++y) {
            auto& p=particles[i];p.center={std::int16_t(x),std::int16_t(y)};p.velocity=8;p.active=1;
        }
        phase=0;sprite=mode==Mode::story ? 22 : 26;flag=2;this->x=0;
    }
    if(phase==0) {
        for(unsigned i=0;i<16;++i) {
            auto& p=particles[i];
            if(!p.active)continue;
            p.center.x=motion::wrap(int(p.center.x)+p.velocity);
            if(p.active==1) {if(p.center.x>=96)p.active=2;}
            else if(p.center.x<=64) {p.center.x=64;p.active=0;if(i==0)phase=1;}
            else p.velocity=motion::wrap(int(p.velocity)-1);
        }
        return;
    }
    if(phase==1) {frame=motion::wrap(int(frame)+1);if(frame>86)++phase;return;}
    if(phase==2) {
        for(unsigned side=0;side<2;++side)for(unsigned i=0;i<64;++i) {
            auto& p=particles[side*64+i];
            p.center.x=std::int16_t((side ? 0x1a00 : 0x600)+i*32);
            p.center.y=std::int16_t((random.ring()&511)+0xa80);
            p.angle=std::uint8_t(random.ring());
            p.turn_early=std::uint8_t(random.next()%3);p.turn_late=std::uint8_t(random.next()%3);p.active=1;
        }
        ++phase;frame=0;return;
    }
    if(phase==3) {
        frame=motion::wrap(int(frame)+1);if(frame>=64)++phase;
        for(auto& p:particles)if(p.active) {
            const auto v=motion::polar(p.angle,80);
            p.center.x=motion::wrap(int(p.center.x)+v.x);p.center.y=motion::wrap(int(p.center.y)+v.y);
            if(p.center.x<0||p.center.x>=0x2700||p.center.y<0||p.center.y>=0x1800)p.active=0;
            else p.angle=std::uint8_t(p.angle+(int(frame<32 ? p.turn_early : p.turn_late)-1)*4);
        }
    } else flag=0;
}
void HudIntro::prepare_render(Mode mode) {
    if(!flag)return;
    // DS:331A aliases the x word of slide particle15.
    if(phase==0)x=particles[15].center.x;
    else if(phase==1&&frame==(mode==Mode::story ? 56 : 64)) {x=96;sprite=30;}
}
}
