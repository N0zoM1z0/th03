#include "application.hpp"
#include <stdexcept>

namespace th03 {
Application::Application(const PfArchive& assets,Options options,const Bytes& nem,const std::string& picture,Bytes font_bitmap,const PfArchive* main_assets):assets_(assets),main_assets_(main_assets),
    background_(decode_pi(assets.read(picture))),graphic_font_(std::move(font_bitmap)),font_(assets.read("MIKOFT.BFT")),window_(assets.read("OPWIN.BFT")) {
    menu.options=resident.options=options;available_=characters_unlocked(nem) ? 9 : 7;
}
void Application::start_selection(SelectKind kind) {
    if(!selection_assets_)selection_assets_.emplace(assets_);
    selection.begin(resident,kind,available_);phase=Phase::selection;
}
void Application::start_stage_intro() {
    intro_.emplace(assets_,graphic_font_,resident);phase=Phase::stage_intro;
}
void Application::start_main(bool play) {
    if(!main_assets_)throw std::runtime_error("MAIN setup requires the second original PF archive");
    round.emplace();round->begin(resident,main_assets_->read("ENEDAT.DAT"));
    battle_graphics_.emplace(assets_,*main_assets_,resident);round->set_palette(battle_graphics_->palette());phase=Phase::mainl_handoff;
    round_loop.reset();
    if(play) {round_loop.emplace();round_loop->begin(*round,*battle_graphics_);phase=Phase::battle;}
}
void Application::return_to_title() {
    menu=Menu{};menu.options=resident.options;menu.resident_seed=resident.seed;
    menu.selected=return_selection_;phase=Phase::op;
}
void Application::tick(const InputFrame& input) {
    if(finished())return;
    if(phase==Phase::battle) {
        round_loop->tick(*round,resident,*battle_graphics_,input);
        if(round_loop->outcome==RoundExit::return_to_op) {resident.seed=round->frame;return_to_title();}
        return;
    }
    if(phase==Phase::stage_intro) {
        intro_->tick(input.single);
        if(intro_->done()) {
            start_main();
        }
        return;
    }
    if(transition_wait_) {--transition_wait_;return;}
    if(phase==Phase::selection) {
        selection.tick(resident,input);
        if(selection.cancelled) {
            if(std::uint8_t(resident.mode)>=0x80)resident.mode=Mode::none;
            return_to_title();
        } else if(selection.done) {
            if(resident.mode==Mode::story)resident.choose_story_opponents();
            else resident.scores={};
            start_stage_intro();
        }
        return;
    }
    const bool versus=phase==Phase::versus;
    menu.tick(input.single);
    resident.options=menu.options;resident.seed=menu.resident_seed;
    if(menu.screen==Screen::quit) {phase=Phase::quit;return;}
    if(menu.screen!=Screen::handoff)return;
    if(versus) {
        resident.begin_versus(unsigned(menu.selected));
        start_selection(resident.mode==Mode::two_player ? SelectKind::two_player : SelectKind::versus_cpu);
    } else if(menu.request==Request::story) {
        return_selection_=menu.selected;resident.begin_story();start_selection(SelectKind::story);
    } else if(menu.request==Request::versus) {
        return_selection_=menu.selected;resident.paletted={{1,1}};
        menu.screen=Screen::versus;menu.selected=0;menu.input_allowed=true;
        phase=Phase::versus;transition_wait_=13;
    } else if(menu.request==Request::attract) {
        resident.begin_demo();start_stage_intro();
    } else phase=Phase::mainl_handoff;
}
Frame Application::render() const {
    if(phase==Phase::battle)return round_loop->render(*round,resident,*battle_graphics_);
    if(round&&phase==Phase::mainl_handoff)return battle_graphics_->render(*round,resident);
    if(phase==Phase::stage_intro||(phase==Phase::mainl_handoff&&intro_))return intro_->render();
    if(phase==Phase::selection||(phase==Phase::mainl_handoff&&selection.done))
        return selection_assets_->render(resident,selection);
    return menu_frame(background_,font_,window_,menu);
}
}
