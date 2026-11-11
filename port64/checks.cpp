#include "assets.hpp"
#include "menu.hpp"
#include <algorithm>
#include <iostream>
#include <stdexcept>

namespace {
void check(bool ok, const char* what) { if (!ok) throw std::runtime_error(what); }
template<class Function> void rejects(Function f) {
    bool failed=false;
    try { f(); } catch (const std::runtime_error&) { failed=true; }
    check(failed,"malformed input accepted");
}
void put16(Bytes& b, unsigned at, unsigned value) { b.at(at)=std::uint8_t(value); b.at(at+1)=std::uint8_t(value>>8); }
Bytes archive(bool rle) {
    Bytes raw(80);
    put16(raw,0,64); put16(raw,4,1); put16(raw,6,0x73);
    Bytes directory(64);
    put16(directory,0,rle ? 0x9595 : 0xf388);
    directory[2]=0xa5;
    const std::string name="TEST.BIN";
    std::copy(name.begin(),name.end(),directory.begin()+3);
    put16(directory,16,3); put16(directory,18,rle ? 4 : 3); put16(directory,20,80);
    std::uint8_t key=0x73;
    for (unsigned i=0;i<directory.size();++i) {
        raw[16+i]=directory[i]^key; key=std::uint8_t(key-directory[i]);
    }
    for (auto byte:Bytes{'A','A',rle ? std::uint8_t(3) : std::uint8_t('B')}) raw.push_back(byte^0xa5);
    return raw;
}
Bytes pi(const std::string& bits) {
    Bytes raw={'P','i',26,0,0,0,0,4,'P','C','9','8',0,0,0,4,0,1};
    raw.resize(raw.size()+48);
    for (unsigned i=0;i<bits.size();i+=8) {
        unsigned value=0;
        for (unsigned j=0;j<8;++j) value=(value<<1)|(i+j<bits.size() && bits[i+j]=='1');
        raw.push_back(std::uint8_t(value));
    }
    return raw;
}
void tap(th03::Menu& menu,std::uint16_t key) { menu.tick(0); menu.tick(key); }
}
int main() {
    try {
        static_assert(sizeof(void*)==8 && sizeof(std::uint32_t)==4);
        check(PfArchive(archive(false)).read("test.bin")==Bytes({'A','A','B'}),"PF stored/XOR/case");
        check(PfArchive(archive(true)).read("TEST.BIN")==Bytes(4,'A'),"PF terminal run/logical length");
        auto broken=archive(true); broken.pop_back();
        rejects([&]{PfArchive a(broken);});
        broken=archive(true); broken.back()=0xff^0xa5;
        rejects([&]{PfArchive(broken).read("TEST.BIN");});
        rejects([]{PfArchive(archive(false)).read("MISSING.BIN");});
        // Four-pixel row: two initialized history rows followed by a zero run.
        const auto image=decode_pi(pi("101000100"));
        check(image.width==4 && image.height==1 && image.pixels==Bytes(2,0),"PI history/run");
        rejects([]{decode_pi(pi("101000101"));}); // run of 3 exceeds the 2 output bytes
        rejects([]{decode_pi(Bytes{'P','i'});});
        th03::Menu menu;
        menu.tick(th03::left); menu.tick(th03::down);
        check(menu.screen==th03::Screen::main && menu.selected==0,"title key release lock");
        tap(menu,th03::up); check(menu.selected==5,"menu upward wrap");
        menu.tick(th03::up); check(menu.selected==5,"held input repeats");
        tap(menu,th03::down); check(menu.selected==0,"menu downward wrap");
        tap(menu,th03::up|th03::down); check(menu.selected==0,"simultaneous vertical input order");
        for (int i=0;i<4;++i) tap(menu,th03::down);
        tap(menu,th03::shot); check(menu.screen==th03::Screen::options && menu.selected==0,"option entry");
        tap(menu,th03::left); check(menu.options.rank==3,"rank byte wrap");
        tap(menu,th03::right); check(menu.options.rank==0,"rank forward wrap");
        tap(menu,th03::down); tap(menu,th03::left); check(menu.options.music==0,"music off");
        tap(menu,th03::right); check(menu.options.music==1,"music FM");
        tap(menu,th03::down); tap(menu,th03::left); check(menu.options.keys==2,"keyboard mode wrap");
        tap(menu,th03::cancel); check(menu.screen==th03::Screen::main && menu.selected==4,"option return selection");
        tap(menu,th03::cancel); check(menu.screen==th03::Screen::quit,"menu escape");
        th03::Menu idle;
        for (int i=0;i<520;++i) idle.tick(0);
        check(idle.screen==th03::Screen::title,"early attract request");
        idle.tick(0); check(idle.request==th03::Request::attract && idle.resident_seed==521,"attract boundary/seed");
        std::uint32_t seed=0xffffffffu;
        check(th03::random_next(seed)==32421 && seed==0xfea5b1ccu,"32-bit LCG carry/wrap");
        std::cout<<"PF, PI, menu release/ordering/options and 32-bit RNG checks passed\n";
        return 0;
    } catch (const std::exception& error) { std::cerr<<error.what()<<'\n'; return 1; }
}
