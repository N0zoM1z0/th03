#include "assets.hpp"
#include "menu.hpp"
#include "selection.hpp"
#include "round.hpp"
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
int main(int argc,char** argv) {
    try {
        if(argc==9&&std::string(argv[1])=="--round") {
            th03::Round round;th03::Resident resident;
            round.formations=th03::read_formations(read_file(argv[2]));
            round.random.seed=std::uint32_t(std::stoul(argv[3]));
            resident.options.rank=std::uint8_t(std::stoul(argv[4]));resident.mode=th03::Mode(std::stoul(argv[5]));
            round.id=std::uint8_t(std::stoul(argv[6]));resident.credits=std::uint8_t(std::stoul(argv[7]));
            resident.stage=std::uint8_t(std::stoul(argv[8]));resident.paletted={{5,13}};resident.cpu={{false,true}};
            round.gauge_levels={{3,5}};round.players[0].cpu_safety=777;round.players[1].cpu_safety=888;
            round.prepare(resident,0x5e);
            std::cout<<round.formations.size()<<' '<<round.random.seed<<' '<<unsigned(round.speed)<<' '
                     <<unsigned(round.bullet_base_speed)<<' '<<unsigned(round.boss_level)<<' '
                     <<unsigned(round.gauge_levels[0])<<' '<<unsigned(round.gauge_levels[1])<<' '
                     <<round.players[0].cpu_safety<<' '<<round.players[1].cpu_safety<<'\n';
            const auto row=[&](const auto& values) {for(auto value:values)std::cout<<unsigned(value)<<' ';std::cout<<'\n';};
            row(round.random.bytes);row(round.formation_types);row(round.formation_positions);
            for(const auto& p:round.players) {
                std::cout<<p.center.x<<' '<<p.center.y<<' '<<unsigned(p.invincibility)<<' '<<int(p.halfhearts)<<' '
                         <<unsigned(p.paletted)<<' '<<p.cpu<<' '<<unsigned(p.shot_mode)<<' '<<p.gauge_charged<<' '
                         <<unsigned(p.shot_active)<<' '<<unsigned(p.hit_damage_next)<<' '<<unsigned(p.charge_cursor)<<' '
                         <<unsigned(p.bombs)<<' '<<unsigned(p.lose_time)<<' '<<unsigned(p.hyper_active)<<' '<<p.cpu_frame<<'\n';
                row(p.charge_thresholds);
            }
            return 0;
        }
        if(argc>1&&std::string(argv[1])=="--curves") {
            th03::Canvas canvas;
            th03::selection_curves(canvas,std::uint8_t(std::stoul(argv[2])),std::stoi(argv[3]));
            std::cout.write(reinterpret_cast<const char*>(canvas.pixels.data()),canvas.pixels.size());
            return 0;
        }
        if(argc>1&&std::string(argv[1])=="--opponents") {
            th03::Resident resident;
            resident.seed=std::uint32_t(std::stoul(argv[2]));resident.paletted[0]=std::uint8_t(std::stoul(argv[3]));
            resident.options.rank=std::uint8_t(std::stoul(argv[4]));resident.choose_story_opponents();
            for(auto value:resident.opponents)std::cout<<unsigned(value)<<' ';
            std::cout<<resident.seed<<' '<<unsigned(resident.skill)<<'\n';
            return 0;
        }
        if(argc>1&&std::string(argv[1])=="--selection") {
            unsigned pid,input,available,s0,s1,c0,c1,l0,l1,p0,p1,fade;
            while(std::cin>>pid>>input>>available>>s0>>s1>>c0>>c1>>l0>>l1>>p0>>p1>>fade) {
                th03::Resident resident;th03::Selection s;
                resident.paletted={{std::uint8_t(p0),std::uint8_t(p1)}};
                s.available=std::uint8_t(available);s.selected={{std::uint8_t(s0),std::uint8_t(s1)}};
                s.confirmed={{bool(c0),bool(c1)}};s.locked={{bool(l0),bool(l1)}};s.fade=std::uint16_t(fade);
                s.update_player(resident,std::uint16_t(input),pid);
                std::cout<<unsigned(s.selected[0])<<' '<<unsigned(s.selected[1])<<' '
                         <<s.confirmed[0]<<' '<<s.confirmed[1]<<' '<<s.locked[0]<<' '<<s.locked[1]<<' '
                         <<unsigned(resident.paletted[0])<<' '<<unsigned(resident.paletted[1])<<' '<<s.fade<<'\n';
            }
            return 0;
        }
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
        th03::Menu vs;vs.screen=th03::Screen::versus;vs.input_allowed=true;
        vs.tick(th03::cancel);check(vs.screen==th03::Screen::versus,"original VS ignores Escape");
        th03::Resident resident;resident.begin_story();
        th03::Selection select;select.begin(resident,th03::SelectKind::story,7);
        select.update_player(resident,th03::up,0);check(select.selected[0]==6,"selection upward wrap");
        select.update_player(resident,th03::shot,0);check(!select.confirmed[0],"selection held input lock");
        select.update_player(resident,0,0);select.update_player(resident,th03::bomb,0);
        check(select.confirmed[0]&&resident.paletted[0]==14,"alternate character palette");
        select.begin(resident,th03::SelectKind::story,7);check(select.locked[0],"selection lock survives cancel/reentry");
        Bytes cdg(56);put16(cdg,0,8);put16(cdg,2,32);put16(cdg,4,2);
        cdg[16]=0x80;cdg[24]=0x80;cdg[28]=0x80;
        th03::Cdg picture(cdg);th03::Canvas canvas;canvas.fill(0,0,639,399,2);
        picture.put(canvas,0,0,0);
        check(canvas.pixels[0]==3&&canvas.pixels[640]==1,"CDG bottom-up clear/OR");
        picture.put(canvas,0,0,0,true,true);check(canvas.pixels[640+31]==1,"CDG horizontal flip");
        picture.put(canvas,0,0,0,false);check(canvas.pixels[0]==1,"CDG no-alpha overwrite");
        cdg.pop_back();rejects([&]{th03::Cdg invalid(cdg);});
        th03::RandomRing random;random.bytes[255]=0x73;random.bytes[0]=0xab;random.cursor=255;
        check(random.ring()==0x73&&random.cursor==0,"ring WORD aliases incremented cursor");
        random.cursor=254;random.fill();check(random.cursor==254,"ring refill retains cursor");
        th03::Player player;player.center={144<<4,336<<4};player.speeds={{64,64,48,48,28}};
        check(player.move(th03::left)&&player.center.x==(140<<4),"player aligned Q4 movement");
        check(player.move(th03::left|th03::right)&&player.center.x==(144<<4),"last human direction resolves overlap");
        check(player.move(th03::up_right)&&player.center.x==2352&&player.center.y==5328,"player diagonal Q4 movement");
        player.center={8<<4,24<<4};player.move(th03::up_left);
        check(player.center.x==128&&player.center.y==384,"player clamps to original field");
        th03::Round shots;shots.players[0].center={144<<4,336<<4};shots.add_shots(0);
        check(shots.shots[0].alive&&shots.shots[0].top_left.x==(128<<4)&&!shots.shots[1].alive,"single shot pair allocation");
        shots.update_shots();check(shots.shots[0].top_left.y==(324<<4),"shot Q4 velocity");
        shots.shots[0].top_left.y=0;shots.update_shots();check(!shots.shots[0].alive,"shot top-edge removal");
        std::cout<<"PF, PI, menu release/ordering/options and 32-bit RNG checks passed\n";
        return 0;
    } catch (const std::exception& error) { std::cerr<<error.what()<<'\n'; return 1; }
}
