#pragma once
#include "combat.hpp"
#include <array>

namespace th03 {
class Round;
struct ReimuCharge {
    std::uint8_t state=0,frame=0,angle=0,speed=0;
    std::array<Point,7> history{};
};
struct MimaCharge {
    std::uint8_t active=0,unused=0;
    Point center,velocity;
};
struct MarisaCharge {
    std::uint8_t active=0,frame=0;
    std::array<Point,12> history{};
};
struct EllenCharge {
    std::uint8_t state=0,phase=0,angle=0,length=0;
    Point center,velocity;
};
struct KotohimeCharge {
    std::uint8_t active=0,animation=0;
    Point center;
    std::int16_t velocity_y=0;
};
struct KanaCharge {
    std::array<Point,13> history{};
    std::uint8_t angle=0,length=0;
};
struct RikakoCharge {Point center;std::uint8_t angle=0,unused=0;};
struct ChiyuriCharge {std::uint8_t age=0,animation=0;Point center;};
struct YumemiCharge {std::uint8_t state=0,frame=0;Point center;};
class ChargeShots {
public:
    std::array<std::array<ReimuCharge,12>,2> reimu{};
    // This flag is shared between the two physical Reimu pools in MAIN.
    std::uint8_t reimu_alternate_hit=0;
    std::array<std::array<MimaCharge,15>,2> mima{};
    std::array<std::uint8_t,2> mima_active{},mima_frame{};
    std::array<MarisaCharge,2> marisa{};
    std::array<std::array<EllenCharge,32>,2> ellen{};
    std::array<KotohimeCharge,2> kotohime{};
    std::array<std::array<KanaCharge,4>,2> kana{};
    std::array<std::uint8_t,2> kana_active{},kana_frame{};
    std::array<std::array<RikakoCharge,4>,2> rikako{};
    std::array<std::uint8_t,2> rikako_active{},rikako_frame{};
    std::array<std::int16_t,2> rikako_radius{};
    std::array<Point,2> rikako_center{};
    std::array<std::array<ChiyuriCharge,8>,2> chiyuri{};
    std::array<YumemiCharge,2> yumemi{};
    void reset();
    void add(Round& round,Point center,unsigned pid);
    void update(Round& round,unsigned pid);
    ChargeHit hit(Round& round,const Hitbox& box);
    void reimu_hyper(Point center,unsigned pid);
    void marisa_hyper(Round& round,unsigned pid);
    void ellen_hyper(Round& round,Point center,unsigned pid);
};
}
