#include "application.hpp"

namespace th03 {
Application::Application(const PfArchive& assets,Options options,const Bytes& nem,const std::string& picture):assets_(assets),
    background_(decode_pi(assets.read(picture))),font_(assets.read("MIKOFT.BFT")),window_(assets.read("OPWIN.BFT")) {
    menu.options=resident.options=options;available_=characters_unlocked(nem) ? 9 : 7;
}
void Application::start_selection(SelectKind kind) {
    if(!selection_assets_)selection_assets_.emplace(assets_);
    selection.begin(resident,kind,available_);phase=Phase::selection;
}
void Application::return_to_title() {
    menu=Menu{};menu.options=resident.options;menu.resident_seed=resident.seed;
    menu.selected=return_selection_;phase=Phase::op;
}
void Application::tick(const InputFrame& input) {
    if(finished())return;
    if(transition_wait_) {--transition_wait_;return;}
    if(phase==Phase::selection) {
        selection.tick(resident,input);
        if(selection.cancelled) {
            if(std::uint8_t(resident.mode)>=0x80)resident.mode=Mode::none;
            return_to_title();
        } else if(selection.done) {
            if(resident.mode==Mode::story)resident.choose_story_opponents();
            else resident.scores={};
            phase=Phase::mainl_handoff;
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
        resident.begin_demo();phase=Phase::mainl_handoff;
    } else phase=Phase::mainl_handoff;
}
Frame Application::render() const {
    if(phase==Phase::selection||(phase==Phase::mainl_handoff&&selection.done))
        return selection_assets_->render(resident,selection);
    return menu_frame(background_,font_,window_,menu);
}
}
