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
                int clip_left=0,int clip_right=639,bool clipped=true,int monochrome=-1) const;
    void pattern(Canvas& dest,unsigned index,int left,int top) const;
    const Palette& palette() const {return palette_;}
private:
    void bullets(Canvas& graphics,const Round& round) const;
    void intro(Canvas& graphics,const Round& round,const Resident& resident) const;
    std::uint8_t pattern_pixel(unsigned index,unsigned x,unsigned y) const;
    void hud(Canvas& display,const Round& round,const Resident& resident) const;
    Canvas atlas_;
    Palette palette_{};
    std::vector<Bfnt> patterns_;
    Bytes font_;
};
}
