#pragma once
#include "graphics.hpp"
#include "game_types.hpp"

namespace th03 {
class Round;
struct Resident;
struct MatchResult {
    std::array<std::uint8_t,5> counts{};
    std::uint8_t lives=0,pid=0;
    std::uint16_t step=0,low=0,high=0;
    std::int32_t remaining=0;
    void update(Round& round,const Resident& resident);
};
struct PlayfieldTransition {
    enum class Phase {none,cover,uncover};
    Phase phase=Phase::none;
    std::array<Point,4> vertices{};
    std::uint8_t frame=0;
    bool midpoint=false;
    void update(Canvas& graphics);
};
}
