#include "boss.hpp"
#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>

namespace th03 {
namespace {
Point orbit(Point center,std::uint8_t angle,int length) {
    const auto v=motion::polar(angle,motion::wrap(length));
    return {motion::wrap(int(center.x)+v.x),motion::wrap(int(center.y)+v.y)};
}
void restore(Round& r,unsigned pid) {std::copy_n(r.palette_backup.begin()+pid*3,3,r.palette.begin()+pid*3);}
}
void Bosses::reimu_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;
    s.hp=110;s.sprite=std::uint16_t(0x28c+pid*40);
}
bool Bosses::start(Round& r,unsigned pid) {
    if(r.gauge_flags[pid]!=5)return false;
    if(r.boss_launched_by==255) {
        state=templates[pid];state.count=std::uint8_t(1+(r.random.ring()&7));frame=0;
        r.boss_launched_by=std::uint8_t(pid);r.gauge_flags[pid]=0;r.sounds.push_back(18);
        restore(r,pid^1);r.boss_active[pid^1]=1;return true;
    }
    if(state.mode==255)return false;
    state.mode=255;frame=0;restore(r,pid^1);r.boss_active[pid]=0;return false;
}
void Bosses::move_sine() {
    auto& s=state;s.center.x=motion::wrap(int(s.center.x)+s.velocity.x);s.center.y=motion::wrap(int(s.center.y)+s.velocity.y);
    ++s.angle;s.velocity.y=motion::wrap(motion::floor_shift8(16*motion::sine(s.angle)));
    if(s.center.x<=768)s.velocity.x=32;else if(s.center.x>=3840)s.velocity.x=-32;
}
void Bosses::fall(Round& r,unsigned pid) {
    auto& s=state;s.center.x=motion::wrap(int(s.center.x)+s.velocity.x);s.center.y=motion::wrap(int(s.center.y)+32);
    if(s.center.x<=768)s.velocity.x=32;else if(s.center.x>=3840)s.velocity.x=-32;
    r.boss_active[pid^1]=0;
    if(s.center.y>=6656) {s.mode=0;r.boss_launched_by=255;r.combo_points_for_boss_attack=5120;}
}
void Bosses::next_pattern(Round& r) {
    move_sine();if(frame<80)return;
    std::uint8_t choice;
    do {choice=std::uint8_t(r.random.ring()&15);}while(int(previous)+2>=choice&&int(previous)-2<=choice);
    previous=choice;frame=0;state.mode=std::uint8_t(2+choice);++state.pattern;
    if(state.pattern>state.count)state.mode=128;
}
void Bosses::hit_end(Round& r,unsigned pid) {
    if(state.hp>0||state.mode==255)return;
    state.mode=255;frame=0;restore(r,pid^1);
    if(r.gauge_flags[pid^1]!=5)r.combo_points_for_boss_attack=5120;
    r.boss_active[pid^1]=0;if(r.boss_level<16)++r.boss_level;
}
void Bosses::prepare_render(Round& r,unsigned pid) {
    if(r.boss_launched_by!=pid||state.mode!=255)return;
    if(frame==1)r.sounds.push_back(16);
    if(motion::wrap(int(frame)*8)>=200) {r.score_add(pid^1,2560);state.mode=0;r.boss_launched_by=255;}
}
void Bosses::reimu_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.mode=1;frame=0;};
    const auto bullet=[&](unsigned speed) {t.type=2;t.speed=std::uint8_t(speed);t.pid=std::uint8_t(other);t.center=s.center;};
    if(s.mode>=2&&s.mode<=6) {
        if(!frame) {s.scratch={s.center.x,motion::wrap(int(s.center.y)+768)};reimu_direction=std::uint8_t(r.random.ring()&1);reimu_speed=16;}
        auto angle=std::uint8_t(frame*2);if(reimu_direction)angle=std::uint8_t(-angle);
        if(!(frame%parameters[0])) {
            t.type=4;t.group=0;t.pid=std::uint8_t(other);t.angle=std::uint8_t(angle*2);t.speed=reimu_speed;t.center=orbit(s.center,angle,512);add();
            t.angle=std::uint8_t(angle*2+128);angle=std::uint8_t(angle+128);t.center=orbit(s.center,angle,512);add();
        }
        if(!(frame%2))++reimu_speed;
        s.center.y=orbit(s.scratch,std::uint8_t(frame*2-64),768).y;
        if(frame>=128)finish();
    } else if(s.mode==8||s.mode==9||s.mode==10||s.mode==13) {
        move_sine();bullet(parameters[2]);
        if(frame<64) {
            if(r.frame%16)return;
            t.angle=32;t.group=8;add();t.angle=96;add();return;
        }
        if(frame<100) {if(r.frame%16)return;t.group=21;t.angle=64;add();}else finish();
    } else if(s.mode>=15&&s.mode<=17) {
        move_sine();
        if(!frame) {s.render_mode=1;reimu_angle=std::uint8_t(r.random.ring());}
        if(frame<80) {
            for(unsigned i=0;i<parameters[3];++i)reimu_orbit[i]=orbit(s.center,std::uint8_t(i*256/parameters[3]+reimu_angle),frame<24 ? frame*32 : 768);
            reimu_angle=std::uint8_t(reimu_angle+8);
            if(frame>=24&&!(r.frame%16)) {bullet(parameters[4]);t.angle=std::uint8_t(r.random.ring());t.group=38;t.count=parameters[5];add();}
        } else if(frame==80) {
            for(unsigned i=0;i<parameters[3];++i)r.extra_attacks.special(r,reimu_orbit[i],pid,std::uint8_t(i*256/parameters[3]+reimu_angle));
            finish();s.render_mode=0;
        }
    } else if(s.mode==7||s.mode==11||s.mode==12||s.mode==14) {
        move_sine();
        if(frame<128) {
            if(frame%16)return;
            bullet(parameters[2]);t.angle=std::uint8_t(frame);t.group=14;add();t.angle=std::uint8_t(120-std::uint8_t(frame));add();
        } else finish();
    } else if(s.mode==128)fall(r,pid);
}
void Bosses::update_reimu(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;
        parameters[0]=std::uint8_t(5-level/5);parameters[1]=std::uint8_t(level+24);parameters[2]=std::uint8_t(level*2+40);
        parameters[3]=std::uint8_t(level/8+4);parameters[4]=std::uint8_t(level+16);parameters[5]=std::uint8_t(level+16);
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;
    if(!state.mode) {if(frame!=100)return;frame=0;state.mode=1;}
    if(state.mode==1)next_pattern(r);
    reimu_pattern(r,pid);if(state.mode==255)return;
    const unsigned other=pid^1;const auto center=state.center;
    collision.rectangle(other,center,28,28);
    const Hitbox box{{motion::wrap(int(center.x)-512),motion::wrap(int(center.y)-512)},
        {motion::wrap(int(center.x)+512),motion::wrap(int(center.y)+512)},std::uint8_t(other),{512,512}};
    state.hit=r.hitbox_hits(box,center.y,charge,Against::enemy,true);state.hp=motion::wrap(int(state.hp)-state.hit);hit_end(r,pid);
}
}
