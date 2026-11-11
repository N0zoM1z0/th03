#pragma once
#include "game_types.hpp"
#include <array>
#include <functional>

namespace th03 {
class Round;
// Original movement helper return values, including the distinct idle result.
enum class MoveResult {invalid=0,valid=1,idle=2};
MoveResult movement(std::uint16_t input,const std::array<std::uint8_t,4>& speed,Point& velocity);
void move_position(Point& center,Point velocity);
// The original state machine calls these character/CPU/loss owners. Bindings
// are required; an absent owner must not silently behave as a no-op in a game.
struct PlayerServices {
    using Service=std::function<void(Round&,unsigned)>;
    Service hyper,cpu,bomb,lose;
    std::function<void(Round&,Point,unsigned)> charge;
};
}
