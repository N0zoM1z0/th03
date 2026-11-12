#pragma once
#include "cutscene.hpp"
#include "motion.hpp"
#include <functional>

namespace th03 {
struct MusicPolygon {
    Point center{},velocity{}; // X is pixels; Y is signed Q4.
    std::uint8_t angle=0,angle_speed=0;
};
struct MusicState {
    std::array<MusicPolygon,16> polygons{};
    bool initialized=false;
    std::uint32_t seed=1; // OP's process-local master.lib seed, independent of resident.rand.
    std::uint8_t playing=0;
    void update(const std::function<void(const std::vector<Point>&)>& draw);
};
void music_polygon(Canvas& dest,const std::vector<Point>& points);
class MusicRoom {
public:
    MusicRoom(const PfArchive& assets,const Font& font,MusicState& state,std::uint16_t input=0);
    void tick(std::uint16_t input);
    bool done() const {return phase==Phase::done;}
    Frame render() const {return pages[shown].frame(palette_);}
    enum class Phase {release,controls,after_play,exit_release,done};
    Phase phase=Phase::release;
    std::array<Canvas,2> pages;
    unsigned selected=0,back=1,accessed=0,shown=0,frames=0;
    std::vector<SceneSound> sounds;
private:
    const Font& font_;
    MusicState& state_;
    Palette palette_{};
    Bytes comments_,blue_;
    Canvas comment_background_;
    std::uint16_t sampled_=0;
    void track(unsigned index,unsigned color);
    void comment();
    void restore_blue();
    void animate();
    void pump(std::uint16_t input);
};
}
