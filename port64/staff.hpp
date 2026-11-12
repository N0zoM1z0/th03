#pragma once
#include "cutscene.hpp"
#include "resident.hpp"
#include "motion.hpp"

namespace th03 {
struct StaffFlake {
    bool alive=false;
    motion::Point position{},velocity{};
    std::uint16_t cel=0;
};
struct StaffSnow {
    std::array<StaffFlake,80> flakes{};
    std::uint32_t seed=0;
    unsigned limit=80;
    void update(std::int16_t frame);
    void draw(Canvas& dest) const;
};
struct StaffVerdict {
    explicit StaffVerdict(const Resident& resident);
    void draw(Canvas& dest,const Font& font) const;
    std::array<std::uint8_t,9> score{};
    std::uint8_t character=0,rank=0,skill=0;
};
class StaffRoll {
public:
    enum class State {black_out,sync,initial,enter,leave,hold,clear,gallery,verdict,done};
    StaffRoll(const PfArchive& assets,const Font& font,const Resident& resident,const Cutscene* previous=nullptr);
    void tick(std::uint16_t input,std::optional<unsigned> measure={},unsigned elapsed_refreshes=1);
    Frame render() const {return pages[shown_page].frame(palette_,tone);}
    bool done() const {return state==State::done;}
    StaffSnow snow;
    StaffVerdict verdict;
    std::array<Canvas,2> pages;
    State state=State::black_out;
    std::int16_t frame=0;
    unsigned back=0,shown_page=0,segment=0;
    int tone=100,speed=2,duration=65,center_limit=200,height_offset=0,secondary_y=0;
    std::array<int,2> centers{};
    unsigned secondary_slot=0;
    bool alpha_enabled=false,alpha_requested=true,auto_adjust=true;
    std::vector<SceneSound> sounds;
private:
    const PfArchive& assets_;
    const Font& font_;
    Palette palette_{};
    std::vector<Cdg> pictures_;
    unsigned wait_=1,clears_=0;
    int fade_tone_=0;
    void setup();
    void begin_segment();
    void clear_blue();
    void clear_interior();
    void unput(int x,int y,unsigned slot);
    void dissolve(int x,int y,unsigned slot,int strength);
    void enter();
    void leave();
    void present(unsigned elapsed_refreshes);
    bool gate(unsigned measure_target,std::optional<unsigned> measure) const;
};
}
