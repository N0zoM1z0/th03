#include "round.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
void GaugeAttacks::update(Round& r,unsigned pid) {
    if(r.gauge_flags[pid])pattern(r,pid,1);
    if(r.gauge_flags[pid])pattern(r,pid,2);
}
void GaugeAttacks::pattern(Round& r,unsigned pid,std::uint8_t type) {
    const unsigned expected=type==1 ? 1 : 3,character=character_id(r.players[pid].paletted),other=pid^1;
    auto& active=r.gauge_flags[pid];auto& time=timing[pid];auto& f=frame[character][pid];auto& at=center[character][pid];
    const auto level=r.gauge_levels[pid];
    if(active==expected) {
        f=0;++active;
        switch(character) {
        case 0:time[0]=std::uint8_t(level+32);time[1]=std::uint8_t(32-level);break;
        case 1:
            mima_step[pid]=(r.random.ring()&1) ? 7 : std::uint8_t(-7);mima_angle[pid]=64;
            time[0]=std::uint8_t(level+38);time[1]=std::uint8_t(level*2+24);break;
        case 2:at.y=std::int16_t(-int(r.random.ring()&31)*16);time[0]=std::uint8_t(48-level);break;
        case 3:at={2304,0};time[0]=std::uint8_t(level+14);time[1]=std::uint8_t(level+28);break;
        case 4:time[0]=std::uint8_t(level/2+4);time[1]=std::uint8_t(r.random.ring()&1);time[2]=type;break;
        case 5:at.x=0;time[0]=std::uint8_t(8-level/4);time[1]=std::uint8_t(level+48);break;
        case 6:time[0]=std::uint8_t(16-level/2);time[1]=std::uint8_t(level+48);break;
        case 7:at.x=-384;time[0]=std::uint8_t((level/2)*16+32);break;
        case 8:time[0]=std::uint8_t(level+24);time[1]=std::uint8_t(level+32);break;
        }
        return;
    }
    if(active!=expected+1)return;
    auto& t=r.bullets.model;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto effect=[&](int x,int y,Effect kind=Effect::center) {r.effect_add({motion::wrap(x),motion::wrap(y)},other,kind);};
    const auto finish=[&] {active=0;std::copy_n(r.palette_backup.begin()+other*3,3,r.palette.begin()+other*3);};
    switch(character) {
    case 0:
        t.type=type;t.center.y=128;t.pid=std::uint8_t(other);t.speed=32;t.angle=0;
        if(!time[1])throw std::domain_error("Reimu Gauge period divide error");
        if(!(f%time[1])) {
            t.group=24;t.center.x=512;effect(512,128);add();t.center.x=4096;effect(4096,128);add();
        }
        if(f%32==16) {
            t.group=38;t.count=time[0];t.speed=50;t.center.x=1024;effect(1024,128);add();t.center.x=3584;effect(3584,128);add();
        }
        if(f>64)finish();
        break;
    case 1:
        if(!(f%8)) {
            t.type=type;t.center={std::int16_t(mima_step[pid]>7 ? 512 : 4096),256};t.speed=time[1];
            t.pid=std::uint8_t(other);t.angle=mima_angle[pid];t.animated=false;t.group=20;
            effect(t.center.x,256);add();
            if(f%16) {t.group=38;t.count=time[0];t.speed=54;effect(t.center.x,256);add();}
            mima_angle[pid]=std::uint8_t(mima_angle[pid]+mima_step[pid]);t.animated=true;
        }
        if(f>64)finish();
        break;
    case 2:
        t.type=type;t.center.y=at.y;t.pid=std::uint8_t(other);t.speed=56;t.group=0;
        if(f%24==8)effect(0,at.y);
        else if(f%24==20)effect(4608,at.y);
        else if(f%24==0||f%24==12) {
            t.angle=f%24==0 ? 32 : 96;t.center.x=f%24==0 ? 0 : 4608;
            for(unsigned i=0;i<5;++i) {add();t.speed=std::uint8_t(t.speed-6);}
            at.y=motion::wrap(int(at.y)+time[0]*16);
        }
        if(at.y>=5888)finish();
        break;
    case 3:
        if(!(f%8)) {
            t.type=type;t.center.y=128;t.pid=std::uint8_t(other);
            if(at.x>0) {
                t.angle=0;t.speed=56;t.group=44;t.count=time[0];t.center.y=0;
                t.center.x=at.x;effect(t.center.x,0);add();t.center.x=motion::wrap(4608-at.x);effect(t.center.x,0);add();at.x=motion::wrap(int(at.x)-384);
            } else if(at.y<2304) {
                t.angle=std::uint8_t(r.random.ring());t.speed=time[1];t.group=36;t.center={0,at.y};effect(0,at.y);add();
                t.center.x=4608;effect(4608,at.y);add();t.angle=std::uint8_t(r.random.ring());at.y=motion::wrap(int(at.y)+384);
            } else finish();
        }
        break;
    case 4:
        if(!f)r.extra_attacks.kotohime_gauge(r,{std::int16_t(r.random.ring()%2560+1024),0},pid);
        else if(f>=128)finish();
        break;
    case 5:
        if(!time[0])throw std::domain_error("Kana Gauge period divide error");
        if(!(f%time[0])) {
            t.type=type;t.pid=std::uint8_t(other);t.center={at.x,0};t.group=0;t.angle=64;t.speed=time[1];
            add();effect(t.center.x,0);t.center.x=motion::wrap(4608-at.x);add();effect(t.center.x,0);
        }
        at.x=motion::wrap(int(at.x)+(f%64<32 ? 128 : -128));if(f>=128)finish();
        break;
    case 6:
        if(!time[0])throw std::domain_error("Rikako Gauge period divide error");
        if(!(f%time[0])) {
            t.type=type;t.pid=std::uint8_t(other);t.center.y=0;t.group=1;t.angle=std::uint8_t(32-f/4);t.speed=time[1];
            t.center.x=0;add();t.center.x=4608;add();t.angle=std::uint8_t(-t.angle);add();t.center.x=0;add();effect(0,0);effect(4608,0);
        }
        if(f>=128)finish();
        break;
    case 7: {
        auto x=at.x;
        if(!(f%16)) {at.x=motion::wrap(int(at.x)+384);x=motion::wrap(int(x)+384);effect(x,0);effect(4608-x,0);}
        if(f&1) {
            t.type=type;t.pid=std::uint8_t(other);t.speed=std::uint8_t((f%16)*4+24);t.group=1;t.angle=0;t.center={x,0};t.animated=false;
            add();t.center.x=motion::wrap(4608-x);add();t.animated=true;
        }
        ++f;if(f>=time[0])finish();return;
    }
    case 8:
        if(!(f%8)) {
            t.type=type;t.speed=time[1];t.pid=std::uint8_t(other);t.angle=0;t.group=44;t.count=time[0];
            Point warning;
            switch(f) {
            case 0:warning={2304,512};break;
            case 8:warning={1536,1280};break;
            case 16:warning={3072,1280};t.center={2304,512};break;
            case 24:warning={1536,896};t.center={1536,1280};break;
            case 32:warning={3072,896};t.center={3072,1280};break;
            case 40:warning={2304,1664};t.center={1536,896};break;
            case 48:t.center={3072,896};break;
            case 56:t.center={2304,1664};finish();
        break;
            }
            if(f<=40)effect(warning.x,warning.y,Effect::axis);
            if(f>=16)add();
        }
        break;
    }
    ++f;
}
}
