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
    std::uint8_t marisa_angle=0;
    std::array<std::uint8_t,2> ellen_angles{},kana_angles{},rikako_angles{},chiyuri_angles{};
    std::array<std::uint8_t,3> yumemi_state{};
    Point yumemi_origin;
    void init_template(unsigned pid,unsigned character);
    void update(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void reimu_template(unsigned pid);
    void mima_template(unsigned pid);
    void marisa_template(unsigned pid);
    void ellen_template(unsigned pid);
    void kotohime_template(unsigned pid);
    void kana_template(unsigned pid);
    void rikako_template(unsigned pid);
    void chiyuri_template(unsigned pid);
    void yumemi_template(unsigned pid);
    bool start(Round& round,unsigned pid);
    void move_sine();
    void fall(Round& round,unsigned pid);
    void next_pattern(Round& round);
    void hit_end(Round& round,unsigned pid);
    // Explosion-ring completion changes score and ownership after drawing.
    void prepare_render(Round& round,unsigned pid);
    void update_reimu(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_mima(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_marisa(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_ellen(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_kotohime(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_kana(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_rikako(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_chiyuri(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
    void update_yumemi(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge);
private:
    void reimu_pattern(Round& round,unsigned pid);
    void mima_pattern(Round& round,unsigned pid);
    void marisa_pattern(Round& round,unsigned pid);
    void ellen_pattern(Round& round,unsigned pid);
    void kotohime_pattern(Round& round,unsigned pid);
    void kana_pattern(Round& round,unsigned pid);
    void rikako_pattern(Round& round,unsigned pid);
    void chiyuri_pattern(Round& round,unsigned pid);
    void yumemi_pattern(Round& round,unsigned pid);
    void hit(Round& round,unsigned pid,CollisionMap& collision,const ChargeQuery& charge,int width=28,int height=28,int radius=512);
};
}
