#include "sound.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
constexpr std::uint8_t priorities[]={0,0,32,16,2,18,18,18,64,16,17,2,17,32,18,18,18,18,32,32,18,18,14,0,0,0,0,0,0,0,0,0,0};
constexpr std::uint8_t lengths[]={0,0,36,16,4,16,8,10,48,80,24,17,11,4,80,16,48,74,50,32,24,68,0,0,0,0,0,0,0,0,0,0,0};
}
Sound::Sound(const PfArchive& assets,pmd::Board board,Bytes rom,Samples samples):assets_(assets),samples_(std::move(samples)),
    player_(board,board==pmd::Board::fm26 ? 3993600 : 7987200,std::move(rom),[this](pmd::StereoSample sample){block_.push_back(sample);},pmd::TimerEpoch::cold) {
    player_.stop_music();
    for(unsigned bank=0;bank<2;++bank)for(unsigned address=0;address<256;++address)player_.mirror(std::uint8_t(bank),std::uint8_t(address),0);
    install(board);player_.load_effects(assets.read("YUME.EFC"));
}
void Sound::install(pmd::Board board) {
    // Semantic PMD installation sequence shared with TH04's resident owner.
    // Legacy Board values are PMD=0, PMDB2=1, PMD86=2.
    const auto write=[&](unsigned bank,unsigned a,unsigned v){player_.initialize({std::uint8_t(bank),std::uint8_t(a),std::uint8_t(v)});};
    if(board==pmd::Board::fm86) {
        write(0,0x29,0x83);write(1,0,1);write(1,0x10,0x17);write(1,0x10,0x80);
        write(1,0,0x60);write(1,1,2);write(1,12,255);write(1,13,255);
        write(1,2,255);write(1,3,31);write(1,4,255);write(1,5,255);
        write(1,8,0);write(1,0x10,0);write(1,0x10,0x80);write(1,0,1);
    }
    write(0,7,63);write(0,0x29,0);
    for(unsigned a=0x24;a<=0x26;++a)write(0,a,0);
    write(0,0x27,63);write(0,0x29,0x83);write(0,6,0);
    const unsigned banks=board==pmd::Board::fm26 ? 1 : 2;
    for(unsigned bank=0;bank<banks;++bank)for(unsigned c=0;c<3;++c)write(bank,0xb4+c,192);
    write(0,0x22,0);
    if(board==pmd::Board::fm26){write(1,0x10,0x80);write(1,0x10,0x18);}else{write(0,0x10,255);write(0,0x11,48);}
    write(0,7,191);
    for(unsigned bank=0;bank<banks;++bank)for(unsigned slot=0;slot<4;++slot)for(unsigned c=0;c<3;++c)write(bank,0x80+slot*4+c,255);
    for(unsigned bank=0;bank<banks;++bank)for(unsigned c=0;c<3;++c)write(0,0x28,c+(bank ? 4 : 0));
    write(0,7,191);
    if(board==pmd::Board::speakboard){write(1,0x10,0x80);write(1,0x10,0x18);}
    write(0,0x26,200);write(0,0x25,0);write(0,0x24,0);write(0,0x27,63);write(0,0x29,0x83);
}
void Sound::configure(bool enabled) {
    if(enabled_==enabled)return;
    if(!enabled)player_.stop_music();
    enabled_=enabled;
    if(enabled)player_.start_music();
}
void Sound::load(const std::string& song) {player_.load_music(assets_.read(song));}
void Sound::command(std::uint16_t value) {
    if(!enabled_)return;
    switch(value>>8) {
    case 0:player_.start_music();break;
    case 1:player_.stop_music();break;
    case 2:player_.fade(std::int8_t(value&255));break;
    default:throw std::runtime_error("unrecovered TH03 sound command");
    }
}
void Sound::event(const SceneSound& e) {
    if(e.kind==SceneSound::Kind::load)load(e.name);
    else if(e.kind==SceneSound::Kind::control)command(std::uint16_t(e.value));
    else effect(unsigned(e.value));
}
void Sound::effect(unsigned id) {
    if(id==255){reset_effect();return;}
    if(id>=sizeof(priorities))throw std::runtime_error("unrecovered TH03 effect priority alias");
    if(effect_==255){effect_=std::uint8_t(id);return;}
    if(priorities[effect_]<=priorities[id]){effect_=std::uint8_t(id);effect_frame_=0;}
}
void Sound::update_effect() {
    if(effect_==255)return;
    if(!effect_frame_)player_.start_effect(effect_);
    ++effect_frame_;
    if(effect_frame_>lengths[effect_]){effect_frame_=0;effect_=255;}
}
void Sound::refresh() {const auto scaled=1000000000u+fraction_;advance(scaled/60);fraction_=scaled%60;}
void Sound::advance(std::uint64_t ns) {player_.advance_ns(ns);if(samples_)samples_(block_);block_.clear();}
std::optional<unsigned> Sound::measure() const {return enabled_ ? std::optional<unsigned>(player_.player().player().music().sequence().state().measure) : std::nullopt;}
WavWriter::WavWriter(const std::string& path):file_(path,std::ios::binary|std::ios::trunc) {
    if(!file_)throw std::runtime_error("cannot create WAV output");
    const char header[44]{};file_.write(header,44);
}
void WavWriter::write(const std::vector<pmd::StereoSample>& block) {
    if(block.size()>0x3ffffff0u-frames_)throw std::runtime_error("WAV output exceeds RIFF size");
    frames_+=std::uint32_t(block.size());
    static_assert(sizeof(pmd::StereoSample)==4,"x64 signed16 stereo layout");
    file_.write(reinterpret_cast<const char*>(block.data()),std::streamsize(block.size()*4));
    if(!file_)throw std::runtime_error("WAV write failed");
}
void WavWriter::finish() {
    file_.seekp(0);const auto word=[&](unsigned value,unsigned count){for(unsigned i=0;i<count;++i)file_.put(char(value>>(i*8)));};
    file_.write("RIFF",4);word(36+frames_*4,4);file_.write("WAVEfmt ",8);word(16,4);word(1,2);word(2,2);
    word(48000,4);word(192000,4);word(4,2);word(16,2);file_.write("data",4);word(frames_*4,4);file_.close();
    if(!file_)throw std::runtime_error("WAV finalize failed");
}
}
