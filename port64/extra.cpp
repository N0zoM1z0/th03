#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

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

namespace th03 {
namespace {
constexpr unsigned slot_count[9]={8,6,14,12,10,8,14,16,16};
bool outside(Point p,int radius) {return p.x<=-radius||p.x>=4608+radius||p.y<=-radius||p.y>=5888+radius;}
void advance(Point& p,Point v) {p.x=motion::wrap(int(p.x)+v.x);p.y=motion::wrap(int(p.y)+v.y);}
Point polar(std::uint8_t angle,int length) {const auto v=motion::polar(angle,motion::wrap(length));return {v.x,v.y};}
void clover(CollisionMap& collision,unsigned pid,Point center) {
    collision.rectangle(pid,center,8,16);
    center.x=motion::wrap(int(center.x)-192);collision.rectangle(pid,center,4,8);
    center.x=motion::wrap(int(center.x)+384);collision.rectangle(pid,center,4,8);
}
}
void ExtraAttacks::add(Round& r,Point center,unsigned pid) {
    const auto character=character_id(r.players[pid].paletted);
    if(character==4) {add_kotohime(r,center,pid);return;}
    // Ellen and Kana draw these values before looking for a free slot.
    Point target;std::uint8_t angle=0,spin=0;
    if(character==3) {
        target.x=std::int16_t(r.random.ring()%3200+704);target.y=std::int16_t(r.random.ring()%3200+1280);
        spin=(r.random.ring()&1) ? 1 : 255;angle=std::uint8_t(r.random.ring());
    } else if(character==5)target.x=std::int16_t(r.random.ring()%4608);
    const unsigned count=character==6||character==8 ? 8 : slot_count[character],step=character==7 ? 2 : 1;
    unsigned added=0;
    for(unsigned i=0;i<count;i+=step) {
        auto& e=items[pid][i];if(e.state)continue;
        switch(character) {
        case 0: {
            // Pascal arguments are evaluated from left to right by TC4.
            const auto x=std::int16_t(r.random.ring()%4608),y=std::int16_t(r.random.ring()&2047);
            fly_init(r,e,center,{x,y},pid,90);return;
        }
        case 1: {
            const auto x=std::int16_t(r.random.ring()%4608),y=std::int16_t(r.random.ring()%4608);
            fly_init(r,e,center,{x,y},pid,90);e.duration=0;e.frame=3;return;
        }
        case 2:fly_init(r,e,center,{std::int16_t(r.random.ring()%4608),5888},pid,110);return;
        case 3:
            fly_init(r,e,center,target,pid,70);e.radius=0;e.mode=spin;e.angle=std::uint8_t(angle+added*128);
            if(added++)return;
            break;
        case 5:
            target.y=std::int16_t(r.random.ring()%2048);fly_init(r,e,center,target,pid,90);
            e.angle=std::uint8_t((r.random.ring()&31)-15+(target.x>=2304 ? 128 : 0));return;
        case 6:
            fly_init(r,e,center,{std::int16_t(r.random.ring()%4608),256},pid,100);
            e.homing_disabled=r.random.ring()&1;e.angle=64;e.speed=std::uint8_t((r.random.ring()&15)+32);return;
        case 7:
            fly_init(r,e,center,{std::int16_t(r.random.ring()%4416+96),0},pid,80);
            fly_init(r,items[pid][i+1],center,{std::int16_t(r.random.ring()%4416+96),6016},pid,80);return;
        case 8: {
            const auto x=std::int16_t(r.random.ring()%4608),y=std::int16_t(r.random.ring()%4096+1536);
            fly_init(r,e,center,{x,y},pid,70);e.radius=0;e.duration=96;return;
        }
        }
    }
}
void ExtraAttacks::special(Round& r,Point center,unsigned owner,std::uint8_t angle,std::uint8_t mode) {
    const auto character=character_id(r.players[owner].paletted);
    if(character==4) {kotohime_gauge(r,center,owner);return;}
    const unsigned first=character==8 ? 8 : 0;
    for(unsigned i=first;i<slot_count[character];++i) {
        auto& e=items[owner][i];if(e.state)continue;
        e.center=center;
        switch(character) {
        case 0:e.state=1;e.frame=0;e.pid=std::uint8_t(owner^1);e.velocity=polar(angle,80);break;
        case 2:e.state=3;e.frame=0;e.pid=std::uint8_t(owner^1);break;
        case 3:e.state=1;e.frame=0;e.radius=0;e.mode=mode;e.angle=angle;e.pid=std::uint8_t(owner^1);break;
        case 5:e.state=1;e.frame=0;e.angle=angle;e.speed=8;break;
        case 6:e.state=1;e.homing_disabled=true;e.frame=64;e.angle=angle;e.speed=32;e.pid=std::uint8_t(owner^1);break;
        case 8:e.state=3;e.frame=0;e.pid=std::uint8_t(owner^1);e.radius=0;e.duration=32;break;
        default:throw std::runtime_error("character has no special Extra allocator");
        }
        return;
    }
}
void ExtraAttacks::prepare_render(const Round& r,unsigned pid) {
    if(character_id(r.players[pid].paletted)==0)for(unsigned i=0;i<8;++i)if(items[pid][i].state)++items[pid][i].frame;
}
void ExtraAttacks::update(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    const auto character=character_id(r.players[pid].paletted),other=pid^1;
    if(character==4) {update_kotohime(r,pid,collision,charge);return;}
    const auto hit=[&](Point center,Point radius=Point{256,256}) {
        const Hitbox box{{motion::wrap(int(center.x)-radius.x),motion::wrap(int(center.y)-radius.y)},
            {motion::wrap(int(center.x)+radius.x),motion::wrap(int(center.y)+radius.y)},std::uint8_t(other),radius};
        return r.hitbox_hits(box,center.y,charge,Against::enemy,true);
    };
    if(character==7) {
        for(unsigned i=0;i<16;i+=2) {
            auto& a=items[pid][i];auto& b=items[pid][i+1];if(!a.state)continue;
            if(a.state==1) {
                ++a.frame;
                if(a.frame==4) {r.effect_add({a.center.x,0},a.pid,Effect::center);r.effect_add({b.center.x,5888},b.pid,Effect::center);}
                else if(a.frame==16)r.sounds.push_back(20);
                else if(a.frame>40&&a.frame<112)collision.slope(other,a.center.x,b.center.x,2);
                else if(a.frame>136)a.state=b.state=0;
                continue;
            }
            bool arrived=false;
            if(a.state==2) {if(fly_update(a,pid))a.center.y=0;}
            else if(a.state<=28)++a.state;
            else {a.frame=0;arrived=true;}
            ++a.frame;
            if(b.state==2) {if(fly_update(b,pid))b.center.y=5888;}
            else if(b.state<=28)++b.state;
            else {b.frame=0;if(arrived) {a.state=1;++a.frame;continue;}}
            ++b.frame;
        }
        return;
    }
    for(unsigned i=0;i<slot_count[character];++i) {
        auto& e=items[pid][i];if(!e.state)continue;
        switch(character) {
        case 0:
            if(e.state==1) {
                e.center.x=motion::wrap(int(e.center.x)+e.velocity.x);
                if(e.center.x<=0||e.center.x>=4608) {e.velocity.x=motion::wrap(-int(e.velocity.x));e.center.x=motion::wrap(int(e.center.x)+e.velocity.x);}
                e.center.y=motion::wrap(int(e.center.y)+e.velocity.y);
                if(e.center.y< -384) {e.velocity.y=motion::wrap(-int(e.velocity.y));e.center.y=-384;}
                if(e.center.y>=5888) {e.state=0;continue;}
                e.velocity.y=motion::wrap(int(e.velocity.y)+1);hit(e.center);clover(collision,other,e.center);
            } else if(e.state==2) {
                if(fly_update(e,pid)) {
                    auto angle=std::uint8_t(r.random.ring()&31);angle=std::uint8_t(angle+((r.random.ring()&1)*96+128));
                    e.velocity=polar(angle,r.speed/8+50);
                }
            } else if(e.state<=20)++e.state;
            else e.state=1;
            break;
        case 1:
            if(e.state==1) {
                Point next{motion::wrap(int(e.center.x)+e.velocity.x),motion::wrap(int(e.center.y)+e.velocity.y)};
                if(next.x<=0||next.x>=4608) {
                    if(!e.frame) {e.state=0;continue;}
                    --e.frame;e.velocity.x=motion::wrap(-int(e.velocity.x));e.angle=motion::angle_to({}, {e.velocity.x,e.velocity.y});
                } else if(next.y<=0||next.y>=5888) {
                    if(!e.frame) {e.state=0;continue;}
                    --e.frame;e.velocity.y=motion::wrap(-int(e.velocity.y));e.angle=motion::angle_to({}, {e.velocity.x,e.velocity.y});
                } else e.center=next;
                if(e.duration>=16) {if(e.duration<32)e.speed=std::uint8_t(e.speed+(std::uint16_t(e.duration)%2));else if(e.duration<80)++e.speed;}
                if(e.duration<80)e.velocity=polar(e.angle,e.speed);
                if(hit(next))e.velocity.y=motion::wrap(int(e.velocity.y)-8);
                collision.rectangle(other,next,8,8);
            } else if(e.state==2) {
                if(fly_update(e,pid)) {e.angle=std::uint8_t(r.random.ring());e.speed=0;e.velocity={};continue;}
            } else if(e.state<=28)++e.state;
            else {e.duration=0;e.state=1;r.sounds.push_back(10);}
            e.duration=motion::wrap(int(e.duration)+1);break;
        case 2:
            if(e.state==1) {
                if(e.frame<48) {e.center.y=motion::wrap(int(e.center.y)-256);if(e.center.y< -256) {e.frame=48;e.center.y=-256;}}
                else if(e.frame>=120) {e.state=0;continue;}
                const int bottom=std::max(0,int(e.center.y)),height=5888-bottom;
                if(e.frame<100)collision.rectangle(other,{e.center.x,motion::wrap(bottom+height/2)},2,height/32);
            } else if(e.state==2) {if(fly_update(e,pid)) {e.center.y=5888;continue;}}
            else if(e.state<=28) {++e.state;if(e.state==12)r.effect_add({e.center.x,6176},e.pid,Effect::center);}
            else {e.frame=0;e.state=1;r.sounds.push_back(20);}
            ++e.frame;break;
        case 3: {
            auto& h=ellen_history[pid][i];
            if(e.state==1) {
                for(unsigned j=6;j>0;--j)h[j]=h[j-1];
                if(e.radius<=3328) {
                    const auto v=polar(e.angle,e.radius);h[0]={motion::wrap(int(e.center.x)+v.x),motion::wrap(int(e.center.y)+v.y)};
                    e.velocity={motion::wrap(int(h[0].x)-h[1].x),motion::wrap(int(h[0].y)-h[1].y)};
                    e.radius=motion::wrap(int(e.radius)+24);e.angle=std::uint8_t(e.angle+e.mode);
                } else {
                    if(outside(h[0],384)&&outside(h[6],384)) {e.state=0;continue;}
                    advance(h[0],e.velocity);
                }
                hit(h[0]);collision.rectangle(other,h[0],6,6);
            } else if(e.state==2) {if(fly_update(e,pid))h.fill(e.center);}
            else if(e.state<=28)++e.state;
            else {e.frame=0;e.state=1;r.sounds.push_back(10);}
            ++e.frame;break;
        }
        case 5:
            if(e.state==1) {
                advance(e.center,polar(e.angle,e.speed));++e.speed;
                if(!(e.frame%16)) {
                    auto& t=r.bullets.model;t.type=8;t.angle=64;t.group=0;t.acceleration=128;t.sprite=std::uint16_t(pid*40+5760);
                    t.speed=16;t.center=e.center;t.pid=std::uint8_t(other);r.bullets.add(r,pid*40);
                }
                if(outside(e.center,384)) {e.state=0;continue;}
            } else if(e.state==2)fly_update(e,pid);
            else if(e.state<=28)++e.state;
            else {e.frame=0;e.state=1;e.speed=8;}
            ++e.frame;break;
        case 6:
            if(e.state==1) {
                advance(e.center,polar(e.angle,e.speed));
                if(!e.homing_disabled&&e.frame>=64&&e.frame<=80) {
                    const auto angle=motion::angle_to({e.center.x,e.center.y},{r.players[other].center.x,r.players[other].center.y});
                    ++e.speed;const auto raw=std::uint8_t(angle-e.angle);const int delta=raw<128 ? raw : int(raw)-256;
                    e.angle=std::uint8_t(e.angle+delta/8);
                }
                if(outside(e.center,512)) {e.state=0;continue;}
                hit(e.center);clover(collision,other,e.center);
            } else if(e.state==2)fly_update(e,pid);
            else if(e.state<=28)++e.state;
            else {e.frame=0;e.state=1;}
            ++e.frame;break;
        case 8:
            if(e.state==1) {
                if(e.frame<=8)e.radius=motion::wrap(int(e.radius)+6);
                else if(e.frame>=e.duration&&e.frame<e.duration+8)e.radius=motion::wrap(int(e.radius)-6);
                else if(e.frame>=e.duration+8)e.state=0;
                const auto radius=motion::wrap(int(e.radius)*8);hit(e.center,{radius,64});hit(e.center,{64,radius});
                collision.rectangle(other,e.center,e.radius,8);
                collision.rectangle(other,{e.center.x,motion::wrap(int(e.center.y)+int(e.radius)*4)},8,e.radius/4+e.radius);
            } else if(e.state==2) {if(fly_update(e,pid))continue;}
            else if(e.state<=40)++e.state;
            else {e.radius=16;e.frame=0;e.state=1;r.sounds.push_back(7);}
            ++e.frame;break;
        }
    }
}
}
