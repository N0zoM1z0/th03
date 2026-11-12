#include "battle_graphics.hpp"
#include "score_font.hpp"
#include "motion.hpp"
#include "raster.hpp"
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
        std::snprintf(name,sizeof(name),"%02uBM.MRS",unsigned(resident.paletted[p])-1);
        bomb_images_.emplace_back(main.read(name),p!=0);
        std::snprintf(name,sizeof(name),"%02uEX.MRS",unsigned(resident.paletted[p])-1);
        portraits_.emplace_back(main.read(name),p!=0);
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
void BattleGraphics::sprite(Canvas& dest,int left,int top,unsigned offset,unsigned width,unsigned height,int clip_left,int clip_right,bool clipped,int monochrome,bool overlap_clear,std::uint16_t mask) const {
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
        const auto px=left+int(x),py=physical_top+int(y);
        const unsigned bit=7-(unsigned(px)&7)+((unsigned(px)&8) ? 8 : 0);
        if(color&&(mask&(1u<<bit))) {
            const auto under=px>=0&&px<640&&py>=0&&py<400 ? dest.pixels[unsigned(py)*640+unsigned(px)] : 0;
            dest.put(px,py,monochrome>=0 ? std::uint8_t(monochrome) : overlap_clear ? color : std::uint8_t(under|color));
        }
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
    for(unsigned pid=0;pid<2;++pid) {
        const auto& warning=round.warning_text[pid];if(!warning.visible)continue;
        const int x=pid ? 32 : 352;
        // Bit3 marks opaque black glyph ink when the TRAM attribute is1.
        const auto color=std::uint8_t(8|((warning.attribute>>5)&7));
        const auto put=[&](unsigned code,int left,int row,std::uint8_t ink) {gaiji(display,font_,code,left,row*16,ink);};
        for(unsigned row=0;row<3;++row)for(unsigned i=0;i<16;++i)put(0x50+row*16+i,x+int(i)*16,11+int(row),color);
        for(unsigned i=0;i<11;++i)put(130+i,x+32+int(i)*16,14,color);
        for(unsigned i=0;i<8;++i)put((warning.boss&&i<3 ? 208 : 199)+i,x+48+int(i)*16,15,color);
        put(warning.level+0x1f,x+184,15,15);
        constexpr unsigned peril[]={141,142,143,146,147,148,149,150,151,152,153,154,155,156};
        for(unsigned i=0;i<14;++i)put(peril[i],x+32+int(i)*16,16,color);
    }
}
void BattleGraphics::charges(Canvas& graphics,const Round& round,unsigned pid) const {
    const auto& charges=round.charge_shots;
    {
        const int left_clip=pid ? 320 : 0,right_clip=pid ? 639 : 319;
        const auto screen_x=[&](int x) {return 16+int(pid)*320+pixels(x)+round.fg_shift[pid];};
        switch(character_id(round.players[pid].paletted)) {
        case 0:
            for(const auto& shot:charges.reimu[pid])if(shot.state) {
                constexpr int colors[4]={2,5,6,-1};
                for(unsigned pass=0;pass<4;++pass) {
                    const auto at=shot.history[6-pass*2];
                    const unsigned so=0x1180+pid*40+((3-pass+round.result_frame)&3)*6;
                    sprite(graphics,screen_x(at.x)-24,pixels(at.y)-8,so,48,24,left_clip,right_clip,true,colors[pass]);
                }
            }
            break;
        case 1:
            if(charges.mima_active[pid])for(unsigned i=0;i<15;++i) {
                const auto& shot=charges.mima[pid][i];if(!shot.active)continue;
                sprite(graphics,screen_x(shot.center.x)-16,pixels(shot.center.y)+8,0x10+pid*40+(i%3)*4,32,8,left_clip,right_clip);
            }
            break;
        case 2: {
            const auto& shot=charges.marisa[pid];if(!shot.active)break;
            const auto box=[&](Point at,std::uint32_t tile) {
                const int x=screen_x(at.x),bottom=(at.y>=0 ? at.y/32 : -((-int(at.y)+31)/32))+8;
                for(int y=8;y<=bottom;++y)for(int px=x-2;px<=x+1;++px) {
                    const unsigned mask=0x80u>>(unsigned(px)&7);unsigned color=0;
                    for(unsigned plane=0;plane<4;++plane)if((tile>>(plane*8))&mask)color|=1u<<plane;
                    graphics.put(px,y,std::uint8_t(color));
                }
            };
            constexpr unsigned ends[3]={6,3,0},starts[3]={11,6,3};
            constexpr std::uint32_t tiles[3]={0xaa0055aa,0xff00aa55,0xff55ff55};
            for(unsigned band=0;band<3;++band) {
                int previous_x=0;
                for(unsigned i=starts[band];i>ends[band];--i) {
                    const auto at=shot.history[i];const auto x=screen_x(at.x);
                    if(previous_x!=x)box(at,tiles[band]);
                    previous_x=x;
                }
            }
            box(shot.history[0],0xffffffff);break;
        }
        case 3:
            for(const auto& shot:charges.ellen[pid])if(shot.state==1) {
                const auto cel=(std::uint8_t(shot.angle+16)>>5)*2;
                sprite(graphics,screen_x(shot.center.x)-8,pixels(shot.center.y)+8,0x10+pid*40+cel,16,8,left_clip,right_clip);
            }
            break;
        case 4: {
            const auto& shot=charges.kotohime[pid];if(shot.active)
                sprite(graphics,screen_x(shot.center.x)-48,pixels(shot.center.y)+8,0x1188+pid*40,96,16,left_clip,right_clip);
            break;
        }
        case 5:
            if(charges.kana_active[pid])for(const auto& shot:charges.kana[pid])for(int i=12,so=0x1180;i>=0;i-=4,so-=0x500) {
                const auto at=shot.history[unsigned(i)];
                sprite(graphics,screen_x(at.x)-16,pixels(at.y),unsigned(so)+pid*40,32,16,left_clip,right_clip,true,-1,false);
            }
            break;
        case 6:
            if(charges.rikako_active[pid])for(const auto& shot:charges.rikako[pid])
                sprite(graphics,screen_x(shot.center.x)-16,pixels(shot.center.y),0x280+pid*40,32,16,left_clip,right_clip);
            break;
        case 7:
            for(int i=7;i>=0;--i) {
                const auto& shot=charges.chiyuri[pid][unsigned(i)];if(!shot.age)break;if(shot.age!=1)continue;
                sprite(graphics,screen_x(shot.center.x)-16,pixels(shot.center.y)-8,0x280+pid*40+(shot.animation&1)*4,32,24,left_clip,right_clip);
            }
            break;
        case 8: {
            const auto& shot=charges.yumemi[pid];if(!shot.state)break;
            const unsigned frame=shot.frame,so=0xc80+pid*40+(frame&1)*4;
            if(shot.state==1) {sprite(graphics,screen_x(shot.center.x)-16,pixels(shot.center.y),so,32,16,left_clip,right_clip);break;}
            const auto ring=[&](int radius,unsigned phase) {
                for(unsigned i=0;i<16;++i) {
                    const auto angle=std::uint8_t(frame*2+i*16);
                    const auto x=motion::wrap(int(shot.center.x)-256+motion::polar(angle,std::int16_t(radius)).x);
                    const auto y=motion::wrap(int(shot.center.y)-256+motion::polar(std::uint8_t(angle+phase),std::int16_t(radius)).y);
                    sprite(graphics,screen_x(x),pixels(y)+16,so+0x500,32,16,left_clip,right_clip);
                }
            };
            if(frame<8)ring(int(frame)*128,0);
            else if(frame<16)ring((int(frame)-7)*128,32);
            else if(frame<24)ring((int(frame)-15)*128,224);
            else if(frame<32)ring((int(frame)-24)*128,0);
            else if(frame<40)ring((int(frame)-31)*128,32);
            else if(frame<48)ring((int(frame)-39)*128,224);
            else if(frame<64) {
                if(frame<56) {ring((int(frame)-47)*128,32);ring((int(frame)-47)*128,224);}
                ring((int(frame)-48)*128,0);
            }
            break;
        }
        }
    }
}
void BattleGraphics::extras(Canvas& graphics,const Round& round,unsigned pid) const {
    const auto character=character_id(round.players[pid].paletted),other=pid^1;
    constexpr unsigned counts[9]={8,6,14,12,10,8,14,16,16};
    const int clip_left=other ? 320 : 0,clip_right=other ? 639 : 319;
    const auto xy=[&](const Extra& e) {return Point{std::int16_t(16+e.pid*320+pixels(e.center.x)+round.fg_shift[e.pid]),std::int16_t(pixels(e.center.y)+16)};};
    const auto transition=[&](const Extra& e,unsigned appear_frame) {
        const auto p=xy(e);
        if(e.state==2) {
            const auto frame=character==1 ? std::uint8_t(e.duration) : e.frame;
            if(!(frame&1))sprite(graphics,p.x-16,p.y-16,0x1928+((frame&7)<=3 ? 4 : 0),32,16);
        } else sprite(graphics,p.x-24,p.y-24,0x1930+((appear_frame/4)%3)*6,48,24);
    };
    for(unsigned i=0;i<counts[character];i+=character==7 ? 2 : 1) {
        const auto& e=round.extra_attacks.items[pid][i];if(!e.state)continue;
        const auto p=xy(e);const int left=p.x,top=p.y;
        if(e.state!=1) {
            transition(e,character<=3 ? e.state : e.frame);
            if(character==7) {const auto& b=round.extra_attacks.items[pid][i+1];transition(b,b.frame);}
            continue;
        }
        switch(character) {
        case 0: {
            unsigned so=pid*40+0x280,phase=e.frame/4;
            if((phase&3)==1)so+=6;else if(phase&3)so+=0x780+(phase&1)*6;
            sprite(graphics,left-24,top-24,so,48,24,clip_left,clip_right);break;
        }
        case 1: {
            unsigned so=pid*40+0x280;
            if(!e.frame)so+=0x786;else if(e.frame==1)so+=0x780;else if(e.frame==2)so+=6;
            sprite(graphics,left-24,top-24,so,48,24,clip_left,clip_right);break;
        }
        case 2: {
            unsigned so=pid*40+0x1a;
            if(e.frame<48) {sprite(graphics,left-8,top-8,so,16,8,clip_left,clip_right);so+=2;}
            else if(e.frame<96)so+=2;else if(e.frame<102)so+=4;else if(e.frame<108)so+=6;else if(e.frame<114)so+=8;else so+=10;
            // SPF_DOWNWARDS_COLUMN repeats the tile through physical VRAM.
            for(int y=top+8;y<400;y+=16)sprite(graphics,left-8,y,so,16,8,clip_left,clip_right);
            break;
        }
        case 3: {
            unsigned so=pid*40+0x28c;
            for(int j=6;j>=0;j-=2) {
                const auto h=round.extra_attacks.ellen_history[pid][i][unsigned(j)];
                const int x=16+e.pid*320+pixels(h.x)+round.fg_shift[e.pid],y=pixels(h.y)+16;
                sprite(graphics,x-16,y-16,so,32,16,e.pid ? 320 : 0,e.pid ? 639 : 319);so-=4;
            }
            break;
        }
        case 4: {
            unsigned so=pid*40+0x280;
            if(motion::wrap(int(e.duration)-e.center.y)<=1536&&e.frame%4<2)so+=0xa00;
            if(!e.mode)sprite(graphics,left-16,top-16,so+0x282,32,16);
            else sprite(graphics,left-32,top-32,so,64,32);
            break;
        }
        case 5:sprite(graphics,left-16,top-16,pid*40+0x284+((e.frame/4)%4)*1280,32,16,clip_left,clip_right);break;
        case 6:sprite(graphics,left-24,top-24,pid*40+0x780+(e.frame&1)*0x780,48,24,clip_left,clip_right);break;
        case 7: {
            const auto b=xy(round.extra_attacks.items[pid][i+1]);const auto f=e.frame;
            const auto trapezoid=[&](int radius,unsigned color) {grcg_trapezoid(graphics,8,left-radius,left+radius,192,b.x-radius,b.x+radius,std::uint8_t(color),{});};
            if(f>=40&&f<112) {trapezoid(6,9);trapezoid(3,10);trapezoid(1,15);}
            else if(f<136) {
                if(f>=16) {const int radius=(f<40 ? int(f)-16 : 136-int(f))/4;trapezoid(radius,9);trapezoid(radius/2,10);}
                grcg_line(graphics,{std::int16_t(left),8},{b.x,192},15,{});
            }
            break;
        }
        case 8: {
            const Clip clip{other ? 336 : 16,8,other ? 623 : 303,191};
            const auto hline=[&](int x1,int x2,int y,unsigned color) {
                if(y>=clip.top&&y<=clip.bottom)graphics.fill(std::max(clip.left,std::min(x1,x2)),y,std::min(clip.right,std::max(x1,x2)),y,std::uint8_t(color));
            };
            const auto vline=[&](int x,int y1,int y2,unsigned color) {
                if(x>=clip.left&&x<=clip.right)graphics.fill(x,std::max(clip.top,std::min(y1,y2)),x,std::min(clip.bottom,std::max(y1,y2)),std::uint8_t(color));
            };
            const auto outline=[&](int l,int r,int t,int b,unsigned color) {hline(l,r,t,color);hline(l,r,b,color);vline(l,t,b,color);vline(r,t,b,color);};
            const int mid=top/2;
            if(e.frame<=16) {
                const int extent=e.frame,half=extent/2;
                outline(left+extent-32,left+32-extent,mid+half-40,mid+52-half,6);
                outline(left+extent-80,left+80-extent,mid+half-16,mid+16-half,6);
            } else {
                const auto raw=std::uint8_t(e.duration-8-e.frame);const int extent=raw<128 ? raw : int(raw)-256,half=extent/2,color=extent>16 ? 5 : 6;
                outline(left+extent-16,left+16-extent,mid+half-32,mid+44-half,color);
                outline(left+extent-64,left+64-extent,mid+half-8,mid+8-half,color);
            }
            const int l=left-16;const unsigned so=pid*40+0x280;
            sprite(graphics,l,top-e.radius,so,32,8,clip_left,clip_right);
            for(int y=top-e.radius+16;y<top-16;y+=16)sprite(graphics,l,y,so+0x502,32,8,clip_left,clip_right);
            const int bottom=e.radius/2+e.radius+top-16;
            sprite(graphics,l,bottom,so+0x280,32,8,clip_left,clip_right);
            for(int y=bottom-16;y>top;y-=16)sprite(graphics,l,y,so+0x502,32,8,clip_left,clip_right);
            const int t=top-16,first=l-e.radius+16,last=e.radius+l;
            sprite(graphics,first,t,so,16,16,clip_left,clip_right);
            for(int x=first+16;x<l;x+=16)sprite(graphics,x,t,so+0x500,16,16,clip_left,clip_right);
            sprite(graphics,last,t,so+2,16,16,clip_left,clip_right);
            for(int x=last-16;x>l+16;x-=16)sprite(graphics,x,t,so+0x500,16,16,clip_left,clip_right);
            if(e.radius>24)sprite(graphics,l,t,so+4,32,16,clip_left,clip_right);
            break;
        }
        }
    }
}
void BattleGraphics::boss(Canvas& graphics,const Round& round,unsigned pid) const {
    if(round.boss_launched_by!=pid)return;
    const auto character=character_id(round.players[pid].paletted);
    const auto& b=round.bosses;const auto& state=b.state;const unsigned other=pid^1;
    const int lclip=other ? 320 : 0,rclip=other ? 639 : 319;
    const auto orbit=[&](Point center,unsigned angle,int radius) {
        const auto v=motion::polar(std::uint8_t(angle),motion::wrap(radius));
        return Point{motion::wrap(int(center.x)+v.x),motion::wrap(int(center.y)+v.y)};
    };
    const auto put=[&](Point center,unsigned so,unsigned width,unsigned height,int ymargin) {
        sprite(graphics,16+other*320+pixels(center.x)+round.fg_shift[other]-int(width)/2,pixels(center.y)-ymargin,so,width,height,lclip,rclip);
    };
    if(state.mode==255) {
        const int length=motion::wrap(int(b.frame)*8),x=16+other*320+pixels(state.center.x)+round.fg_shift[other],y=16+pixels(state.center.y);
        for(unsigned i=0;i<16;++i) {const auto p=orbit({std::int16_t(x),std::int16_t(y)},length+i*16,length);sprite(graphics,p.x-24,p.y-24,0x1930,48,24,lclip,rclip);}
        for(unsigned i=0;i<8;++i) {const auto p=orbit({std::int16_t(x),std::int16_t(y)},-length+i*32,length*2);sprite(graphics,p.x-24,p.y-24,0x1930,48,24,lclip,rclip);}
        return;
    }
    if(character==1) {
        const int left=16+other*320+pixels(state.center.x)+round.fg_shift[other]-72,top=pixels(state.center.y)-40;
        const auto draw=[&](int x,int y,unsigned so,unsigned w,unsigned h,std::uint16_t mask=0xffff) {sprite(graphics,x,y,so,w,h,lclip,rclip,true,-1,true,mask);};
        if(!state.mode) {
            const int distance=200-int(b.frame)*2;const auto p=orbit({std::int16_t(left),std::int16_t(top)},b.frame*3,distance);
            draw(p.x,p.y,state.sprite,144,56,0xaaaa);
            const auto q=orbit({std::int16_t(left),std::int16_t(top)},b.frame*3+128,distance);draw(q.x,q.y,state.sprite,144,56,0x5555);return;
        }
        draw(left,top,state.sprite,144,56);
        if(state.hit) {draw(left+32,top+16,state.sprite+0x12,64,40);return;}
        if(state.render_mode==2||state.render_mode==5) {
            const unsigned frame=state.render_mode==5 ? 0 : state.render_frame;
            draw(left+48,top+32,state.sprite+0x1a,16,8);draw(left+80,top,state.sprite+0xef4+(frame>=16 ? 4 : 0),32,16);
        } else if(state.render_mode==3)draw(left+32,top+16,state.sprite+0xc92,80,24);
        else if(state.render_mode==4)draw(left+48,top+32,state.sprite+0x1a,16,8);
        return;
    }
    if(character==2) {
        const int left=16+other*320+pixels(state.center.x)+round.fg_shift[other]-88,top=pixels(state.center.y)-32;
        const auto draw=[&](int x,int y,unsigned so,unsigned w,unsigned h,std::uint16_t mask=0xffff) {sprite(graphics,x,y,so,w,h,lclip,rclip,true,-1,true,mask);};
        if(!state.mode) {const int offset=200-int(b.frame)*2;draw(left-offset,top,state.sprite,176,48,0xaaaa);draw(left+offset,top,state.sprite,176,48,0x5555);return;}
        draw(left,top,state.sprite,176,48);
        if(state.hit) {draw(left+64,top+16,state.sprite+0x16,48,40);return;}
        if(state.render_mode==1) {
            if((round.result_frame&3)<2) {draw(left+64,top+16,state.sprite+0x1c,48,40);draw(left+32,top+48,state.sprite+0xf00,112,8);}
            else draw(left+32,top+48,state.sprite+0x1180,112,8);
        }
        return;
    }
    if(character==3) {
        constexpr int y_offsets[9]={108,96,80,64,48,32,16,8,4},heights[9]={2,8,16,16,16,16,16,8,2};
        const int x=16+other*320+pixels(state.center.x)+round.fg_shift[other],y=pixels(state.center.y);
        const auto strips=[&](unsigned frame) {
            for(unsigned j=0;j<3;++j) {
                const auto i=(frame+9-j)%9;
                const auto so=std::uint16_t(y_offsets[i]*40+state.sprite-1264);
                sprite(graphics,x-48,y+y_offsets[i]-40,so,96,unsigned(heights[i]/2),lclip,rclip);
            }
        };
        if(!state.mode) {
            strips(std::uint8_t(b.frame)%9);
            if(round.frame%2&&b.frame<64)return;
            auto angle=std::uint8_t(b.frame*3);unsigned so=pid*40+0x28c;
            for(unsigned i=0;i<4;++i,so-=4) {
                for(unsigned j=0;j<8;++j,angle=std::uint8_t(angle+32))put(orbit(state.center,angle,(200-int(b.frame)*2)*16),so,32,16,0);
                angle=std::uint8_t(angle+3);
            }
            return;
        }
        sprite(graphics,x-32,y-32,state.sprite+(state.hit ? 8 : 0),64,48,lclip,rclip);
        strips((state.render_frame/4)%9);return;
    }
    if(character==4) {
        const auto ring=[&](unsigned count,unsigned phase,int radius,unsigned mode) {
            const unsigned so=pid*40+0x502+(mode==2&&b.frame%4<2 ? 0xa00 : 0);
            for(unsigned i=0;i<count;++i)put(orbit(state.center,std::uint8_t(i*256/count+phase),radius),so,32,16,0);
        };
        if(!state.mode) {
            if(round.frame%2&&b.frame<64)return;
            ring(8,std::uint8_t(state.move_phase+2),(200-int(b.frame)*2)*16,1);return;
        }
        put(state.center,state.sprite+(state.hit ? 16 : 0),128,48,32);
        if(state.render_mode)ring(b.parameters[1],state.move_phase,motion::wrap(state.effect_radius),state.render_mode);
        return;
    }
    if(character==5) {
        if(!state.mode) {
            if(b.frame<32&&round.frame%2)return;
            const unsigned so=pid*40+0x284+((b.frame>>2)&3)*1280;
            for(unsigned i=0;i<16;++i)put(orbit(state.center,std::uint8_t(-state.move_phase+i*16),3200-int(b.frame)*32),so,32,16,0);
            return;
        }
        const int left=16+other*320+pixels(state.center.x)+round.fg_shift[other]-64,top=pixels(state.center.y)-24;
        sprite(graphics,left,top,state.sprite+(state.hit ? 16 : 0),128,40,lclip,rclip);
        if(state.render_mode==1)sprite(graphics,left+32,top,state.sprite+0xc80,64,32,lclip,rclip);
        else if(state.render_mode==2)sprite(graphics,left+32,top,state.sprite+0xc80+(state.render_frame>=24 ? 24 : state.render_frame>=16 ? 16 : state.render_frame>=8 ? 8 : 0),64,32,lclip,rclip);
        return;
    }
    if(character==6) {
        if(!state.mode) {
            if(b.frame<64&&(round.result_frame&1))return;
            const unsigned so=pid*40+0x780+(b.frame&1)*0x780;
            for(unsigned i=0;i<16;++i)put(orbit(state.center,std::uint8_t(-b.frame*4+i*16),3200-int(b.frame)*32),so,48,24,8);
            return;
        }
        put(state.center,state.sprite+(state.hit ? 12 : 0),96,48,32);
        const Point center{std::int16_t(16+other*320+pixels(state.center.x)+round.fg_shift[other]-8),std::int16_t(pixels(state.center.y)+8)};
        for(unsigned i=0;i<8;++i) {
            const auto p=orbit(center,state.render_frame+i*32,48);
            sprite(graphics,p.x,p.y,pid*40+(i%4 ? 0x167e + (i%4)*2 : 0x284),16,8,lclip,rclip);
        }
        return;
    }
    if(character==7) {
        if(!state.mode) {
            if(round.frame%2&&b.frame<64)return;
            const int radius=(b.frame<32 ? 256 : b.frame<64 ? 512 : 768)-int(b.frame)*8;
            const auto phase=std::uint8_t(state.move_phase+(b.frame>=32&&b.frame<64 ? -4 : 4));
            for(unsigned i=0;i<16;++i)put(orbit(state.center,std::uint8_t(phase+i*16),radius*16),state.sprite+0x790+state.render_frame*4,32,16,0);
            return;
        }
        const int left=16+other*320+pixels(state.center.x)+round.fg_shift[other]-64,top=pixels(state.center.y)-48;
        if(state.render_mode) {
            const unsigned f=state.render_mode,color=f>=24 ? 6 : f>=20 ? 5 : f>=12 ? 2 : f>=8 ? 5 : f>=4 ? 6 : 15;
            sprite(graphics,left,top,state.sprite,128,64,lclip,rclip,true,int(color));return;
        }
        sprite(graphics,left,top,state.sprite,128,64,lclip,rclip);
        if(state.hit)sprite(graphics,left+48,top+32,state.sprite+0x778,48,40,lclip,rclip);
        else if(state.render_frame)sprite(graphics,left+48,top+32,state.sprite+0xc+4*state.render_frame,32,24,lclip,rclip);
        return;
    }
    if(character==8) {
        const int top=pixels(state.center.y)-40;
        const auto screen=[&](int x) {return 16+int(other)*320+pixels(x)+round.fg_shift[other];};
        if(!state.mode) {
            const auto draw=[&](int x) {sprite(graphics,x,top,state.sprite,112,56,lclip,rclip,true,-1,false);};
            const int frame=b.frame;
            if(frame<24)for(int x=screen(-1664),end=screen(frame*128-1664);x<=end;x+=8)draw(x);
            else if(frame<48)for(int x=screen((frame-24)*128-1664),end=screen(1408);x<=end;x+=8)draw(x);
            else if(frame<72) {for(int x=screen(4352),end=screen(4352-(frame-48)*128);x>=end;x-=8)draw(x);draw(screen(1408));}
            else if(frame<96)for(int x=screen(4352-(frame-72)*128),end=screen(1408);x>=end;x-=8)draw(x);
            return;
        }
        const int left=screen(state.center.x)-56;
        sprite(graphics,left,top,state.sprite,112,56,lclip,rclip);
        if(state.render_mode)sprite(graphics,left+32,top,state.sprite + 0xe + (state.render_mode==2 ? 0xa00 : 0),64,32,lclip,rclip);
        else if(state.hit)sprite(graphics,left+16,top,state.sprite+0x16,80,48,lclip,rclip);
        if(state.effect_radius||state.render_frame) {
            const Clip clip{other ? 336 : 16,8,other ? 623 : 303,191};
            // The original uses SAR5, including negative odd physical rows.
            const auto physical=[](int q4) {return q4>=0 ? q4/32 : -((-q4+31)/32);};
            const Point origin{std::int16_t(screen(b.yumemi_origin.x)),std::int16_t(8+physical(b.yumemi_origin.y))};
            if(!state.render_frame)grcg_circle(graphics,origin,state.effect_radius,10,clip);
            else grcg_line(graphics,origin,{std::int16_t(screen(state.scratch.x)),std::int16_t(8+physical(state.scratch.y))},10,clip);
        }
        return;
    }
    if(character!=0)throw std::runtime_error("unimplemented Boss renderer");
    unsigned animation=std::uint8_t(b.frame/4),offset=0;
    if((animation&3)==1)offset=6;else if(animation&3)offset=0x780+(animation&1)*6;
    if(!state.mode) {
        if(round.frame%2&&b.frame<64)return;
        for(unsigned i=0;i<8;++i)put(orbit(state.center,std::uint8_t(b.frame+i*32),3200-b.frame*32),pid*40+0x280+offset,48,24,8);
        return;
    }
    put(state.center,state.sprite+(state.hit ? 12 : 0),96,48,32);
    if(state.render_mode==1)for(unsigned i=0;i<b.parameters[3];++i)put(b.reimu_orbit[i],std::uint16_t(state.sprite-12+offset),48,24,8);
}
void BattleGraphics::background(Canvas& graphics,const Round& round) const {
    const auto& bg=round.background;if(!bg.chain)return;
    for(unsigned i=0;i<24;++i) {
        const auto p=bg.particles[i].center;
        // The original pixel helper writes a rotated WORD through a raw
        // VRAM byte offset. Keep the row/byte carry of that two-dot mask.
        const int x=pixels(p.x);
        const int byte=x>=0 ? x/8 : -((-x+7)/8);
        const unsigned rotate=unsigned(x)&7;
        const auto mask=std::uint16_t(rotate ? (0xc0u>>rotate)|(0xc0u<<(16-rotate)) : 0xc0);
        const auto doubled=std::uint16_t((std::uint16_t(p.y)&0xffe0u)<<1);
        const auto address=std::uint16_t(byte+doubled+(doubled>>2));
        for(unsigned part=0;part<2;++part)for(unsigned bit=0;bit<8;++bit)if((mask>>(part*8))&(0x80u>>bit)) {
            const unsigned at=std::uint16_t(address+part)*8+bit;
            if(at<640*200)graphics.put(int(at%640),int(at/640),bg.chain==1 ? 10 : 13);
        }
    }
    const unsigned count=bg.chain==1 ? 48 : 50,height=bg.chain==1 ? 3 : 8;
    for(unsigned i=24;i<count;++i) {
        const auto& p=bg.particles[i];
        const unsigned delta=bg.chain==2&&bg.draw_periodic&&i>=40 ? ((bg.phase_frame&31)>>3)*2 : 0;
        sprite(graphics,pixels(p.center.x),pixels(p.center.y),p.sprite+delta,16,height,0,639,!bg.draw_periodic&&bg.chain==1);
    }
}
void BattleGraphics::bombs(Canvas& graphics,const Round& round) const {
    const auto& bombs=round.bombs;
    for(unsigned pid=0;pid<2;++pid)if(round.bomb_flags[pid]) {
        const unsigned character=character_id(round.players[pid].paletted),frame=bombs.frame[pid];
        const int left=int(pid)*320+16;
        const Clip clip{left,8,left+287,191};
        const auto x=[&](int q4) {return left+pixels(q4)+round.fg_shift[pid];};
        if(character==1 ? frame<=80 : character!=5&&character!=8&&frame<64)
            graphics.fill(left,8,left+287,191,std::uint8_t(pid));
        bool portrait=false;int portrait_left=left;
        switch(character) {
        case 0:
            portrait=frame>=64&&frame<=96;
            if(frame<96)for(const auto& p:bombs.reimu[pid])if(p.active)
                sprite(graphics,x(p.center.x)-8,pixels(p.center.y)+8,pid*40+0x18,16,8);
            break;
        case 1:
            portrait=frame>80&&frame<144;portrait_left+=round.fg_shift[pid];
            if(frame<=80)for(const auto& p:bombs.mima[pid]) {
                if(!p.sprite)break;
                for(int y=16;y<400;y+=16)sprite(graphics,x(p.x),y,p.sprite,16,8);
            }
            break;
        case 2:portrait=frame>=64&&frame<128;portrait_left=(frame&3)<2 ? left : left-8;break;
        case 3:case 4:case 5:case 6:portrait=frame>=64&&frame<128;break;
        case 7:portrait=frame>=64&&frame<144;break;
        case 8:
            portrait=frame>64&&frame<144;
            if(frame<=64) {
                constexpr std::uint8_t angles[6]={192,21,107,64,235,149};
                const auto triangle=[&](unsigned start,int radius,std::uint8_t color) {
                    std::array<Point,3> points{};
                    for(unsigned i=0;i<3;++i) {
                        const auto v=motion::polar(angles[start+i],std::int16_t(radius));
                        points[i]={std::int16_t(144+v.x+left),std::int16_t((200+v.y)/2)};
                    }
                    grcg_triangle(graphics,points,color,clip);
                };
                triangle(0,frame<32 ? 224-int(frame)*3 : 128,frame<32 ? 8 : 7);
                if(frame>32)triangle(3,320-int(frame)*3,8);
            }
            break;
        }
        if(portrait)bomb_images_[pid].put(graphics,portrait_left,16,false,pid!=0);
        if(character==2&&portrait) {
            const auto at=bombs.marisa_draw_point[pid];
            sprite(graphics,at.x-24,at.y-24,pid*40+0xf16+((frame&3)<2 ? 6 : 0),48,24);
        } else if(character==3&&portrait) {
            for(const auto& p:bombs.ellen[pid])if(p.center.x!=19999&&p.center.x!=9999)
                sprite(graphics,left+pixels(p.center.x)-32,pixels(p.center.y)-16,pid*40+0x29c,64,32,pid ? 320 : 0,pid ? 639 : 319);
        } else if(character==6&&portrait) {
            const int offset=bombs.rikako_draw_offset[pid];
            for(int factor:{-1,1,-2,2})graphics.fill(x(2304+offset*factor),8,x(2304+offset*factor),192,15);
        }
    }
}
void BattleGraphics::effects(Canvas& graphics,const Round& round) const {
    for(const auto& effect:round.effects)if(effect.kind) {
        const Clip clip=effect.center.x<320 ? Clip{16,8,303,191} : Clip{336,8,623,191};
        if(effect.kind==1) {
            const int y=effect.center.y>=0 ? effect.center.y/2 : -((-int(effect.center.y)+1)/2);
            grcg_circle(graphics,{effect.center.x,std::int16_t(y)},effect.radius,13,clip);
        } else {
            std::array<Point,4> points{};
            for(unsigned i=0;i<4;++i) {
                const auto v=motion::polar(std::uint8_t(effect.angle+i*64),effect.radius);
                points[i]={std::int16_t(effect.center.x+v.x),std::int16_t((effect.center.y+v.y)/2)};
            }
            for(unsigned i=0;i<4;++i)grcg_line(graphics,points[i],points[(i+1)%4],13,clip);
        }
    }
}
Frame BattleGraphics::render(const Round& round,const Resident& resident) const {
    Canvas graphics;
    graphics.fill(16,8,303,191,0);graphics.fill(336,8,623,191,1);
    background(graphics,round);
    bombs(graphics,round);
    for(unsigned pid=0;pid<2;++pid)boss(graphics,round,pid);
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
    for(unsigned pid=0;pid<2;++pid) {extras(graphics,round,pid);charges(graphics,round,pid);}
    for(unsigned pid=0;pid<2;++pid) {
        const auto& p=round.players[pid];
        if(p.lose_time) {
            if(p.lose_time!=255)for(unsigned ring=0;ring<3;++ring)for(unsigned i=0;i<16;++i) {
                const auto angle=std::uint8_t((ring==1 ? -round.lose_radius/4 : round.lose_radius/4)+int(i)*16);
                const auto phase=ring==0 ? 32 : ring==1 ? -32 : 0;
                const auto x=motion::polar(angle,round.lose_radius).x;
                const auto y=motion::polar(std::uint8_t(angle+phase),round.lose_radius).y;
                sprite(graphics,round.lose_left+x+round.fg_shift[pid],round.lose_top+y,0x34b4,48,24,pid ? 320 : 0,pid ? 639 : 319);
            }
            continue;
        }
        const int left=16+int(pid)*320+pixels(p.center.x)+round.fg_shift[pid]-16,top=pixels(p.center.y)-16;
        if(p.pattern_glow)pattern(graphics,p.pattern_glow+pid*9+p.pattern_movement*3,left,top/2);
        else sprite(graphics,left,top,0x2844+p.pattern_movement*4+pid*0xa00,32,32);
        if(p.gauge_charged>=0x100) {
            const unsigned base=p.gauge_charged<0x400 ? 44 : p.gauge_charged<0x800 ? 48 : p.gauge_charged<0xff0 ? 52 : 56;
            pattern(graphics,base+((round.result_frame>>2)&3),left,p.center.y/32-15);
        }
    }
    effects(graphics,round);
    bullets(graphics,round);
    if(round.defeat==2) {
        const auto loser=round.defeated_player;const auto winner=loser^1;
        const int frame=round.result_frame%32,top=frame<16 ? frame+32 : 64-frame;
        pattern(graphics,18,loser*320+96,40);pattern(graphics,19,loser*320+160,40);
        pattern(graphics,20,winner*320+96,top);pattern(graphics,21,winner*320+160,top);
    }
    // Gauge highlight strip resides in ENEMYxx's final eight atlas rows.
    for(unsigned pid=0;pid<2;++pid)for(unsigned y=0;y<8;++y)for(unsigned x=0;x<288;++x)
        graphics.put(16+int(pid)*320+int(x),192+int(y),atlas_.pixels[(192+y)*640+320+x]);
    for(unsigned pid=0;pid<2;++pid) {
        const auto& p=round.players[pid];
        if(p.hyper_active&&(round.result_frame&1)) {
            const auto level=p.gauge_avail>>10;
            graphics.fill(16+int(pid)*320,192,303+int(pid)*320,199,level==1 ? 8 : level==2 ? 12 : 6);
        }
        const unsigned charged=p.gauge_charged>>4,available=p.gauge_avail>>4;
        const auto bar=[&](unsigned x,unsigned width,unsigned color) {
            if(!width)return;
            // B3F6 rounds X down to a WORD and extends width by its low
            // four bits; it does not mask away pixels before the supplied X.
            width+=x&15;x&=~15u;
            graphics.fill(int(x),194,int(x+width-1),197,std::uint8_t(color));
        };
        if(available>charged)bar(pid*320+charged+32,available-charged,p.hyper_active&&!(round.result_frame&1) ? 15 : 9);
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
    for(unsigned pid=0;pid<2;++pid)if(round.warning_portrait[pid])portraits_[pid].put(graphics,16+int(pid)*320,16,true);
    intro(graphics,round,resident);
    Canvas display;
    for(unsigned y=0;y<400;++y)std::copy_n(graphics.pixels.begin()+(y/2)*640,640,display.pixels.begin()+y*640);
    auto frame=display.frame(round.palette_initialized ? round.palette : palette_,round.palette_tone);
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
