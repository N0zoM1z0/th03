#pragma once
#include "assets.hpp"
#include "graphics.hpp"
#include "round.hpp"

namespace th03 {
class BattleGraphics {
public:
    BattleGraphics(const PfArchive& op,const PfArchive& main,const Resident& resident);
    Frame render(const Round& round,const Resident& resident) const;
    void clear_playfields(Canvas& graphics) const;
    void background(Canvas& graphics,const Round& round) const;
    // Live rendering executes the original draw-owned state changes once.
    void draw(Canvas& graphics,const Round& round,const Resident& resident,Round* live=nullptr,Resident* live_resident=nullptr,
              std::optional<std::uint8_t> kotohime_stack_color={}) const;
    Frame compose(const Canvas& graphics,const Round& round,const Resident& resident,const Palette* shown_palette=nullptr,std::optional<int> shown_tone={},const std::array<std::uint8_t,3>* hud_levels=nullptr) const;
    void sprite(Canvas& dest,int left,int top,unsigned offset,unsigned width,unsigned height,
                int clip_left=0,int clip_right=639,bool clipped=true,int monochrome=-1,bool overlap_clear=true,std::uint16_t mask=0xffff) const;
    void pattern(Canvas& dest,unsigned index,int left,int top) const;
    const Palette& palette() const {return palette_;}
private:
    void bombs(Canvas& graphics,const Round& round,unsigned pid) const;
    void effects(Canvas& graphics,const Round& round) const;
    void charges(Canvas& graphics,const Round& round,unsigned pid) const;
    void extras(Canvas& graphics,const Round& round,unsigned pid) const;
    void boss(Canvas& graphics,const Round& round,unsigned pid) const;
    void bullets(Canvas& graphics,const Round& round) const;
    void intro(Canvas& graphics,const Round& round,const Resident& resident) const;
    std::uint8_t pattern_pixel(unsigned index,unsigned x,unsigned y) const;
    void hud(Canvas& display,const Round& round,const Resident& resident,const std::array<std::uint8_t,3>* levels=nullptr) const;
    Canvas atlas_;
    Palette palette_{};
    std::vector<Bfnt> patterns_;
    std::vector<Mrs> bomb_images_,portraits_;
    Bytes font_;
};
}
