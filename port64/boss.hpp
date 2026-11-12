#pragma once
#include "combat.hpp"
#include <array>

namespace th03 {
class Round;
class CollisionMap;
struct BossState {
    Point center,scratch,velocity;
    std::int16_t hp=0;
    std::uint16_t sprite=0,effect_radius=0;
    std::uint8_t hit=0,mode=0,angle=0,pattern=0,count=0,render_mode=0,render_frame=0,move_phase=0;
    std::int8_t spin=0;
    std::array<std::uint8_t,5> tail{};
};
class Bosses {
public:
    BossState state;
    std::array<BossState,2> templates{};
    std::uint16_t frame=0;
    std::uint8_t previous=0;
    // All characters alias the same seven level-derived parameter bytes.
    std::array<std::uint8_t,7> parameters{};
    std::uint8_t reimu_direction=0,reimu_speed=0,reimu_angle=0;
    std::array<Point,6> reimu_orbit{};
    std::array<std::uint8_t,4> mima_angles{};
    void reimu_template(unsigned pid);
    void mima_template(unsigned pid);
    bool start(Round& round,unsigned pid);
    void move_sine();
    void fall(Round& round,unsigned pid);
    void next_pattern(Round& round);
    void hit_end(Round& round,unsigned pid);
    // Explosion-ring completion changes score and ownership after drawing.
    void prepare_render(Round& round,unsigned pid);
    void update_reimu(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_mima(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
private:
    void reimu_pattern(Round& round,unsigned pid);
    void mima_pattern(Round& round,unsigned pid);
    void hit(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
};
}
