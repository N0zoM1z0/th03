#include "battle_graphics.hpp"
#include "score_font.hpp"
#include "motion.hpp"
#include <algorithm>
#include <cstdio>
#include <stdexcept>

namespace th03 {
namespace {
int pixels(int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);}
void interlace(Canvas& dest,const PiImage& image,int left,int top) {
    for(unsigned y=0;y<image.height;y+=2)for(unsigned x=0;x<image.width;++x) {
        const auto packed=image.pixels.at((std::size_t(y)*image.width+x)/2);
        dest.put(left+int(x),top+int(y/2),std::uint8_t((x&1) ? packed&15 : packed>>4));
    }
}
constexpr unsigned enemy_sprites[4]={104*80+48/8,112*80+96/8,104*80+272/8,128*80+192/8};
constexpr unsigned explosion_sprites[4][4]={
    {128*80+256/8,128*80+288/8,144*80+256/8,144*80+288/8},
    {104*80+320/8,128*80+320/8,152*80+320/8,168*80+368/8},
    {104*80+368/8,136*80+368/8,104*80+432/8,136*80+432/8},
    {160*80,160*80+80/8,160*80+160/8,160*80+240/8}
};
}
BattleGraphics::BattleGraphics(const PfArchive& op,const PfArchive& main,const Resident& resident):font_(main.read("GAMEFT.BFT")) {
    char name[16];
    for(unsigned p=0;p<2;++p) {
        std::snprintf(name,sizeof(name),"%02u16.PI",unsigned(resident.paletted[p])-1);
        interlace(atlas_,decode_pi(op.read(name)),p*320,0);
        std::snprintf(name,sizeof(name),"%02uEX.PI",unsigned(resident.paletted[p])-1);
        interlace(atlas_,decode_pi(op.read(name)),p*320,8);
        std::snprintf(name,sizeof(name),"%02uCH.BF2",unsigned(resident.paletted[p])-1);
        patterns_.emplace_back(main.read(name));
    }
    interlace(atlas_,decode_pi(op.read("EN2.PI")),0,80);
    constexpr unsigned enemy_image[9]={0,0,1,2,1,2,0,3,4};
    std::snprintf(name,sizeof(name),"ENEMY%02u.PI",enemy_image[character_id(resident.paletted[1])]);
    const auto enemy=decode_pi(op.read(name));palette_=enemy.palette;
    interlace(atlas_,enemy,0,104);
    // The six normal poses are copied from super.lib's pattern list into
    // the SPRITE16 atlas at stage_prepare_shot_sprites' original positions.
    for(unsigned p=0;p<2;++p)for(unsigned pose=0;pose<3;++pose)
        patterns_[p].put(atlas_,pose*3,544+pose*32,128+p*32);
    patterns_.emplace_back(main.read("LOSE.BF2"));
    patterns_.emplace_back(main.read("ROUND.BF2"));
    patterns_.emplace_back(main.read("ZIKICW.BF2"));
}
void BattleGraphics::sprite(Canvas& dest,int left,int top,unsigned offset,unsigned width,unsigned height,int clip_left,int clip_right,bool clipped,int monochrome) const {
    // The TH03 wrapper clips whole 16-pixel columns before invoking
    // SPRITE16. The latter reads physical 200-line rows; color0 is alpha.
    int right=left+int(width);
    if(clipped&&right>=clip_right) {
        if(left>=clip_right)return;
        do {right-=16;width-=16;if(!width)return;}while(right>=clip_right);
    } else if(clipped&&left<clip_left) {
        if(right<clip_left)return;
        do {left+=16;width-=16;offset+=2;if(!width)return;}while(left<clip_left);
    }
    const int physical_top=top>=0 ? top/2 : -((-top+1)/2);
    for(unsigned y=0;y<height;++y)for(unsigned x=0;x<width;++x) {
        const auto address=(std::size_t(offset)+y*80)*8+x;
        if(address>=640*200)throw std::runtime_error("sprite source outside original atlas");
        const auto color=atlas_.pixels[address];
        if(color)dest.put(left+int(x),physical_top+int(y),monochrome<0 ? color : std::uint8_t(monochrome));
    }
}
void BattleGraphics::pattern(Canvas& dest,unsigned index,int left,int top) const {
    for(const auto& bank:patterns_) {
        if(index<bank.count) {bank.put(dest,index,left,top);return;}
        index-=bank.count;
    }
    throw std::runtime_error("super.lib pattern outside original bank");
}
std::uint8_t BattleGraphics::pattern_pixel(unsigned index,unsigned x,unsigned y) const {
    for(const auto& bank:patterns_) {
        if(index<bank.count)return bank.pixel(index,x,y);
        index-=bank.count;
    }
    throw std::runtime_error("intro pattern outside original bank");
}
void BattleGraphics::intro(Canvas& graphics,const Round& round,const Resident& resident) const {
    const auto& intro=round.intro;
    if(intro.flag!=2)return;
    if(intro.phase==0) {
        const auto strip=[&](int left,int top,unsigned pattern,unsigned row) {
            // The original four-byte strip tests X once per byte before
            // shifting its red-plane mask into physical VRAM.
            for(unsigned column=0;column<4;++column,left+=8) {
                if(left>=624)break;
                if(left<0)continue;
                for(unsigned bit=0;bit<8;++bit)
                    if(pattern_pixel(pattern,column*8+bit,row)&2)graphics.put(left+int(bit),top,15);
            }
        };
        for(unsigned i=0;i<16;++i) {
            const auto& p=intro.particles[i];
            for(unsigned part=0;part<4;++part) {
                strip(p.center.x+int(part)*32,p.center.y,intro.sprite+part,i);
                strip(544-p.center.x-int(part)*32,p.center.y,intro.sprite+3-part,i);
            }
        }
    } else if(intro.phase==1) {
        if(intro.frame>=24&&intro.frame<(resident.mode==Mode::story ? 56 : 64)) {
            const auto number=34+(resident.mode==Mode::story ? resident.stage : round.id);
            pattern(graphics,number,208,84);pattern(graphics,number,544,84);
        }
        for(unsigned side=0;side<2;++side)for(unsigned part=0;part<4;++part)
            pattern(graphics,intro.sprite+part,intro.x+int(side)*320+int(part)*32,84);
    } else if(intro.phase==3) {
        for(const auto& p:intro.particles)if(p.active) {
            // DS helper maps Q4 to an even physical row and writes two dots.
            const auto x=unsigned(std::uint16_t(p.center.x))>>4,y=unsigned(std::uint16_t(p.center.y))>>5;
            graphics.put(int(x),int(y),15);graphics.put(int(x+1),int(y),15);
        }
    }
}
void BattleGraphics::bullets(Canvas& graphics,const Round& round) const {
    const auto position=[&](Point point,unsigned pid,int half) {
        return std::pair<int,int>{16+int(pid)*320+pixels(point.x)+round.fg_shift[pid]-half,16+pixels(point.y)-half};
    };
    for(const auto& b:round.bullets.items)if(b.flag==2) {
        unsigned so=b.sprite;
        if(b.has_trail) {
            const auto& trail=round.bullets.trails[b.trail];so+=6;
            for(int i=5;i>0;i-=2,so-=2) {
                const auto at=position({trail.x[unsigned(i)],trail.y[unsigned(i)]},b.pid,8);
                sprite(graphics,at.first,at.second,so,16,8,0,639,false);
            }
        }
        if(b.animated)so+=(b.age%4)*2;
        const auto at=position(b.center,b.pid,8);
        sprite(graphics,at.first,at.second,so,16,8,0,639,false);
    }
    for(const auto& b:round.bullets.items)if(b.flag==4) {
        const auto at=position(b.center,b.pid,16);
        sprite(graphics,at.first,at.second,b.sprite,32,16,0,639,true,15);
    }
    for(const auto& b:round.bullets.items)if(b.flag&1) {
        const int left=16+b.pid*320+pixels(b.center.x)+round.fg_shift[b.pid]-4;
        const int top=(pixels(b.center.y)>=0 ? pixels(b.center.y)/2 : -((-pixels(b.center.y)+1)/2))+6;
        pellet(graphics,left,top,b.flag==1 ? 0 : 1);
    }
}
void BattleGraphics::hud(Canvas& display,const Round& round,const Resident& resident) const {
    // TRAM glyphs keep sixteen display rows even while graphics is doubled.
    for(unsigned pid=0;pid<2;++pid) {
        const int left=16+int(pid)*320;
        const auto& p=round.players[pid];
        for(int i=0;i<10;i+=2)gaiji(display,font_,p.halfhearts-i>=2 ? 5 : p.halfhearts-i==1 ? 6 : 4,left+104+i*8,16,15);
        for(unsigned i=0;i<p.bombs;++i)gaiji(display,font_,7,pid ? left+int(i)*16 : left+272-int(i)*16,368,15);
        for(unsigned i=0;i<p.rounds_won;++i)gaiji(display,font_,9,left+int(i)*16,16,15);
        gaiji(display,font_,0x20-1+round.gauge_levels[pid],left,384,4);
        gaiji(display,font_,0x20+std::min<unsigned>(round.boss_level,15),left+272,384,2);

    }
    if(resident.mode==Mode::story)for(unsigned i=0;i<resident.lives;++i)gaiji(display,font_,2,288-int(i)*16,32,15);
}
Frame BattleGraphics::render(const Round& round,const Resident& resident) const {
    Canvas graphics;
    graphics.fill(16,8,303,191,0);graphics.fill(336,8,623,191,1);
    for(const auto& shot:round.shots)if(shot.alive) {
        const int left=16+shot.pid*320+pixels(shot.top_left.x)+round.fg_shift[shot.pid],top=16+pixels(shot.top_left.y);
        sprite(graphics,left,top,shot.animation+shot.pid*40,16,8);
        sprite(graphics,left+16,top,shot.animation+shot.pid*40,16,8);
    }
    for(const auto& enemy:round.enemies)if(enemy.flag&&enemy.flag!=3) {
        if(enemy.size_words<1||enemy.size_words>4)throw std::runtime_error("enemy sprite size outside atlas");
        unsigned offset=enemy_sprites[enemy.size_words-1]-enemy.hp*enemy.size_words*2,size=enemy.size_pixels;
        if(enemy.flag>=9) {
            const auto cel=enemy.frame<10 ? 0 : enemy.frame<32 ? 1+((enemy.frame/4)&1) : 3;
            offset=explosion_sprites[enemy.size_words-1][cel];size+=16;
        }
        const int left=16+enemy.pid*320+pixels(enemy.center.x)+round.fg_shift[enemy.pid]-int(size/2),top=16+pixels(enemy.center.y)-int(size/2);
        sprite(graphics,left,top,offset,size,size/2,enemy.pid ? 320 : 0,enemy.pid ? 639 : 319);
    }
    for(const auto& f:round.fireballs)if(f.flag) {
        unsigned offset,size;
        if(f.flag>=9) {
            const auto cel=f.frame<12 ? 0 : f.frame<32 ? 1+((f.frame/4)&1) : 3;
            offset=explosion_sprites[2][cel];size=64;
        } else if(f.flag==1) {offset=80*80-16+f.size_words*8+((f.frame&7)<=3 ? 4 : 0);size=32;}
        else {offset=96*80-8+f.size_words*4+((f.frame&7)<=3 ? 2 : 0);size=16;}
        const int left=16+f.pid*320+pixels(f.center.x)+round.fg_shift[f.pid]-int(size/2);
        const int top=16+pixels(f.center.y)-(f.flag>=9 ? 24 : int(size/2));
        sprite(graphics,left,top,offset,size,size/2);
    }
    for(unsigned i=0;i<round.circles.size();++i) {
        const auto& c=round.circles[i];if(!c.age)continue;
        const unsigned so=80*80+16+((c.age-1)/4)*6;
        sprite(graphics,c.left,c.top,so,48,24,c.pid ? 320 : 0,c.pid ? 639 : 319,true,i==12 ? 15 : 11+(round.result_frame&1));
    }
    for(unsigned pid=0;pid<2;++pid) {
        const auto& p=round.players[pid];
        if(p.lose_time)continue;
        const int left=16+int(pid)*320+pixels(p.center.x)+round.fg_shift[pid]-16,top=pixels(p.center.y)-16;
        if(p.pattern_glow)pattern(graphics,p.pattern_glow+pid*9+p.pattern_movement*3,left,top/2);
        else sprite(graphics,left,top,0x2844+p.pattern_movement*4+pid*0xa00,32,32);
        if(p.gauge_charged>=0x100) {
            const unsigned base=p.gauge_charged<0x400 ? 44 : p.gauge_charged<0x800 ? 48 : p.gauge_charged<0xff0 ? 52 : 56;
            pattern(graphics,base+((round.result_frame>>2)&3),left,p.center.y/32-15);
        }
    }
    bullets(graphics,round);
    // Gauge highlight strip resides in ENEMYxx's final eight atlas rows.
    for(unsigned pid=0;pid<2;++pid)for(unsigned y=0;y<8;++y)for(unsigned x=0;x<288;++x)
        graphics.put(16+int(pid)*320+int(x),192+int(y),atlas_.pixels[(192+y)*640+320+x]);
    for(unsigned pid=0;pid<2;++pid) {
        const auto& p=round.players[pid];
        const unsigned charged=p.gauge_charged>>4,available=p.gauge_avail>>4;
        const auto bar=[&](unsigned x,unsigned width,unsigned color) {
            if(!width)return;
            // B3F6 rounds X down to a WORD and extends width by its low
            // four bits; it does not mask away pixels before the supplied X.
            width+=x&15;x&=~15u;
            graphics.fill(int(x),194,int(x+width-1),197,std::uint8_t(color));
        };
        if(available>charged)bar(pid*320+charged+32,available-charged,9);
        if(charged)bar(pid*320+32,charged,charged<64 ? 15 : charged<128 ? 10 : charged<192 ? 8 : charged<255 ? 6 : 12);
    }
    // Graphics HUD: seven visible font rows, eight BCD digits followed by
    // an implicit zero for P2 and the spent-credit digit for P1.
    for(unsigned pid=0;pid<2;++pid) {
        const int origin=224+int(pid)*320;
        const auto digit_put=[&](unsigned digit,int left) {
            for(unsigned y=1;y<8;++y)for(unsigned x=0;x<8;++x)
                if(score_font[digit][y]&(0x80u>>x))graphics.put(left+int(x),8+int(y),15);
        };
        bool leading=true;
        for(int i=7;i>=0;--i) {
            const auto digit=round.scores[pid][unsigned(i)];
            if(digit)leading=false;
            if(!leading)digit_put(digit,origin+(7-i)*8);
        }
        digit_put(pid||resident.mode!=Mode::story ? 0 : 3-resident.credits,origin+64);
    }
    intro(graphics,round,resident);
    Canvas display;
    for(unsigned y=0;y<400;++y)std::copy_n(graphics.pixels.begin()+(y/2)*640,640,display.pixels.begin()+y*640);
    auto frame=display.frame(palette_);
    // hud_wipe leaves opaque reversed-black TRAM cells around the two
    // white playfield rectangles. Their color is independent of Palettes[0].
    for(unsigned y=0;y<400;++y)for(unsigned x=0;x<640;++x)
        if(y<16||x<16||(x>=304&&x<336)||x>=624)frame[y*640+x]=0xff000000;
    Canvas text;
    hud(text,round,resident);
    for(unsigned at=0;at<text.pixels.size();++at)if(const auto color=text.pixels[at])
        frame[at]=0xff000000u|((color&2) ? 0xff0000 : 0)|((color&4) ? 0xff00 : 0)|((color&1) ? 0xff : 0);
    return frame;
}
}
