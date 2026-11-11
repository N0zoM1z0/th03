#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"

namespace th03 {
namespace {
int pixel(int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);}
int screen_x(const Round& r,int x,unsigned pid) {return 16+int(pid)*320+pixel(x)+r.fg_shift[pid];}
}
void ExtraAttacks::reset() {for(auto& pool:items)for(auto& e:pool)e.state=0;}
void ExtraAttacks::fly_init(Round& r,Extra& e,Point from,Point target,unsigned pid,int speed) {
    e.state=2;e.frame=0;e.center=from;e.pid=std::uint8_t(pid);e.target_x=target.x;
    const auto source_x=motion::wrap(screen_x(r,from.x,pid)*16),target_x=motion::wrap(screen_x(r,target.x,pid^1)*16);
    const auto angle=motion::angle_to({source_x,from.y},{target_x,target.y});
    const auto v=motion::polar(angle,std::int16_t(r.speed/4+speed));e.velocity={v.x,v.y};
    e.boundary_x=motion::wrap((screen_x(r,target.x,pid^1)-16-int(pid)*320)*16);
}
bool ExtraAttacks::fly_update(Extra& e,unsigned owner) {
    const auto next=motion::wrap(int(e.center.x)+e.velocity.x);
    if(e.pid ? e.boundary_x>=next : e.boundary_x<=next) {
        e.center.x=e.target_x;e.state=3;e.pid=std::uint8_t(owner^1);return true;
    }
    e.center.x=next;e.center.y=motion::wrap(int(e.center.y)+e.velocity.y);return false;
}
void ExtraAttacks::add_kotohime(Round& r,Point center,unsigned pid) {
    for(unsigned i=0;i<8;++i) {
        auto& e=items[pid][i];if(e.state)continue;
        const auto x=std::int16_t(r.random.ring()%4608),y=std::int16_t(r.random.ring()%1024);
        fly_init(r,e,center,{x,y},pid,90);
        e.duration=std::int16_t((r.random.ring()&4095)+1536);e.radius=std::int16_t((r.random.ring()&31)+16);
        e.angle=0;e.mode=0;return;
    }
}
void ExtraAttacks::kotohime_gauge(Round& r,Point target,unsigned pid) {
    auto& e=items[pid][items[pid][8].state ? 9 : 8];
    fly_init(r,e,r.players[pid].center,target,pid,120);e.duration=3072;e.radius=32;e.angle=0;e.mode=1;
}
void ExtraAttacks::update_kotohime(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    const unsigned other=pid^1;
    for(unsigned i=0;i<10;++i) {
        auto& e=items[pid][i];if(!e.state)continue;
        if(e.state==1) {
            if(e.center.y>=e.duration) {
                const auto effect=[&] {r.sounds.push_back(3);r.effect_add(e.center,other,Effect::explosion);};
                auto& t=r.bullets.model;
                const auto ring=[&](unsigned count,int delta) {
                    const auto& pattern=r.gauges.timing[pid];t.type=pattern[2];t.count=pattern[0];t.speed=16;
                    for(unsigned j=0;j<count;++j) {r.bullets.add(r,pid*40);t.speed=std::uint8_t(t.speed+2);t.angle=std::uint8_t(t.angle+delta);}
                };
                const auto bullet_origin=[&] {t.angle=std::uint8_t(r.random.ring());t.group=38;t.pid=std::uint8_t(other);t.center=e.center;};
                if(e.angle==4) {
                    effect();if(e.mode) {t.speed=28;bullet_origin();ring(4,r.gauges.timing[pid][1] ? -12 : 12);}
                } else if(e.angle==8||e.angle==12)effect();
                else if(e.angle==16) {
                    effect();t.speed=24;bullet_origin();
                    if(!e.mode) {t.type=2;t.count=10;r.bullets.add(r,pid*40);}
                    else ring(10,r.gauges.timing[pid][1] ? 7 : -7);
                    e.state=0;
                }
                ++e.angle;
            } else {
                e.center.y=motion::wrap(int(e.center.y)+e.radius);
                const Hitbox box{{motion::wrap(int(e.center.x)-256),motion::wrap(int(e.center.y)-256)},
                    {motion::wrap(int(e.center.x)+256),motion::wrap(int(e.center.y)+256)},std::uint8_t(other),{256,256}};
                r.hitbox_hits(box,e.center.y,charge,Against::enemy,true);collision.rectangle(other,e.center,6,6);
            }
        } else if(e.state==2)fly_update(e,pid);
        else if(e.state<=28)++e.state;
        else {e.frame=0;e.state=1;}
        ++e.frame;
    }
}
}
