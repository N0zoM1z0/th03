#include "win.hpp"
#include <algorithm>
#include <cstdio>
#include <stdexcept>

namespace th03 {
StoryRoute story_dispatch(Resident& resident) {
    if(resident.mode!=Mode::story||resident.winner!=0)return StoryRoute::other;
    // Original MAINL reads the opponent before testing stage9. That byte is
    // resident_t::unused_2, immediately after the nine-element array.
    resident.paletted[1]=resident.stage==9 ? resident.opponent_tail : resident.opponents.at(resident.stage);
    if(resident.stage==7)return StoryRoute::dialogue;
    if(resident.stage==8)return StoryRoute::final_dialogue;
    if(resident.stage==9)return StoryRoute::ending;
    if(character_id(resident.paletted[1])>=7)resident.paletted[1]=1;
    return StoryRoute::stage;
}
WinMessage::WinMessage(const PfArchive& assets,const Resident& resident,std::array<std::uint8_t,2> played) {
    const auto winner=resident.winner;
    character=character_id(played.at(winner));palette=(played[winner]-1)&1;
    message=winner==0&&resident.stage==6 ? 9 : winner==0&&resident.stage==7 ? 10 : character_id(played[winner^1]);
    char filename[16];std::snprintf(filename,sizeof(filename),"@%02uTX.TXT",character);
    const auto text=assets.read(filename);
    for(unsigned row=0;row<3;++row) {
        const auto at=message*180+row*60;
        if(at+60>text.size())throw std::runtime_error("winner message block is truncated");
        lines[row]=std::string(text.begin()+at,text.begin()+at+60);
    }
}
WinScreen::WinScreen(const PfArchive& assets,const Font& font,const Resident& resident,std::array<std::uint8_t,2> played):
    message(assets,resident,played),font_(font),logo_(assets.read("LOGO.CD2")),final_logo_(assets.read("LOGO5.CDG")),
    portrait_([&] {char file[16];std::snprintf(file,sizeof(file),"%02uSL.CD2",message.character*2);return assets.read(file);}()),
    palette_(read_palette(assets.read("LOGO0.RGB"))),final_palette_(read_palette(assets.read("LOGO1.RGB"))) {
    logo_.put(canvas_,0,352,300,false);
}
void WinScreen::tick(std::uint16_t input,std::optional<unsigned> measure) {
    if(done())return;
    ++age_;
    if(state_==State::input) {
        if(input) {state_=State::black_out;wait_=2;}
        return;
    }
    if((state_==State::first_measure||state_==State::second_measure||state_==State::flash)&&measure) {
        const unsigned target=state_==State::first_measure ? 6 : state_==State::second_measure ? 10 : 11;
        if(*measure<target)return;
    } else if(--wait_)return;
    switch(state_) {
    case State::black_in:
        tone_=std::min(tone_+6,100);wait_=2;
        if(tone_==100) {state_=State::first_measure;wait_=16;}
        break;
    case State::first_measure:
        cel_=1;logo_.put(canvas_,cel_,352,300,false);state_=State::logo;wait_=6;break;
    case State::logo:
        if(cel_<4) {logo_.put(canvas_,++cel_,352,300,false);wait_=6;}
        else {state_=State::second_measure;wait_=64;}
        break;
    case State::second_measure:
        tone_=200;cel_=5;
        portrait_.put(canvas_,message.palette,224,64,false);
        final_logo_.put(canvas_,0,352,300,false);palette_=final_palette_;
        state_=State::flash;wait_=4;break;
    case State::flash:state_=State::white_in;wait_=2;break;
    case State::white_in:
        tone_=std::max(tone_-6,100);wait_=1;
        if(tone_==100) {state_=State::text;wait_=8;}
        break;
    case State::text:
        if(!font_.present())throw std::runtime_error("winner text requires --font-bmp FILE");
        for(unsigned row=0;row<3;++row)font_.text(canvas_,80,272+int(row)*16,message.lines[row],15,2);
        state_=State::input;
        if(input) {state_=State::black_out;wait_=2;}
        break;
    case State::black_out:
        tone_=std::max(tone_-6,0);wait_=1;if(!tone_)state_=State::done;break;
    default:break;
    }
}
}
