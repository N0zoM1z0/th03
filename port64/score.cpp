#include "score.hpp"
#include "resident.hpp"
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iterator>
#include <stdexcept>
#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace th03 {
unsigned regi::ascii(char c) {
    if(c==' ')return space;
    if(c>='A'&&c<='M')return unsigned(c-'A');
    if(c>='N'&&c<='Z')return 16+unsigned(c-'N');
    return period;
}
void ScoreSection::decode() {
    for(unsigned i=0;i<203;++i) {
        const unsigned next=bytes[i+1],feedback=((next>>3)|(next<<5))&255;
        bytes[i]=std::uint8_t(bytes[i]+bytes[key1]+(feedback^bytes[key2]));
    }
    bytes[203]=std::uint8_t(bytes[203]+bytes[key1]+bytes[key2]);
}
bool ScoreSection::valid() const {
    unsigned sum=0;for(unsigned i=2;i<size;++i)sum+=bytes[i];
    return (sum&65535)==(unsigned(bytes[0])|(unsigned(bytes[1])<<8));
}
Bytes ScoreSection::encode(std::uint32_t& seed,const Resident& resident,bool mainl) {
    bytes[key1]=std::uint8_t(random_next(seed));bytes[key2]=std::uint8_t(random_next(seed));bytes[unknown]=std::uint8_t(random_next(seed));
    if(mainl&&resident.stage==99&&resident.credits==3)bytes[clear]=99;
    unsigned sum=0;for(unsigned i=2;i<size;++i)sum+=bytes[i];
    bytes[0]=std::uint8_t(sum);bytes[1]=std::uint8_t(sum>>8);
    Bytes encrypted(bytes.begin(),bytes.end());unsigned feedback=bytes[key2];
    for(int i=203;i>=0;--i) {
        auto& byte=encrypted[unsigned(i)];byte=std::uint8_t(byte-bytes[key1]-feedback);
        feedback=(((unsigned(byte)>>3)|(unsigned(byte)<<5))&255)^bytes[key2];
    }
    return encrypted;
}
void ScoreSection::defaults() {
    for(unsigned place=0;place<10;++place) {
        std::fill_n(bytes.begin()+names+place*8,8,regi::period);
        std::fill_n(bytes.begin()+scores+place*10,10,regi::zero);
        bytes[characters+place]=0;bytes[stages+place]=regi::zero+1;
        bytes[scores+place*10+(place ? 3 : 4)]=std::uint8_t(regi::zero+(place ? 10-place : 1));
    }
    bytes[clear]=18;
}
int ScoreSection::insert(const Resident& resident) {
    unsigned place;
    for(place=0;place<10;++place) {
        bool greater=false;
        for(int digit=7;digit>=0;--digit) {
            const unsigned current=regi::zero+resident.scores[0][unsigned(digit)],other=bytes[scores+place*10+unsigned(digit)+1];
            if(current>other) {greater=true;break;}
            if(current<other)break;
        }
        if(greater)break;
    }
    if(place==10)return -1;
    for(unsigned row=9;row>place;--row) {
        std::copy_n(bytes.begin()+names+(row-1)*8,8,bytes.begin()+names+row*8);
        std::copy_n(bytes.begin()+scores+(row-1)*10,10,bytes.begin()+scores+row*10);
        bytes[characters+row]=bytes[characters+row-1];bytes[stages+row]=bytes[stages+row-1];
    }
    std::fill_n(bytes.begin()+names+place*8,8,regi::space);
    for(unsigned digit=0;digit<8;++digit)bytes[scores+place*10+digit+1]=std::uint8_t(regi::zero+resident.scores[0][digit]);
    bytes[scores+place*10]=std::uint8_t(regi::zero+3-resident.credits);
    bytes[characters+place]=std::uint8_t(character_id(resident.paletted[0])+1);
    bytes[stages+place]=std::uint8_t(resident.stage==99 ? regi::all : regi::zero+resident.stage);
    return int(place);
}
void ScoreSection::default_name(unsigned place,unsigned character) {
    const auto start=bytes.begin()+names+place*8;
    if(!std::all_of(start,start+8,[&](std::uint8_t c){return c==*start;}))return;
    constexpr const char* defaults[]={"REIMU   ","MIMA    ","MARISA  ","ELEN    ","KOTOHIME","KANA    ","RIKAKO  ","CHIYURI ","YUMEMI  "};
    for(unsigned i=0;i<8;++i)start[7-i]=std::uint8_t(regi::ascii(defaults[character][i]));
}
bool NameEntry::tick(std::uint16_t input,ScoreSection& section,unsigned place) {
    if(done)return false;
    old_count=erase_count=0;bool redraw=first;first=false;
    constexpr unsigned directions[]={up,down,left,right};
    for(unsigned direction=0;direction<4;++direction) {
        auto& held=holds[direction];
        if(!(input&directions[direction])) {held=0;continue;}
        if(held==0||(held>=30&&held%4==0)) {
            if(direction>=2||letter!=regi::question) {
                old_letters[old_count++]=letter;
                if(direction==0)letter=(letter+32)%48;
                else if(direction==1)letter=(letter+16)%48;
                else if(direction==2)letter=letter%16==0 ? letter+14 : letter==30||letter==14 ? letter-2 : letter-1;
                else letter=letter%16==14 ? letter-14 : letter==12||letter==28 ? letter+2 : letter+1;
                redraw=true;
            }
        }
        held=std::int16_t(held==32767 ? -32768 : held+1);
    }
    const auto blank=[&] {
        erased[erase_count++]=cursor;
        if(cursor==255)snow_spill=45+place*8;
        else section.bytes[ScoreSection::names+place*8+cursor]=regi::space;
    };
    const auto back=[&] {blank();if(cursor<7)++cursor;};
    if(input&(ok|shot)) {
        if(!enter_locked) {
            if(letter==regi::backspace)back();
            else if(letter==regi::end)done=true;
            else {section.bytes[ScoreSection::names+place*8+cursor]=std::uint8_t(letter);if(!cursor)done=true;--cursor;}
            redraw=true;
        }
        enter_locked=true;
    } else enter_locked=false;
    if(input&bomb) {if(!back_locked) {back();redraw=true;}back_locked=true;}else back_locked=false;
    if(redraw)blank();
    return redraw;
}
ScoreFile::ScoreFile(Bytes original,std::filesystem::path directory):encoded_(std::move(original)) {
    if(directory.empty())return;
    path_=std::move(directory)/"YUME.NEM";
    if(std::filesystem::exists(path_)) {
        std::ifstream input(path_,std::ios::binary);if(!input)throw std::runtime_error("cannot read native YUME.NEM");
        encoded_=Bytes(std::istreambuf_iterator<char>(input),{});
        if(input.bad())throw std::runtime_error("native YUME.NEM read failed");
    }
}
ScoreSection ScoreFile::load(unsigned rank,std::uint32_t& seed,const Resident& resident,bool mainl) {
    ScoreSection section;
    if(encoded_.size()>=4*ScoreSection::size) {
        std::copy_n(encoded_.begin()+rank*ScoreSection::size,ScoreSection::size,section.bytes.begin());section.decode();
        if(section.valid())return section;
    }
    // The host treats a short external file as missing. MAINL's real recreate
    // path saves all four ranks and returns the last decoded default section.
    section.defaults();
    if(encoded_.size()<4*ScoreSection::size)encoded_.resize(4*ScoreSection::size);
    for(unsigned difficulty=0;difficulty<4;++difficulty)save(section,difficulty,seed,resident,mainl);
    return section;
}
void ScoreFile::save(ScoreSection& section,unsigned rank,std::uint32_t& seed,const Resident& resident,bool mainl) {
    if(encoded_.size()<4*ScoreSection::size)encoded_.resize(4*ScoreSection::size);
    const auto encrypted=section.encode(seed,resident,mainl);
    std::copy(encrypted.begin(),encrypted.end(),encoded_.begin()+rank*ScoreSection::size);commit();
}
void ScoreFile::commit() const {
    if(path_.empty())return;
    std::filesystem::create_directories(path_.parent_path());
    auto temporary=path_;temporary+=".tmp";
    std::ofstream output(temporary,std::ios::binary|std::ios::trunc);
    if(!output)throw std::runtime_error("cannot create native score temporary file");
    output.write(reinterpret_cast<const char*>(encoded_.data()),std::streamsize(encoded_.size()));output.flush();
    if(!output)throw std::runtime_error("cannot write native scores");
    output.close();
    if(!output)throw std::runtime_error("cannot close native score temporary file");
#ifdef _WIN32
    if(!MoveFileExW(temporary.c_str(),path_.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("cannot replace native YUME.NEM");
#else
    std::filesystem::rename(temporary,path_);
#endif
}
std::filesystem::path default_save_directory() {
#ifdef _WIN32
    if(const auto* root=std::getenv("LOCALAPPDATA"))if(*root)return std::filesystem::path(root)/"TH03";
    if(const auto* root=std::getenv("USERPROFILE"))if(*root)return std::filesystem::path(root)/"AppData"/"Local"/"TH03";
#else
    if(const auto* root=std::getenv("XDG_DATA_HOME"))if(*root&&std::filesystem::path(root).is_absolute())return std::filesystem::path(root)/"th03";
    if(const auto* root=std::getenv("HOME"))if(*root)return std::filesystem::path(root)/".local"/"share"/"th03";
#endif
    throw std::runtime_error("cannot determine native save directory; supply --save-dir");
}
}
