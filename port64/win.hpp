#pragma once
#include "stage_intro.hpp"
#include <optional>

namespace th03 {
enum class StoryRoute {stage=0,other=1,dialogue=3,final_dialogue=4,ending=5};
StoryRoute story_dispatch(Resident& resident);
struct WinMessage {
    WinMessage(const PfArchive& assets,const Resident& resident,std::array<std::uint8_t,2> played);
    unsigned character=0,palette=0,message=0;
    std::array<std::string,3> lines;
};
class WinScreen {
public:
    WinScreen(const PfArchive& assets,const Font& font,const Resident& resident,std::array<std::uint8_t,2> played);
    // No measure means the original no-BGM frame delays. An audio service can
    // supply the current WIN.M measure without changing the animation owner.
    void tick(std::uint16_t input,std::optional<unsigned> measure={});
    Frame render() const {return canvas_.frame(palette_,tone_);}
    bool done() const {return state_==State::done;}
    bool waiting() const {return state_==State::input;}
    unsigned age() const {return age_;}
    int tone() const {return tone_;}
    unsigned cel() const {return cel_;}
    const WinMessage message;
private:
    const Font& font_;
    Cdg logo_,final_logo_,portrait_;
    Palette palette_,final_palette_;
    Canvas canvas_;
    enum class State {black_in,first_measure,logo,second_measure,flash,white_in,text,input,black_out,done};
    State state_=State::black_in;
    unsigned age_=0,wait_=3,cel_=0;
    int tone_=0;
};
}
