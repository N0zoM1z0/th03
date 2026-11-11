#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>

namespace th03 {
namespace {
std::int16_t byte(int value) {
    const auto bits=std::uint8_t(value);return std::int16_t(bits<128 ? int(bits) : int(bits)-256);
}
}
void Round::find_target(unsigned pid) {
    if(boss_active[pid]) {target_formation_marker=254;target=boss_target;return;}
    const Enemy* selected=nullptr;std::uint8_t formation=255;
    for(const auto& e:enemies)if(e.flag==1&&e.pid==pid&&e.center.x>=0&&e.center.x<=4608&&e.center.y>=0&&e.center.y<=6144&&e.formation_i<formation) {
        formation=e.formation_i;selected=&e;if(!formation)break;
    }
    target_formation_marker=formation;
    if(!selected) {target={2304,4800};return;}
    target={motion::wrap(int(selected->center.x)-256),motion::wrap(int(selected->center.y)+1760)};
    if(target.x<=0||target.x>=4608||target.y<=0||target.y>=6144)target={2304,4800};
}
void Round::hyper_update(unsigned pid) {
    auto& p=players[pid];
    if(!p.hyper_handler) {p.shot_mode=1;if(p.hyper_active)p.hyper_handler=true;return;}
    const auto character=character_id(p.paletted);
    if(!p.hyper_active) {p.hyper_handler=false;if(character==6)charge_shots.rikako_active[pid]=0;return;}
    switch(character) {
    case 0:p.shot_mode=4;break;
    case 1:p.shot_mode=2;p.shot_active=2;break;
    case 2:p.shot_mode=0;charge_shots.marisa_hyper(*this,pid);break;
    case 3:p.shot_mode=1;if(!(frame&3))charge_shots.ellen_hyper(*this,p.center,pid);return;
    case 4:case 5:case 7:case 8:p.shot_mode=3;break;
    case 6:
        if(p.gauge_avail>4000) {charge_shots.add(*this,p.center,pid);charge_shots.rikako_active[pid]=2;}
        break;
    }
    const bool slow=character==2||character==6;
    for(unsigned axis=0;axis<4;++axis) {
        const int adjustment=axis<2 ? (slow ? -16 : 32) : (slow ? (character==2 ? -12 : -8) : 24);
        movement_speed[axis]=std::uint8_t(movement_speed[axis]+adjustment);
    }
}
void Round::player_lose_update(unsigned pid,Resident& resident) {
    auto& p=players[pid];
    const auto pixel=[](int q4) {return q4>=0 ? q4/16 : -((-q4+15)/16);};
    if(p.lose_time==48) {
        lose_left=std::int16_t(16+int(pid)*320+pixel(p.center.x)+fg_shift[pid]-24);
        lose_top=std::int16_t(pixel(p.center.y)-8);defeat=1;sounds.push_back(14);damage_all[pid^1]=1;lose_radius=0;
    } else lose_radius=motion::wrap(int(lose_radius)+9);
    fg_shift[pid]=(p.lose_time&3)<2 ? 6 : -6;reset_frames=2;
    if(!--p.lose_time) {
        lose_left=lose_top=lose_radius=0;fg_shift[pid]=0;p.lose_time=255;palette_tone=100;defeat=2;
        ++players[pid^1].rounds_won;resident.winner=std::uint8_t(pid^1);result_frame=0;
    } else palette_tone=std::int16_t(100+(result_frame%2)*30);
}
MoveResult movement(std::uint16_t input,const std::array<std::uint8_t,4>& speed,Point& velocity) {
    velocity={};int x=0,y=0;
    switch(input) {
    case left:x=-1;break;
    case down|left:case down_left:x=-1;y=1;break;
    case down:y=1;break;
    case down|right:case down_right:x=1;y=1;break;
    case right:x=1;break;
    case up|right:case up_right:x=1;y=-1;break;
    case up:y=-1;break;
    case up|left:case up_left:x=-1;y=-1;break;
    case 0:return MoveResult::idle;
    default:return MoveResult::invalid;
    }
    velocity.x=byte(x*byte(speed[x&&y ? 2 : 0]));velocity.y=byte(y*byte(speed[x&&y ? 3 : 1]));
    return MoveResult::valid;
}
void move_position(Point& center,Point velocity) {
    center.x=std::clamp<std::int16_t>(motion::wrap(int(center.x)+velocity.x),8<<4,280<<4);
    center.y=std::clamp<std::int16_t>(motion::wrap(int(center.y)+velocity.y),24<<4,352<<4);
}
MoveResult Round::move_player(unsigned pid,std::uint16_t input) {
    const auto result=movement(input,movement_speed,player_velocity);
    if(result==MoveResult::valid)move_position(players[pid].center,player_velocity);
    return result;
}
void Round::player_hit(unsigned pid,int tiles,const CollisionMap& collision) {
    if(const auto hit=collision.hit(pid,players[pid],tiles)) {players[pid].is_hit=true;collision_top=*hit;}
}
std::int8_t Round::hit_damage(unsigned pid,Resident& resident) {
    auto& p=players[pid];auto& other=players[pid^1];
    auto damage=byte(p.hit_damage_next+(p.cpu ? cpu_damage_additional : 0));
    p.hit_damage_next=3;if(other.hit_damage_next>3)--other.hit_damage_next;
    if(p.halfhearts-damage<=0&&p.halfhearts>1)damage=std::int16_t(p.halfhearts-1);
    if(pid==0&&resident.skill)--resident.skill;
    return std::int8_t(damage);
}
void Round::knockback_update(unsigned pid) {
    auto& p=players[pid];
    if(p.knockback_time==64) {
        sounds.push_back(2);p.knockback_angle=std::uint8_t(random.ring()&63);
        if(p.center.x<144*16) {if(p.center.y>184*16)p.knockback_angle=std::uint8_t(p.knockback_angle+192);}
        else p.knockback_angle=std::uint8_t(p.knockback_angle+(p.center.y<184*16 ? 64 : 128));
        p.knockback_length=64;
    }
    if(p.knockback_time>32) {
        p.knockback_length=std::uint8_t(p.knockback_length-2);
        const auto v=motion::polar(p.knockback_angle,p.knockback_length);
        player_velocity={byte(v.x),byte(v.y)};move_position(p.center,player_velocity);
    } else if(!p.knockback_time)p.knockback_active=false;
    --p.knockback_time;
}
void Round::player_update(unsigned pid,std::uint16_t input,CollisionMap& collision,Resident& resident,const PlayerServices& services) {
    auto& p=players[pid];
    if(p.invincibility)--p.invincibility;
    if(damage_all[pid])--damage_all[pid];
    if(defeat!=2) {
        if(!p.lose_time) {
            std::copy_n(p.speeds.begin(),4,movement_speed.begin());
            services.hyper(*this,pid);
            if(!p.move_lock) {
                if(!p.cpu) {
                    auto mask=std::uint16_t(input&0x0f0f);bool first=true;
                    for(;;) {
                        const auto result=move_player(pid,mask);
                        if(result==MoveResult::invalid&&first) {
                            if(p.human_movement_last!=mask) {mask&=std::uint16_t(~p.human_movement_last);first=false;continue;}
                            break;
                        }
                        break;
                    }
                    if(first)p.human_movement_last=mask;
                } else {
                    ++p.cpu_frame;services.cpu(*this,pid);
                    const unsigned period=target_formation_marker==0 ? 6 : target_formation_marker==255 ? 32 : target_formation_marker==254 ? 7 : 10;
                    if(!(result_frame%period)) {shot_release[pid]=4;input=shot;}
                    target_formation_marker=0;
                    if(!p.is_hit) {
                        if(p.bombs||p.halfhearts>3) {
                            if(p.charge_thresholds[p.charge_cursor]<(p.gauge_avail>>4)||p.gauge_avail==4080) {
                                shot_release[pid]=0;input=shot;
                                if(p.gauge_charged>=p.gauge_avail) {
                                    shot_release[pid]=4;input=0;p.charge_cursor=std::uint8_t((p.charge_cursor+1)%64);
                                }
                            }
                        }
                    } else {p.is_hit=false;shot_release[pid]=4;input=0;}
                }
            } else --p.move_lock;
            bool suppress_collision=false;
            if(p.knockback_active) {
                knockback_update(pid);p.gauge_charged=0;p.cpu_frame=0;suppress_collision=true;
            } else if(shot_release[pid]<=2&&!p.hyper_active) {
                if(p.gauge_charged<p.gauge_avail) {
                    p.gauge_charged=std::uint16_t(p.gauge_charged+p.speeds[4]);
                    if(p.gauge_charged>p.gauge_avail) {p.gauge_charged=p.gauge_avail;p.spell_ready_frames=0;}
                    if(p.gauge_charged==384)sounds.push_back(9);
                } else {
                    ++p.spell_ready_frames;if(p.spell_ready_frames>=128)goto fire_charge;
                }
            } else if(shot_release[pid]<=4) {
            fire_charge:
                const auto charged=motion::wrap(p.gauge_charged);
                if(charged>=1024) {
                    services.charge(*this,p.center,pid);
                    if(charged>=2048) {
                        warning[pid]=1;
                        if(charged>=4080) {
                            if(boss_launched_by==pid)goto fire_gauge_bullet;
                            gauge_next[pid]=5;p.gauge_avail=1024;
                            if(boss_level<16)++boss_level;
                            combo_points_for_boss_attack=std::uint16_t(combo_points_for_boss_attack+10240);
                            if(boss_launched_by==255)++p.boss_attacks;else ++p.boss_reversals;
                        } else if(charged>=3072) {
                        fire_gauge_bullet:
                            ++p.gauge_attacks;gauge_next[pid]=3;p.gauge_avail=std::uint16_t(p.gauge_avail-2048);
                            if(gauge_levels[pid]<16)++gauge_levels[pid];
                        } else {
                            ++p.gauge_attacks;gauge_next[pid]=1;p.gauge_avail=std::uint16_t(p.gauge_avail-1024);
                            if(gauge_levels[pid]<16)++gauge_levels[pid];
                        }
                    }
                    p.invincibility=std::uint8_t(p.invincibility+6);suppress_collision=true;
                }
                p.gauge_charged=0;
            }
            if(p.shot_active==2)input=0;
            if(!p.move_lock&&p.shot_active) {
                if(((input&shot)||p.shot_active==2)&&shot_release[pid]>2) {add_shots(pid);shot_release[pid]=0;}
                else if(!(input&shot)&&shot_release[pid]<8)++shot_release[pid];
                if(input&bomb)services.bomb(*this,pid);
                if(p.shot_active==2)p.shot_active=1;
            }
            if(p.hyper_active) {
                if(p.gauge_avail>1024)p.gauge_avail=std::uint16_t(p.gauge_avail-6);
                else {p.hyper_active=0;p.gauge_avail=1024;}
                suppress_collision=true;
            }
            if(!defeat&&!suppress_collision) {
                player_hit(pid,4,collision);
                if(p.is_hit) {
                    if(p.halfhearts) {
                        player_circle(p.center,std::uint8_t(pid));
                        p.halfhearts=std::int8_t(byte(p.halfhearts-hit_damage(pid,resident)));
                        if(p.halfhearts<0)p.halfhearts=0;
                        if(!p.halfhearts) {p.lose_time=48;defeated_player=std::uint8_t(pid);}
                        else {p.knockback_active=true;p.knockback_time=64;p.invincibility=110;p.move_lock=64;}
                    }
                    p.is_hit=false;
                }
            }
        } else if(p.lose_time!=255)services.lose(*this,pid);
    }
    // The shared velocity deliberately survives locked/loss paths and may
    // still contain the preceding player's movement when selecting this cel.
    p.pattern_movement=player_velocity.x==0 ? 0 : player_velocity.x<0 ? 1 : 2;
    p.pattern_glow=0;
    if(page_back)p.pattern_glow=p.hyper_active ? 2 : p.invincibility ? 1 : 0;
}
}
