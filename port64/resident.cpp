#include "resident.hpp"
#include <stdexcept>

namespace th03 {
unsigned character_id(std::uint8_t paletted) {
    return unsigned((int(paletted)-1)/2);
}
void Resident::begin_story() {
    demo=winner=stage=0;cpu={{false,true}};mode=Mode::story;lives=2;
    show_scores=false;paletted[1]=255;
}
void Resident::begin_versus(unsigned choice) {
    if(choice>2)throw std::runtime_error("invalid versus mode");
    cpu={{choice==2,choice!=1}};demo=winner=stage=0;
    mode=Mode(0x80+choice);show_scores=false;
}
void Resident::choose_story_opponents() {
    constexpr std::uint8_t decisive[]={1,0,0,2,0,3,5,4,6};
    const auto selected=character_id(paletted[0]);
    if(selected>=9)throw std::runtime_error("invalid story character");
    std::array<bool,7> seen{};
    // OP's LCG is process-local. MAIN is subsequently seeded afresh from the
    // resident counter, not from the last opponent-selection random draw.
    auto process_seed=seed;
    for(unsigned stage=0;stage<6;++stage) {
        unsigned candidate;
        do {candidate=random_next(process_seed)%7;}while(seen[candidate]||candidate==decisive[selected]);
        seen[candidate]=true;
        opponents[stage]=std::uint8_t(candidate*2+1);
        if(opponents[stage]==paletted[0])++opponents[stage];
    }
    opponents[6]=std::uint8_t(decisive[selected]*2+1);
    opponents[7]=15;opponents[8]=17;
    if(paletted[0]==15)++opponents[7];
    if(paletted[0]==17)++opponents[8];
    paletted[1]=opponents[0];scores={};credits=3;fast_title=false;
    skill=std::uint8_t(70+options.rank*25);
}
void Resident::begin_demo() {
    constexpr std::uint8_t pairings[4][2]={{3,1},{5,13},{7,11},{9,5}};
    constexpr std::uint32_t seeds[]={600,1000,3200,500};
    cpu={{true,true}};demo=std::uint8_t(demo%4+1);winner=stage=0;mode=Mode::demo;show_scores=false;
    paletted={{pairings[demo-1][0],pairings[demo-1][1]}};seed=seeds[demo-1];scores={};
}
bool characters_unlocked(const Bytes& nem) {
    if(nem.size()!=4*206)return false;
    bool unlocked=false;
    for(unsigned rank=0;rank<4;++rank) {
        Bytes section(nem.begin()+rank*206,nem.begin()+(rank+1)*206);
        const auto key1=section[204],key2=section[205];
        for(unsigned at=0;at<203;++at) {
            const auto next=section[at+1];
            const auto feedback=std::uint8_t(((next>>3)|(next<<5))^key2);
            section[at]=std::uint8_t(section[at]+key1+feedback);
        }
        section[203]=std::uint8_t(section[203]+key1+key2);
        unsigned sum=0;
        for(unsigned at=2;at<206;++at)sum+=section[at];
        if((sum&65535)!=(section[0]|(unsigned(section[1])<<8)))return false;
        if(section[82]==99)unlocked=true;
    }
    return unlocked;
}
}
