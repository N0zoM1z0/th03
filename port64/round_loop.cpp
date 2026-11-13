#include "round_loop.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
void Round::prepare_combos_render() {
    for(unsigned pid=0;pid<2;++pid) {
        auto& combo=combos[pid];combo.points_visible=false;
        if(!combo.time)continue;
        if(combo.time==80) {combo.display_hits=combo.hits;combo.text_visible=true;}
        --combo.time;combo.points_visible=true;combo.display_bonus=combo.bonus;
        combo.display_color=combo.time<32&&result_frame%4<2 ? 8 : 12;
        if(!combo.time) {combo.text_visible=false;combo.hits=0;score_add(pid,combo.bonus);combo.bonus=0;}
    }
}
std::uint8_t Round::collision_adjacent_read(std::uint16_t address) const {
    // A negative first column wraps the original unsigned MUL into
    // earlier DGROUP owners. Preserve the read rather than clipping it.
    if(address>=0x2cc&&address<0x2d4)return 0; // No SAJ joystick is attached.
    if(address>=0x2d4&&address<0x2d6)return std::uint8_t(std::uint16_t(palette_tone)>>((address-0x2d4)*8));
    if(address>=0x2d6&&address<0x306) {
        const unsigned at=address-0x2d6,color=at/3,channel=at%3;
        if(color==8)return 0x77;
        const unsigned bit=channel==0 ? 2 : channel==1 ? 4 : 1;
        return color&bit ? (color<8 ? 0xff : 0xaa) : 0;
    }
    if(address>=0x316&&address<0x596) {
        const auto at=address-0x316;
        return std::uint8_t(std::uint16_t(motion::sine(std::uint8_t(at/2)))>>((at&1)*8));
    }
    // The two 128-byte CRT exception name/static workspaces stay empty
    // on the game's ordinary non-throwing DOS path.
    if(address>=0xf76&&address<0x1076)return 0;
    // The original runtime baseline uses a 486-class guest CPU. Its
    // exception/signal handlers have not been installed by ordinary play.
    if(address>=0x1076&&address<0x1078)return address==0x1076 ? 4 : 0;
    if(address>=0x1078&&address<0x1092)return 0;
    if(address>=0x1092&&address<0x109a) {
        constexpr std::uint8_t interrupts[]={2,4,8,11,15,22,0,21};
        return interrupts[address-0x1092];
    }
    if(address>=0x109a&&address<0x109e)return std::uint8_t(0xb8cu>>((address-0x109a)*8));
    if(address>=0x10d0&&address<0x10dc) {
        constexpr std::uint16_t string_options[]={1,0,1,63,64,63};
        const auto at=address-0x10d0;
        return std::uint8_t(string_options[at/2]>>((at&1)*8));
    }
    if(address>=0x10dc&&address<0x1133) {
        constexpr char message[]="String reference out of range";
        return std::uint8_t(message[(address-0x10dc)%sizeof(message)]);
    }
    throw std::runtime_error("unowned collision DGROUP read "+std::to_string(address)+" at round frame "+std::to_string(frame));
}

