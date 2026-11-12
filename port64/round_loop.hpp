#pragma once
#include "battle_graphics.hpp"
#include "collision.hpp"
#include "selection.hpp"

namespace th03 {
enum class RoundExit {running,return_to_op,next_round,end_match};
class RoundLoop {
public:
    void begin(Round& round,const BattleGraphics& graphics);
    void restart(Round& round,const Resident& resident);
    void tick(Round& round,Resident& resident,const BattleGraphics& graphics,const InputFrame& input);
    Frame render(const Round& round,const Resident& resident,const BattleGraphics& graphics) const;
    CollisionMap collision;
    PlayfieldTransition transition;
    std::uint16_t demo_frame=0;
    RoundExit outcome=RoundExit::running;
    bool render_timing=false;
    std::optional<std::uint8_t> kotohime_stack_color;
    unsigned draws=0,refresh_wait=0;
private:
    enum class Step {update,after_pause,flash,present};
    Step step_=Step::update;
    std::array<Canvas,2> pages_;
    unsigned front_=1,back_=0;
    std::uint16_t vsync_count_=0;
    Palette shown_palette_{};
    std::array<std::uint8_t,3> hud_levels_{};
    int shown_tone_=100;
    void present(Round& round,const BattleGraphics& graphics);
    void advance(Round& round);
    bool result_step(Round& round,Resident& resident,const BattleGraphics& graphics);
};
}
