#pragma once
#include "pi_image.hpp"
#include <cstdint>
#include <vector>

namespace th03 {
enum Input : std::uint16_t {
    up=1, down=2, left=4, right=8, bomb=0x10, shot=0x20,
    up_left=0x100,down_left=0x200,up_right=0x400,down_right=0x800,
    cancel=0x1000, ok=0x2000, q=0x4000
};
enum class Screen { title, main, options, handoff, quit, versus };
enum class Request { none, story, versus, music, scores, attract };
struct Options { std::uint8_t music=1, keys=0, rank=0; };
struct Menu {
    Screen screen=Screen::title;
    Request request=Request::none;
    Options options;
    std::int8_t selected=0;
    std::uint16_t idle_frames=0;
    std::uint32_t resident_seed=0;
    bool input_allowed=false;
    void tick(std::uint16_t input);
};
// IRAND's unsigned modulo-2^32 recurrence, independent of host long width.
inline std::uint16_t random_next(std::uint32_t& seed) {
    seed = seed * UINT32_C(0x015a4e35) + 1u;
    return std::uint16_t((seed >> 16) & 0x7fffu);
}
using Frame = std::vector<std::uint32_t>;
Frame pi_frame(const PiImage& image);
Frame menu_frame(const PiImage& background, const Bytes& gaiji, const Bytes& window, const Menu& menu);
Bytes ppm(const Frame& frame);
}
