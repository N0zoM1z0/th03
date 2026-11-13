// Adapted from TH04 port/modern-64 1ba7107 (MIT); checked with TH03 resources.
#pragma once
#include "pmd_sequence.hpp"
#include "pmd_fm_effects.hpp"

namespace th03::pmd {
struct RhythmState {
    std::uint8_t attenuation=0,initial_attenuation=0,mask=255;
    bool enabled=false;
    std::uint8_t active=0,total=60;
    std::uint16_t request=0;
    std::array<std::uint8_t,6> levels{},starts{},stops{};
};
// Hardware rhythm requests share the musical timeline. This owner emits chip
// writes and state only; samples, wall clocks and audio devices are separate.
class Rhythm {
public:
    explicit Rhythm(Board board,FmSink sink={}):board_(board),sink_(std::move(sink)) {state_.enabled=board!=Board::fm26;if(state_.enabled){state_.levels.fill(207);state_.total=48;}}
    void start();
    void restore_total() {if(state_.enabled)total(0);}
    void event(const Event&,const State&);
    const RhythmState& state() const {return state_;}
private:
    Board board_;FmSink sink_;RhythmState state_{};
    void write(unsigned,unsigned);
    void total(std::uint8_t fade);
    std::uint8_t& indexed(unsigned);
};
}
