#pragma once
#include "font.hpp"
#include "assets.hpp"
#include "score.hpp"
#include "resident.hpp"

namespace th03 {
class ScoreMenu {
public:
    ScoreMenu(const PfArchive& assets,const Font& font,ScoreFile& file,const Resident& resident);
    void tick(std::uint16_t input);
    Frame render() const {return canvas_.frame(palette_,tone_);}
    bool done() const {return state_==State::done;}
    bool editing() const {return state_==State::name;}
    int tone() const {return tone_;}
    int place=-1;
    ScoreSection section;
    NameEntry name;
private:
    const Font& font_;
    ScoreFile& file_;
    Resident resident_;
    std::uint32_t seed_;
    Bfnt normal_,highlight_;
    Canvas canvas_,background_;
    Palette palette_;
    int tone_=0;
    unsigned wait_=3;
    enum class State {fade_in,name,name_finish,release,press,fade_out,done};
    State state_=State::fade_in;
    void sprite(int x,int y,unsigned code,bool highlight);
    void glyph(int x,int y,unsigned code,bool highlight);
    void alphabet(unsigned code,bool highlight);
    void unput(std::uint8_t cursor);
    void row(unsigned place);
    void rows();
    void edit(std::uint16_t input);
};
class ContinueMenu {
public:
    ContinueMenu(const PfArchive& assets,const Font& font,Resident& resident);
    void tick(std::uint16_t input);
    Frame render() const {return canvas_.frame(palette_,tone_);}
    bool done() const {return state_==State::done;}
    bool selected=true;
    int tone() const {return tone_;}
private:
    const PfArchive& assets_;
    const Font& font_;
    Resident& resident_;
    Cdg choices_;
    Canvas canvas_;
    Palette palette_;
    bool held_=false;
    unsigned wait_=2;
    int tone_=0;
    enum class State {fade_in,input,fade_out,done};
    State state_=State::fade_in;
    void choices();
    void credits();
};
class GameOver {
public:
    explicit GameOver(const PfArchive& assets);
    void tick();
    Frame render() const {return canvas_.frame(palette_,tone_);}
    bool done() const {return state_==State::done;}
private:
    Canvas canvas_;
    Palette palette_;
    unsigned wait_=2;
    int tone_=0;
    enum class State {fade_in,hold,fade_out,done};
    State state_=State::fade_in;
};
}
