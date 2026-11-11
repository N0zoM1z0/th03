#pragma once
#include "game_types.hpp"
#include <array>

namespace th03 {
struct RandomRing;
struct BackgroundParticle {
    Point center,velocity;
    std::uint8_t speed=0;
    std::uint16_t sprite=0;
    std::int16_t auxiliary=0;
};
class Background {
public:
    std::array<BackgroundParticle,80> particles{};
    std::uint8_t chain=0,angle=64;
    bool periodic=false,draw_periodic=false;
    std::uint16_t phase_frame=0;
    void begin(RandomRing& random,unsigned character);
    void reset_velocity();
    // Original background callbacks update and draw before the render-skip
    // branch. This update belongs to every game tick, unlike Bomb rendering.
    void update(RandomRing& random,std::uint32_t round_frame,std::uint16_t result_frame);
};
}
