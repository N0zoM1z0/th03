#include "round.hpp"
#include "motion.hpp"
#include <stdexcept>

namespace th03 {
namespace {
int signed_byte(unsigned value) {return value<128 ? int(value) : int(value)-256;}
}
bool Enemy::run(const Round& round,std::uint8_t enemy_speed) {
    const auto& player=round.players.at(pid);
    auto cursor=ip;
    const auto byte=[&](unsigned at) {return unsigned(script->at(unsigned(cursor)+at));};
    const auto velocity_set=[&] {
        const auto v=motion::polar(std::uint8_t(angle>>8),speed);velocity={v.x,v.y};
    };
    const auto tune=[&](int v) {return motion::wrap(enemy_speed*v)/9+motion::wrap(2*v)/3;};
    const auto move=[&] {
        auto x=tune(velocity.x);if(!(pos_type&0x80))x=-x;
        center.x=motion::wrap(int(center.x)+x);
        if((pos_type&1)&&(center.x<=-512||center.x>=5120)) {flag=0;return true;}
        center.y=motion::wrap(int(center.y)+tune(velocity.y));
        if((pos_type&2)&&center.y>=6400) {flag=0;return true;}
        return false;
    };
    const auto angle_update=[&] {
        auto wide=motion::wrap(int(angle_speed)*512)/3;
        wide=motion::wrap(wide+motion::wrap(enemy_speed*wide)/9);
        angle=std::uint16_t(angle+wide);
    };
    // Loop opcodes are unused by the original data and read an indeterminate
    // op_size in DOS. Recover that stack context before accepting custom files.
    for(;;) {
        unsigned size=0,duration=0;
        const auto op=byte(0);
        switch(op) {
        case 0:flag=0;return true;
        case 1:case 8:case 9:
            if(!op_frame) {speed=std::uint8_t(byte(2));angle=std::uint16_t(byte(1)<<8);velocity_set();}
            if(move())return true;
            duration=byte(3);size=4;
            if(op==8&&center.y>=player.center.y-512&&center.y<=player.center.y+512) {op_frame=0;goto next_op;}
            if(op==9&&center.x>=player.center.x-256&&center.x<=player.center.x+256) {op_frame=0;goto next_op;}
            break;
        case 6:
            if(move())return true;
            duration=byte(1);size=2;break;
        case 7:
            if(!op_frame) {speed=std::uint8_t(byte(1));velocity_set();}
            if(move())return true;
            duration=byte(2);size=3;break;
        case 2:case 10:
            if(!op_frame) {angle=std::uint16_t(byte(1)<<8);angle_speed=std::int8_t(signed_byte(byte(3)));}
            speed=std::uint8_t(byte(2));velocity_set();
            if(op==10) {
                velocity.x=motion::wrap(int(velocity.x)+signed_byte(byte(4)));
                velocity.y=motion::wrap(int(velocity.y)+signed_byte(byte(5)));
                duration=byte(6);size=7;
            } else {duration=byte(4);size=5;}
            if(move())return true;
            angle_update();break;
        case 3:duration=byte(1);size=2;break;
        case 4:case 5:
            if(!op_frame) {angle=0;angle_speed=std::int8_t(signed_byte(byte(2)));}
            velocity.x=motion::polar(std::uint8_t(angle>>8),std::int16_t(byte(1))).x;
            velocity.y=std::int16_t(signed_byte(byte(3)));
            if(op==5)std::swap(velocity.x,velocity.y);
            if(move())return true;
            angle_update();duration=byte(4);size=5;break;
        case 0x10:
            flag=1;
            center.x=motion::wrap(signed_byte(byte(1))*128);
            if(!(pos_type&0x80))center.x=motion::wrap(4608-int(center.x));
            center.y=motion::wrap(signed_byte(byte(2))*128);
            size_words=std::uint8_t(byte(3+enemy_speed));size_pixels=std::uint8_t(size_words*16);
            hp=std::uint8_t(byte(7+enemy_speed));
            if(byte(11))pos_type|=1;
            if(byte(12))pos_type|=2;
            size=14;goto next_op;
        case 0x82:pos_type|=1;size=1;goto next_op;
        case 0x83:pos_type|=2;size=1;goto next_op;
        default:throw std::runtime_error("enemy script opcode needs its original stack context");
        }
        // Independent signed divisions, not a combined rational expression.
        if(int((duration/2)*3-(enemy_speed*duration)/6)<=op_frame) {op_frame=0;ip=std::uint16_t(ip+size);}
        else ++op_frame;
        return false;
    next_op:
        ip=std::uint16_t(ip+size);cursor=std::uint16_t(cursor+size);
    }
}
void Round::update_formations() {
    for(unsigned p=0;p<2;++p) {
        if(enemies_alive[p])continue;
        const auto cursor=formation_cursors[p]++;
        const auto type=formation_types[cursor];
        const auto& formation=formations.at(type);
        for(unsigned i=0;i<formation.scripts.size();++i)for(auto& enemy:enemies)if(!enemy.flag) {
            enemy.flag=3;enemy.ip=0;enemy.op_frame=0;enemy.loop_i=0;
            enemy.script=&formation.scripts[i];enemy.pid=std::uint8_t(p);enemy.formation=type;
            enemy.formation_i=std::uint8_t(i);enemy.pos_type=formation_positions[cursor];break;
        }
    }
}
void Round::update_enemy_scripts() {
    enemies_alive={};
    for(auto& enemy:enemies)if(enemy.flag) {
        ++enemy.frame;
        if(enemy.flag>=9) {
            if(enemy.frame==10)enemy.flag=10;
            else if(enemy.frame==32)enemy.flag=9;
            else if(enemy.frame>=36)enemy.flag=0;
            continue;
        }
        if(!enemy.run(*this,speed/32))++enemies_alive[enemy.pid];
    }
}
}
