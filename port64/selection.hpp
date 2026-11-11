#pragma once
#include "assets.hpp"
#include "graphics.hpp"
#include "resident.hpp"

namespace th03 {
struct InputFrame {
    std::uint16_t single=0;
    std::array<std::uint16_t,2> players{};
};
enum class SelectKind {story,versus_cpu,two_player};
struct Selection {
    SelectKind kind=SelectKind::story;
    std::array<std::uint8_t,2> selected{};
    std::array<bool,2> confirmed{},locked{};
    std::uint8_t available=7,cycle=0,display_cycle=0,trail=8,display_trail=8;
    std::uint16_t fade=0;
    unsigned active_player=0,initial_wait=30,flash=0,vblank=0;
    int tone=100;
    bool done=false,cancelled=false,first_iteration=true;
    void begin(const Resident& resident,SelectKind mode,unsigned unlocked);
    void update_player(Resident& resident,std::uint16_t input,unsigned pid);
    void tick(Resident& resident,const InputFrame& input);
};
class SelectionAssets {
public:
    explicit SelectionAssets(const PfArchive& archive);
    Frame render(const Resident& resident,const Selection& selection) const;
private:
    Palette palette;
    Bytes font;
    std::vector<Cdg> portraits;
    Cdg question,stats,extra,extras;
    Bfnt names;
};
void selection_curves(Canvas& canvas,std::uint8_t cycle,int trails);
}
