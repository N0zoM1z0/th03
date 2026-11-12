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
    if(r.boss_launched_by!=pid)return;
    if(state.mode==255) {
        if(frame==1)r.sounds.push_back(16);
        if(motion::wrap(int(frame)*8)>=200) {r.score_add(pid^1,2560);state.mode=0;r.boss_launched_by=255;}
    } else if(state.mode&&character_id(r.players[pid].paletted)==1&&!state.hit) {
        if(state.render_mode==5)state.render_frame=0;
        if(state.render_mode==2||state.render_mode==5) {if(state.render_frame>=32)state.render_mode=3;++state.render_frame;}
    }
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
    hit(r,pid,collision,charge);
}
void Bosses::hit(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    const unsigned other=pid^1;const auto center=state.center;
    collision.rectangle(other,center,28,28);
    const Hitbox box{{motion::wrap(int(center.x)-512),motion::wrap(int(center.y)-512)},
        {motion::wrap(int(center.x)+512),motion::wrap(int(center.y)+512)},std::uint8_t(other),{512,512}};
    state.hit=r.hitbox_hits(box,center.y,charge,Against::enemy,true);state.hp=motion::wrap(int(state.hp)-state.hit);hit_end(r,pid);
}
void Bosses::mima_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;
    s.hp=110;s.sprite=std::uint16_t(0x28c+pid*40);
}
void Bosses::mima_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.render_mode=0;s.mode=1;frame=0;};
    if(s.mode>=2&&s.mode<=5) {
        if(frame<2) {s.render_mode=2;s.render_frame=0;mima_angles[0]=0;mima_angles[1]=192;return;}
        if(frame<32)return;
        if(!(frame%2)) {
            r.sounds.push_back(3);t.angle=mima_angles[0];t.group=34;t.center=s.center;t.speed=parameters[0];t.type=2;t.animated=false;add();t.animated=true;
            mima_angles[0]=std::uint8_t(mima_angles[0]+9);
            if(frame<parameters[5]&&!(frame%6)) {t.type=1;t.group=15;t.speed=parameters[4];t.angle=mima_angles[1];add();t.angle=std::uint8_t(128-mima_angles[1]);add();}
            mima_angles[1]=std::uint8_t(mima_angles[1]+3);
        }
        if(frame>130)finish();
    } else if(s.mode>=6&&s.mode<=10) {
        if(frame==16)s.render_mode=5;else if(frame<32)return;
        const Point center{motion::wrap(int(s.center.x)+384),motion::wrap(int(s.center.y)-512)};
        if(frame==32||frame==36||frame==40) {r.effect_add(center,other,Effect::center);return;}
        if(frame<=48)return;
        if(!(frame%4)) {
            t.angle=0;t.group=28;t.center=center;t.count=parameters[1];t.speed=parameters[2];t.type=2;t.animated=false;add();t.type=1;add();t.animated=true;
        }
        if(frame==64) {t.angle=std::uint8_t(r.random.ring());t.group=37;t.center=center;t.speed=32;t.type=2;t.animated=false;add();t.animated=true;}
        if(!(frame%2))r.sounds.push_back(3);
        if(frame>=128)finish();
    } else if(s.mode>=11&&s.mode<=13) {
        const auto remainder=std::uint8_t(frame%parameters[3]);move_sine();s.render_mode=5;
        if(remainder==1||remainder==parameters[3]/2) {
            t.group=remainder==parameters[3]/2 ? 18 : 24;r.sounds.push_back(10);t.angle=0;
            t.center={motion::wrap(int(s.center.x)+384),motion::wrap(int(s.center.y)-512)};
            t.speed=88;t.type=2;t.animated=false;t.has_trail=true;add();t.has_trail=false;t.animated=true;
        }
        if(frame>=150)finish();
    } else if(s.mode>=14&&s.mode<=17) {
        move_sine();
        if(frame==1) {mima_angles[2]=(r.random.ring()&1) ? 7 : std::uint8_t(-7);mima_angles[3]=std::uint8_t(r.random.ring());}
        if(!(frame%2)) {t.center=orbit(s.center,mima_angles[3],768);t.angle=std::uint8_t(mima_angles[3]+64);t.type=4;t.group=33;t.speed=parameters[6];add();r.sounds.push_back(10);mima_angles[3]=std::uint8_t(mima_angles[3]+mima_angles[2]);}
        if(frame>=72) {s.mode=1;frame=0;}
    }
}
void Bosses::update_mima(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;
        parameters={{std::uint8_t(32+level),std::uint8_t(2+level/4),std::uint8_t(32+level),std::uint8_t(64-2*level),
            std::uint8_t(40+level),std::uint8_t(64+level*4),std::uint8_t(54+level)}};
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    r.bullets.model.pid=std::uint8_t(pid^1);++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:mima_pattern(r,pid);break;
    }
    hit(r,pid,collision,charge);
}

}
