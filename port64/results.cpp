#include "results.hpp"
#include "round.hpp"
#include "raster.hpp"
#include <algorithm>

namespace th03 {
void Round::text_gaiji(unsigned x,unsigned y,unsigned code,unsigned attribute) {
    text_cells[y*80+x]={std::uint16_t(code),std::uint16_t(attribute),true,false};
    text_cells[y*80+x+1]={std::uint16_t(code),std::uint16_t(attribute),true,true};
}
void Round::text_japanese(unsigned x,unsigned y,std::string_view cp932,unsigned attribute) {
    for(unsigned i=0;i<cp932.size();i+=2,x+=2) {
        const auto code=std::uint16_t((unsigned(std::uint8_t(cp932[i]))<<8)|std::uint8_t(cp932[i+1]));
        text_cells[y*80+x]={code,std::uint16_t(attribute),false,false};
        text_cells[y*80+x+1]={code,std::uint16_t(attribute),false,true};
    }
}
void Round::text_clear(unsigned x,unsigned y,unsigned cells) {
    std::fill_n(text_cells.begin()+y*80+x,cells,TextCell{});
}
void MatchResult::update(Round& r,const Resident& resident) {
    pid=std::uint8_t(1-r.defeated_player);
    const unsigned x=4+pid*40;
    if(r.result_frame%8==1) {
        const bool clear_header=resident.stage>=8,lives_number=resident.stage==8;
        if(r.result_frame==1) {
            const auto& p=r.players[pid];counts={{p.combo_hits_max,p.gauge_attacks,p.boss_attacks,p.boss_reversals,p.boss_panics}};
            constexpr unsigned weights[]={1000,10000,15000,20000,30000};
            remaining=0;
            for(unsigned i=0;i<5;++i)remaining+=std::int32_t(counts[i])*weights[i];
            if(resident.stage==8) {lives=resident.lives;remaining+=std::int32_t(lives)*100000;r.extends_gained=255;}
            step=std::uint16_t(std::min<std::uint32_t>(std::uint32_t(remaining/192),65535));
            low=std::uint16_t(remaining%10000);high=std::uint16_t(remaining/10000);
        }
        // Original full-width CP932 result labels, in their TRAM draw order.
        constexpr const char* labels[]={
            "\x82\x6c\x82\x60\x82\x77\x81\x40\x82\x62\x82\x8f\x82\x8d\x82\x82\x82\x8f\x81\x40\x81\x40\x81\x40\x81\x7e",
            "\x83\x51\x81\x5b\x83\x57\x83\x41\x83\x5e\x83\x62\x83\x4e\x89\xf1\x90\x94\x81\x40\x81\x40\x81\x40\x81\x7e",
            "\x83\x7b\x83\x58\x83\x41\x83\x5e\x83\x62\x83\x4e\x89\xf1\x90\x94\x81\x40\x81\x40\x81\x40\x81\x40\x81\x7e",
            "\x83\x7b\x83\x58\x83\x8a\x83\x6f\x81\x5b\x83\x54\x83\x8b\x89\xf1\x90\x94\x81\x40\x81\x40\x81\x40\x81\x7e",
            "\x83\x7b\x83\x58\x83\x70\x83\x6a\x83\x62\x83\x4e\x89\xf1\x90\x94\x81\x40\x81\x40\x81\x40\x81\x40\x81\x7e",
            "\x81\x40\x81\x40\x81\x40\x82\x73\x82\x6e\x82\x73\x82\x60\x82\x6b\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40",
            "\x81\x40\x81\x40\x82\x76\x82\x68\x82\x6d\x82\x6d\x82\x64\x82\x71\x81\x40\x82\x61\x82\x6e\x82\x6d\x82\x74\x82\x72\x81\x40\x81\x40",
            "\x81\x40\x81\x40\x81\x40\x82\x60\x82\x6b\x82\x6b\x81\x40\x82\x62\x82\x6b\x82\x64\x82\x60\x82\x71\x81\x49\x81\x49\x81\x40\x81\x40",
            "\x8e\x63\x82\xe8\x90\x6c\x90\x94\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x81\x40\x81\x7e"
        };
        for(unsigned i=0;i<5;++i)r.text_japanese(x,8+i*2,labels[i]);
        r.text_japanese(x,20,labels[5]);r.text_japanese(x,6,labels[clear_header ? 7 : 6]);
        if(clear_header)r.text_japanese(x,18,labels[8]);
        const auto number=[&](unsigned row,unsigned value) {
            if(value>=100)r.text_gaiji(x+18,row,0xa0+value/100,0xe1);
            if(value>=10)r.text_gaiji(x+20,row,0xa0+(value%100)/10,0xe1);
            r.text_gaiji(x+22,row,0xa0+value%10,0xe1);
        };
        for(unsigned i=0;i<5;++i)number(8+i*2,counts[i]);
        if(lives_number)number(18,lives);
    }
    if(remaining>step) {r.score_add(pid,step);remaining-=step;}
    else if(remaining>0) {r.score_add(pid,std::uint16_t(remaining));remaining=0;}
}
void PlayfieldTransition::update(Canvas& graphics) {
    if(phase==Phase::none)return;
    const bool covering=phase==Phase::cover;
    if(!frame)vertices=covering ? std::array<Point,4>{{{303,382},{16,382},{16,16},{303,16}}}
                                  : std::array<Point,4>{{{303,16},{303,382},{16,382},{16,16}}};
    const auto triangle=[&](Point a,Point b,Point c,unsigned pattern) {
        const Clip clip=covering ? Clip{8,0,623,191} : Clip{16,0,623,191};
        if(pattern==2) {grcg_triangle(graphics,{{a,b,c}},2,clip);return;}
        Canvas mask;grcg_triangle(mask,{{a,b,c}},1,clip);
        // GRCG's 5555/AAAA WORD masks select odd/even physical columns.
        for(unsigned y=0;y<192;++y)for(unsigned x=unsigned(clip.left);x<=unsigned(clip.right);++x)
            if(mask.pixels[y*640+x]&&(x&1)==pattern)graphics.put(int(x),int(y),2);
    };
    if(covering) {
        vertices[0].x-=18;vertices[1].y-=23;vertices[2].x+=18;vertices[3].y+=23;
        for(int side=0;side<=320;side+=320) {
            triangle({std::int16_t(side+303),8},{std::int16_t(side+303),191},{std::int16_t(vertices[0].x+side),std::int16_t(vertices[0].y/2)},1);
            triangle({std::int16_t(side+16),8},{std::int16_t(side+16),191},{std::int16_t(vertices[2].x+side),std::int16_t(vertices[2].y/2)},1);
        }
        for(int side=0;side<=320;side+=320) {
            triangle({std::int16_t(side+16),191},{std::int16_t(side+303),191},{std::int16_t(vertices[1].x+side),std::int16_t(vertices[1].y/2)},0);
            triangle({std::int16_t(side+16),8},{std::int16_t(side+303),8},{std::int16_t(vertices[3].x+side),std::int16_t(vertices[3].y/2)},0);
        }
    } else {
        vertices[0].y+=23;vertices[1].x-=18;vertices[2].y-=23;vertices[3].x+=18;
        for(int side=0;side<=320;side+=320) {
            triangle({std::int16_t(side+16),191},{std::int16_t(side+303),191},{std::int16_t(vertices[0].x+side),std::int16_t(vertices[0].y/2)},2);
            triangle({std::int16_t(side+16),8},{std::int16_t(side+16),191},{std::int16_t(vertices[1].x+side),std::int16_t(vertices[1].y/2)},2);
            triangle({std::int16_t(side+16),8},{std::int16_t(side+303),8},{std::int16_t(vertices[2].x+side),std::int16_t(vertices[2].y/2)},2);
            triangle({std::int16_t(side+303),8},{std::int16_t(side+303),191},{std::int16_t(vertices[3].x+side),std::int16_t(vertices[3].y/2)},2);
        }
    }
    if(++frame>=16) {
        frame=0;
        if(covering) {
            graphics.fill(16,8,303,191,2);graphics.fill(336,8,623,191,2);
            midpoint=true;phase=Phase::uncover;
        } else phase=Phase::none;
    }
}
}
