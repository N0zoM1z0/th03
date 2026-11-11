#pragma once
#include "game_types.hpp"
#include <array>
#include <optional>

namespace th03 {
class Round;
enum class Effect {explosion,center,axis};
struct PlayerEffect {
    std::uint8_t kind=0,age=0,radius=0,angle=0;
    std::int8_t radius_delta=0;
    Point center;
};
struct ReimuBombParticle {std::uint8_t active=0;Point center;std::int16_t velocity_y=0;};
struct MimaBombColumn {std::int16_t x=0;std::uint16_t sprite=0;};
struct EllenBombParticle {Point center,velocity;};
class Bombs {
public:
    std::array<std::uint8_t,2> frame{};
    std::array<std::array<ReimuBombParticle,32>,2> reimu{};
    std::array<std::array<MimaBombColumn,8>,2> mima{};
    std::array<std::array<EllenBombParticle,8>,2> ellen{};
    std::int16_t ellen_spawn_count=0,kotohime_y=0,rikako_line_offset=0;
    std::uint8_t kana_angle=0;
    Point marisa_point;
    std::array<Point,2> marisa_draw_point{};
    std::array<std::int16_t,2> rikako_draw_offset{};
    void update(Round& round,unsigned pid);
    // Original Bomb render calls mutate palette/RNG/effects. Run this once
    // per scheduled game render, before reading the resulting drawing state.
    // Kotohime's fade reads an uninitialized stack byte; the caller must
    // supply that context rather than silently filling it with zero.
    void prepare_render(Round& round,unsigned pid,std::optional<std::uint8_t> kotohime_stack_color={});
};
}
