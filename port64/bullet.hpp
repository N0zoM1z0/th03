#pragma once
#include "game_types.hpp"
#include <array>
#include <functional>

namespace th03 {
class Round;
class CollisionMap;
struct BulletTemplate {
    Point center,velocity;
    std::uint8_t speed=0,angle=0,pid=0,group=0,acceleration=0,count=0,type=0;
    std::uint16_t sprite=0;
    bool collidable=false,animated=false,has_trail=false;
    void reset();
};
struct Bullet {
    std::uint8_t flag=0,age=0;
    Point center,velocity;
    std::int16_t target_x=0,target_x_origin=0;
    std::uint8_t speed_next=0,angle_next=0,pid=0,group_next=0,acceleration=0,trail=0;
    std::uint16_t sprite=0;
    bool collidable=false,animated=false,has_trail=false;
};
struct BulletTrail {std::array<std::int16_t,6> x{},y{};};
class Bullets {
public:
    BulletTemplate model;
    std::array<Bullet,320> items{};
    std::array<BulletTrail,48> trails{};
    std::uint8_t trail_cursor=0,group_angle=0;
    void reset();
    bool group_velocity(Round& round,int index);
    void add(Round& round,unsigned sprite_base);
    // The pellet query performs the original explosion/chain side effects.
    using PelletHit=std::function<bool(Point,std::uint8_t)>;
    void update(Round& round,CollisionMap& collision,const PelletHit& explosion_hit);
private:
    void add_next(Round& round,const Bullet& bullet);
};
}
