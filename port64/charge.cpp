#include "charge.hpp"
#include "round.hpp"
#include "motion.hpp"
#include <stdexcept>

namespace th03 {
namespace {
bool outside(Point point,int radius) {
    return point.x<=-radius||point.x>=4608+radius||point.y<=-radius||point.y>=5888+radius;
}
void advance(Point& point,Point velocity) {
    point.x=motion::wrap(int(point.x)+velocity.x);point.y=motion::wrap(int(point.y)+velocity.y);
}
bool overlap(Point point,const Hitbox& box,int margin) {
    return motion::wrap(int(point.x)-box.right_bottom.x)<=margin&&motion::wrap(int(box.left_top.x)-point.x)<=margin&&
        motion::wrap(int(point.y)-box.right_bottom.y)<=margin&&motion::wrap(int(box.left_top.y)-point.y)<=margin;
}
}
void ChargeShots::reset() {
    for(auto& pool:reimu)for(auto& shot:pool)shot.state=0;
    for(auto& pool:mima)for(auto& shot:pool)shot.active=0;
    // The original Mima reset does not clear its two controller bytes.
    for(auto& shot:marisa)shot.active=0;
    for(auto& pool:ellen)for(auto& shot:pool)shot.state=0;
    // Round preparation calls only these four charge reset functions. The
    // remaining owners' dedicated reset procedures are unused in this path.
}
void ChargeShots::add(Round& round,Point center,unsigned pid) {
    switch(character_id(round.players[pid].paletted)) {
    case 0:
        for(unsigned i=0;i<4;++i) {
            auto& shot=reimu[pid][i];shot.state=1;shot.frame=0;shot.history.fill(center);
            shot.angle=std::uint8_t(0x90+i*0x20);shot.speed=0x60;
        }
        reimu_alternate_hit=1;return;
    case 1: {
        constexpr std::uint8_t angles[6]={192,182,202,192,176,208};
        mima_active[pid]=1;mima_frame[pid]=0;
        for(unsigned i=0;i<15;++i) {
            auto& shot=mima[pid][i];shot.active=i==0;shot.unused=0;shot.center=center;
            const auto v=motion::polar(angles[i%6],176);shot.velocity={v.x,v.y};
        }
        return;
    }
    case 2: {
        auto& shot=marisa[pid];shot.active=1;shot.frame=0;
        shot.history.fill({center.x,motion::wrap(int(center.y)-256)});
        round.players[pid].shot_active=0;round.sounds.push_back(6);return;
    }
    case 3:
        for(unsigned i=0;i<32;++i) {
            auto& shot=ellen[pid][i];shot.state=std::uint8_t(i*2);shot.phase=0;shot.center=center;
            shot.angle=std::uint8_t(round.random.ring());shot.length=80;
        }
        return;
    case 4: {
        auto& shot=kotohime[pid];shot.active=1;shot.animation=0;shot.center=center;shot.velocity_y=-16;
        round.sounds.push_back(6);return;
    }
    case 5:
        kana_active[pid]=1;kana_frame[pid]=0;
        for(unsigned i=0;i<4;++i) {
            constexpr std::uint8_t angles[4]={0x90,0xb8,0xc8,0xf0};
            auto& shot=kana[pid][i];shot.history.fill(center);shot.length=48;shot.angle=angles[i];
        }
        return;
    case 6:
        rikako_active[pid]=1;rikako_frame[pid]=0;rikako_radius[pid]=128;rikako_center[pid]=center;
        for(unsigned i=0;i<4;++i) {auto& shot=rikako[pid][i];shot.center=center;shot.angle=std::uint8_t(i*64+32);}
        return;
    case 7:
        chiyuri[pid][0].animation=0;chiyuri[pid][0].center=center;round.players[pid].shot_active=0;
        for(unsigned i=0;i<8;++i)chiyuri[pid][i].age=std::uint8_t(i*4+2);
        return;
    case 8: {
        auto& shot=yumemi[pid];shot.state=1;shot.frame=0;shot.center=center;return;
    }
    default:throw std::runtime_error("invalid charge-shot character");
    }
}
void ChargeShots::reimu_hyper(Point center,unsigned pid) {
    for(auto& shot:reimu[pid])if(!shot.state) {
        shot.state=2;shot.frame=0;shot.history.fill(center);shot.angle=shot.speed=0xc0;break;
    }
    reimu_alternate_hit=0;
}
void ChargeShots::marisa_hyper(Round& round,unsigned pid) {
    auto& shot=marisa[pid];
    if(!shot.active) {
        shot.active=1;const auto center=round.players[pid].center;
        shot.history.fill({center.x,motion::wrap(int(center.y)-256)});round.sounds.push_back(6);
    }
    shot.frame=16;round.players[pid].shot_active=0;
}
void ChargeShots::ellen_hyper(Round& round,Point center,unsigned pid) {
    for(auto& shot:ellen[pid])if(!shot.state) {
        shot.state=1;shot.phase=0;shot.center=center;shot.angle=std::uint8_t(round.random.ring());shot.length=80;return;
    }
}
void ChargeShots::update(Round& round,unsigned pid) {
    auto& player=round.players[pid];
    switch(character_id(player.paletted)) {
    case 0:
        for(unsigned i=0;i<12;++i) {
            auto& shot=reimu[pid][i];if(!shot.state)continue;
            player.gauge_charged=0;
            for(unsigned j=6;j>0;--j)shot.history[j]=shot.history[j-1];
            const auto v=motion::polar(shot.angle,shot.speed);advance(shot.history[0],{v.x,v.y});
            if(shot.state==1) {
                if(shot.speed)shot.speed=std::uint8_t(shot.speed-4);
                else if(shot.frame>=64) {shot.state=2;shot.angle=i<2 ? 0xb0 : 0xd0;shot.speed=0xe0;}
            }
            ++shot.frame;if(outside(shot.history[6],384))shot.state=0;
        }
        return;
    case 1: {
        if(!mima_active[pid])return;
        const auto frame=++mima_frame[pid];
        for(unsigned i=0;i<15;++i) {
            auto& shot=mima[pid][i];if(!shot.active)continue;
            advance(shot.center,shot.velocity);
            if(outside(shot.center,256)) {shot.active=0;if(i==14)mima_active[pid]=0;}
        }
        if(frame<60&&!(frame%4)) {
            auto& shot=mima[pid][frame/4];shot.active=1;shot.center=player.center;round.sounds.push_back(13);
        }
        player.gauge_charged=0;return;
    }
    case 2: {
        auto& shot=marisa[pid];if(!shot.active)return;
        player.gauge_charged=0;++shot.frame;
        for(unsigned i=11;i>0;--i) {
            shot.history[i]=shot.history[i-1];shot.history[i].y=motion::wrap(int(shot.history[i].y)+24);
        }
        if(shot.frame<24)shot.history[0]={player.center.x,motion::wrap(int(player.center.y)-256)};
        else if(shot.frame>36) {player.shot_active=1;shot.active=0;}
        return;
    }
    case 3: {
        auto& pool=ellen[pid];
        bool active=false;for(const auto& shot:pool)if(shot.state) {active=true;break;}
        if(!active)return;
        round.find_target(pid);const Point target{round.target.x,motion::wrap(int(round.target.y)-1760)};
        player.gauge_charged=0;
        for(auto& shot:pool)if(shot.state) {
            if(shot.state==1) {
                advance(shot.center,shot.velocity);
                if(!shot.phase) {
                    shot.length=std::uint8_t(shot.length-2);
                    auto v=motion::polar(shot.angle,shot.length);shot.velocity={v.x,v.y};
                    if(!shot.length) {
                        shot.phase=1;shot.angle=motion::angle_to({shot.center.x,shot.center.y},{target.x,target.y});
                        v=motion::polar(shot.angle,160);shot.velocity={v.x,v.y};
                    }
                } else if(outside(shot.center,128))shot.state=0;
            } else {
                if(--shot.state==1)round.sounds.push_back(1);
                shot.center=player.center;
            }
        }
        return;
    }
    case 4: {
        auto& shot=kotohime[pid];if(!shot.active)return;
        player.gauge_charged=0;shot.center.y=motion::wrap(int(shot.center.y)+shot.velocity_y);
        if(shot.center.y<=-256) {shot.active=0;return;}
        shot.velocity_y=motion::wrap(int(shot.velocity_y)-2);return;
    }
    case 5: {
        if(!kana_active[pid])return;
        player.gauge_charged=0;const auto state=kana_active[pid];
        for(auto& shot:kana[pid]) {
            const auto v=motion::polar(shot.angle,shot.length);
            for(unsigned i=12;i>0;--i)shot.history[i]=shot.history[i-1];
            advance(shot.history[0],{v.x,v.y});if(state==1)--shot.length;
        }
        if(state==1) {
            kana[pid][3].angle=std::uint8_t(kana[pid][3].angle-2);kana[pid][0].angle=std::uint8_t(kana[pid][0].angle+2);
            if(kana_frame[pid]>40) {kana_active[pid]=2;for(auto& shot:kana[pid])shot.length=128;}
        }
        if(kana[pid][0].history[12].y<=-256)kana_active[pid]=0;
        ++kana_frame[pid];return;
    }
    case 6: {
        if(!rikako_active[pid])return;
        player.gauge_charged=0;const auto frame=rikako_frame[pid];auto radius=rikako_radius[pid];
        auto& center=rikako_center[pid];
        if(rikako_active[pid]==1)center.y=motion::wrap(int(center.y)-32);else center=player.center;
        for(unsigned i=0;i<4;++i) {
            auto& shot=rikako[pid][i];const auto v=motion::polar(shot.angle,radius);
            shot.center=center;advance(shot.center,{v.x,v.y});shot.angle=std::uint8_t(shot.angle+((i&1) ? 8 : -8));
        }
        if(frame<32)radius=motion::wrap(int(radius)+32);
        else if(rikako_active[pid]==1) {if(frame>128) {radius=motion::wrap(int(radius)+96);if(frame>144)rikako_active[pid]=0;}}
        else rikako_frame[pid]=32;
        rikako_radius[pid]=radius;++rikako_frame[pid];return;
    }
    case 7:
        if(!chiyuri[pid][7].age)return;
        player.gauge_charged=0;
        for(int i=7;i>=0;--i) {
            auto& shot=chiyuri[pid][unsigned(i)];if(!shot.age)return;
            if(shot.age!=1) {if(--shot.age==1) {shot.center=player.center;round.sounds.push_back(15);}}
            else {
                shot.center.y=motion::wrap(int(shot.center.y)-224);
                if(shot.center.y< -768) {if(i==7)player.shot_active=1;shot.age=0;continue;}
            }
            ++shot.animation;
        }
        return;
    case 8: {
        auto& shot=yumemi[pid];if(!shot.state)return;
        const auto frame=++shot.frame;
        if(shot.state==1) {
            shot.center.y=motion::wrap(int(shot.center.y)-64);
            if(frame>=64||shot.center.y<=0) {shot.state=2;shot.frame=0;round.sounds.push_back(7);}
        } else {
            if(frame>=24&&!(frame%2))round.sounds.push_back(15);
            if(frame>=64)shot.state=0;
        }
        player.gauge_charged=0;return;
    }
    default:throw std::runtime_error("invalid charge-shot character");
    }
}
ChargeHit ChargeShots::hit(Round& round,const Hitbox& box) {
    const auto pid=box.pid;
    switch(character_id(round.players[pid].paletted)) {
    case 0:
        if(reimu_alternate_hit&&(round.result_frame%2))return {};
        for(unsigned i=0;i<6;++i) {
            const auto& shot=reimu[pid][i];if(!shot.state)continue;
            const auto p=shot.history[0];if(p.x<=-256||p.x>=4608||p.y<=-256)continue;
            if(motion::wrap(int(p.x)-box.right_bottom.x)<=320&&motion::wrap(int(box.left_top.x)-p.x)<=320&&
               motion::wrap(int(p.y)-box.right_bottom.y)<=320&&motion::wrap(int(box.left_top.y)-p.y)<=320) {
                round.charge_circle(box);return {1,false};
            }
        }
        return {};
    case 1: {
        if(!mima_active[pid])return {};
        std::uint8_t hits=0;
        for(const auto& shot:mima[pid])if(shot.active) {
            const auto p=shot.center;
            if(motion::wrap(int(p.x)-256)<=box.right_bottom.x&&motion::wrap(int(p.x)+256)>=box.left_top.x&&
               p.y>=box.left_top.y&&p.y<=box.right_bottom.y) {round.charge_circle(box);++hits;}
        }
        return {hits,false};
    }
    case 2: {
        const auto& shot=marisa[pid];if(!shot.active)return {};
        for(unsigned i=0;i<12;i+=4) {
            const auto p=shot.history[i];
            if(p.x>=box.left_top.x&&p.x<=box.right_bottom.x&&p.y>=box.left_top.y) {
                // Charge hits randomize their circles inside the target box;
                // the original point arguments are ignored on this path.
                round.charge_circle(box);return {1,false};
            }
        }
        return {};
    }
    case 3: {
        std::uint8_t hits=0;
        for(auto& shot:ellen[pid])if(shot.state==1&&shot.center.x>=box.left_top.x&&shot.center.x<=box.right_bottom.x&&
                                   shot.center.y>=box.left_top.y&&shot.center.y<=box.right_bottom.y) {
            round.charge_circle(box);shot.state=0;hits=std::uint8_t(hits+2);
        }
        return {hits,false};
    }
    case 4: {
        const auto& shot=kotohime[pid];const auto p=shot.center;
        if(shot.active&&motion::wrap(int(p.x)-box.right_bottom.x)<=640&&motion::wrap(int(box.left_top.x)-p.x)<=640&&
           p.y>=box.left_top.y&&p.y<=box.right_bottom.y) {round.charge_circle(box);return {3,true};}
        return {};
    }
    case 5:
        if(kana_active[pid])for(const auto& shot:kana[pid])for(unsigned i=0;i<=12;i+=4)
            if(overlap(shot.history[i],box,192)) {round.charge_circle(box);return {1,false};}
        return {};
    case 6: {
        std::uint8_t hits=0;
        if(rikako_active[pid])for(const auto& shot:rikako[pid])if(overlap(shot.center,box,192)) {round.charge_circle(box);++hits;}
        return {hits,false};
    }
    case 7: {
        std::uint8_t hits=0;
        for(int i=7;i>=0;--i) {
            const auto& shot=chiyuri[pid][unsigned(i)];if(!shot.age)break;if(shot.age!=1)continue;
            const auto p=shot.center;
            if(motion::wrap(int(p.x)-box.right_bottom.x)<=224&&motion::wrap(int(box.left_top.x)-p.x)<=224&&
               motion::wrap(int(p.y)-box.right_bottom.y)<=512&&motion::wrap(int(box.left_top.y)-p.y)<=-256) {
                round.charge_circle(box);++hits;
            }
        }
        return {hits,false};
    }
    case 8: {
        auto& shot=yumemi[pid];if(!shot.state)return {};
        if(shot.state==1) {
            if(motion::wrap(int(shot.center.x)-128)<=box.right_bottom.x&&motion::wrap(int(shot.center.x)+128)>=box.left_top.x&&
               motion::wrap(int(shot.center.y)-128)<=box.right_bottom.y&&motion::wrap(int(shot.center.y)+128)>=box.left_top.y) {
                shot.state=2;shot.frame=0;round.sounds.push_back(7);
            }
            return {};
        }
        if(motion::wrap(int(shot.center.x)-896)<=box.right_bottom.x&&motion::wrap(int(shot.center.x)+896)>=box.left_top.x&&
           motion::wrap(int(shot.center.y)-896)<=box.right_bottom.y&&motion::wrap(int(shot.center.y)+896)>=box.left_top.y) {
            round.charge_circle(box);return {1,false};
        }
        return {};
    }
    default:throw std::runtime_error("invalid charge-shot character");
    }
}
}
