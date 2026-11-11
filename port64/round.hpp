#pragma once
#include "resident.hpp"
#include <array>
#include <vector>

namespace th03 {
struct RandomRing {
    std::uint32_t seed=0;
    std::array<std::uint8_t,256> bytes{};
    std::uint8_t cursor=0;
    std::uint16_t next();
    void fill();
    std::uint16_t ring();
};
struct Formation {
    std::vector<Bytes> scripts;
};
std::vector<Formation> read_formations(const Bytes& file);
struct Point {std::int16_t x=0,y=0;}; // Signed Q4 playfield coordinates.
struct Player {
    Point center;
    std::uint8_t paletted=1;
    bool cpu=false,is_hit=false,knockback_active=false;
    std::uint8_t invincibility=0,knockback_time=0,move_lock=0,shot_mode=1,shot_active=1;
    std::int8_t halfhearts=10;
    std::array<std::uint8_t,5> speeds{};
    std::uint16_t gauge_charged=0,gauge_avail=0,cpu_safety=0,cpu_frame=0;
    std::array<std::uint8_t,64> charge_thresholds{};
    std::uint8_t charge_cursor=0,bombs=0,lose_time=0,hyper_active=0,hit_damage_next=1;
    std::uint8_t rounds_won=0,gauge_attacks=0,boss_attacks=0,boss_reversals=0,boss_panics=0;
    std::uint16_t combo_bonus_max=0,human_movement_last=0;
    std::uint8_t combo_hits_max=0,pattern_movement=0,pattern_glow=0;
    bool move(std::uint16_t input);
};
struct ShotPair {
    bool alive=false;
    Point top_left;
    std::int16_t velocity_y=0;
    std::uint8_t pid=0,animation=0;
};
class Round {
public:
    void begin(const Resident& resident,const Bytes& enedat);
    // The original first call inherits InitStart's low byte on the stack.
    // A later-round caller must supply its recovered stack context explicitly.
    void prepare(const Resident& resident,std::uint8_t formation_previous);
    void randomize_formations(std::uint8_t previous);
    void add_shots(unsigned pid);
    void update_shots();
    RandomRing random;
    std::array<Player,2> players{};
    std::array<ShotPair,32> shots{};
    std::vector<Formation> formations;
    std::array<std::uint8_t,256> formation_types{},formation_positions{};
    std::array<std::uint8_t,2> formation_cursors{},gauge_levels{};
    std::array<std::array<std::uint8_t,8>,2> scores{};
    std::uint8_t id=0,speed=0,bullet_base_speed=0,boss_level=0,cpu_damage_additional=0,extends_gained=0;
    std::uint16_t result_wait=0,combo_points_for_boss_attack=5120;
    std::uint16_t frame=0,result_frame=0;
};
}
