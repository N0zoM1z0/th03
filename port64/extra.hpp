#pragma once
#include "combat.hpp"
#include <array>

namespace th03 {
class Round;
class CollisionMap;
struct Extra {
    std::uint8_t state=0,frame=0,pid=0,mode=0,angle=0,speed=0;
    Point center,velocity;
    std::int16_t target_x=0,boundary_x=0,duration=0,radius=0;
    bool homing_disabled=false;
};
class ExtraAttacks {
public:
    std::array<std::array<Extra,16>,2> items{};
    std::array<std::array<std::array<Point,7>,12>,2> ellen_history{};
    void reset();
    void add(Round& round,Point center,unsigned pid);
    void special(Round& round,Point center,unsigned owner,std::uint8_t angle=64,std::uint8_t mode=1);
    void update(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    // Reimu alone advances its animation during the original render call.
    void prepare_render(const Round& round,unsigned pid);
    void fly_init(Round& round,Extra& extra,Point from,Point target,unsigned pid,int speed);
    bool fly_update(Extra& extra,unsigned owner);
    void add_kotohime(Round& round,Point center,unsigned pid);
    void kotohime_gauge(Round& round,Point target,unsigned pid);
    void update_kotohime(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
};
}