void RoundLoop::begin(Round& r,const BattleGraphics& graphics) {
    *this=RoundLoop{};
    shown_palette_=r.palette;shown_tone_=r.palette_tone;
    hud_levels_={{r.gauge_levels[0],r.gauge_levels[1],r.boss_level}};
    for(auto& page:pages_)graphics.clear_playfields(page);
    for(unsigned pid=0;pid<2;++pid)r.bosses.init_template(pid,character_id(r.players[pid].paletted));
    // Both callback binders assign this global hook; the second player wins.
    r.background.begin(r.random,character_id(r.players[1].paletted));
    collision.adjacent_read=[&r](std::uint16_t address){return r.collision_adjacent_read(address);};
}
void RoundLoop::restart(Round& r,const Resident& resident) {
    // MAIN keeps round_loop's PLAY_NEXT result in SI. The real resetters
    // save that SI into the randomizer's otherwise uninitialized first byte.
    ++r.id;r.prepare(resident,1);r.background.reset_velocity();
    for(auto& p:r.players)p.hyper_handler=false;
    r.sounds.push_back(255);r.palette=r.palette_backup;r.palette_tone=100;
    r.text_cells={};r.warning_text={};r.warning_portrait={};r.warning_flash_frame=27;
    for(auto& c:r.combos) {c.text_visible=false;c.points_visible=false;}
    for(auto& page:pages_)std::fill(page.pixels.begin(),page.pixels.end(),2);
    // The hardware access/display pages are explicitly set to0/1, while
    // the original page_back bookkeeping byte keeps its existing parity.
    front_=1;back_=0;step_=Step::update;outcome=RoundExit::running;refresh_wait=0;
    transition.frame=0;transition.midpoint=false;
    shown_palette_=r.palette;shown_tone_=100;hud_levels_={{r.gauge_levels[0],r.gauge_levels[1],r.boss_level}};
}
bool RoundLoop::result_step(Round& r,Resident& resident,const BattleGraphics& graphics) {
    if(r.defeat!=2)return true;
    const bool story=resident.mode==Mode::story;
    const bool match=story ? resident.winner==0 : r.players[0].rounds_won>=2||r.players[1].rounds_won>=2;
    const auto commit=[&](unsigned pid) {resident.scores[pid]=r.scores[pid];resident.scores[pid^1]={};};
    if(match) {
        r.result.update(r,resident);graphics.draw_result(pages_[back_],r,resident);
        if(r.result_frame==r.result_wait)transition.phase=PlayfieldTransition::Phase::cover;
        else if(transition.midpoint) {commit(resident.winner);outcome=RoundExit::end_match;return false;}
    } else if(r.result_frame==160)transition.phase=PlayfieldTransition::Phase::cover;
    else if(transition.midpoint) {
        if(story) {
            if(!resident.lives) {commit(0);outcome=RoundExit::end_match;return false;}
            --resident.lives;
        }
        outcome=RoundExit::next_round;return false;
    }
    return true;
}
Frame RoundLoop::render(const Round& r,const Resident& resident,const BattleGraphics& graphics) const {
    return graphics.compose(pages_[front_],r,resident,&shown_palette_,shown_tone_,&hud_levels_);
}
void RoundLoop::present(Round& r,const BattleGraphics& graphics) {
    const auto needed=render_timing ? 0u : unsigned(r.reset_frames);
    refresh_wait=vsync_count_<needed ? needed-vsync_count_ : 0;
    if(refresh_wait) {step_=Step::present;return;}
    if(!render_timing) {vsync_count_=0;r.reset_frames=1;}
    shown_palette_=r.palette;shown_tone_=r.palette_tone;
    front_=unsigned(r.page_back);back_=1-unsigned(r.page_back);r.page_back=!r.page_back;++draws;
    graphics.clear_playfields(pages_[back_]);advance(r);step_=Step::update;
}
void RoundLoop::advance(Round& r) {
    ++r.frame;++r.result_frame;
    if(!(r.result_frame%64)) {
        if(r.speed<127)++r.speed;
        if(!(r.result_frame%1024)) {
            r.random.fill();for(auto& p:r.players)if(p.hit_damage_next<6)++p.hit_damage_next;
        }
        if(r.result_frame<2000)for(auto& p:r.players)p.cpu_frame=0;
    }
}
void RoundLoop::tick(Round& r,Resident& resident,const BattleGraphics& graphics,const InputFrame& input) {
    if(outcome!=RoundExit::running)return;
    ++vsync_count_;
    if(step_==Step::present) {present(r,graphics);return;}
    if(r.pause!=Pause::none) {
        const bool fading=r.pause==Pause::fade,active=r.pause_tick(input.single);
        if(fading) {shown_palette_=r.palette;shown_tone_=r.palette_tone;}
        if(active)return;
    }
    const ChargeQuery charge=[&](const Hitbox& box){return r.charge_shots.hit(r,box);};
    const ExtraAdd extra=[&](Point center,std::uint8_t pid){r.extra_attacks.add(r,center,pid);};
    if(step_==Step::update) {
        if(r.quit_requested) {outcome=RoundExit::return_to_op;return;}
        collision.clear();r.bullets.model.reset();
        for(unsigned pid=0;pid<2;++pid) {
            r.extra_attacks.update(r,pid,collision,charge);
            r.bosses.update(r,pid,collision,charge);r.bombs.update(r,pid);
        }
        r.update_circles();r.update_shots();
        for(unsigned pid=0;pid<2;++pid)r.charge_shots.update(r,pid);
        r.intro.update(r.random,resident.mode);r.update_formations();
        r.update_bullets(collision);r.update_enemies(collision,charge,extra);r.update_fireballs(collision);
        for(unsigned pid=0;pid<2;++pid)r.gauges.update(r,pid);
        r.update_effects();
        const PlayerServices services{
            [](Round& state,unsigned pid){state.hyper_update(pid);},
            [&](Round& state,unsigned pid){state.cpu_update(pid,collision,resident);},
            [&](Round& state,unsigned pid){state.player_bomb(pid,resident);},
            [&](Round& state,unsigned pid){state.player_lose_update(pid,resident);},
            [](Round& state,Point center,unsigned pid){state.charge_shots.add(state,center,pid);}
        };
        auto keys=input.players;
        if(r.players[1].cpu&&!r.players[0].cpu) {keys[0]|=input.single;keys[1]=0;}
        else if(r.players[0].cpu&&!r.players[1].cpu) {keys[1]=input.single|input.players[0];keys[0]=0;}
        r.player_update(0,keys[0],collision,resident,services);r.player_update(1,keys[1],collision,resident,services);
        if(r.sound_update)r.sound_update();
        step_=Step::after_pause;
        if(input.single&cancel) {r.begin_pause(resident);return;}
    }
    if(step_==Step::after_pause) {
        if(r.begin_warning_flash()) {hud_levels_={{r.gauge_levels[0],r.gauge_levels[1],r.boss_level}};step_=Step::flash;return;}
    } else if(step_==Step::flash) {
        if(input.single&cancel) {r.begin_pause(resident);return;}
        const bool flashing=r.warning_flash_tick();shown_palette_=r.palette;shown_tone_=r.palette_tone;
        if(flashing)return;
    }
    r.warning_update(0);r.warning_update(1);
    r.background.update(r.random,r.frame,r.result_frame);graphics.background(pages_[back_],r);
    if(!render_timing||(r.result_frame&1)) {
        graphics.draw_battle(pages_[back_],r,&r,kotohime_stack_color);
        if(!result_step(r,resident,graphics))return;
        graphics.draw_hud(pages_[back_],r,resident,&r,&resident);
        transition.update(pages_[back_]);
        if(resident.demo) {
            if(demo_frame<7000)++demo_frame;
            else if(demo_frame==7000)transition.phase=PlayfieldTransition::Phase::cover;
            if(transition.midpoint||input.single)r.quit_requested=true;
        }
        present(r,graphics);return;
    }
    advance(r);step_=Step::update;
}
}
