#pragma once
#include "game_types.hpp"
#include <array>
#include <functional>

namespace th03 {
// The DOS EFE pool contains forty enemies followed by twenty-four fireballs.
// Portable owners share these named fields without serializing the DOS ABI.
struct Efe {
    std::uint8_t flag=0,frame=0,size_words=0,hp=0,pid=0,size_pixels=0,chain_slot=0;
    Point center;
};
struct Fireball:Efe {
    Point velocity;
    std::int16_t target_x=0,target_x_origin=0;
    std::uint8_t fall_speed=0,generation=0;
};
struct Chains {
    using Slots=std::array<std::array<std::uint8_t,16>,2>;
    Slots hits{},value{},fireball{},extra{};
    std::array<std::uint8_t,2> cursor{};
    std::uint8_t start(Efe& origin);
};
struct HitCircle {std::uint8_t age=0,pid=0;std::int16_t left=0,top=0;};
struct Combo {
    std::uint8_t time=0,hits=0;
    std::uint16_t bonus=0;
};
enum class Against:std::uint8_t {enemy=0,pellet=1,fireball_blue=2,fireball_red=3};
struct Hitbox {
    Point left_top,right_bottom;
    std::uint8_t pid=0;
};
struct ChargeHit {std::uint8_t damage=0;bool one_hit=false;};
using ChargeQuery=std::function<ChargeHit(const Hitbox&)>;
using ExtraAdd=std::function<void(Point,std::uint8_t)>;
}
