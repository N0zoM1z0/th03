#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <stdexcept>

namespace th03 {
namespace {
// Original authored input-word tables, twelve 3x3 dodge grids and three
// nine-direction retry sequences. Diagonals use the original dedicated bits.
constexpr std::uint16_t dodge[12][9]={
    {up_right,right,down_right,up,right,right,up_left,up_right,up_right},
    {left,left,up_left,down,down,down,up_left,up,up_right},
    {left,left,up_left,left,left,up_left,up_left,left,up_left},
    {down_left,down_left,right,down,down_right,down_right,left,right,right},
    {down_left,down_left,down_right,up,down_left,up,up,left,right},
    {left,down_left,down,down_left,up_left,up_right,up_left,left,up},
    {up,up_right,down,up_left,up_right,up_right,up,down_right,up},
    {up_left,right,right,up_left,up_right,down_right,left,right,up},
    {down_left,down_right,down_right,up_left,down_left,up,up,up_right,up_right},
    {down,down_right,right,down,down_right,down_right,left,right,right},
    {down_left,down_left,down_right,down,down_left,down,down,left,right},
    {left,down_left,down,down_left,up_left,up_right,up_left,left,up}
};
constexpr std::uint16_t retry[3][9]={
    {right,down_right,down,0,up_right,down_left,up_left,left,up},
    {left,right,down,down_left,down_right,0,up_left,up_right,up},
    {left,down_left,down,0,up_left,down_right,up_right,right,up}
};
std::uint16_t toward(Point p,Point target) {
    const unsigned flags=unsigned(motion::wrap(int(target.x)+256)<p.x)|
        (unsigned(motion::wrap(int(target.x)-256)>p.x)<<1)|
        (unsigned(motion::wrap(int(target.y)+1280)<p.y)<<2)|(unsigned(p.y<target.y)<<3);
    switch(flags) {
    case 1:return left;case 2:return right;case 4:return up;case 8:return down;
    case 5:return up|left;case 9:return down|left;case 6:return up|right;case 10:return down|right;
    default:return 0;
    }
}
std::uint16_t away(unsigned pattern,int relative_y,Point player) {
    if(pattern>=12)throw std::runtime_error("unrecovered CPU dodge table alias");
    const unsigned column=player.x>=3840 ? 0 : player.x>=256 ? 1 : 2;
    std::uint16_t direction;
    if(relative_y< -256) {
        if(column==1||player.y>=2048)direction=dodge[pattern][column];
        else direction=column==0 ? left : right;
    } else direction=dodge[pattern][(relative_y<512 ? 3 : 6)+column];
    if(player.y>=4864&&direction==down)direction=player.x>=2048 ? left : right;
    return direction;
}
}
void Round::cpu_update(unsigned pid,CollisionMap& collision,Resident& resident) {
    auto& p=players[pid];const auto origin=p.center;
    if(p.cpu_frame>p.cpu_safety) {
        find_target(pid);const auto direction=toward(origin,target);
        (void)(random.ring()%3);move_player(pid,direction);player_hit(pid,4,collision);
        if(!p.is_hit)return;
        p.is_hit=false;
        if(p.gauge_charged<=1280&&!(random.ring()%4))player_bomb(pid,resident);else p.is_hit=true;
        return;
    }
    if(!(result_frame%4))for(int radius=32;radius<=80;radius+=16) {player_hit(pid,radius,collision);if(p.is_hit)break;}
    std::uint16_t direction;
    if(!p.is_hit) {find_target(pid);direction=toward(origin,target);}
    else {
        const auto dx=motion::wrap(int(collision_top.x)-origin.x),dy=motion::wrap(int(collision_top.y)-origin.y);
        p.is_hit=false;const unsigned pattern=(dx<=-256 ? 0u : dx<=256 ? 1u : 2u)+p.cpu_dodge_strategy*3u;
        cpu_pattern=std::uint8_t(pattern+1);direction=away(pattern,dy,origin);
    }
    std::uint8_t attempt=0;unsigned radius_or_retry=0,retry_region=0;
    for(;;) {
        move_player(pid,direction);player_hit(pid,radius_or_retry ? 4 : 20,collision);
        if(!p.is_hit)break;
        p.is_hit=false;p.center=origin;++attempt;
        if(attempt<9) {
            retry_region=collision_top.x<1280 ? 0 : collision_top.x<2816 ? 1 : 2;
            direction=retry[retry_region][attempt];
        } else if(radius_or_retry<9) {
            if(!attempt) {if(++p.cpu_dodge_strategy>=2)p.cpu_dodge_strategy=0;retry_region=random.ring()%3;}
            direction=retry[retry_region][radius_or_retry++];
        } else {
            if(p.gauge_charged<=1024)player_bomb(pid,resident);else p.is_hit=true;
            break;
        }
    }
}
}
