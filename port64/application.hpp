#pragma once
#include "selection.hpp"
#include "stage_intro.hpp"
#include "round.hpp"
#include "battle_graphics.hpp"
#include "round_loop.hpp"
#include "win.hpp"
#include "score_menu.hpp"
#include "cutscene.hpp"
#include "staff.hpp"
#include "music.hpp"
#include "configuration.hpp"
#include <optional>

namespace th03 {
enum class Phase {op,versus,selection,mainl_handoff,quit,stage_intro,battle,winner,scores,continuing,game_over,cutscene,ending_wait,staff,music};
class Application {
public:
    Application(const PfArchive& assets,Options options,const Bytes& nem,const std::string& picture="TL02.PI",Bytes font_bitmap={},const PfArchive* main_assets=nullptr,std::filesystem::path save_directory={},Bytes configuration={});
    void tick(const InputFrame& input);
    Frame render() const;
    bool finished() const {return phase==Phase::quit||phase==Phase::mainl_handoff;}
    void start_selection(SelectKind kind);
    void return_to_title();
    void start_stage_intro();
    void start_main(bool play=true);
    void start_post_match(std::uint16_t input=0);
    void start_scores();
    void start_story_dialogue(unsigned part,std::uint16_t input=0);
    void start_ending();
    void start_staff();
    void start_music(std::uint16_t input=0);
    void save_configuration(bool exiting=true) {configuration.save(resident.options,exiting);}
    Phase phase=Phase::op;
    Menu menu;
    Resident resident;
    Selection selection;
    std::optional<Round> round;
    std::optional<RoundLoop> round_loop;
    ScoreFile score_file;
    Configuration configuration;
    MusicState music_state;
private:
    const PfArchive& assets_;
    const PfArchive* main_assets_;
    PiImage background_;
    Font graphic_font_;
    std::optional<StageIntro> intro_;
    std::optional<BattleGraphics> battle_graphics_;
    std::optional<WinScreen> win_;
    std::optional<ScoreMenu> scores_;
    std::optional<ContinueMenu> continue_;
    std::optional<GameOver> game_over_;
    std::optional<Cutscene> cutscene_;
    std::optional<StaffRoll> staff_;
    std::optional<MusicRoom> music_;
    bool op_process_active_=true;
    enum class DialogueRoute {story,ending,bonus};
    DialogueRoute dialogue_route_=DialogueRoute::story;
    bool ending_registration_=false;
    Bytes font_,window_;
    std::optional<SelectionAssets> selection_assets_;
    unsigned available_=7,transition_wait_=0;
    std::int8_t return_selection_=0;
};
}
