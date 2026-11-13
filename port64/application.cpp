#include "application.hpp"
#include <stdexcept>
#include <cstdio>

namespace th03 {
Application::Application(const PfArchive& assets,Options options,const Bytes& nem,const std::string& picture,Bytes font_bitmap,const PfArchive* main_assets,std::filesystem::path save_directory,Bytes cfg):score_file(nem,save_directory),configuration(options,std::move(save_directory),std::move(cfg)),assets_(assets),main_assets_(main_assets),
    background_(decode_pi(assets.read(picture))),graphic_font_(std::move(font_bitmap)),font_(assets.read("MIKOFT.BFT")),window_(assets.read("OPWIN.BFT")) {
    menu.options=resident.options=configuration.options();available_=characters_unlocked(score_file.encoded()) ? 9 : 7;
}
void Application::attach_sound(Sound& sound) {
    sound_=&sound;sound.load("OP.M");sound.configure(resident.options.music!=0);sound.command(0);
}
void Application::scene_audio(const std::vector<SceneSound>& events,std::size_t& cursor) {
    if(sound_)while(cursor<events.size())sound_->event(events[cursor++]);
}
void Application::play_song(const std::string& name) {if(sound_){sound_->command(0x100);sound_->load(name);sound_->command(0);}}
void Application::tick(const InputFrame& input) {if(finished())return;tick_game(input);if(sound_)sound_->refresh();}
void Application::start_selection(SelectKind kind) {
    if(!selection_assets_)selection_assets_.emplace(assets_);
    music_state.seed=resident.seed;
    play_song("SELECT.M");
    selection.begin(resident,kind,available_);phase=Phase::selection;
}
void Application::start_stage_intro() {
    if(op_process_active_)save_configuration(false);
    op_process_active_=false;
    if(sound_)sound_->command(0x100);
    intro_.emplace(assets_,graphic_font_,resident);phase=Phase::stage_intro;
}
void Application::start_main(bool play) {
    if(!main_assets_)throw std::runtime_error("MAIN setup requires the second original PF archive");
    round.emplace();round->begin(resident,main_assets_->read("ENEDAT.DAT"));round_audio_=0;
    round->sound_update=[this] {if(sound_){while(round_audio_<round->sounds.size())sound_->effect(round->sounds[round_audio_++]);sound_->update_effect();}};
    if(sound_) {
        sound_->reset_effect();char name[16];std::snprintf(name,sizeof(name),"%02uMM.M",character_id(resident.paletted[1]));
        play_song(intro_ ? intro_->music() : resident.stage==6 ? "DEC.M" : name);
    }
    battle_graphics_.emplace(assets_,*main_assets_,resident,&graphic_font_);round->set_palette(battle_graphics_->palette());phase=Phase::mainl_handoff;
    round_loop.reset();
    if(play) {round_loop.emplace();round_loop->begin(*round,*battle_graphics_);phase=Phase::battle;}
}
void Application::return_to_title() {
    if(!op_process_active_) {music_state=MusicState{};op_process_active_=true;}
    play_song("OP.M");
    menu=Menu{};menu.options=resident.options;menu.resident_seed=resident.seed;
    menu.selected=return_selection_;phase=Phase::op;
}
void Application::start_post_match(std::uint16_t input) {
    win_.reset();if(sound_)sound_->reset_effect();
    const auto played=resident.paletted;
    const auto route=story_dispatch(resident);
    if(route==StoryRoute::final_dialogue) {start_story_dialogue(1,input);return;}
    if(route==StoryRoute::ending) {start_ending();return;}
    play_song("WIN.M");
    win_.emplace(assets_,graphic_font_,resident,played);phase=Phase::winner;
}
void Application::start_scores() {if(op_process_active_)save_configuration(false);op_process_active_=false;scores_.emplace(assets_,graphic_font_,score_file,resident);score_audio_=0;scene_audio(scores_->sounds,score_audio_);phase=Phase::scores;}
void Application::start_story_dialogue(unsigned part,std::uint16_t input) {
    char file[16];std::snprintf(file,sizeof(file),"@%02uDM%u.TXT",character_id(resident.paletted[0]),part);
    cutscene_.emplace(assets_,graphic_font_,file,input,[this]{return sound_ ? sound_->measure() : std::nullopt;});cutscene_audio_=0;scene_audio(cutscene_->sounds,cutscene_audio_);dialogue_route_=DialogueRoute::story;phase=Phase::cutscene;
}
void Application::start_ending() {transition_wait_=96;phase=Phase::ending_wait;}
void Application::start_staff() {staff_.emplace(assets_,graphic_font_,resident,cutscene_ ? &*cutscene_ : nullptr);phase=Phase::staff;staff_audio_=0;scene_audio(staff_->sounds,staff_audio_);}
void Application::start_music(std::uint16_t input) {music_.emplace(assets_,graphic_font_,music_state,input);phase=Phase::music;music_audio_=0;scene_audio(music_->sounds,music_audio_);}
void Application::tick_game(const InputFrame& input) {
    if(finished())return;
    if(phase==Phase::music) {music_->tick(input.single);scene_audio(music_->sounds,music_audio_);if(music_->done())return_to_title();return;}
    if(phase==Phase::ending_wait) {
        if(!--transition_wait_) {
            char file[16];std::snprintf(file,sizeof(file),"@%02uED.TXT",character_id(resident.paletted[0]));
            cutscene_.emplace(assets_,graphic_font_,file,input.single,[this]{return sound_ ? sound_->measure() : std::nullopt;});cutscene_audio_=0;scene_audio(cutscene_->sounds,cutscene_audio_);dialogue_route_=DialogueRoute::ending;phase=Phase::cutscene;
        }
        return;
    }
    if(phase==Phase::cutscene) {
        cutscene_->tick(input.single);scene_audio(cutscene_->sounds,cutscene_audio_);
        if(cutscene_->done()) {
            if(dialogue_route_==DialogueRoute::ending)start_staff();
            else if(dialogue_route_==DialogueRoute::bonus)return_to_title();
            else start_stage_intro();
        }
        return;
    }
    if(phase==Phase::staff) {
        staff_->tick(input.single,sound_ ? sound_->measure() : std::nullopt,1,sound_&&resident.options.music ? std::optional<unsigned>(sound_->volume()) : std::nullopt);scene_audio(staff_->sounds,staff_audio_);
        if(staff_->done()) {resident.stage=99;ending_registration_=true;start_scores();}
        return;
    }
    if(phase==Phase::scores) {
        scores_->tick(input.single,sound_&&resident.options.music ? std::optional<unsigned>(sound_->volume()) : std::nullopt);scene_audio(scores_->sounds,score_audio_);
        if(scores_->done()) {
            available_=characters_unlocked(score_file.encoded()) ? 9 : 7;
            if(ending_registration_) {
                ending_registration_=false;
                if(resident.credits==3&&resident.paletted[0]<15) {
                    cutscene_.emplace(assets_,graphic_font_,"@99ED.TXT",input.single,[this]{return sound_ ? sound_->measure() : std::nullopt;});cutscene_audio_=0;scene_audio(cutscene_->sounds,cutscene_audio_);dialogue_route_=DialogueRoute::bonus;phase=Phase::cutscene;
                } else return_to_title();
            } else if(resident.show_scores)return_to_title();
            else {
                continue_.emplace(assets_,graphic_font_,resident);continue_audio_=0;phase=Phase::continuing;
                if(continue_->done()) {game_over_.emplace(assets_);phase=Phase::game_over;}
            }
        }
        return;
    }
    if(phase==Phase::continuing) {
        continue_->tick(input.single);scene_audio(continue_->sounds,continue_audio_);
        if(continue_->done()) {
            if(continue_->selected)start_stage_intro();
            else {game_over_.emplace(assets_);phase=Phase::game_over;}
        }
        return;
    }
    if(phase==Phase::game_over) {game_over_->tick();if(game_over_->done())return_to_title();return;}
    if(phase==Phase::winner) {
        win_->tick(input.single,sound_ ? sound_->measure() : std::nullopt);
        if(win_->done()) {
            if(sound_)sound_->command(0x100);
            const auto route=story_dispatch(resident);
            if(resident.mode!=Mode::story)return_to_title();
            else if(route==StoryRoute::stage)start_stage_intro();
            else if(route==StoryRoute::other)start_scores();
            else if(route==StoryRoute::dialogue)start_story_dialogue(0,input.single);
            else phase=Phase::mainl_handoff;
        }
        return;
    }
    if(phase==Phase::battle) {
        round_loop->tick(*round,resident,*battle_graphics_,input);
        if(round_loop->outcome!=RoundExit::running) {
            resident.seed=round->frame;
            if(round_loop->outcome==RoundExit::return_to_op)return_to_title();
            else if(round_loop->outcome==RoundExit::next_round)round_loop->restart(*round,resident);
            else {++resident.stage;start_post_match(input.single);}
        }
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
    if(sound_)sound_->configure(resident.options.music!=0);
    if(menu.screen==Screen::quit) {save_configuration();phase=Phase::quit;return;}
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
    } else if(menu.request==Request::music) {
        return_selection_=menu.selected;start_music(input.single);
    } else if(menu.request==Request::scores) {
        return_selection_=menu.selected;resident.show_scores=true;resident.stage=255;start_scores();
    } else phase=Phase::mainl_handoff;
}
Frame Application::render() const {
    if(phase==Phase::ending_wait)return Frame(640*400,0xff000000);
    if(phase==Phase::staff)return staff_->render();
    if(phase==Phase::music)return music_->render();
    if(phase==Phase::cutscene)return cutscene_->render();
    if(phase==Phase::scores)return scores_->render();
    if(phase==Phase::continuing)return continue_->render();
    if(phase==Phase::game_over)return game_over_->render();
    if(win_&&(phase==Phase::winner||phase==Phase::mainl_handoff))return win_->render();
    if(round_loop&&(phase==Phase::battle||phase==Phase::mainl_handoff))return round_loop->render(*round,resident,*battle_graphics_);
    if(round&&phase==Phase::mainl_handoff)return battle_graphics_->render(*round,resident);
    if(phase==Phase::stage_intro||(phase==Phase::mainl_handoff&&intro_))return intro_->render();
    if(phase==Phase::selection||(phase==Phase::mainl_handoff&&selection.done))
        return selection_assets_->render(resident,selection);
    return menu_frame(background_,font_,window_,menu);
}
}
