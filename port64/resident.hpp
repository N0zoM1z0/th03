#pragma once
#include "menu.hpp"
#include <array>

namespace th03 {
enum class Mode:std::uint8_t {none=0,story=1,demo=0x7f,versus_cpu=0x80,two_player=0x81,cpu_cpu=0x82};
struct Resident {
    Options options;
    std::array<std::uint8_t,2> paletted{{1,1}};
    std::array<bool,2> cpu{{false,true}};
    std::array<std::array<std::uint8_t,8>,2> scores{};
    std::uint32_t seed=0;
    Mode mode=Mode::none;
    std::array<std::uint8_t,9> opponents{};
    std::uint8_t winner=0,stage=0,lives=2,credits=3,skill=70,demo=0;
    bool show_scores=false,fast_title=false;
    void begin_story();
    void begin_versus(unsigned choice);
    void choose_story_opponents();
    void begin_demo();
};
unsigned character_id(std::uint8_t paletted);
bool characters_unlocked(const Bytes& nem);
}
