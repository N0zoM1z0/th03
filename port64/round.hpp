#pragma once
#include "resident.hpp"
#include "game_types.hpp"
#include "bullet.hpp"
#include "combat.hpp"
#include "player.hpp"
#include "charge.hpp"
#include "bomb.hpp"
#include "graphics.hpp"
#include "background.hpp"
#include "extra.hpp"
#include "gauge_attacks.hpp"
#include "boss.hpp"
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
    bool cpu=false,is_hit=false,knockback_active=false,hyper_handler=false;
    std::uint8_t invincibility=0,knockback_time=0,move_lock=0,shot_mode=1,shot_active=1;
    std::uint8_t knockback_angle=0,knockback_length=0,spell_ready_frames=0,cpu_dodge_strategy=0;
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
struct Enemy:Efe {
    Point velocity;
    std::uint16_t ip=0,op_frame=0,angle=0;
    std::int8_t angle_speed=0;
    std::uint8_t formation=0,formation_i=0,speed=0,loop_i=0,pos_type=0;
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
struct WarningText {
    std::uint16_t attribute=0;
    std::uint8_t level=0;
    bool boss=false,visible=false;
};
enum class Pause {none,release,command,resume_release,resume_finish,fade};
class Round {
public:
    void begin(const Resident& resident,const Bytes& enedat);
    // The original first call inherits InitStart's low byte on the stack.
    // A later-round caller must supply its recovered stack context explicitly.
    void prepare(const Resident& resident,std::uint8_t formation_previous);
    void randomize_formations(std::uint8_t previous);
    void add_shots(unsigned pid);
    void update_shots();
    void player_update(unsigned pid,std::uint16_t input,CollisionMap& collision,Resident& resident,const PlayerServices& services);
    MoveResult move_player(unsigned pid,std::uint16_t input);
    void knockback_update(unsigned pid);
    void player_hit(unsigned pid,int tiles,const CollisionMap& collision);
    std::int8_t hit_damage(unsigned pid,Resident& resident);
    Point player_velocity;
    std::array<std::uint8_t,4> movement_speed{};
    std::array<std::uint8_t,2> shot_release{};
    std::uint8_t target_formation_marker=0,defeated_player=255;
    Point target,boss_target;
    std::array<std::uint16_t,2> boss_active{};
    void find_target(unsigned pid);
    void hyper_update(unsigned pid);
    void cpu_update(unsigned pid,CollisionMap& collision,Resident& resident);
    Point collision_top;
    std::uint8_t cpu_pattern=0;
    void player_lose_update(unsigned pid,Resident& resident);
    std::int16_t lose_left=0,lose_top=0,lose_radius=0,palette_tone=100;
    std::uint8_t reset_frames=1;
    bool page_back=false;
    // Ordered SE plays; 0xff is the original snd_se_reset service event.
    std::vector<std::uint8_t> sounds;
    RandomRing random;
    Background background;
    HudIntro intro;
    Bullets bullets;
    ChargeShots charge_shots;
    Bombs bombs;
    ExtraAttacks extra_attacks;
    GaugeAttacks gauges;
    Bosses bosses;
    Palette palette{},palette_backup{};
    bool palette_initialized=false;
    void set_palette(const Palette& colors);
    void player_bomb(unsigned pid,Resident& resident);
    std::array<PlayerEffect,12> effects{};
    std::uint8_t effect_cursor=0;
    void effect_add(Point center,unsigned pid,Effect type);
    void update_effects();
    void prepare_effects_render();
    std::array<std::int16_t,2> fg_shift{};
    std::array<std::uint8_t,2> bomb_flags{},damage_all{},gauge_flags{};
    std::array<Player,2> players{};
    std::array<ShotPair,32> shots{};
    std::array<Enemy,40> enemies{};
    std::array<Fireball,24> fireballs{};
    Chains chains;
    std::array<HitCircle,13> circles{};
    std::uint8_t circle_cursor=0;
    void enemy_circle(Point center,std::uint8_t pid);
    void charge_circle(const Hitbox& box);
    void player_circle(Point center,std::uint8_t pid);
    void update_circles();
    std::array<Combo,2> combos{};
    std::array<std::uint8_t,2> gauge_next{},warning{};
    std::array<std::uint8_t,2> warning_brightness{},warning_fading_out{};
    std::array<WarningText,2> warning_text{};
    std::array<bool,2> warning_portrait{};
    std::uint8_t warning_flash_frame=27;
    // Called once per actual draw, after the score and before page flipping.
    void prepare_warning_portraits();
    bool begin_warning_flash();
    // One physical refresh, with simulation/counters frozen. Pause handling
    // belongs to the caller before this refresh, as in round_CA3C.
    bool warning_flash_tick();
    void warning_update(unsigned pid);
    void warning_text_put(unsigned pid,std::uint16_t attribute);
    Pause pause=Pause::none;
    std::uint8_t pause_fade_frame=0;
    bool quit_requested=false;
    void begin_pause(const Resident& resident);
    // A physical refresh of the blocking pause owner. No game clocks move.
    bool pause_tick(std::uint16_t input);
    std::array<bool,2> boss_panic{};
    std::uint8_t boss_launched_by=255,defeat=0,fireball_variant=0,generation_previous=0,last_chain_slot=0;
    bool last_explosion_hit=false,one_hit=false,enemy_killed=false,fireball_hit=false;
    void score_add(unsigned pid,std::uint16_t value);
    void gauge_add(unsigned pid,std::uint8_t value);
    std::uint16_t combo_add(unsigned pid,unsigned slot,std::uint16_t value);
    void point_attack(unsigned pid,std::uint16_t points);
    void fireball_add(const Efe& origin);
    void update_fireballs(CollisionMap& collision);
    std::uint8_t explosion_hit(const Hitbox& hitbox,Against against);
    void charged_fireball(unsigned pid,const Efe& origin);
    void charged_extra(unsigned pid,unsigned slot,const Efe& origin,const ExtraAdd& add);
    std::uint8_t hitbox_hits(Hitbox box,std::int16_t center_y,const ChargeQuery& charge,Against against,bool skip_explosions=false);
    void hit_enemies(const ChargeQuery& charge,const ExtraAdd& extra);
    void hit_fireballs(const ChargeQuery& charge,const ExtraAdd& extra,std::uint8_t stack_chain_slot);
    std::array<std::uint8_t,2> enemies_alive{};
    void update_formations();
    void update_enemy_scripts();
    void update_enemies(CollisionMap& collision,const ChargeQuery& charge,const ExtraAdd& extra);
    void update_bullets(CollisionMap& collision);
    std::vector<Formation> formations;
    std::array<std::uint8_t,256> formation_types{},formation_positions{};
    std::array<std::uint8_t,2> formation_cursors{},gauge_levels{};
    std::array<std::array<std::uint8_t,8>,2> scores{};
    std::uint8_t id=0,speed=0,enemy_speed=0,bullet_base_speed=0,boss_level=0,cpu_damage_additional=0,extends_gained=0;
    std::uint16_t result_wait=0,combo_points_for_boss_attack=5120;
    std::uint32_t frame=0;
    std::uint16_t result_frame=0;
};
}
