#include "bullet.hpp"
#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
int pixel(int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);}
Point vector(Point from,Point to,unsigned plus,int speed) {
    const auto angle=std::uint8_t(motion::angle_to({from.x,from.y},{to.x,to.y})+plus);
    const auto v=motion::polar(angle,std::int16_t(speed));return {v.x,v.y};
}
}
void BulletTemplate::reset() {angle=0;count=0;animated=true;collidable=true;has_trail=false;}
void Bullets::reset() {for(auto& bullet:items)bullet.flag=0;trail_cursor=0;}
bool Bullets::group_velocity(Round& round,int index) {
    auto& t=model;
    int offset=0;
    auto speed=t.speed;
    bool done=false,aim=true;
    const auto group=t.group;
    if(group>=2&&group<=25) {
        const unsigned family=(group-2)/6,variant=(group-2)%6;
        const int spread=int(variant%3);
        aim=variant>=3;
        offset=spread*(family==0 ? 3 : family==1 ? 8 : 6);
        switch(family) {
        case 0:
            if(index==0)offset=3+spread*3;
            else if(index==1) {offset=-3-spread*3;done=true;}
            break;
        case 1:
            if(index==0)offset=0;
            else if(index==1)offset=8+spread*8;
            else if(index==2) {offset=-8-spread*8;done=true;}
            break;
        case 2:
            switch(index) {
            case 0:offset=3+spread*6;break;
            case 1:offset=-3-spread*6;break;
            case 2:offset=9+spread*18;break;
            case 3:offset=-9-spread*18;done=true;break;
            }
            break;
        case 3:
            switch(index) {
            case 0:offset=0;break;
            case 1:offset=6+spread*6;break;
            case 2:offset=-6-spread*6;break;
            case 3:offset=12+spread*12;break;
            case 4:offset=-12-spread*12;done=true;break;
            }
            break;
        }
    } else if(group==32||group==33||(group>=35&&group<=37)||(group>=39&&group<=43)) {
        const unsigned count=group==33||group==39 ? 2 : group==32||group==40 ? 4 :
                             group==35||group==41 ? 8 : group==36||group==42 ? 16 : 32;
        offset=index*int(256/count);done=index>=int(count)-1;aim=group>=39;
    } else switch(group) {
    case 0:done=true;aim=false;break;
    case 1:done=true;break;
    case 26:offset=motion::wrap(round.random.ring());done=true;aim=false;break;
    case 27:case 28:
        offset=motion::wrap(round.random.ring());
        if(group==28)speed=std::uint8_t(speed+(round.random.ring()&31));
        done=index>=t.count;aim=false;break;
    case 29:offset=int(round.random.ring()&31)-16;done=index>=t.count;break;
    case 34:if(index) {offset=128-int(t.angle)*2;done=true;}aim=false;break;
    case 38:case 44:
        if(!t.count)throw std::domain_error("bullet N-ring divide by zero");
        offset=motion::wrap(index*256)/t.count;done=index>=int(t.count)-1;aim=group==44;break;
    }
    group_angle=std::uint8_t(offset+t.angle);
    if(aim)t.velocity=vector(t.center,round.players[t.pid].center,group_angle,speed);
    else {const auto v=motion::polar(group_angle,speed);t.velocity={v.x,v.y};}
    return done;
}
void Bullets::add(Round& round,unsigned sprite_base) {
    auto& t=model;
    if(t.center.y<=-128||t.center.y>=6016||t.center.x<=-128||t.center.x>=4736)return;
    unsigned flag=t.type;
    bool acceleration=false;
    switch(t.type) {
    case 6:acceleration=true;flag=1;break;
    case 7:acceleration=true;[[fallthrough]];
    case 2:t.sprite=std::uint16_t(sprite_base+8);flag=2;break;
    case 5:flag=2;break;
    case 8:acceleration=true;flag=2;break;
    }
    const auto original_speed=t.speed;
    t.speed=std::clamp<std::uint8_t>(std::uint8_t(t.speed+round.bullet_base_speed),16,128);
    int group_index=0;
    for(auto& bullet:items)if(!bullet.flag) {
        bullet.flag=std::uint8_t(flag);bullet.age=0;bullet.center=t.center;bullet.group_next=t.group;bullet.pid=t.pid;
        bullet.sprite=t.sprite;bullet.animated=t.animated;bullet.collidable=t.collidable;bullet.has_trail=t.has_trail;
        if(t.has_trail) {
            bullet.trail=trail_cursor++;if(trail_cursor>=48)trail_cursor=0;
            trails[bullet.trail].x.fill(t.center.x);trails[bullet.trail].y.fill(t.center.y);
        }
        bullet.acceleration=acceleration ? t.acceleration : 0;
        if(flag==3) {
            const int origin=16+t.pid*320+pixel(t.center.x)+round.fg_shift[t.pid];
            bullet.target_x=std::int16_t(round.random.ring()%4608);
            const auto other=t.pid^1;
            const int target=16+other*320+pixel(bullet.target_x)+round.fg_shift[other];
            const auto y=std::int16_t(round.random.ring()&255);
            bullet.velocity=vector({motion::wrap(origin*16),bullet.center.y},{motion::wrap(target*16),y},0,70+round.speed/3);
            bullet.target_x_origin=motion::wrap((target-16-t.pid*320)*16);
            bullet.angle_next=t.angle;bullet.speed_next=t.speed;break;
        }
        const bool done=group_velocity(round,group_index);
        bullet.velocity=t.velocity;bullet.angle_next=group_angle;bullet.speed_next=t.speed;
        if(flag==4)bullet.sprite=80*80+528/8;
        if(done)break;
        ++group_index;
    }
    t.speed=original_speed;
}
void Bullets::add_next(Round& round,const Bullet& bullet) {
    model.type=bullet.flag;model.center=bullet.center;
    model.speed=bullet.speed_next;model.angle=bullet.angle_next;model.pid=bullet.pid;model.group=bullet.group_next;
    // bullets_update runs after both players' attack updates. The union
    // pid.so_attack still contains the P2 atlas base at this call site.
    add(round,40);
}
void Bullets::update(Round& round,CollisionMap& collision,const PelletHit& explosion_hit) {
    const auto trail_step=[](std::array<std::int16_t,6>& coordinates,std::int16_t previous,int maximum) {
        coordinates[5]=coordinates[4];
        if(coordinates[5]<=-128||coordinates[5]>=maximum)return true;
        for(unsigned i=4;i>0;--i)coordinates[i]=coordinates[i-1];
        coordinates[0]=previous;return false;
    };
    for(auto& b:items) {
        if(!b.flag||b.flag>=5)continue;
        ++b.age;
        if(b.flag==4) {
            if(!(b.age&3)) {
                const auto next=std::uint16_t(b.sprite+4);
                if(next>=0x1942+12)b.flag=1;else b.sprite=next;
            }
            continue;
        }
        auto next_x=motion::wrap(int(b.center.x)+b.velocity.x);
        if(b.flag!=3) {
            if(round.bomb_flags[b.pid]||round.damage_all[b.pid]) {b.flag=0;continue;}
            if(b.has_trail) {
                next_x=std::clamp<std::int16_t>(next_x,-128,4736);
                if(trail_step(trails[b.trail].x,b.center.x,4736)) {b.flag=0;continue;}
            } else if(next_x<=-128||next_x>=4736) {b.flag=0;continue;}
        } else if(b.pid==0 ? next_x>=b.target_x_origin : next_x<=b.target_x_origin) {
            b.flag=4;b.pid^=1;b.center.x=b.target_x;b.center.y=32;b.speed_next=std::uint8_t(b.speed_next+8);
            model.count=0;add_next(round,b);b.flag=0;continue;
        }
        b.center.x=next_x;
        const auto next_y=motion::wrap(int(b.center.y)+b.velocity.y);
        if(b.has_trail) {
            if(trail_step(trails[b.trail].y,b.center.y,6016)) {b.flag=0;continue;}
        } else if(next_y<=-128||next_y>=6016) {b.flag=0;continue;}
        b.center.y=next_y;
        if(b.acceleration==128&&b.velocity.y<80)b.velocity.y=motion::wrap(int(b.velocity.y)+1);
        if(b.flag==1&&explosion_hit(b.center,b.pid)) {
            if(!round.gauge_flags[b.pid^1]) {
                b.flag=3;b.group_next=29;b.angle_next=0;add_next(round,b);
            }
            b.flag=0;continue;
        }
        if(b.flag!=3&&b.collidable)collision.vertical(b.pid,b.center,1);
    }
}

}
