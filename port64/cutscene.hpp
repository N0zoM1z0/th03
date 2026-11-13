#pragma once
#include "assets.hpp"
#include "font.hpp"
#include "game_types.hpp"
#include <optional>
#include <functional>

namespace th03 {
struct ScriptCursor {
    explicit ScriptCursor(Bytes bytes,std::uint16_t start=0):bytes(std::move(bytes)),start(start),at(start) {}
    std::uint8_t peek(unsigned ahead=0) const {return bytes.at(std::uint16_t(at+ahead-start));}
    std::uint8_t take() {const auto c=peek();++at;return c;}
    int first();
    int first(int fallback) {number_default=fallback;return first();}
    int second();
    std::string filename();
    Bytes bytes;
    std::uint16_t start=0,at=0;
    int number_default=0;
    bool carry=false;
};
struct SceneSound {
    enum class Kind {load,control,effect};
    Kind kind;
    std::string name;
    int value=0;
};
class Cutscene {
public:
    enum class Wait {none,delay,release,press,ok,fade,measure};
    using Measure=std::function<std::optional<unsigned>()>;
    Cutscene(const PfArchive& assets,const Font& font,std::string filename,std::uint16_t input=0,Measure measure={});
    Cutscene(const PfArchive& assets,const Font& font,Bytes bytes,std::uint16_t input=0,Measure measure={});
    void tick(std::uint16_t input);
    Frame render() const;
    bool done() const {return stopped_;}
    ScriptCursor script;
    Point cursor{80,320};
    int interval=1,weight=2,tone=0;
    std::uint8_t color=15;
    unsigned shown_page=0,scroll=0;
    std::uint8_t speedup_cycle=0;
    bool fast_forward=false;
    Wait wait=Wait::none;
    std::vector<SceneSound> sounds;
    // The graphics pages remain distinct for gaiji, vp and picture transitions.
    std::array<Canvas,2> pages;
    const Palette& palette() const {return palette_;}
private:
    Measure measure_;
    unsigned measure_target_=0;
    bool measure_key_=false;
    const PfArchive& assets_;
    const Font& font_;
    Bytes gaiji_,box_;
    std::optional<PiImage> picture_;
    Palette palette_{};
    bool stopped_=false,fade_sync_=false;
    enum class After {none,clear,clear_glyph,tone,mask,shake,speedup};
    After after_=After::none;
    unsigned ticks_=0,timeout_=0;
    int pending_tone_=0,fade_value_=0,fade_target_=0,fade_step_=0,fade_speed_=0;
    unsigned mask_quarter_=0,mask_step_=0,mask_delay_=0,shake_step_=0,shake_last_=0;
    void pump(std::uint16_t input);
    void op(unsigned command,std::uint16_t input);
    void snapshot();
    void restore(unsigned page);
    void clear_text();
    void quarter(unsigned id,std::optional<unsigned> mask={});
    void masked_step();
    void shake_step();
    bool advance_cursor(std::uint16_t input,bool glyph);
    void glyph_delay(std::uint16_t input);
    void sleep(unsigned frames,After after=After::none);
    bool wait_change(unsigned frames,std::uint16_t input,After after);
    void fade(int from,int to,int speed);
    void complete_wait(std::uint16_t input);
    void gaiji(unsigned page,std::uint16_t id,bool carry);
};
}
