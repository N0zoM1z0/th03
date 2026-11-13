#pragma once
#include "assets.hpp"
#include "cutscene.hpp"
#include "pmd/pmd_pcm.hpp"
#include <fstream>

namespace th03 {
class Sound {
public:
    using Samples=std::function<void(const std::vector<pmd::StereoSample>&)>;
    Sound(const PfArchive& assets,pmd::Board board,Bytes rhythm_rom,Samples samples={});
    void configure(bool enabled);
    void load(const std::string& song);
    void command(std::uint16_t value);
    void event(const SceneSound& event);
    void effect(unsigned id);
    void update_effect();
    void reset_effect() {effect_=255;effect_frame_=0;}
    void refresh();
    void advance(std::uint64_t nanoseconds);
    std::optional<unsigned> measure() const;
    unsigned volume() const {return player_.player().player().music().sequence().state().fade;}
    std::uint64_t samples() const {return player_.pcm().samples();}
    const pmd::PcmPlayer& player() const {return player_;}
private:
    const PfArchive& assets_;
    Samples samples_;
    std::vector<pmd::StereoSample> block_;
    pmd::PcmPlayer player_;
    bool enabled_=true;
    unsigned fraction_=0;
    std::uint8_t effect_=255,effect_frame_=0;
    void install(pmd::Board board);
};
class WavWriter {
public:
    explicit WavWriter(const std::string& path);
    void write(const std::vector<pmd::StereoSample>& block);
    void finish();
private:
    std::ofstream file_;
    std::uint32_t frames_=0;
};
}
