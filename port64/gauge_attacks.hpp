#pragma once
#include "game_types.hpp"
#include <array>

namespace th03 {
class Round;
class GaugeAttacks {
public:
    std::array<std::array<std::uint8_t,4>,2> timing{};
    std::array<std::array<std::uint8_t,2>,9> frame{};
    std::array<std::array<Point,2>,9> center{};
    std::array<std::uint8_t,2> mima_angle{},mima_step{};
    void update(Round& round,unsigned pid);
private:
    void pattern(Round& round,unsigned pid,std::uint8_t type);
};
}
