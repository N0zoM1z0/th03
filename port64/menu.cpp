#include "menu.hpp"
#include <array>
#include <stdexcept>
#include <string>

namespace th03 {
namespace {
void move(std::int8_t& selected, int delta, int count) {
    selected = std::int8_t(selected + delta);
    if (selected < 0) selected = std::int8_t(count - 1);
    if (selected >= count) selected = 0;
}
void cycle(std::uint8_t& value, int delta, int count) {
    value = std::uint8_t((value + count + delta) % count);
}
std::uint32_t color(const PiImage& image, unsigned index) {
    const auto component = [&](unsigned c) {
        const unsigned four = image.palette[index * 3 + c] >> 4;
        const unsigned six = (four << 2) | (four >> 2);
        return (six << 2) | (six >> 4);
    };
    return 0xff000000u | (component(0) << 16) | (component(1) << 8) | component(2);
}
using Colors=std::array<std::uint32_t,16>;
Colors colors(const PiImage& image) {
    Colors out{};for(unsigned i=0;i<out.size();++i)out[i]=color(image,i);return out;
}
Frame expand_picture(const PiImage& image,const Colors& palette) {
    Frame frame(std::size_t(image.width)*image.height);
    std::size_t i=0;
    for(;i+1<frame.size();i+=2) {
        const auto packed=image.pixels.at(i/2);
        frame[i]=palette[packed>>4];frame[i+1]=palette[packed&15];
    }
    if(i<frame.size())frame[i]=palette[image.pixels.at(i/2)>>4];
    return frame;
}
unsigned word(const Bytes& data, unsigned at) {
    return data.at(at) | (unsigned(data.at(at + 1)) << 8);
}
void text(Frame& frame, const Bytes& font, unsigned first, unsigned count,
          int center, int line, int shift, bool selected) {
    const int left = ((center - (int(count) + shift) * 8) / 8) * 8;
    const unsigned base = 32 + word(font, 28);
    for (unsigned i=0; i<count; ++i)
        for (unsigned y=0; y<16; ++y)
            for (unsigned x=0; x<16; ++x)
                if (font.at(base + (first+i)*32 + y*2 + x/8) & (0x80u >> (x&7)))
                    frame.at((272 + line*16 + y)*640 + left+i*16+x) = selected ? 0xffffffffu : 0xff000000u;
}
void box(Frame& frame, const Colors& palette, const Bytes& window, int width) {
    // OPWIN.BFT: three packed 16x128 patterns, palette, transparent color 0.
    const unsigned base = 32 + word(window, 28) + 48;
    const Frame background=frame;
    const auto sprite = [&](int left, unsigned pattern) {
        for (unsigned y=0; y<128; ++y)
            for (unsigned x=0; x<16; ++x) {
                const auto packed = window.at(base + pattern*1024 + y*8 + x/2);
                const unsigned index = (x&1) ? packed&15 : packed>>4;
                if (index) frame.at((256+y)*640+left+x) = palette[index];
            }
    };
    sprite(160,0);
    for (int x=176; x<160+width-8; x+=8) {
        // Each animation step restores this full column from page 1 before
        // drawing the next transparent right edge; overlapping is not OR.
        for (unsigned y=0;y<128;++y)
            for (unsigned dx=0;dx<16;++dx)
                frame[(256+y)*640+x+dx]=background[(256+y)*640+x+dx];
        sprite(x,2);
    }
}
}

void Menu::tick(std::uint16_t input) {
    if (screen == Screen::quit || screen == Screen::handoff) return;
    if (screen == Screen::title) {
        ++resident_seed;
        if (++idle_frames > 520) {
            request=Request::attract; screen=Screen::handoff;
        } else if (input) {
            screen=Screen::main; input_allowed=false;
        }
        return;
    }
    if (!input) input_allowed=true;
    if (!input_allowed) return;
    if(screen==Screen::versus) {
        if(input&up)move(selected,-1,3);
        if(input&down)move(selected,1,3);
        if(input&(ok|shot)) {request=Request::versus;screen=Screen::handoff;}
        // The original VS submenu has no Escape branch.
        if(input)input_allowed=false;
        return;
    }
    const bool option = screen == Screen::options;
    // These are independent tests: simultaneous Up and Down cancel in order.
    if (input&up) move(selected,-1,option ? 4 : 6);
    if (input&down) move(selected,1,option ? 4 : 6);
    if (option) {
        const auto adjust = [&](int delta) {
            if (selected==0) cycle(options.rank,delta,4);
            if (selected==1) options.music = options.music ? 0 : 1;
            if (selected==2) cycle(options.keys,delta,3);
        };
        if (input&right) adjust(1);
        if (input&left) adjust(-1);
        if ((input&cancel) || ((input&(ok|shot)) && selected==3)) {
            screen=Screen::main; selected=4;
        }
    } else {
        if (input&(ok|shot)) {
            if (selected==4) { screen=Screen::options; selected=0; }
            else if (selected==5) screen=Screen::quit;
            else {
                request=std::array<Request,4>{Request::story,Request::versus,Request::music,Request::scores}[selected];
                screen=Screen::handoff;
            }
        }
        if (input&cancel) screen=Screen::quit;
    }
    if (input) input_allowed=false;
}

Frame pi_frame(const PiImage& image) {
    return expand_picture(image,colors(image));
}

Frame menu_frame(const PiImage& background, const Bytes& gaiji, const Bytes& window, const Menu& menu) {
    if (background.width!=640 || background.height!=400 || gaiji.size()!=8224 || window.size()!=3152)
        throw std::runtime_error("unexpected TH03 title/menu geometry");
    const auto palette=colors(background);
    auto frame=expand_picture(background,palette);
    if (menu.screen==Screen::title ||
        (menu.screen==Screen::handoff && menu.request==Request::attract)) return frame;
    const bool option=menu.screen==Screen::options;
    const bool versus=menu.screen==Screen::versus;
    box(frame,palette,window,(option||versus) ? 240 : 136);
    if(versus) {
        for(int i=0;i<3;++i) {
            text(frame,gaiji,i==2 ? 0x92 : 0x88,4,248,i+1,0,menu.selected==i);
            text(frame,gaiji,i==1 ? 0x96 : 0x8c,4,312,i+1,0,menu.selected==i);
        }
        return frame;
    }
    if (!option) {
        constexpr unsigned starts[]={0x30,0x33,0x41,0x82,0x3d,0x48};
        constexpr unsigned counts[]={3,6,7,5,4,3};
        constexpr int shifts[]={0,-1,-1,-1,-1,-1};
        for (int i=0;i<6;++i) text(frame,gaiji,starts[i],counts[i],228,i,shifts[i],menu.selected==i);
    } else {
        const auto selected=[&](int i){return menu.selected==i;};
        text(frame,gaiji,0x6e,3,228,0,0,selected(0));
        text(frame,gaiji,0x4b,4,228,2,-1,selected(1));
        text(frame,gaiji,0x5c,6,228,4,-1,selected(2));
        text(frame,gaiji,0x48,3,280,5,0,selected(3));
        constexpr unsigned rank_first[]={0x71,0x74,0x78,0x7b};
        constexpr unsigned rank_count[]={3,4,3,6};
        text(frame,gaiji,rank_first[menu.options.rank],rank_count[menu.options.rank],340,0,1,selected(0));
        // Values include the original space cells around proportional glyphs.
        if (menu.options.music==2) text(frame,gaiji,0x53,7,336,2,0,true);
        else text(frame,gaiji,menu.options.music ? 0x4f : 0x5a,menu.options.music ? 4 : 2,328,2,0,true);
        text(frame,gaiji,menu.options.keys==1 ? 0x6a : 0x68,2,300,4,0,selected(2));
        text(frame,gaiji,0x6c,2,332,4,0,selected(2));
        text(frame,gaiji,menu.options.keys==2 ? 0x6a : 0x68,2,364,4,0,selected(2));
    }
    return frame;
}

Bytes ppm(const Frame& frame) {
    const std::string header="P6\n640 400\n255\n";
    Bytes out(header.begin(),header.end());
    for (auto pixel:frame) {
        out.push_back(std::uint8_t(pixel>>16));
        out.push_back(std::uint8_t(pixel>>8));
        out.push_back(std::uint8_t(pixel));
    }
    return out;
}
}
