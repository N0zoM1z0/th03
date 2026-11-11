#pragma once
#include "assets.hpp"
#include "font.hpp"
#include "resident.hpp"

namespace th03 {
class StageIntro {
public:
    StageIntro(const PfArchive& assets,const Font& font,Resident& resident);
    void tick(std::uint16_t input);
    Frame render() const {return canvas_.frame(palette_,tone_);}
    bool done() const {return done_;}
    unsigned age() const {return age_;}
    const std::string& music() const {return music_;}
private:
    Canvas canvas_;
    Palette palette_{};
    std::string music_;
    unsigned age_=0,wait_=0;
    int tone_=0;
    enum class State {black_in,wait,white_out,white_in} state_=State::black_in;
    bool done_=false;
};
}
