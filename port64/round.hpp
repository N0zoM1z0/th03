#pragma once
#include "resident.hpp"
#include "game_types.hpp"
#include "bullet.hpp"
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
class Round;
struct Enemy {
    std::uint8_t flag=0,frame=0,size_words=0,hp=0,pid=0,size_pixels=0;
    Point center,velocity;
    std::uint16_t ip=0,op_frame=0,angle=0;
    std::int8_t angle_speed=0;
    std::uint8_t chain_slot=0,formation=0,formation_i=0,speed=0,loop_i=0,pos_type=0;
    const Bytes* script=nullptr;
    bool run(const Round& round,std::uint8_t enemy_speed);
};
struct HudParticle {
    Point center;
    std::int16_t velocity=0;
    std::uint8_t angle=0,active=0,turn_early=0,turn_late=0;
};
struct HudIntro {
    std::array<HudParticle,128> particles{};
    std::uint8_t flag=1,phase=0;
    std::int16_t frame=0,sprite=0,x=0;
    void update(RandomRing& random,Mode mode);
    // Original renderer mutates banner state after updating the particles.
    void prepare_render(Mode mode);
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
    HudIntro intro;
    Bullets bullets;
    std::array<std::int16_t,2> fg_shift{};
    std::array<std::uint8_t,2> bomb_flags{},damage_all{},gauge_flags{};
    std::array<Player,2> players{};
    std::array<ShotPair,32> shots{};
    std::array<Enemy,40> enemies{};
    std::array<std::uint8_t,2> enemies_alive{};
    void update_formations();
    void update_enemy_scripts();
    std::vector<Formation> formations;
    std::array<std::uint8_t,256> formation_types{},formation_positions{};
    std::array<std::uint8_t,2> formation_cursors{},gauge_levels{};
    std::array<std::array<std::uint8_t,8>,2> scores{};
    std::uint8_t id=0,speed=0,bullet_base_speed=0,boss_level=0,cpu_damage_additional=0,extends_gained=0;
    std::uint16_t result_wait=0,combo_points_for_boss_attack=5120;
    std::uint32_t frame=0;
    std::uint16_t result_frame=0;
};
}
