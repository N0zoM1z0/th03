#include "assets.hpp"
#include "menu.hpp"
#include "selection.hpp"
#include "round.hpp"
#include "collision.hpp"
#include "battle_graphics.hpp"
#include "raster.hpp"
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
void attack_pools(const th03::Round& r,const th03::CollisionMap& collision) {
    for(auto f:r.gauge_flags)std::cout<<unsigned(f)<<' ';
    std::cout<<unsigned(r.random.cursor)<<' '<<unsigned(r.bullets.trail_cursor)<<' '<<unsigned(r.effect_cursor)<<' ';
    for(const auto& frames:r.gauges.frame)for(auto f:frames)std::cout<<unsigned(f)<<' ';
    for(const auto& centers:r.gauges.center)for(auto p:centers)std::cout<<p.x<<' '<<p.y<<' ';
    for(auto a:r.gauges.mima_angle)std::cout<<unsigned(a)<<' ';
    for(auto a:r.gauges.mima_step)std::cout<<unsigned(a)<<' ';
    for(const auto& time:r.gauges.timing)for(auto b:time)std::cout<<unsigned(b)<<' ';
    for(auto b:r.palette)std::cout<<unsigned(b)<<' ';
    const auto& t=r.bullets.model;
    std::cout<<t.center.x<<' '<<t.center.y<<' '<<unsigned(t.speed)<<' '<<unsigned(t.angle)<<' '<<unsigned(t.pid)<<' '
        <<unsigned(t.group)<<' '<<unsigned(t.acceleration)<<' '<<unsigned(t.count)<<' '<<t.velocity.x<<' '<<t.velocity.y<<' '
        <<t.sprite<<' '<<unsigned(t.type)<<' '<<t.collidable<<' '<<t.animated<<' '<<t.has_trail<<' '<<unsigned(r.bullets.group_angle)<<' ';
    for(const auto& b:r.bullets.items)std::cout<<unsigned(b.flag)<<' '<<unsigned(b.age)<<' '<<b.center.x<<' '<<b.center.y<<' '
        <<b.target_x<<' '<<b.target_x_origin<<' '<<b.velocity.x<<' '<<b.velocity.y<<' '<<unsigned(b.speed_next)<<' '
        <<unsigned(b.angle_next)<<' '<<unsigned(b.pid)<<' '<<unsigned(b.group_next)<<' '<<b.sprite<<' '<<unsigned(b.acceleration)<<' '
        <<b.collidable<<' '<<b.animated<<' '<<b.has_trail<<' '<<unsigned(b.has_trail ? b.trail : 0)<<' ';
    for(const auto& pool:r.extra_attacks.items)for(const auto& e:pool)std::cout<<unsigned(e.state)<<' '<<unsigned(e.frame)<<' '
        <<e.center.x<<' '<<e.center.y<<' '<<e.velocity.x<<' '<<e.velocity.y<<' '<<e.target_x<<' '<<e.boundary_x<<' '
        <<e.duration<<' '<<unsigned(e.pid)<<' '<<unsigned(e.mode)<<' '<<unsigned(e.angle)<<' '<<unsigned(e.speed)<<' '<<e.radius<<' ';
    for(const auto& e:r.effects)std::cout<<unsigned(e.kind)<<' '<<unsigned(e.age)<<' '<<e.center.x<<' '<<e.center.y<<' '
        <<unsigned(e.radius)<<' '<<int(e.radius_delta)<<' '<<unsigned(e.angle)<<' ';
    std::cout<<r.one_hit<<' '<<unsigned(r.circle_cursor)<<' ';
    for(const auto& c:r.circles)std::cout<<unsigned(c.age)<<' '<<unsigned(c.pid)<<' '<<c.left<<' '<<c.top<<' ';
    for(const auto& shot:r.shots)std::cout<<shot.alive<<' ';
    for(auto b:collision.bytes)std::cout<<unsigned(b)<<' ';
    std::cout<<r.sounds.size()<<' ';for(auto sound:r.sounds)std::cout<<unsigned(sound)<<' ';
    std::cout<<'\n';
}
}
int main(int argc,char** argv) {
    try {
        if((argc==7&&std::string(argv[1])=="--gauge")||(argc==5&&std::string(argv[1])=="--koto-extra")) {
            const bool extra=std::string(argv[1])=="--koto-extra";
            const auto character=extra ? 4u : unsigned(std::stoul(argv[2])),pid=unsigned(std::stoul(argv[extra ? 2 : 3]));
            const auto ticks=unsigned(std::stoul(argv[extra ? 3 : 6]));
            if(character>8||pid>1)throw std::runtime_error("unknown attack fixture");
            th03::Round r;th03::CollisionMap collision;r.speed=64;r.bullet_base_speed=8;r.fg_shift={{3,-4}};
            r.players[0].center={3600,4800};r.players[1].center={800,5200};
            r.players[0].paletted=r.players[1].paletted=std::uint8_t(character*2+1);
            r.random.cursor=254;for(unsigned i=0;i<256;++i)r.random.bytes[i]=std::uint8_t(i*13+7);
            th03::Palette palette{};for(unsigned i=0;i<48;++i)palette[i]=std::uint8_t(i*5+7);r.set_palette(palette);
            r.bullets.model.acceleration=128;
            if(extra) {
                r.gauges.timing[pid]={{6,1,2,0}};
                if(std::stoi(argv[4]))r.extra_attacks.kotohime_gauge(r,{2048,0},pid);
                else r.extra_attacks.add_kotohime(r,r.players[pid].center,pid);
                const auto& e=r.extra_attacks.items[pid][std::stoi(argv[4]) ? 8 : 0];
                r.shots[0].alive=true;r.shots[0].pid=std::uint8_t(pid^1);r.shots[0].top_left={std::int16_t(e.target_x-256),1920};
            } else {r.gauge_flags[pid]=std::uint8_t(std::stoi(argv[4])==1 ? 1 : 3);r.gauge_levels[pid]=std::uint8_t(std::stoul(argv[5]));}
            for(unsigned tick=0;tick<ticks;++tick) {
                r.result_frame=std::uint16_t(tick);collision.clear();r.bullets.model.reset();
                if(extra)r.extra_attacks.update_kotohime(r,pid,collision,[&](const th03::Hitbox& box){return r.charge_shots.hit(r,box);});
                else r.gauges.update(r,pid);
                r.update_effects();r.prepare_effects_render();
            }
            attack_pools(r,collision);return 0;
        }
        if(argc==7&&std::string(argv[1])=="--background") {
            const auto chain=unsigned(std::stoul(argv[2])),accel=unsigned(std::stoul(argv[3])),first=unsigned(std::stoul(argv[4])),count=unsigned(std::stoul(argv[5]));
            if(chain<1||chain>2)throw std::runtime_error("unknown background chain");
            th03::Round round;round.random.seed=0x12345678;round.background.begin(round.random,chain==1 ? 0 : 2);
            for(unsigned f=0;f<accel;++f)round.background.update(round.random,f,std::uint16_t(f));
            if(std::stoi(argv[6]))round.background.reset_velocity();
            for(unsigned i=0;i<count;++i)round.background.update(round.random,first+i,std::uint16_t(first+i));
            const auto& bg=round.background;
            std::cout<<round.random.seed<<' '<<unsigned(bg.angle)<<' '<<bg.periodic<<' '<<bg.draw_periodic<<' '<<bg.phase_frame<<' ';
            for(const auto& p:bg.particles)std::cout<<p.center.x<<' '<<p.center.y<<' '<<p.velocity.x<<' '<<p.velocity.y<<' '
                <<unsigned(p.speed)<<' '<<p.sprite<<' '<<p.auxiliary<<' ';
            std::cout<<'\n';return 0;
        }
        if(argc==3&&std::string(argv[1])=="--cpu") {
            const unsigned fixture=unsigned(std::stoul(argv[2]));if(fixture>7)throw std::runtime_error("unknown CPU fixture");
            const auto pid=fixture&1;th03::Round round;th03::Resident resident;th03::CollisionMap collision;
            auto& p=round.players[pid];p.center={2304,5376};p.cpu_frame=1;p.cpu_safety=fixture==0||fixture==4||fixture==5 ? 0 : 1000;
            p.bombs=2;p.gauge_charged=fixture==3||fixture==5 ? 2048 : 0;p.cpu_dodge_strategy=fixture==7;
            round.movement_speed={{64,64,48,48}};round.result_frame=4;
            for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            if(fixture==1||fixture==7)collision.bytes[pid*3312+9*184+144]=0x80;
            if(fixture>=2&&fixture<=5)std::fill_n(collision.bytes.begin()+pid*3312,3312,0xff);
            if(fixture==6) {round.boss_active[pid]=1;round.boss_target={3000,2000};}
            round.cpu_update(pid,collision,resident);
            std::cout<<p.center.x<<' '<<p.center.y<<' '<<p.is_hit<<' '<<round.player_velocity.x<<' '<<round.player_velocity.y<<' '
                <<unsigned(p.cpu_dodge_strategy)<<' '<<round.collision_top.x<<' '<<round.collision_top.y<<' '
                <<(round.cpu_pattern ? 0x67e +(round.cpu_pattern-1)*18 : 0)<<' '<<round.target.x<<' '<<round.target.y<<' '
                <<unsigned(round.target_formation_marker)<<' '<<unsigned(round.random.cursor)<<' '<<unsigned(round.bomb_flags[pid])<<' '
                <<unsigned(p.bombs)<<' '<<unsigned(p.invincibility)<<' '<<unsigned(p.hyper_active)<<' '<<unsigned(round.damage_all[pid])<<' '
                <<unsigned(resident.skill)<<'\n';return 0;
        }
        if(argc==8&&std::string(argv[1])=="--mrs") {
            th03::Canvas canvas;
            for(unsigned i=0;i<640*200;++i) {
                const unsigned shift=7-(i&7);
                canvas.pixels[i]=std::uint8_t(((0xaa>>shift)&1)|(((0x33>>shift)&1)<<1)|(((0x55>>shift)&1)<<2)|8);
            }
            th03::Mrs image(read_file(argv[2]),std::stoi(argv[7]));image.put(canvas,std::stoi(argv[3]),std::stoi(argv[4]),std::stoi(argv[5]),std::stoi(argv[6]));
            std::cout.write(reinterpret_cast<const char*>(canvas.pixels.data()),640*200);return 0;
        }
        if(argc==6&&std::string(argv[1])=="--bomb-run") {
            const auto character=unsigned(std::stoul(argv[2])),pid=unsigned(std::stoul(argv[3])),ticks=unsigned(std::stoul(argv[4]));
            const auto stack=std::uint8_t(std::stoul(argv[5]));
            if(character>8||pid>1)throw std::runtime_error("unknown Bomb fixture");
            th03::Round round;round.players[pid].paletted=std::uint8_t(character*2+1);round.bomb_flags[pid]=1;
            th03::Palette palette{};for(unsigned i=0;i<48;++i)palette[i]=std::uint8_t(i*5+7);round.set_palette(palette);
            round.random.cursor=254;for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            for(unsigned tick=0;tick<ticks;++tick) {
                round.bombs.update(round,pid);round.update_effects();round.bombs.prepare_render(round,pid,stack);round.prepare_effects_render();
            }
            std::cout<<unsigned(round.bomb_flags[pid])<<' '<<unsigned(round.bombs.frame[pid])<<' '<<round.fg_shift[pid]<<' '
                <<round.palette_tone<<' '<<unsigned(round.random.cursor)<<' '<<unsigned(round.effect_cursor)<<' ';
            for(auto c:round.palette)std::cout<<unsigned(c)<<' ';
            for(const auto& p:round.bombs.reimu[pid])std::cout<<unsigned(p.active)<<' '<<p.center.x<<' '<<p.center.y<<' '<<p.velocity_y<<' ';
            for(const auto& p:round.bombs.mima[pid])std::cout<<p.x<<' '<<p.sprite<<' ';
            for(const auto& p:round.bombs.ellen[pid])std::cout<<p.center.x<<' '<<p.center.y<<' '<<p.velocity.x<<' '<<p.velocity.y<<' ';
            std::cout<<round.bombs.ellen_spawn_count<<' '<<round.bombs.kotohime_y<<' '<<unsigned(round.bombs.kana_angle)<<' '
                <<round.bombs.rikako_line_offset<<' '<<round.bombs.marisa_point.x<<' '<<round.bombs.marisa_point.y<<' ';
            for(const auto& e:round.effects)std::cout<<unsigned(e.kind)<<' '<<unsigned(e.age)<<' '<<e.center.x<<' '<<e.center.y<<' '
                <<unsigned(e.radius)<<' '<<int(e.radius_delta)<<' '<<unsigned(e.angle)<<' ';
            std::cout<<round.sounds.size()<<' ';for(auto sound:round.sounds)std::cout<<unsigned(sound)<<' ';
            std::cout<<'\n';return 0;
        }
        if(argc>=3&&std::string(argv[1])=="--raster") {
            th03::Canvas canvas;const std::string kind=argv[2];const th03::Clip clip{16,8,303,191};
            const auto number=[&](int i) {return std::int16_t(std::stoi(argv[i]));};
            if(kind=="circle"&&argc==6)th03::grcg_circle(canvas,{number(3),number(4)},unsigned(std::stoul(argv[5])),13,clip);
            else if(kind=="line"&&argc==7)th03::grcg_line(canvas,{number(3),number(4)},{number(5),number(6)},13,clip);
            else if(kind=="triangle"&&argc==9)th03::grcg_triangle(canvas,{{{number(3),number(4)},{number(5),number(6)},{number(7),number(8)}}},13,clip);
            else throw std::runtime_error("invalid raster fixture");
            std::cout.write(reinterpret_cast<const char*>(canvas.pixels.data()),640*200);return 0;
        }
        if(argc==6&&(std::string(argv[1])=="--charge-picture"||std::string(argv[1])=="--loss-picture"||std::string(argv[1])=="--bomb-picture"||std::string(argv[1])=="--background-picture"||std::string(argv[1])=="--gauge-picture"||std::string(argv[1])=="--extra-picture")) {
            const auto disk=read_file(argv[2]);
            const PfArchive op(hdi_file(disk,op_archive_name)),main(hdi_file(disk,main_archive_name));
            const auto character=unsigned(std::stoul(argv[3])),ticks=unsigned(std::stoul(argv[4]));
            if(character>8)throw std::runtime_error("unknown charge picture character");
            th03::Resident resident;resident.mode=th03::Mode::story;
            resident.paletted={{std::uint8_t(character*2+1),std::uint8_t(character*2+2)}};
            th03::Round round;round.begin(resident,main.read("ENEDAT.DAT"));round.intro.flag=0;
            th03::BattleGraphics graphics(op,main,resident);
            round.set_palette(graphics.palette());
            const bool loss=std::string(argv[1])=="--loss-picture",bomb=std::string(argv[1])=="--bomb-picture",background=std::string(argv[1])=="--background-picture",
                gauge=std::string(argv[1])=="--gauge-picture",extra=std::string(argv[1])=="--extra-picture";
            th03::CollisionMap collision;
            if(gauge)for(unsigned p=0;p<2;++p) {round.gauge_flags[p]=3;round.gauge_levels[p]=15;}
            else if(extra)for(unsigned p=0;p<2;++p) {round.gauges.timing[p]={{6,1,2,0}};round.extra_attacks.kotohime_gauge(round,{2048,0},p);}
            else if(background)round.background.begin(round.random,character);
            else if(loss) {round.players[0].lose_time=48;round.defeated_player=0;}
            else if(bomb)for(unsigned p=0;p<2;++p)round.player_bomb(p,resident);
            else for(unsigned p=0;p<2;++p)round.charge_shots.add(round,round.players[p].center,p);
            for(unsigned i=0;i<ticks;++i) {
                round.result_frame=std::uint16_t(i);
                if(gauge||extra) {
                    collision.clear();round.bullets.model.reset();
                    for(unsigned p=0;p<2;++p) {
                        if(gauge)round.gauges.update(round,p);
                        if(character==4)round.extra_attacks.update_kotohime(round,p,collision,[&](const th03::Hitbox& box){return round.charge_shots.hit(round,box);});
                    }
                    round.bullets.update(round,collision,[&](th03::Point center,std::uint8_t pid) {
                        const th03::Hitbox box{center,center,pid,{0,0}};
                        return round.explosion_hit(box,th03::Against::pellet)!=0;
                    });
                    round.update_effects();round.prepare_effects_render();
                }
                else if(background)round.background.update(round.random,i,std::uint16_t(i));
                else if(loss) {if(round.players[0].lose_time!=255)round.player_lose_update(0,resident);}
                else if(bomb) {
                    for(unsigned p=0;p<2;++p)round.bombs.update(round,p);
                    round.update_effects();
                    for(unsigned p=0;p<2;++p)round.bombs.prepare_render(round,p,90);
                    round.prepare_effects_render();
                }
                else for(unsigned p=0;p<2;++p)round.charge_shots.update(round,p);
            }
            write_file(argv[5],th03::ppm(graphics.render(round,resident)));return 0;
        }
        if(argc==6&&std::string(argv[1])=="--charge-run") {
            const auto character=unsigned(std::stoul(argv[2])),pid=unsigned(std::stoul(argv[3])),ticks=unsigned(std::stoul(argv[4]));
            const bool hyper=std::stoi(argv[5]);
            if(character>8||pid>1)throw std::runtime_error("unknown charge fixture");
            th03::Round round;auto& player=round.players[pid];player.paletted=std::uint8_t(character*2+1);
            player.center={1200,5000};player.gauge_charged=1234;round.fg_shift={{6,-6}};
            round.random.cursor=254;for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            if(hyper&&character==0)round.charge_shots.reimu_hyper(player.center,pid);
            else if(hyper&&character==2)round.charge_shots.marisa_hyper(round,pid);
            else if(hyper&&character==3)round.charge_shots.ellen_hyper(round,player.center,pid);
            else round.charge_shots.add(round,player.center,pid);
            if(hyper&&character==6)round.charge_shots.rikako_active[pid]=2;
            for(unsigned tick=0;tick<ticks;++tick) {
                player.center={std::int16_t(1200+(tick%32)*28),std::int16_t(5000-(tick%17)*16)};
                round.result_frame=std::uint16_t(tick);
                if(hyper&&character==2&&tick<40)round.charge_shots.marisa_hyper(round,pid);
                if(hyper&&character==1&&tick==25)round.charge_shots.add(round,player.center,pid);
                round.charge_shots.update(round,pid);
            }
            const th03::Hitbox box{{900,3000},{2300,5100},std::uint8_t(pid),{700,1050}};
            const auto hit=round.charge_shots.hit(round,box);
            std::cout<<player.gauge_charged<<' '<<unsigned(player.shot_active)<<' '<<unsigned(round.charge_shots.reimu_alternate_hit)<<' '
                <<unsigned(round.charge_shots.mima_active[pid])<<' '<<unsigned(round.charge_shots.mima_frame[pid])<<' '
                <<unsigned(round.random.cursor)<<' '<<unsigned(round.circle_cursor)<<' '<<unsigned(hit.damage)<<' '<<hit.one_hit<<' ';
            for(const auto& shot:round.charge_shots.reimu[pid]) {
                std::cout<<unsigned(shot.state)<<' '<<unsigned(shot.frame)<<' '<<unsigned(shot.angle)<<' '<<unsigned(shot.speed)<<' ';
                for(const auto& point:shot.history)std::cout<<point.x<<' '<<point.y<<' ';
            }
            for(const auto& shot:round.charge_shots.mima[pid])std::cout<<unsigned(shot.active)<<' '<<unsigned(shot.unused)<<' '
                <<shot.center.x<<' '<<shot.center.y<<' '<<shot.velocity.x<<' '<<shot.velocity.y<<' ';
            const auto& beam=round.charge_shots.marisa[pid];std::cout<<unsigned(beam.active)<<' '<<unsigned(beam.frame)<<' ';
            for(const auto& point:beam.history)std::cout<<point.x<<' '<<point.y<<' ';
            for(const auto& shot:round.charge_shots.ellen[pid])std::cout<<unsigned(shot.state)<<' '<<unsigned(shot.phase)<<' '
                <<unsigned(shot.angle)<<' '<<unsigned(shot.length)<<' '<<shot.center.x<<' '<<shot.center.y<<' '<<shot.velocity.x<<' '<<shot.velocity.y<<' ';
            const auto& koto=round.charge_shots.kotohime[pid];std::cout<<unsigned(koto.active)<<' '<<unsigned(koto.animation)<<' '
                <<koto.center.x<<' '<<koto.center.y<<' '<<koto.velocity_y<<' ';
            std::cout<<unsigned(round.charge_shots.kana_active[pid])<<' '<<unsigned(round.charge_shots.kana_frame[pid])<<' ';
            for(const auto& shot:round.charge_shots.kana[pid]) {
                std::cout<<unsigned(shot.angle)<<' '<<unsigned(shot.length)<<' ';
                for(const auto& at:shot.history)std::cout<<at.x<<' '<<at.y<<' ';
            }
            std::cout<<unsigned(round.charge_shots.rikako_active[pid])<<' '<<unsigned(round.charge_shots.rikako_frame[pid])<<' '
                <<round.charge_shots.rikako_radius[pid]<<' '<<round.charge_shots.rikako_center[pid].x<<' '<<round.charge_shots.rikako_center[pid].y<<' ';
            for(const auto& shot:round.charge_shots.rikako[pid])std::cout<<shot.center.x<<' '<<shot.center.y<<' '<<unsigned(shot.angle)<<' '<<unsigned(shot.unused)<<' ';
            for(const auto& shot:round.charge_shots.chiyuri[pid])std::cout<<unsigned(shot.age)<<' '<<unsigned(shot.animation)<<' '<<shot.center.x<<' '<<shot.center.y<<' ';
            const auto& yume=round.charge_shots.yumemi[pid];std::cout<<unsigned(yume.state)<<' '<<unsigned(yume.frame)<<' '<<yume.center.x<<' '<<yume.center.y<<' ';
            for(const auto& circle:round.circles)std::cout<<unsigned(circle.age)<<' '<<unsigned(circle.pid)<<' '<<circle.left<<' '<<circle.top<<' ';
            std::cout<<round.sounds.size()<<' ';for(auto sound:round.sounds)std::cout<<unsigned(sound)<<' ';
            std::cout<<'\n';return 0;
        }
        if((argc==3&&(std::string(argv[1])=="--explosion"||std::string(argv[1])=="--enemy-hit"||std::string(argv[1])=="--fireball-hit"||std::string(argv[1])=="--combat-pipeline"))||
           (argc==4&&std::string(argv[1])=="--fireball-hit")||
           (argc==5&&std::string(argv[1])=="--fireball-run")) {
            const auto fixture=unsigned(std::stoul(argv[2]));if(fixture>6)throw std::runtime_error("unknown combat fixture");
            th03::Round round;
            constexpr unsigned speeds[7]={0,0,96,64,127,32,0},against[7]={0,1,1,2,3,1,1};
            const auto pid=std::uint8_t(fixture&1);round.speed=std::uint8_t(speeds[fixture]);round.last_chain_slot=9;
            round.result_frame=fixture==3||fixture==4 ? 300 : 0;
            round.random.cursor=255;for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            round.players[0].center={3600,4800};round.players[1].center={800,5200};
            for(unsigned p=0;p<2;++p) {
                round.players[p].gauge_avail=1024;round.gauge_levels[p]=15;
                round.scores[p][0]=9;round.scores[p][1]=9;round.scores[p][2]=9;
            }
            const auto set=[&](th03::Efe& e,unsigned flag,unsigned frame,unsigned slot) {
                e.flag=std::uint8_t(flag);e.frame=std::uint8_t(frame);e.center={1200,1800};
                e.size_words=2;e.hp=0;e.pid=pid;e.size_pixels=32;e.chain_slot=std::uint8_t(slot);
            };
            set(round.enemies[0],9,0,3);
            if(fixture==0||fixture==2)set(round.enemies[1],10,4,4);
            if(fixture==2)set(round.fireballs[0],10,0,3);
            if(fixture==3)round.fireballs[0].frame=37;
            round.chains.hits[pid][3]=fixture==3 ? 10 : fixture==4 ? 12 : 1;
            round.chains.hits[pid][4]=1;round.chains.value[pid][3]=fixture==3 ? 8 : fixture==4 ? 18 : 0;
            round.chains.fireball[pid][3]=fixture==3 ? 7 : fixture==4 ? 6 : 0;
            round.chains.extra[pid][3]=2;
            if(fixture==2)round.players[pid].hyper_active=1;
            if(fixture==4) {
                round.boss_launched_by=pid;round.boss_level=15;round.combos[pid].bonus=29900;
                round.fireball_variant=1;round.generation_previous=2;
            }
            if(fixture==5) {round.combos[pid].bonus=65530;round.combo_points_for_boss_attack=65000;round.scores[pid].fill(9);}
            const th03::Hitbox box=fixture==6 ? th03::Hitbox{{4000,5000},{4200,5200},pid} : th03::Hitbox{{1100,1700},{1300,1900},pid};
            th03::CollisionMap collision;
            const std::string operation=argv[1];
            std::vector<int> extra_events;
            const auto extra=[&](th03::Point point,std::uint8_t pid) {extra_events.insert(extra_events.end(),{point.x,point.y,pid});};
            std::uint8_t result=0;
            if(operation=="--enemy-hit"||operation=="--fireball-hit") {
                for(auto& e:round.enemies)e.flag=0;
                for(auto& f:round.fireballs)f.flag=0;
                round.bullets.model.reset();
                round.shots[0].alive=fixture!=2&&fixture!=3;round.shots[0].pid=pid;
                round.shots[0].top_left={944,std::int16_t(fixture==4&&operation=="--enemy-hit" ? -28 : 1672)};
                if(operation=="--enemy-hit") {
                    auto& e=round.enemies[0];set(e,1,20,0);e.hp=fixture==0 ? 1 : fixture==1 ? 3 : 0;
                    e.center.y=fixture==4 ? 100 : fixture==6 ? 0 : 1800;
                    if(fixture==2) {set(round.enemies[1],10,0,3);round.chains.extra[pid][round.speed/32]=3;}
                    if(fixture==3)round.damage_all[pid]=1;
                    if(fixture==5)round.defeat=2;
                    round.hit_enemies([&](const th03::Hitbox&) {return th03::ChargeHit{std::uint8_t(fixture==1),fixture==1};},extra);
                } else {
                    auto& f=round.fireballs[0];set(f,1,20,0);f.hp=fixture==0 ? 1 : 0;f.size_words=2;f.size_pixels=48;
                    f.generation=fixture==2 ? 3 : fixture==3 ? 4 : fixture==4 ? 2 : 0;
                    if(fixture==2||fixture==3)set(round.enemies[0],9,0,3);
                    if(fixture==5)round.defeat=2;
                    if(fixture==6)f.center.y=-1000;
                    if(argc==4)round.extends_gained=255;
                    round.hit_fireballs([&](const th03::Hitbox&) {return th03::ChargeHit{std::uint8_t(fixture==1),false};},extra,
                                       argc==4 ? std::uint8_t(std::stoul(argv[3])) : 15);
                }
            } else if(operation=="--combat-pipeline") {
                auto& t=round.bullets.model;t.reset();t.center={1200,1800};t.speed=16;t.angle=64;t.pid=pid;t.group=0;t.type=1;
                round.bullets.add(round,40);collision.clear();round.update_bullets(collision);round.update_fireballs(collision);
            } else {
                result=round.explosion_hit(box,th03::Against(against[fixture]));
                if(operation=="--fireball-run") {
                    const auto ticks=unsigned(std::stoul(argv[3]));const bool bomb=std::stoi(argv[4]);
                    for(unsigned tick=0;tick<ticks;++tick) {
                        collision.clear();round.bomb_flags[0]=round.bomb_flags[1]=bomb&&tick>=20;
                        round.update_fireballs(collision);
                    }
                }
            }
            std::cout<<unsigned(result)<<' '<<unsigned(round.last_chain_slot)<<' '<<round.last_explosion_hit<<' '
                     <<unsigned(round.fireball_variant)<<' '<<unsigned(round.generation_previous)<<' '
                     <<unsigned(round.boss_launched_by)<<' '<<unsigned(round.boss_level)<<' '<<round.combo_points_for_boss_attack
                     <<' '<<unsigned(round.random.cursor)<<' ';
            for(unsigned p=0;p<2;++p)std::cout<<unsigned(round.gauge_flags[p])<<' '<<unsigned(round.gauge_next[p])<<' '
                <<unsigned(round.warning[p])<<' '<<round.boss_panic[p]<<' '<<unsigned(round.gauge_levels[p])<<' ';
            for(auto& digits:round.scores)for(auto value:digits)std::cout<<unsigned(value)<<' ';
            const auto slots=[&](const auto& pool) {for(auto& row:pool)for(auto value:row)std::cout<<unsigned(value)<<' ';};
            slots(round.chains.hits);slots(round.chains.value);slots(round.chains.fireball);slots(round.chains.extra);
            for(auto value:round.chains.cursor)std::cout<<unsigned(value)<<' ';
            for(auto& combo:round.combos)std::cout<<unsigned(combo.time)<<' '<<unsigned(combo.hits)<<' '<<combo.bonus<<' ';
            for(auto& p:round.players)std::cout<<p.gauge_avail<<' '<<unsigned(p.combo_hits_max)<<' '<<p.combo_bonus_max<<' '
                <<unsigned(p.boss_attacks)<<' '<<unsigned(p.boss_reversals)<<' '<<unsigned(p.boss_panics)<<' ';
            const auto efe=[&](const th03::Efe& e) {std::cout<<unsigned(e.flag)<<' '<<unsigned(e.frame)<<' '<<e.center.x<<' '<<e.center.y
                <<' '<<unsigned(e.size_words)<<' '<<unsigned(e.hp)<<' '<<unsigned(e.pid)<<' '<<unsigned(e.size_pixels)<<' '<<unsigned(e.chain_slot)<<' ';};
            for(const auto& e:round.enemies)efe(e);
            for(const auto& f:round.fireballs)efe(f);
            for(const auto& f:round.fireballs)std::cout<<f.velocity.x<<' '<<f.velocity.y<<' '<<f.target_x<<' '<<f.target_x_origin<<' '
                <<unsigned(f.fall_speed)<<' '<<unsigned(f.generation)<<' ';
            if(operation=="--fireball-run"||operation=="--combat-pipeline")for(auto value:collision.bytes)std::cout<<unsigned(value)<<' ';
            if(operation=="--enemy-hit"||operation=="--fireball-hit"||operation=="--combat-pipeline") {
                std::cout<<round.one_hit<<' '<<round.enemy_killed<<' '<<round.fireball_hit<<' '<<unsigned(round.circle_cursor)<<' ';
                for(const auto& circle:round.circles)std::cout<<unsigned(circle.age)<<' '<<unsigned(circle.pid)<<' '<<circle.left<<' '<<circle.top<<' ';
                for(const auto& shot:round.shots)std::cout<<shot.alive<<' ';
                const auto& t=round.bullets.model;
                std::cout<<t.center.x<<' '<<t.center.y<<' '<<unsigned(t.speed)<<' '<<unsigned(t.angle)<<' '<<unsigned(t.pid)<<' '
                    <<unsigned(t.group)<<' '<<unsigned(t.count)<<' '<<t.sprite<<' '<<unsigned(t.type)<<' ';
                for(const auto& b:round.bullets.items)std::cout<<unsigned(b.flag)<<' '<<unsigned(b.age)<<' '<<b.center.x<<' '<<b.center.y<<' '
                    <<b.target_x<<' '<<b.target_x_origin<<' '<<b.velocity.x<<' '<<b.velocity.y<<' '<<unsigned(b.speed_next)<<' '
                    <<unsigned(b.angle_next)<<' '<<unsigned(b.pid)<<' '<<unsigned(b.group_next)<<' '<<b.sprite<<' ';
                std::cout<<unsigned(round.extends_gained)<<' '<<extra_events.size()/3<<' ';for(auto value:extra_events)std::cout<<value<<' ';
            }
            std::cout<<'\n';return 0;
        }
        if(argc==5&&std::string(argv[1])=="--pellet") {
            th03::Canvas canvas;th03::pellet(canvas,std::stoi(argv[2]),std::stoi(argv[3]),unsigned(std::stoul(argv[4])));
            std::cout.write(reinterpret_cast<const char*>(canvas.pixels.data()),640*200);return 0;
        }
        if((argc==14&&std::string(argv[1])=="--bullet-spawn")||
           (argc==16&&std::string(argv[1])=="--bullet-run")) {
            th03::Round round;auto& bullets=round.bullets;auto& t=bullets.model;
            t.center={1200,1600};round.players[0].center={3600,4800};round.players[1].center={800,5200};
            t.type=std::uint8_t(std::stoul(argv[2]));t.group=std::uint8_t(std::stoul(argv[3]));
            t.count=std::uint8_t(std::stoul(argv[4]));t.speed=std::uint8_t(std::stoul(argv[5]));
            t.angle=std::uint8_t(std::stoul(argv[6]));t.pid=std::uint8_t(std::stoul(argv[7]));
            round.bullet_base_speed=std::uint8_t(std::stoul(argv[8]));t.has_trail=bool(std::stoi(argv[9]));
            bullets.trail_cursor=std::uint8_t(std::stoul(argv[10]));round.random.cursor=std::uint8_t(std::stoul(argv[11]));
            round.fg_shift={{std::int16_t(std::stoi(argv[12])),std::int16_t(std::stoi(argv[13]))}};
            t.sprite=0x1234;t.acceleration=128;t.collidable=true;t.animated=true;bullets.items[0].flag=5;
            for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            bullets.add(round,t.pid ? 40 : 0);
            th03::CollisionMap collision;
            if(argc==16) {
                const auto ticks=unsigned(std::stoul(argv[14])),policy=unsigned(std::stoul(argv[15]));
                for(unsigned tick=0;tick<ticks;++tick) {
                    collision.clear();round.bomb_flags[0]=policy==2&&tick>=2;
                    round.damage_all[1]=policy==3&&tick>=1;round.gauge_flags[0]=round.gauge_flags[1]=policy==4;
                    bullets.update(round,collision,[&](th03::Point,std::uint8_t) {return (policy==1||policy==4)&&tick==2;});
                }
            }
            std::cout<<t.center.x<<' '<<t.center.y<<' '<<unsigned(t.speed)<<' '<<unsigned(t.angle)<<' '
                     <<unsigned(t.pid)<<' '<<unsigned(t.group)<<' '<<unsigned(t.acceleration)<<' '<<unsigned(t.count)<<' '
                     <<t.velocity.x<<' '<<t.velocity.y<<' '<<t.sprite<<' '<<unsigned(t.type)<<' '
                     <<t.collidable<<' '<<t.animated<<' '<<t.has_trail<<' '
                     <<unsigned(bullets.group_angle)<<' '<<unsigned(round.random.cursor)<<' '<<unsigned(bullets.trail_cursor)<<' ';
            for(const auto& b:bullets.items)std::cout<<unsigned(b.flag)<<' '<<unsigned(b.age)<<' '<<b.center.x<<' '<<b.center.y<<' '
                <<b.target_x<<' '<<b.target_x_origin<<' '<<b.velocity.x<<' '<<b.velocity.y<<' '
                <<unsigned(b.speed_next)<<' '<<unsigned(b.angle_next)<<' '<<unsigned(b.pid)<<' '<<unsigned(b.group_next)<<' '
                <<b.sprite<<' '<<unsigned(b.acceleration)<<' '<<b.collidable<<' '<<b.animated<<' '<<b.has_trail<<' '
                <<unsigned(b.has_trail ? b.trail : 0)<<' ';
            for(const auto& trail:bullets.trails) {
                for(auto value:trail.x)std::cout<<value<<' ';
                for(auto value:trail.y)std::cout<<value<<' ';
            }
            if(argc==16)for(auto value:collision.bytes)std::cout<<unsigned(value)<<' ';
            std::cout<<'\n';return 0;
        }
        if(argc==8&&std::string(argv[1])=="--bullet-group") {
            th03::Round round;
            auto& t=round.bullets.model;t.center={1200,1600};
            round.players[0].center={3600,4800};
            t.group=std::uint8_t(std::stoul(argv[2]));t.count=std::uint8_t(std::stoul(argv[3]));
            t.speed=std::uint8_t(std::stoul(argv[4]));t.angle=std::uint8_t(std::stoul(argv[5]));
            const auto index=std::stoi(argv[6]);round.random.cursor=std::uint8_t(std::stoul(argv[7]));
            for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            const auto done=round.bullets.group_velocity(round,index);
            std::cout<<done<<' '<<t.velocity.x<<' '<<t.velocity.y<<' '<<unsigned(round.bullets.group_angle)
                     <<' '<<unsigned(round.random.cursor)<<'\n';return 0;
        }
        if(argc==5&&(std::string(argv[1])=="--hud-picture"||std::string(argv[1])=="--combat-picture")) {
            const auto disk=read_file(argv[2]);
            const PfArchive op(hdi_file(disk,op_archive_name)),main(hdi_file(disk,main_archive_name));
            th03::Resident resident;resident.mode=th03::Mode::story;resident.paletted={{5,13}};
            th03::Round round;round.begin(resident,main.read("ENEDAT.DAT"));
            th03::BattleGraphics graphics(op,main,resident);
            const auto ticks=unsigned(std::stoul(argv[3]));
            if(std::string(argv[1])=="--hud-picture")for(unsigned i=0;i<ticks;++i) {
                round.intro.update(round.random,resident.mode);round.intro.prepare_render(resident.mode);
            } else {
                const auto ef=[&](th03::Efe& e,unsigned flag,unsigned frame,unsigned size,unsigned pid,int x,int y) {
                    e.flag=std::uint8_t(flag);e.frame=std::uint8_t(frame);e.size_words=std::uint8_t(size);
                    e.pid=std::uint8_t(pid);e.size_pixels=std::uint8_t(size*16);e.center={std::int16_t(x*16),std::int16_t(y*16)};
                };
                ef(round.enemies[0],9,14,2,0,100,100);ef(round.enemies[1],10,18,4,0,180,160);
                ef(round.fireballs[0],1,0,2,0,80,240);ef(round.fireballs[1],1,5,3,1,180,290);
                ef(round.fireballs[2],2,3,2,1,220,100);ef(round.fireballs[3],9,16,2,1,180,80);
                round.fireballs[3].size_pixels=48;
                round.enemy_circle({144*16,200*16},0);round.player_circle({144*16,280*16},1);
                auto& b=round.bullets.items;
                b[0].flag=2;b[0].center={150*16,120*16};b[0].sprite=8;
                b[1].flag=4;b[1].pid=1;b[1].center={100*16,160*16};b[1].sprite=0x1942;
                b[2].flag=1;b[2].center={180*16,240*16};b[3].flag=3;b[3].pid=1;b[3].center={100*16,140*16};
            }
            write_file(argv[4],th03::ppm(graphics.render(round,resident)));return 0;
        }
        if(argc==10&&std::string(argv[1])=="--collmap") {
            th03::CollisionMap map;
            const std::string kind=argv[2];const auto pid=unsigned(std::stoul(argv[3]));
            const th03::Point point{std::int16_t(std::stoi(argv[4])),std::int16_t(std::stoi(argv[5]))};
            const auto width=std::stoi(argv[6]),height=std::stoi(argv[7]),right=std::stoi(argv[8]);
            if(kind=="rectangle")map.rectangle(pid,point,width,height);
            else if(kind=="vertical")map.vertical(pid,point,height);
            else if(kind=="slope")map.slope(pid,point.x,right,unsigned(width));
            else throw std::runtime_error("unknown collision primitive");
            if(std::string(argv[9])=="hit") {
                th03::Player player;player.invincibility=0;player.center=point;
                const auto hit=map.hit(pid,player,4);
                std::cout<<bool(hit)<<' '<<(hit ? hit->x : 0)<<' '<<(hit ? hit->y : 0)<<'\n';
            } else std::cout.write(reinterpret_cast<const char*>(map.bytes.data()),map.bytes.size());
            return 0;
        }
        if(argc==6&&std::string(argv[1])=="--hud-intro") {
            th03::Round round;th03::Resident resident;
            round.random.seed=std::uint32_t(std::stoul(argv[2]));resident.mode=th03::Mode(std::stoul(argv[3]));
            const auto ticks=unsigned(std::stoul(argv[4]));round.random.cursor=std::uint8_t(std::stoul(argv[5]));
            for(unsigned i=0;i<256;++i)round.random.bytes[i]=std::uint8_t(i*13+7);
            for(unsigned tick=0;tick<ticks;++tick) {
                round.intro.update(round.random,resident.mode);round.intro.prepare_render(resident.mode);
                const auto& intro=round.intro;
                std::cout<<unsigned(intro.flag)<<' '<<unsigned(intro.phase)<<' '<<intro.frame<<' '<<intro.sprite<<' '<<intro.x
                         <<' '<<round.random.seed<<' '<<unsigned(round.random.cursor)<<' ';
                for(const auto& p:intro.particles)std::cout<<p.center.x<<' '<<p.center.y<<' '<<p.velocity<<' '
                    <<unsigned(p.angle)<<' '<<unsigned(p.active)<<' '<<unsigned(p.turn_early)<<' '<<unsigned(p.turn_late)<<' ';
                std::cout<<'\n';
            }
            return 0;
        }
        if(argc==9&&std::string(argv[1])=="--enemy") {
            th03::Round round;round.formations=th03::read_formations(read_file(argv[2]));
            const auto formation=unsigned(std::stoul(argv[3])),index=unsigned(std::stoul(argv[4]));
            const auto band=std::uint8_t(std::stoul(argv[5])),mirror=std::uint8_t(std::stoul(argv[6]));
            const auto ticks=unsigned(std::stoul(argv[7])),player_y=unsigned(std::stoul(argv[8]));
            round.players[0].center={144<<4,std::int16_t(player_y)};
            th03::Enemy enemy;enemy.flag=3;enemy.pos_type=mirror;enemy.script=&round.formations.at(formation).scripts.at(index);
            for(unsigned frame=0;frame<ticks&&enemy.flag;++frame) {
                enemy.run(round,band);
                std::cout<<unsigned(enemy.flag)<<' '<<enemy.center.x<<' '<<enemy.center.y<<' '
                         <<unsigned(enemy.size_words)<<' '<<unsigned(enemy.hp)<<' '<<unsigned(enemy.pid)<<' '
                         <<unsigned(enemy.size_pixels)<<' '<<enemy.ip<<' '<<enemy.op_frame<<' '
                         <<enemy.velocity.x<<' '<<enemy.velocity.y<<' '<<enemy.angle<<' '
                         <<int(enemy.angle_speed)<<' '<<unsigned(enemy.speed)<<' '<<unsigned(enemy.pos_type)<<'\n';
            }
            return 0;
        }
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
        th03::Round formation;
        formation.formations.resize(1);formation.formations[0].scripts.push_back(Bytes{0});formation.speed=96;
        formation.update_formations();check(formation.enemy_speed==0&&!formation.enemies[0].flag,"intro gates formation spawn");
        formation.intro.flag=0;formation.enemies_alive={{1,1}};formation.update_formations();
        check(formation.enemy_speed==0,"existing formations retain previous enemy speed band");
        formation.enemies_alive[1]=0;formation.update_formations();
        check(formation.enemy_speed==3&&formation.enemies[0].pid==1,"either player's new formation refreshes shared enemy speed");
        unsigned charges=0,bombs=0,losses=0;th03::Resident game;th03::CollisionMap collision;
        th03::PlayerServices services;
        services.hyper=[](th03::Round& round,unsigned pid){round.hyper_update(pid);};
        services.cpu=[&](th03::Round& round,unsigned pid){round.cpu_update(pid,collision,game);};
        services.bomb=[&](th03::Round& round,unsigned pid){++bombs;round.player_bomb(pid,game);};
        services.lose=[&](th03::Round& round,unsigned pid){++losses;round.player_lose_update(pid,game);};
        services.charge=[&](th03::Round& round,th03::Point at,unsigned pid){++charges;round.charge_shots.add(round,at,pid);};
        th03::Round control;
        auto& human=control.players[0];human.center={144*16,336*16};human.speeds={{64,64,48,48,28}};human.gauge_avail=1024;
        for(unsigned i=0;i<37;++i)control.player_update(0,th03::shot,collision,game,services);
        check(human.gauge_charged==1024&&!charges&&!control.shots[0].alive,"held shot reaches charge without autofiring");
        for(unsigned i=0;i<4;++i)control.player_update(0,0,collision,game,services);
        check(charges==1&&human.gauge_charged==0&&human.invincibility==6,"release window fires one charge shot");
        control.player_update(0,th03::shot,collision,game,services);
        check(control.shots[0].alive&&control.shot_release[0]==0&&control.sounds.back()==1,"tap after release fires an ordinary shot pair");
        th03::Round damage;
        damage.players[0].center=human.center;damage.players[0].halfhearts=2;damage.players[0].hit_damage_next=6;damage.shot_release[0]=8;
        collision.rectangle(0,human.center,4,4);damage.player_update(0,0,collision,game,services);
        check(damage.players[0].halfhearts==1&&damage.players[0].knockback_active&&damage.players[0].invincibility==110,"nonfinal hit preserves one halfheart");
        th03::Round fatal;fatal.players[0].center=human.center;fatal.players[0].halfhearts=1;fatal.shot_release[0]=8;
        fatal.player_update(0,0,collision,game,services);
        check(fatal.players[0].halfhearts==0&&fatal.players[0].lose_time==48&&fatal.defeated_player==0&&fatal.circles[12].age==1,"last halfheart starts actual defeat");
        fatal.player_update(0,0,collision,game,services);
        check(fatal.defeat==1&&fatal.players[0].lose_time==47&&fatal.lose_radius==0&&fatal.fg_shift[0]==6&&fatal.sounds.back()==14,
              "loss starts the particle origin, field shake and explosion sound");
        fatal.result_frame=1;fatal.player_update(0,0,collision,game,services);
        check(fatal.lose_radius==9&&fatal.fg_shift[0]==-6&&fatal.palette_tone==130&&fatal.reset_frames==2,"loss flash and radius follow countdown parity");
        for(unsigned i=2;i<48;++i) {fatal.result_frame=std::uint16_t(i);fatal.player_update(0,0,collision,game,services);}
        check(fatal.defeat==2&&fatal.players[0].lose_time==255&&fatal.players[1].rounds_won==1&&game.winner==1&&
              fatal.result_frame==0&&fatal.lose_radius==0&&fatal.fg_shift[0]==0&&fatal.palette_tone==100,"loss completes the round and records its winner");
        th03::Round computer;collision.clear();computer.result_frame=32;
        computer.players[0].center=human.center;computer.players[0].cpu=true;computer.players[0].gauge_avail=1024;
        computer.players[0].charge_thresholds.fill(255);computer.player_update(0,0,collision,game,services);
        check(computer.players[0].cpu_frame==1&&computer.shots[0].alive&&computer.target_formation_marker==0,"CPU target cadence overrides input then clears marker");
        th03::Round locked;locked.player_velocity.x=-64;locked.page_back=true;locked.shot_release[1]=8;
        locked.players[1].center=human.center;locked.players[1].move_lock=1;locked.players[1].invincibility=50;
        locked.player_update(1,0,collision,game,services);
        check(locked.players[1].center.x==human.center.x&&locked.players[1].pattern_movement==1&&locked.players[1].pattern_glow==1,
              "locked player retains shared velocity for banking and back-page glow");
        th03::Round targeting;
        targeting.enemies[0].flag=1;targeting.enemies[0].center={1200,1000};targeting.enemies[0].formation_i=5;
        targeting.enemies[1]=targeting.enemies[0];targeting.enemies[1].center={200,5000};targeting.enemies[1].formation_i=2;
        targeting.find_target(0);
        check(targeting.target.x==2304&&targeting.target.y==4800&&targeting.target_formation_marker==2,"target fallback retains selected formation marker");
        targeting.boss_active[0]=1;targeting.boss_target={800,900};targeting.find_target(0);
        check(targeting.target.x==800&&targeting.target.y==900&&targeting.target_formation_marker==254,"boss target takes priority over formations");
        th03::Round hyper;
        constexpr unsigned modes[9]={4,2,0,1,3,3,1,3,3};
        for(unsigned character=0;character<9;++character) {
            auto& p=hyper.players[0];p={};p.paletted=std::uint8_t(character*2+1);p.hyper_active=p.paletted;p.center=human.center;p.gauge_avail=4080;
            hyper.movement_speed={{64,64,48,48}};hyper.hyper_update(0);
            check(p.shot_mode==1&&hyper.movement_speed[0]==64,"Hyper standby delays its character callback until next frame");
            hyper.hyper_update(0);
            const unsigned expected=character==3 ? 64 : character==2||character==6 ? 48 : 96;
            check(p.shot_mode==modes[character]&&hyper.movement_speed[0]==expected,"character Hyper mode and movement speeds");
            p.hyper_active=0;hyper.hyper_update(0);hyper.hyper_update(0);
            check(!p.hyper_handler&&p.shot_mode==1,"Hyper returns through standby after expiry");
        }
        hyper.players[0].shot_mode=4;hyper.players[0].center=human.center;
        hyper.add_shots(0);
        check(hyper.charge_shots.reimu[0][0].state==2&&hyper.charge_shots.reimu[0][1].state==2&&
              hyper.shots[0].alive&&hyper.shots[0].top_left.y==human.center.y-16,"Reimu Hyper joins two history shots and the shifted ordinary pair");
        th03::Round bomb_control;th03::Resident bomb_game;
        auto& bomber=bomb_control.players[0];bomber.bombs=2;bomber.gauge_avail=4080;bomber.center=human.center;
        bomb_control.player_bomb(0,bomb_game);
        check(bomb_control.bomb_flags[0]==1&&bomber.bombs==1&&bomber.invincibility==180&&bomb_game.skill==69,"Bomb consumes a stock and starts invincibility");
        bomb_control.player_bomb(0,bomb_game);
        check(bomber.bombs==1&&bomb_game.skill==69,"active Bomb blocks repeated input");
        bomb_control.bomb_flags[0]=0;bomber.bombs=0;bomb_control.player_bomb(0,bomb_game);
        check(bomber.hyper_active==1&&bomb_control.damage_all[0]==1&&bomb_control.effects[1].radius==8&&bomb_game.skill==68,"empty Bomb stock spends full gauge on Hyper and its real explosion effect");
        const auto sounds=bomb_control.sounds.size();bomb_control.player_bomb(0,bomb_game);
        check(bomb_control.sounds.size()==sounds&&bomb_game.skill==68,"active Hyper blocks another Bomb");
        th03::Round kotohime_fade;kotohime_fade.players[0].paletted=9;kotohime_fade.bomb_flags[0]=2;kotohime_fade.bombs.frame[0]=128;
        rejects([&]{kotohime_fade.bombs.prepare_render(kotohime_fade,0);});
        kotohime_fade.bombs.prepare_render(kotohime_fade,0,0x5a);
        check(kotohime_fade.palette[0]==0xb4&&kotohime_fade.palette[2]==255,"Kotohime fade reads the supplied stack color with byte wrap");
        std::cout<<"Portable resources, menus, movement, formations and player-state checks passed\n";
        return 0;
    } catch (const std::exception& error) { std::cerr<<error.what()<<'\n'; return 1; }
}
