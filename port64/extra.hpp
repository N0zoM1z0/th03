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
    void reset();
    void fly_init(Round& round,Extra& extra,Point from,Point target,unsigned pid,int speed);
    bool fly_update(Extra& extra,unsigned owner);
    void add_kotohime(Round& round,Point center,unsigned pid);
    void kotohime_gauge(Round& round,Point target,unsigned pid);
    void update_kotohime(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
};
}
