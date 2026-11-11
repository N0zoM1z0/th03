#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
int pixel(int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);}
Point vector(Point from,Point to,int length) {
    const auto angle=motion::angle_to({from.x,from.y},{to.x,to.y});
    const auto v=motion::polar(angle,std::int16_t(length));return {v.x,v.y};
}
}
std::uint8_t Chains::start(Efe& origin) {
    const auto p=origin.pid,slot=cursor[p];origin.chain_slot=slot;hits[p][slot]=1;value[p][slot]=0;
    cursor[p]=std::uint8_t((slot+1)%16);return slot;
}
void Round::score_add(unsigned pid,std::uint16_t value) {
    auto& digits=scores[pid];
    unsigned carry=0;
    for(unsigned i=0;i<7;++i) {
        const unsigned sum=digits[i]+value%10+carry;
        digits[i]=std::uint8_t(sum%10);carry=sum/10;value=std::uint16_t(value/10);
    }
    // The most significant byte has no AAA, decimal clamp or overflow cap.
    digits[7]=std::uint8_t(digits[7]+carry+value);
}
void Round::gauge_add(unsigned pid,std::uint8_t value) {
    auto& p=players[pid];
    if(!p.hyper_active&&p.gauge_avail<4080)p.gauge_avail=std::min<std::uint16_t>(std::uint16_t(p.gauge_avail+value),4080);
}
std::uint16_t Round::combo_add(unsigned pid,unsigned slot,std::uint16_t value) {
    auto& combo=combos[pid];
    auto hits=chains.hits[pid][slot];
    if(hits<2)return combo.bonus;
    const auto bonus=std::uint16_t(std::min<unsigned>(unsigned(value)+combo.bonus,65535));
    combo.bonus=bonus;
    auto& p=players[pid];p.combo_hits_max=std::max(p.combo_hits_max,hits);p.combo_bonus_max=std::max(p.combo_bonus_max,bonus);
    if(hits>99) {hits=99;if(bonus!=65535)combo.time=80;}
    if(hits>combo.hits||combo.time<32) {combo.hits=hits;if(bonus!=65535)combo.time=80;}
    return combo.bonus;
}
void Round::point_attack(unsigned pid,std::uint16_t points) {
    if(points>=combo_points_for_boss_attack) {
        if(warning[pid])return;
        if(boss_launched_by!=pid) {
            if(gauge_flags[pid]==5)return;
            gauge_next[pid]=5;warning[pid]=1;
            chains.value[pid][last_chain_slot]=0;chains.fireball[pid][last_chain_slot]=0;chains.extra[pid][last_chain_slot]=0;
            combo_points_for_boss_attack=std::uint16_t(combo_points_for_boss_attack+5120);
            if(boss_level<16)++boss_level;
            if(boss_launched_by==255)++players[pid].boss_attacks;else ++players[pid].boss_reversals;
        } else if(points>=30000) {
            if(boss_panic[pid]||gauge_flags[pid])return;
            gauge_next[pid]=3;warning[pid]=1;boss_panic[pid]=true;
            gauge_levels[pid]=std::min<std::uint8_t>(std::uint8_t(gauge_levels[pid]+3),16);++players[pid].boss_panics;
        }
    } else boss_panic[pid]=false;
}
void Round::fireball_add(const Efe& origin) {
    const auto center=origin.center;
    const unsigned origin_pid=origin.pid,target_pid=origin.pid^1;
    for(auto& f:fireballs)if(!f.flag) {
        // The allocator does not reset frame: a reused slot keeps its cycle.
        f.flag=2;f.center=center;f.pid=origin_pid;
        f.fall_speed=std::uint8_t(20+speed/2+(random.ring()&31));f.fall_speed=std::min<std::uint8_t>(f.fall_speed,128);
        f.hp=std::uint8_t(fireball_variant+2);f.size_words=std::uint8_t(fireball_variant+2);f.size_pixels=48;
        f.generation=fireball_variant ? std::uint8_t(generation_previous+1) : 0;
        const int source_x=16+origin_pid*320+pixel(center.x)+fg_shift[origin_pid];
        f.target_x=std::int16_t(result_frame%512<256 ? random.ring()%4608 : players[target_pid].center.x+(random.ring()&511));
        const int target_x=16+target_pid*320+pixel(f.target_x)+fg_shift[target_pid];
        f.velocity=vector({motion::wrap(source_x*16),center.y},{motion::wrap(target_x*16),0},70+speed/3);
        f.target_x_origin=motion::wrap((target_x-16-origin_pid*320)*16);return;
    }
}
void Round::update_fireballs(CollisionMap& collision) {
    for(auto& f:fireballs)if(f.flag) {
        ++f.frame;
        if(f.flag>=9) {
            if(f.frame==14)f.flag=10;else if(f.frame==32)f.flag=9;else if(f.frame>=36)f.flag=0;
        } else if(f.flag==1) {
            const auto x=motion::wrap(int(f.center.x)+f.velocity.x);
            if(bomb_flags[f.pid]||x<=-256||x>=4864) {f.flag=0;continue;}
            f.center.x=x;
            const auto y=motion::wrap(int(f.center.y)+f.velocity.y);
            if(y>=6144) {f.flag=0;continue;}
            f.center.y=y;collision.rectangle(f.pid,{x,motion::wrap(y+128)},8,8);
        } else if(f.flag==2) {
            const auto x=motion::wrap(int(f.center.x)+f.velocity.x);
            if(f.pid==0 ? x>=f.target_x_origin : x<=f.target_x_origin) {
                f.center={f.target_x,0};f.velocity={0,f.fall_speed};f.flag=1;f.pid^=1;continue;
            }
            f.center.x=x;f.center.y=motion::wrap(int(f.center.y)+f.velocity.y);
        }
    }
}
void Round::charged_fireball(unsigned pid,const Efe& origin) {
    auto& charge=chains.fireball[pid][last_chain_slot];
    if(charge<12-speed/16)return;
    charge=0;fireball_add(origin);
}
void Round::charged_extra(unsigned pid,unsigned slot,const Efe& origin,const ExtraAdd& add) {
    // The uninitialized fireball stack slot can address the other player's
    // charges, score digits or extends_gained in the original DGROUP.
    const auto address=std::uint16_t(0x4b3e + pid*16+slot);
    std::uint8_t* charge=nullptr;
    if(address>=0x4b3e&&address<0x4b5e) {
        const auto index=unsigned(address)-0x4b3e;charge=&chains.extra[index/16][index%16];
    } else if(address>=0x4b64&&address<0x4b74) {
        const auto index=unsigned(address)-0x4b64;charge=&scores[index/8][index%8];
    } else if(address==0x4b7c)charge=&extends_gained;
    else throw std::runtime_error("Extra Attack chain slot needs its aliased DATA owner");
    if(*charge<6-speed/32)return;
    *charge=0;add(origin.center,std::uint8_t(pid));
}
std::uint8_t Round::explosion_hit(const Hitbox& box,Against against) {
    unsigned count=0;last_explosion_hit=false;
    const auto process=[&](Efe& e) {
        if(e.flag<9)return;
        if(against==Against::enemy&&(e.flag==9||e.flag>=10+e.size_words*2))return;
        if(e.pid!=box.pid||(e.frame&3))return;
        const int extent=e.size_pixels*6;
        const auto left=motion::wrap(int(e.center.x)-extent),top=motion::wrap(int(e.center.y)-extent);
        if(box.right_bottom.x<left||box.right_bottom.y<top)return;
        if(box.left_top.x>motion::wrap(left+extent*2)||box.left_top.y>motion::wrap(top+extent*2))return;
        last_chain_slot=e.chain_slot;
        if(against==Against::enemy)++e.flag;
        else {
            auto& hits=chains.hits[box.pid][last_chain_slot];if(hits<255)++hits;
            int bonus=against==Against::pellet ? hits*2 : against==Against::fireball_blue ? 100+hits*16 : 444+hits*16;
            score_add(box.pid,against==Against::pellet ? 1 : against==Against::fireball_blue ? 40 : 80);
            bonus=motion::wrap(bonus+speed);
            if(speed<=48)bonus=bonus>=0 ? bonus/2 : -((-bonus+1)/2);else if(speed>=96)bonus=motion::wrap(bonus*2);
            const unsigned weight=against==Against::pellet ? 1 : unsigned(against)*3;
            auto& value=chains.value[box.pid][last_chain_slot];value=std::uint8_t(value+weight);
            gauge_add(box.pid,std::uint8_t(against==Against::pellet ? 4 : weight*3));
            auto& charge=chains.fireball[box.pid][last_chain_slot];
            auto& extra=chains.extra[box.pid][last_chain_slot];
            if(value<4)charge=std::uint8_t(charge+2);
            else if(value<10)charge=std::uint8_t(charge+5);
            else if(value<20) {charge=std::uint8_t(charge+2);++extra;}
            else extra=std::uint8_t(extra+2);
            point_attack(box.pid,combo_add(box.pid,last_chain_slot,std::uint16_t(bonus)));
            charged_fireball(box.pid,e);
        }
        ++count;last_explosion_hit=true;
    };
    for(auto& e:enemies)process(e);
    for(auto& f:fireballs)process(f);
    return std::uint8_t(count);
}
void Round::enemy_circle(Point center,std::uint8_t pid) {
    circle_cursor=std::uint8_t((circle_cursor+1)%12);
    circles[circle_cursor]={1,pid,std::int16_t(16+pid*320+pixel(center.x)+fg_shift[pid]-24),std::int16_t(pixel(center.y)-8)};
}
void Round::charge_circle(const Hitbox& box) {
    const auto width=std::uint16_t(int(box.radius.x)*2),height=std::uint16_t(int(box.radius.y)*2);
    if(!width||!height)throw std::domain_error("hitcircle random center divide error");
    const auto x=motion::wrap(int(box.left_top.x)+random.ring()%width);
    const auto y=motion::wrap(int(box.left_top.y)+random.ring()%height);
    enemy_circle({x,y},box.pid);
}
void Round::player_circle(Point center,std::uint8_t pid) {
    circles[12]={1,pid,std::int16_t(16+pid*320+pixel(center.x)+fg_shift[pid]-24),std::int16_t(pixel(center.y)-8)};
}
void Round::update_circles() {
    for(auto& circle:circles)if(circle.age) {++circle.age;if(circle.age>16)circle.age=0;}
}
std::uint8_t Round::hitbox_hits(Hitbox box,std::int16_t center_y,const ChargeQuery& charge,Against against) {
    if(center_y<0||defeat==2)return 0;
    one_hit=false;
    std::uint8_t damage=0;
    for(auto& shot:shots) {
        if(!shot.alive||shot.pid!=box.pid)continue;
        const auto x=motion::wrap(int(shot.top_left.x)+256),y=motion::wrap(int(shot.top_left.y)+128);
        if(motion::wrap(x-256)>box.right_bottom.x||motion::wrap(x+256)<box.left_top.x||y<box.left_top.y||y>box.right_bottom.y)continue;
        shot.alive=false;damage=std::uint8_t(damage+2);enemy_circle({x,y},box.pid);
    }
    damage=std::uint8_t(damage+explosion_hit(box,against));
    const auto charged=charge(box);damage=std::uint8_t(damage+charged.damage);one_hit=charged.one_hit;
    if(bomb_flags[box.pid]&&!(result_frame%2))++damage;
    return damage;
}
void Round::hit_enemies(const ChargeQuery& charge,const ExtraAdd& extra) {
    for(int i=39;i>=0;--i) {
        auto& e=enemies[unsigned(i)];if(e.flag!=1||e.center.y<=0)continue;
        if(damage_all[e.pid]) {e.hp=0;e.flag=9;chains.start(e);e.frame=0;continue;}
        const int radius=e.size_pixels==16 ? 160 : e.size_pixels*7;
        const Hitbox box{{motion::wrap(e.center.x-radius),motion::wrap(e.center.y-radius)},
                         {motion::wrap(e.center.x+radius),motion::wrap(e.center.y+radius)},e.pid,{std::int16_t(radius),std::int16_t(radius)}};
        if(!hitbox_hits(box,e.center.y,charge,Against::enemy))continue;
        if(!e.hp||one_hit) {
            e.flag=9;enemy_killed=true;
            if(!last_explosion_hit)chains.start(e);
            else {
                gauge_add(e.pid,32);const auto slot=last_chain_slot;e.chain_slot=slot;
                auto& hits=chains.hits[e.pid][slot];if(hits<255)++hits;
                point_attack(e.pid,combo_add(e.pid,slot,std::uint16_t(hits*16)));
                auto& t=bullets.model;t.center=e.center;
                t.speed=std::uint8_t(std::min(24+((24*speed)>>7),127));t.angle=0;t.pid=e.pid;
                const unsigned charge_slot=speed/32;
                auto& fire=chains.fireball[e.pid][charge_slot];auto& ex=chains.extra[e.pid][charge_slot];
                const auto transfer=[&] {t.group=29;t.type=3;bullets.add(*this,40);};
                if(hits<=2)++fire;
                else if(hits<=9-charge_slot) {transfer();fire=std::uint8_t(fire+2);}
                else if(hits<=14-charge_slot*2) {fire=std::uint8_t(fire+3);if(!(hits&1)) {transfer();++ex;}}
                else {fire=std::uint8_t(fire+4);++ex;}
                charged_extra(e.pid,charge_slot,e,extra);
                // This intentionally uses last_chain_slot rather than the
                // round-speed charge slot selected above.
                charged_fireball(e.pid,e);
            }
            score_add(e.pid,std::uint16_t(e.size_words*10));
        } else --e.hp;
        e.frame=0;
    }
}
void Round::hit_fireballs(const ChargeQuery& charge,const ExtraAdd& extra,std::uint8_t stack_chain_slot) {
    auto slot=stack_chain_slot;fireball_variant=1;
    for(int i=23;i>=0;--i) {
        auto& f=fireballs[unsigned(i)];if(f.flag!=1)continue;
        const auto pid=f.pid;
        const Against against=Against(f.size_words);
        const Hitbox box{{motion::wrap(f.center.x-192),motion::wrap(f.center.y+48-160)},
                         {motion::wrap(f.center.x+192),motion::wrap(f.center.y+48+160)},pid,{192,160}};
        if(!hitbox_hits(box,motion::wrap(f.center.y+48),charge,against))continue;
        if(!f.hp||last_explosion_hit||one_hit) {
            generation_previous=f.generation;
            if(last_explosion_hit) {
                f.flag=9;slot=last_chain_slot;f.chain_slot=slot;
                auto& ex=chains.extra[pid][slot];if(against==Against::fireball_red)++ex;
                if(ex>=7-speed/32) {ex=0;extra(f.center,pid);}
                if(generation_previous<4)fireball_add(f);
            } else {
                const auto current=chains.cursor[pid];
                chains.extra[pid][current]=std::uint8_t(chains.extra[pid][current]+unsigned(against)-1);
                f.flag=0;charged_extra(pid,current,f,extra);gauge_add(pid,16);score_add(pid,50);fireball_add(f);
            }
            // Ordinary DOS render flow leaves 0Fh here; the caller supplies
            // that stack context explicitly, including any recovered glitch.
            charged_extra(pid,slot,f,extra);
        } else --f.hp;
        fireball_hit=true;f.frame=0;
    }
    fireball_variant=0;
}

void Round::update_bullets(CollisionMap& collision) {
    bullets.update(*this,collision,[&](Point center,std::uint8_t pid) {
        return explosion_hit({{motion::wrap(center.x-96),motion::wrap(center.y-96)},
                              {motion::wrap(center.x+96),motion::wrap(center.y+96)},pid},Against::pellet)!=0;
    });
}
void Round::update_enemies(CollisionMap& collision,const ChargeQuery& charge,const ExtraAdd& extra) {
    update_enemy_scripts();
    for(const auto& e:enemies)if(e.flag==1) {
        const int tiles=e.size_pixels*3/16;collision.rectangle(e.pid,e.center,tiles,tiles);
    }
    hit_enemies(charge,extra);
}

}
