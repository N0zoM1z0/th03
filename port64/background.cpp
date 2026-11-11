#include "background.hpp"
#include "round.hpp"
#include "motion.hpp"

namespace th03 {
namespace {
void advance(BackgroundParticle& p) {
    // Original CMP/JAE/JBE use unsigned WORD positions after the ADD.
    auto x=std::uint16_t(int(p.center.x)+p.velocity.x),y=std::uint16_t(int(p.center.y)+p.velocity.y);
    if(x<128)x=std::uint16_t(x+9984);else if(x>10112)x=std::uint16_t(x-9984);
    if(y<224)y=std::uint16_t(y+5920);else if(y>6144)y=std::uint16_t(y-5920);
    p.center={motion::wrap(x),motion::wrap(y)};
}
void velocity(BackgroundParticle& p,std::uint8_t angle) {
    const auto v=motion::polar(angle,p.speed);p.velocity={v.x,v.y};
}
}
void Background::begin(RandomRing& random,unsigned character) {
    chain=character==0||character==1||character==6 ? 1 : 2;angle=64;periodic=draw_periodic=false;
    const unsigned count=chain==1 ? 48 : 50;
    for(unsigned i=0;i<count;++i) {
        auto& p=particles[i];p.center={std::int16_t(random.next()%10240),std::int16_t(random.next()%6400)};
        p.velocity={0,16};p.speed=chain==1 ? 32 : 16;
        if(chain==1) {p.sprite=std::uint16_t(0x210e +(random.next()%2 ? 0x280 : 0));p.auxiliary=std::int16_t(random.next()%4000);}
        else p.sprite=i<40 ? 0x233e : 0x20be;
    }
}
void Background::reset_velocity() {
    angle=64;for(auto& p:particles)velocity(p,angle);
}
void Background::update(RandomRing& random,std::uint32_t round_frame,std::uint16_t result_frame) {
    if(!chain)return;
    const unsigned count=chain==1 ? 48 : 50;
    draw_periodic=periodic;
    phase_frame=result_frame%4096;
    if(!periodic) {
        angle=64;
        for(unsigned i=0;i<count;++i) {
            auto& p=particles[i];
            if(chain==1||i<40)p.velocity.y=motion::wrap(int(p.velocity.y)+(random.next()&1));
            p.speed=std::uint8_t(p.velocity.y);advance(p);
        }
        if(round_frame>(chain==1 ? 128u : 144u))periodic=true;
        return;
    }
    const unsigned f=phase_frame;int turn=0;
    if(f>=1024&&f<1280) {if(!(f%8))turn=1;}
    else if(f>=2048&&f<2304) {if(!(f%4))turn=-1;}
    else if(f>=3072&&f<4064)turn=(f&127)<64 ? 1 : -1;
    angle=std::uint8_t(angle+turn);
    for(unsigned i=0;i<count;++i) {
        auto& p=particles[i];advance(p);
        if(turn)velocity(p,angle);
        // Non-tick paths in the original read an indeterminate `changed`
        // byte. Their optional vector2 call rewrites the same velocity:
        // initialization/acceleration, each actual turn and reset preserve
        // velocity == polar(angle,speed). It has no other observable effect.
    }
}
}
