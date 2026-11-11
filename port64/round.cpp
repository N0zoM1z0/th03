#include "round.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
// Original authored DATA: story_cpu_safety_frames and PLAYCHAR_SPEEDS.
constexpr unsigned safety[10][6]={
    {100,50,20,0,0,0},{200,100,50,20,0,0},{300,200,100,50,10,0},
    {400,300,200,100,50,10},{500,400,250,150,70,20},{600,500,300,200,100,50},
    {1000,700,500,300,200,100},{1500,800,600,300,200,100},
    {65530,1500,1000,800,700,500},{65530,2000,1800,1300,1000,700}
};
constexpr std::uint8_t speeds[9][5]={
    {64,64,48,48,32},{72,72,54,54,20},{64,64,48,48,28},
    {52,52,46,46,14},{68,68,52,52,28},{56,56,44,44,32},
    {72,72,54,54,16},{80,80,64,64,28},{80,80,64,64,20}
};
}
std::uint16_t RandomRing::next() {return random_next(seed);}
void RandomRing::fill() {
    for(int i=255;i>=0;--i)bytes[unsigned(i)]=std::uint8_t(next());
    // GAME 3 does not rewind the getter cursor on refill.
}
std::uint16_t RandomRing::ring() {
    const auto at=cursor++;
    // INC precedes the WORD load. At index255 its high byte aliases the
    // just-wrapped cursor, not bytes[0] or the pre-increment index.
    return std::uint16_t(bytes[at]|(unsigned(at==255 ? cursor : bytes[at+1])<<8));
}
std::vector<Formation> read_formations(const Bytes& file) {
    const auto word=[&](std::size_t at) {return unsigned(file.at(at))|(unsigned(file.at(at+1))<<8);};
    if(file.size()<4||word(2)!=0||word(0)>file.size()-4)throw std::runtime_error("invalid ENEDAT header");
    const auto end=std::size_t(word(0))+4;
    std::size_t at=4;
    std::vector<Formation> out;
    while(at+2<=end) {
        const auto count=word(at);at+=2;
        if(!count)return out;
        if(count>16||out.size()>=24)throw std::runtime_error("ENEDAT formation capacity exceeded");
        Formation f;
        for(unsigned i=0;i<count;++i) {
            if(at>=end)throw std::runtime_error("truncated ENEDAT script size");
            const auto size=file[at++];
            if(size>end-at)throw std::runtime_error("truncated ENEDAT script");
            f.scripts.emplace_back(file.begin()+at,file.begin()+at+size);at+=size;
        }
        out.push_back(std::move(f));
    }
    throw std::runtime_error("ENEDAT terminator missing");
}
void Round::randomize_formations(std::uint8_t previous) {
    if(formations.size()<2)throw std::runtime_error("formation randomizer needs original ENEDAT");
    for(unsigned i=0;i<256;++i) {
        std::uint8_t next;
        do {next=std::uint8_t(random.next()%formations.size());}while(next==previous);
        formation_types[i]=next;previous=next;
        formation_positions[i]=std::uint8_t((random.next()&1)*0x80);
    }
    formation_cursors={};
}
void Round::begin(const Resident& resident,const Bytes& enedat) {
    *this=Round{};random.seed=resident.seed;formations=read_formations(enedat);
    prepare(resident,0x5e);
    result_wait=resident.stage<8 ? 320 : 460;
    if(resident.mode==Mode::story) {
        scores[0]=resident.scores[0];
        cpu_damage_additional=resident.stage<6 ? std::uint8_t(3-resident.stage/2) : 0;
        gauge_levels.fill(std::uint8_t(resident.stage+1));
        extends_gained=scores[0][6];
        if(extends_gained>=2||scores[0][7])extends_gained=255;
    } else {
        constexpr unsigned vs_safety[4]={1000,1900,4000,65535};
        players[0].cpu_safety=players[1].cpu_safety=std::uint16_t(
            resident.cpu[0]&&resident.cpu[1] ? 65535 : vs_safety[resident.options.rank]);
        // stage_setup assigns MIN after round_prepare_players, replacing
        // the initial rank increment. Later rounds increment it normally.
        gauge_levels.fill(1);extends_gained=255;
    }
    for(unsigned p=0;p<2;++p) {
        auto& player=players[p];
        player.rounds_won=0;player.gauge_avail=1024;player.combo_hits_max=0;player.combo_bonus_max=0;
        std::copy_n(speeds[character_id(player.paletted)],5,player.speeds.begin());
    }
    if(resident.demo) {speed=64;bullet_base_speed=0;boss_level=8;gauge_levels.fill(9);}
}
void Round::prepare(const Resident& resident,std::uint8_t formation_previous) {
    for(auto& shot:shots)shot.alive=false;
    frame=result_frame=0;
    random.fill();
    if(resident.mode==Mode::story) {
        const int column=std::min(int(id)-resident.credits+3,5);
        // These are valid game-state assumptions, not clamps on DOS behavior.
        if(column<0||resident.stage>=10)throw std::runtime_error("unrecovered story safety context");
        unsigned value=safety[resident.stage][column];
        switch(resident.options.rank) {
        case 0:value/=3;break;
        case 2:value*=2;break;
        case 3:value=value*3+500;break;
        }
        players[1].cpu_safety=std::uint16_t(std::min(value,65535u));
    }
    const auto rank=resident.options.rank;
    if(rank>3)throw std::runtime_error("invalid rank");
    // Assignments truncate to the target's byte before its upper clamps.
    speed=std::uint8_t(rank==3 ? 96 : (id<<(rank==0 ? 4 : 5))+(rank==2 ? 32 : 0));
    bullet_base_speed=rank<2 ? 0 : rank==2 ? 8 : 24;
    boss_level=std::uint8_t((rank==0 ? resident.stage/2+id : resident.stage+id*2)+(rank==2 ? 2 : rank==3 ? 8 : 0));
    if(resident.mode!=Mode::story)for(auto& level:gauge_levels)level=std::uint8_t(level+(rank==0 ? 1 : rank==3 ? 4 : 2));
    speed=std::min<std::uint8_t>(speed,127);boss_level=std::min<std::uint8_t>(boss_level,16);
    for(auto& level:gauge_levels)level=std::min<std::uint8_t>(level,16);
    combo_points_for_boss_attack=5120;
    for(unsigned p=0;p<2;++p) {
        auto& player=players[p];
        player.paletted=resident.paletted[p];player.cpu=resident.cpu[p];player.is_hit=false;
        player.invincibility=50;player.shot_mode=1;player.halfhearts=10;
        player.knockback_time=0;player.move_lock=0;player.knockback_active=false;
        player.center={144<<4,336<<4};player.gauge_charged=0;player.shot_active=1;player.hit_damage_next=1;
        for(auto& value:player.charge_thresholds)value=std::uint8_t(((random.next()&3)<<6)+63);
        player.charge_cursor=0;player.bombs=2;player.lose_time=0;player.hyper_active=0;player.cpu_frame=0;
        player.gauge_attacks=0;player.boss_attacks=0;player.boss_reversals=0;player.boss_panics=0;
    }
    randomize_formations(formation_previous);
}
bool Player::move(std::uint16_t input) {
    const auto velocity=[&](std::uint16_t movement,Point& v) {
        int x=0,y=0;
        switch(movement) {
        case left:x=-1;break;
        case down|left:case down_left:x=-1;y=1;break;
        case down:y=1;break;
        case down|right:case down_right:x=1;y=1;break;
        case right:x=1;break;
        case up|right:case up_right:x=1;y=-1;break;
        case up:y=-1;break;
        case up|left:case up_left:x=-1;y=-1;break;
        case 0:return 0;
        default:return -1;
        }
        v.x=std::int16_t(x*speeds[x&&y ? 2 : 0]);v.y=std::int16_t(y*speeds[x&&y ? 3 : 1]);return 1;
    };
    auto movement=std::uint16_t(input&0x0f0f);
    Point v;
    auto result=velocity(movement,v);
    if(result==-1&&human_movement_last!=movement) {
        movement&=std::uint16_t(~human_movement_last);result=velocity(movement,v);
    } else human_movement_last=movement;
    if(result!=1)return false;
    center.x=std::clamp<std::int16_t>(motion::wrap(int(center.x)+v.x),8<<4,280<<4);
    center.y=std::clamp<std::int16_t>(motion::wrap(int(center.y)+v.y),24<<4,352<<4);
    return true;
}
void Round::add_shots(unsigned pid) {
    const auto& player=players.at(pid);
    if(!player.shot_mode)return;
    if(player.shot_mode>3)throw std::runtime_error("Reimu hyper shot family is not joined yet");
    int pair=player.shot_mode==3 ? 0 : player.shot_mode==2 ? 2 : 3;
    auto left=motion::wrap(int(player.center.x)-(4-pair)*256);
    for(;left<=-512;left=motion::wrap(int(left)+512),++pair){}
    for(auto& shot:shots)if(!shot.alive) {
        shot.alive=true;shot.top_left={left,player.center.y};shot.velocity_y=-192;
        shot.pid=std::uint8_t(pid);shot.animation=0;
        if(++pair>=4)break;
        left=motion::wrap(int(left)+512);if(left>=288<<4)break;
    }
}
void Round::update_shots() {
    for(auto& shot:shots)if(shot.alive) {
        shot.top_left.y=motion::wrap(int(shot.top_left.y)+shot.velocity_y);
        if(shot.top_left.y<=-16)shot.alive=false;
    }
}
}
