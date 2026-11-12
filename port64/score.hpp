#pragma once
#include "menu.hpp"
#include <array>
#include <filesystem>
#include <optional>

namespace th03 {
struct Resident;
namespace regi {
constexpr unsigned space=14,backspace=30,zero=32,period=42,question=45,end=46,all=48,count=49;
unsigned ascii(char c);
}
struct ScoreSection {
    static constexpr unsigned size=206,names=2,clear=82,unknown=83,scores=84,characters=184,stages=194,key1=204,key2=205;
    std::array<std::uint8_t,size> bytes{};
    void decode();
    bool valid() const;
    Bytes encode(std::uint32_t& seed,const Resident& resident,bool mainl=true);
    void defaults();
    int insert(const Resident& resident);
    void default_name(unsigned place,unsigned character);
};
struct NameEntry {
    unsigned letter=0;
    std::uint8_t cursor=7;
    std::array<std::int16_t,4> holds{};
    bool done=false,enter_locked=false,back_locked=false,first=true;
    // Drawing requests keep the original direction/erase/preview order.
    std::array<unsigned,4> old_letters{};
    std::array<std::uint8_t,3> erased{};
    unsigned old_count=0,erase_count=0;
    // The eighth letter writes14 into the snow pool, beyond HI. MAINL then
    // exits or execs MAIN; the snow owner is not used again in this process.
    std::optional<unsigned> snow_spill;
    bool tick(std::uint16_t input,ScoreSection& section,unsigned place);
};
class ScoreFile {
public:
    ScoreFile(Bytes original={},std::filesystem::path directory={});
    ScoreSection load(unsigned rank,std::uint32_t& seed,const Resident& resident,bool mainl=true);
    void save(ScoreSection& section,unsigned rank,std::uint32_t& seed,const Resident& resident,bool mainl=true);
    const Bytes& encoded() const {return encoded_;}
private:
    Bytes encoded_;
    std::filesystem::path path_;
    void commit() const;
};
std::filesystem::path default_save_directory();
}
