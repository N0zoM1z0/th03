#pragma once
#include "assets.hpp"
#include "graphics.hpp"
#include "round.hpp"

namespace th03 {
class BattleGraphics {
public:
    BattleGraphics(const PfArchive& op,const PfArchive& main,const Resident& resident);
    Frame render(const Round& round,const Resident& resident) const;
    void sprite(Canvas& dest,int left,int top,unsigned offset,unsigned width,unsigned height,
                int clip_left=0,int clip_right=639,bool clipped=true,int monochrome=-1,bool overlap_clear=true) const;
    void pattern(Canvas& dest,unsigned index,int left,int top) const;
    const Palette& palette() const {return palette_;}
private:
    void background(Canvas& graphics,const Round& round) const;
    void bombs(Canvas& graphics,const Round& round) const;
    void effects(Canvas& graphics,const Round& round) const;
    void charges(Canvas& graphics,const Round& round) const;
    void bullets(Canvas& graphics,const Round& round) const;
    void intro(Canvas& graphics,const Round& round,const Resident& resident) const;
    std::uint8_t pattern_pixel(unsigned index,unsigned x,unsigned y) const;
    void hud(Canvas& display,const Round& round,const Resident& resident) const;
    Canvas atlas_;
    Palette palette_{};
    std::vector<Bfnt> patterns_;
    std::vector<Mrs> bomb_images_,portraits_;
    Bytes font_;
};
}
