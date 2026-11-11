#include "selection.hpp"
#include "motion.hpp"
#include <cstdio>
#include <stdexcept>

namespace th03 {
void Selection::begin(const Resident& resident,SelectKind mode,unsigned unlocked) {
    kind=mode;available=std::uint8_t(unlocked);confirmed={{false,mode==SelectKind::story}};
    selected={{mode==SelectKind::story ? std::uint8_t(0) : std::uint8_t(character_id(resident.paletted[0])),
               std::uint8_t(character_id(resident.paletted[1]))}};
    // Input locks and curve cycle are OP process statics, retained after cancel.
    fade=0;active_player=0;initial_wait=30;flash=vblank=0;tone=100;
    trail=display_trail=8;display_cycle=cycle;done=cancelled=false;first_iteration=true;
}
void Selection::update_player(Resident& resident,std::uint16_t input,unsigned pid) {
    if(confirmed.at(pid))return;
    if(locked[pid]) {if(!input)locked[pid]=false;return;}
    if(input&up) {
        selected[pid]=std::uint8_t(selected[pid]-1);
        if(selected[pid]>=128)selected[pid]=std::uint8_t(available-1);
        locked[pid]=true;
    }
    if(input&down) {
        selected[pid]=std::uint8_t(selected[pid]+1);
        const int signed_selected=selected[pid]<128 ? selected[pid] : int(selected[pid])-256;
        if(signed_selected>=available)selected[pid]=0;
        locked[pid]=true;
    }
    for(unsigned palette=0;palette<2;++palette) {
        const auto bit=palette==0 ? shot : bomb;
        if(!(input&bit))continue;
        resident.paletted[pid]=std::uint8_t(selected[pid]*2+1+palette);
        if(confirmed[1-pid]&&resident.paletted[0]==resident.paletted[1])
            resident.paletted[pid]=std::uint8_t(resident.paletted[pid]+(palette==0 ? 1 : -1));
        if(confirmed[1-pid])fade=0;
        confirmed[pid]=locked[pid]=true;
        flash=17;
    }
}
void Selection::tick(Resident& resident,const InputFrame& input) {
    if(done||cancelled)return;
    if(initial_wait) {--initial_wait;return;}
    if(flash) {--flash;return;}
    if(++vblank<3)return;
    vblank=0;
    display_cycle=cycle;display_trail=trail;cycle=std::uint8_t(cycle+2);
    if(kind==SelectKind::two_player) {
        update_player(resident,input.players[0],0);
        update_player(resident,input.players[1],1);
    } else update_player(resident,input.single,active_player);
    if(input.single&cancel) {cancelled=true;return;}
    if(kind==SelectKind::versus_cpu&&active_player==0&&confirmed[0]&&fade>12) {
        active_player=1;fade=0;return;
    }
    if(confirmed[0]&&confirmed[1]) {
        if(fade>=16)tone=200-int(fade)*6;
        if(fade>32) {done=true;return;}
    }
    if((first_iteration||flash)&&trail>1)--trail;
    first_iteration=false;
    ++fade;++resident.seed;
}
namespace {
void curve(Canvas& canvas,unsigned ox,unsigned oy,int radius,int fx,int fy,std::uint8_t color) {
    for(unsigned base=0;base<256;++base) {
        // Angle addition wraps to a byte; multiplication wraps to signed WORD
        // before division toward zero. Polar then multiplies in signed DWORD.
        const auto ax=std::uint8_t(motion::wrap(std::int32_t(std::uint8_t(base+ox))*fx)/256);
        const auto ay=std::uint8_t(motion::wrap(std::int32_t(std::uint8_t(base+oy))*fy)/256);
        const int x=320+motion::floor_shift8(radius*motion::sine(std::uint8_t(ax+64)));
        const int y=200+motion::floor_shift8(radius*motion::sine(ay));
        canvas.put(x,y,color);
    }
}
}
void selection_curves(Canvas& canvas,std::uint8_t cycle,int trails) {
    const int triangle=cycle<128 ? cycle : 256-cycle;
    const int other=256+triangle,fx=256+2*triangle,fy=2*other;
    const auto draw=[&](int offset,std::uint8_t color) {
        curve(canvas,unsigned(cycle-offset*2),unsigned(cycle*2-offset*4),220,other,fy,color);
        curve(canvas,unsigned(-int(cycle)+offset*2),unsigned((int(cycle)-offset*2)/2),120,fx,other,color);
    };
    draw(0,6);
    const int half=trails/2+(trails&1 ? 1 : 0);
    for(int i=1;i<=half;++i)draw(i,5);
    for(int i=half+1;i<=trails;++i)draw(i,1);
}
SelectionAssets::SelectionAssets(const PfArchive& archive):
    palette(read_palette(archive.read("TLSL.RGB"))),font(archive.read("MIKOFT.BFT")),
    question(archive.read("99SL.CDG")),stats(archive.read("SLWIN.CDG")),
    extra(archive.read("SLEX.CDG")),extras(archive.read("SLEX.CD2")),names(archive.read("CHNAME.BFT")) {
    for(unsigned c=0;c<9;++c) {
        char name[16];std::snprintf(name,sizeof(name),"%02uSL.CD2",c*2);
        portraits.emplace_back(archive.read(name));
    }
}
Frame SelectionAssets::render(const Resident& resident,const Selection& s) const {
    Canvas canvas;
    selection_curves(canvas,s.display_cycle,s.display_trail);
    const bool story=s.kind==SelectKind::story;
    for(unsigned pid=0;pid<(story ? 1u : 2u);++pid) {
        const int left=pid==0 ? 32 : 416;
        const auto character=s.selected[pid];
        const auto palette=s.confirmed[pid] ? (resident.paletted[pid]-1)&1u : 0u;
        portraits.at(character).put(canvas,palette,left,96,true,pid==1);
        stats.put(canvas,0,left,304,false);
        constexpr std::uint8_t values[9][3]={{3,1,5},{4,4,2},{3,4,3},{2,3,1},{4,1,4},{2,2,5},{4,5,1},{5,2,4},{5,5,3}};
        for(unsigned stat=0;stat<3;++stat) {
            int star=5,x=left+108;
            while(values[character][stat]<star) {
                canvas.fill(x,315+int(stat)*16,x+8,330+int(stat)*16,14);--star;x-=11;
            }
        }
        extra.put(canvas,0,left+128,304,false);
        extras.put(canvas,character,left+144,316,false);
    }
    if(story)question.put(canvas,0,416,96);
    for(unsigned c=0;c<s.available;++c) {
        names.put(canvas,c*2,256,136+int(c)*20);
        names.put(canvas,c*2+1,320,136+int(c)*20);
    }
    for(unsigned pid=0;pid<(story ? 1u : 2u);++pid) {
        if(pid==1&&s.kind==SelectKind::versus_cpu&&!s.confirmed[0])continue;
        const int left=240+int(pid)*128,top=128+int(s.selected[pid])*20;
        const auto color=std::uint8_t(s.confirmed[pid] ? 15 : pid==0 ? 8 : 10);
        for(unsigned row=0;row<2;++row)for(unsigned x=0;x<2;++x)
            gaiji(canvas,font,0x12+pid*4+row*2+x,left+int(x)*16,top+int(row)*16,color);
    }
    const int tone=s.flash ? 100+int(s.flash)*6 : s.tone;
    return canvas.frame(palette,tone);
}
}
