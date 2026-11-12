#include "boss.hpp"
#include "round.hpp"
#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
Point orbit(Point center,std::uint8_t angle,int length) {
    const auto v=motion::polar(angle,motion::wrap(length));
    return {motion::wrap(int(center.x)+v.x),motion::wrap(int(center.y)+v.y)};
}
void restore(Round& r,unsigned pid) {std::copy_n(r.palette_backup.begin()+pid*3,3,r.palette.begin()+pid*3);}
}
void Bosses::reimu_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;
    s.hp=110;s.sprite=std::uint16_t(0x28c+pid*40);
}
bool Bosses::start(Round& r,unsigned pid) {
    if(r.gauge_flags[pid]!=5)return false;
    if(r.boss_launched_by==255) {
        state=templates[pid];state.count=std::uint8_t(1+(r.random.ring()&7));frame=0;
        r.boss_launched_by=std::uint8_t(pid);r.gauge_flags[pid]=0;r.sounds.push_back(18);
        restore(r,pid^1);r.boss_active[pid^1]=1;return true;
    }
    if(state.mode==255)return false;
    state.mode=255;frame=0;restore(r,pid^1);r.boss_active[pid]=0;return false;
}
void Bosses::move_sine() {
    auto& s=state;s.center.x=motion::wrap(int(s.center.x)+s.velocity.x);s.center.y=motion::wrap(int(s.center.y)+s.velocity.y);
    ++s.angle;s.velocity.y=motion::wrap(motion::floor_shift8(16*motion::sine(s.angle)));
    if(s.center.x<=768)s.velocity.x=32;else if(s.center.x>=3840)s.velocity.x=-32;
}
void Bosses::fall(Round& r,unsigned pid) {
    auto& s=state;s.center.x=motion::wrap(int(s.center.x)+s.velocity.x);s.center.y=motion::wrap(int(s.center.y)+32);
    if(s.center.x<=768)s.velocity.x=32;else if(s.center.x>=3840)s.velocity.x=-32;
    r.boss_active[pid^1]=0;
    if(s.center.y>=6656) {s.mode=0;r.boss_launched_by=255;r.combo_points_for_boss_attack=5120;}
}
void Bosses::next_pattern(Round& r) {
    move_sine();if(frame<80)return;
    std::uint8_t choice;
    do {choice=std::uint8_t(r.random.ring()&15);}while(int(previous)+2>=choice&&int(previous)-2<=choice);
    previous=choice;frame=0;state.mode=std::uint8_t(2+choice);++state.pattern;
    if(state.pattern>state.count)state.mode=128;
}
void Bosses::hit_end(Round& r,unsigned pid) {
    if(state.hp>0||state.mode==255)return;
    state.mode=255;frame=0;restore(r,pid^1);
    if(r.gauge_flags[pid^1]!=5)r.combo_points_for_boss_attack=5120;
    r.boss_active[pid^1]=0;if(r.boss_level<16)++r.boss_level;
}
void Bosses::prepare_render(Round& r,unsigned pid) {
    if(r.boss_launched_by!=pid)return;
    if(state.mode==255) {
        if(frame==1)r.sounds.push_back(16);
        if(motion::wrap(int(frame)*8)>=200) {r.score_add(pid^1,2560);state.mode=0;r.boss_launched_by=255;if(character_id(r.players[pid].paletted)==7)restore(r,pid^1);}
    } else if(!state.mode&&character_id(r.players[pid].paletted)==7) {
        if(r.frame%2&&frame<64)return;
        state.effect_radius=std::uint16_t((frame<32 ? 256 : frame<64 ? 512 : 768)-int(frame)*8);
        state.move_phase=std::uint8_t(state.move_phase+(frame>=32&&frame<64 ? -4 : 4));
    } else if(!state.mode&&character_id(r.players[pid].paletted)==4) {
        if(r.frame%2&&frame<64)return;
        state.move_phase=std::uint8_t(state.move_phase+2);state.effect_radius=std::uint16_t((200-int(frame)*2)*16);state.render_mode=0;
    } else if(state.mode&&character_id(r.players[pid].paletted)==1&&!state.hit) {
        if(state.render_mode==5)state.render_frame=0;
        if(state.render_mode==2||state.render_mode==5) {if(state.render_frame>=32)state.render_mode=3;++state.render_frame;}
    }
}
void Bosses::reimu_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.mode=1;frame=0;};
    const auto bullet=[&](unsigned speed) {t.type=2;t.speed=std::uint8_t(speed);t.pid=std::uint8_t(other);t.center=s.center;};
    if(s.mode>=2&&s.mode<=6) {
        if(!frame) {s.scratch={s.center.x,motion::wrap(int(s.center.y)+768)};reimu_direction=std::uint8_t(r.random.ring()&1);reimu_speed=16;}
        auto angle=std::uint8_t(frame*2);if(reimu_direction)angle=std::uint8_t(-angle);
        if(!(frame%parameters[0])) {
            t.type=4;t.group=0;t.pid=std::uint8_t(other);t.angle=std::uint8_t(angle*2);t.speed=reimu_speed;t.center=orbit(s.center,angle,512);add();
            t.angle=std::uint8_t(angle*2+128);angle=std::uint8_t(angle+128);t.center=orbit(s.center,angle,512);add();
        }
        if(!(frame%2))++reimu_speed;
        s.center.y=orbit(s.scratch,std::uint8_t(frame*2-64),768).y;
        if(frame>=128)finish();
    } else if(s.mode==8||s.mode==9||s.mode==10||s.mode==13) {
        move_sine();bullet(parameters[2]);
        if(frame<64) {
            if(r.frame%16)return;
            t.angle=32;t.group=8;add();t.angle=96;add();return;
        }
        if(frame<100) {if(r.frame%16)return;t.group=21;t.angle=64;add();}else finish();
    } else if(s.mode>=15&&s.mode<=17) {
        move_sine();
        if(!frame) {s.render_mode=1;reimu_angle=std::uint8_t(r.random.ring());}
        if(frame<80) {
            for(unsigned i=0;i<parameters[3];++i)reimu_orbit[i]=orbit(s.center,std::uint8_t(i*256/parameters[3]+reimu_angle),frame<24 ? frame*32 : 768);
            reimu_angle=std::uint8_t(reimu_angle+8);
            if(frame>=24&&!(r.frame%16)) {bullet(parameters[4]);t.angle=std::uint8_t(r.random.ring());t.group=38;t.count=parameters[5];add();}
        } else if(frame==80) {
            for(unsigned i=0;i<parameters[3];++i)r.extra_attacks.special(r,reimu_orbit[i],pid,std::uint8_t(i*256/parameters[3]+reimu_angle));
            finish();s.render_mode=0;
        }
    } else if(s.mode==7||s.mode==11||s.mode==12||s.mode==14) {
        move_sine();
        if(frame<128) {
            if(frame%16)return;
            bullet(parameters[2]);t.angle=std::uint8_t(frame);t.group=14;add();t.angle=std::uint8_t(120-std::uint8_t(frame));add();
        } else finish();
    } else if(s.mode==128)fall(r,pid);
}
void Bosses::update_reimu(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;
        parameters[0]=std::uint8_t(5-level/5);parameters[1]=std::uint8_t(level+24);parameters[2]=std::uint8_t(level*2+40);
        parameters[3]=std::uint8_t(level/8+4);parameters[4]=std::uint8_t(level+16);parameters[5]=std::uint8_t(level+16);
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;
    if(!state.mode) {if(frame!=100)return;frame=0;state.mode=1;}
    if(state.mode==1)next_pattern(r);
    reimu_pattern(r,pid);if(state.mode==255)return;
    hit(r,pid,collision,charge);
}
void Bosses::hit(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge,int width,int height,int radius) {
    const unsigned other=pid^1;const auto center=state.center;
    collision.rectangle(other,center,width,height);
    const Hitbox box{{motion::wrap(int(center.x)-radius),motion::wrap(int(center.y)-radius)},
        {motion::wrap(int(center.x)+radius),motion::wrap(int(center.y)+radius)},std::uint8_t(other),{std::int16_t(radius),std::int16_t(radius)}};
    state.hit=r.hitbox_hits(box,center.y,charge,Against::enemy,true);state.hp=motion::wrap(int(state.hp)-state.hit);hit_end(r,pid);
}
void Bosses::mima_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;
    s.hp=110;s.sprite=std::uint16_t(0x28c+pid*40);
}
void Bosses::mima_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.render_mode=0;s.mode=1;frame=0;};
    if(s.mode>=2&&s.mode<=5) {
        if(frame<2) {s.render_mode=2;s.render_frame=0;mima_angles[0]=0;mima_angles[1]=192;return;}
        if(frame<32)return;
        if(!(frame%2)) {
            r.sounds.push_back(3);t.angle=mima_angles[0];t.group=34;t.center=s.center;t.speed=parameters[0];t.type=2;t.animated=false;add();t.animated=true;
            mima_angles[0]=std::uint8_t(mima_angles[0]+9);
            if(frame<parameters[5]&&!(frame%6)) {t.type=1;t.group=15;t.speed=parameters[4];t.angle=mima_angles[1];add();t.angle=std::uint8_t(128-mima_angles[1]);add();}
            mima_angles[1]=std::uint8_t(mima_angles[1]+3);
        }
        if(frame>130)finish();
    } else if(s.mode>=6&&s.mode<=10) {
        if(frame==16)s.render_mode=5;else if(frame<32)return;
        const Point center{motion::wrap(int(s.center.x)+384),motion::wrap(int(s.center.y)-512)};
        if(frame==32||frame==36||frame==40) {r.effect_add(center,other,Effect::center);return;}
        if(frame<=48)return;
        if(!(frame%4)) {
            t.angle=0;t.group=28;t.center=center;t.count=parameters[1];t.speed=parameters[2];t.type=2;t.animated=false;add();t.type=1;add();t.animated=true;
        }
        if(frame==64) {t.angle=std::uint8_t(r.random.ring());t.group=37;t.center=center;t.speed=32;t.type=2;t.animated=false;add();t.animated=true;}
        if(!(frame%2))r.sounds.push_back(3);
        if(frame>=128)finish();
    } else if(s.mode>=11&&s.mode<=13) {
        const auto remainder=std::uint8_t(frame%parameters[3]);move_sine();s.render_mode=5;
        if(remainder==1||remainder==parameters[3]/2) {
            t.group=remainder==parameters[3]/2 ? 18 : 24;r.sounds.push_back(10);t.angle=0;
            t.center={motion::wrap(int(s.center.x)+384),motion::wrap(int(s.center.y)-512)};
            t.speed=88;t.type=2;t.animated=false;t.has_trail=true;add();t.has_trail=false;t.animated=true;
        }
        if(frame>=150)finish();
    } else if(s.mode>=14&&s.mode<=17) {
        move_sine();
        if(frame==1) {mima_angles[2]=(r.random.ring()&1) ? 7 : std::uint8_t(-7);mima_angles[3]=std::uint8_t(r.random.ring());}
        if(!(frame%2)) {t.center=orbit(s.center,mima_angles[3],768);t.angle=std::uint8_t(mima_angles[3]+64);t.type=4;t.group=33;t.speed=parameters[6];add();r.sounds.push_back(10);mima_angles[3]=std::uint8_t(mima_angles[3]+mima_angles[2]);}
        if(frame>=72) {s.mode=1;frame=0;}
    }
}
void Bosses::update_mima(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;
        parameters={{std::uint8_t(32+level),std::uint8_t(2+level/4),std::uint8_t(32+level),std::uint8_t(64-2*level),
            std::uint8_t(40+level),std::uint8_t(64+level*4),std::uint8_t(54+level)}};
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    r.bullets.model.pid=std::uint8_t(pid^1);++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:mima_pattern(r,pid);break;
    }
    hit(r,pid,collision,charge);
}

void Bosses::init_template(unsigned pid,unsigned character) {
    switch(character) {
    case 0:reimu_template(pid);return;
    case 1:mima_template(pid);return;
    case 2:marisa_template(pid);return;
    case 3:ellen_template(pid);return;
    case 4:kotohime_template(pid);return;
    case 5:kana_template(pid);return;
    case 6:rikako_template(pid);return;
    case 7:chiyuri_template(pid);return;
    case 8:yumemi_template(pid);return;
    default:throw std::runtime_error("unimplemented Boss template");
    }
}
void Bosses::update(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    switch(character_id(r.players[pid].paletted)) {
    case 0:update_reimu(r,pid,collision,charge);return;
    case 1:update_mima(r,pid,collision,charge);return;
    case 2:update_marisa(r,pid,collision,charge);return;
    case 3:update_ellen(r,pid,collision,charge);return;
    case 4:update_kotohime(r,pid,collision,charge);return;
    case 5:update_kana(r,pid,collision,charge);return;
    case 6:update_rikako(r,pid,collision,charge);return;
    case 7:update_chiyuri(r,pid,collision,charge);return;
    case 8:update_yumemi(r,pid,collision,charge);return;
    default:throw std::runtime_error("unimplemented Boss update");
    }
}
void Bosses::marisa_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;
    s.hp=110;s.sprite=std::uint16_t(0x280+pid*40);
}
void Bosses::marisa_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.render_mode=0;s.mode=1;frame=0;};
    if(s.mode>=2&&s.mode<=5) {
        s.render_mode=1;if(frame<32)return;if(frame==32)marisa_angle=0;
        if(frame<80) {
            if(!(frame%4)) {t.angle=marisa_angle;t.group=34;t.center=s.center;t.speed=parameters[0];t.type=2;t.pid=std::uint8_t(other);add();t.speed=std::uint8_t(parameters[0]/2);add();marisa_angle=std::uint8_t(marisa_angle+7);}
        } else finish();
    } else if(s.mode==6||s.mode==7||s.mode==17||(s.mode>=8&&s.mode<=10)) {
        const bool wide=s.mode>=8&&s.mode<=10;s.render_mode=1;if(frame<56)return;
        constexpr int columns[2][4][2]={{{512,4096},{1280,3328},{2048,2560},{0,0}},{{128,4480},{896,3712},{1664,2944},{2432,2176}}};
        if(frame>=64&&frame<=112&&!(frame%16)&&(wide||frame<112)) {
            const unsigned i=(frame-64)/16;
            r.extra_attacks.special(r,{std::int16_t(columns[wide][i][0]),5888},pid);
            r.extra_attacks.special(r,{std::int16_t(columns[wide][i][1]),5888},pid);return;
        }
        if(frame==(wide ? 132 : 112))finish();
    } else if(s.mode>=11&&s.mode<=16) {
        move_sine();
        if(!(frame%32)) {
            t.angle=std::uint8_t(r.random.ring());t.group=38;t.center=s.center;t.pid=std::uint8_t(other);
            if(r.boss_level<8)t.count=parameters[1];
            else {t.speed=parameters[3];t.count=parameters[4];t.type=2;add();t.angle=std::uint8_t(t.angle+256/parameters[4]);t.count=parameters[5];}
            t.speed=parameters[2];t.type=4;add();
        }
        if(frame>=130) {s.mode=1;frame=0;}
    }
}
void Bosses::update_marisa(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;parameters[0]=std::uint8_t(level*2+50);parameters[1]=std::uint8_t(level*2+24);parameters[2]=std::uint8_t(level+32);
        parameters[3]=std::uint8_t(level+10);parameters[4]=parameters[5]=std::uint8_t(level+22);
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:marisa_pattern(r,pid);break;
    }
    hit(r,pid,collision,charge);
}

void Bosses::ellen_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=s.render_frame=s.move_phase=0;
    s.hp=100;s.sprite=std::uint16_t(0x780+pid*40);
}
void Bosses::ellen_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    if(s.mode>=2&&s.mode<=5) {
        if(frame==16||frame==20) {r.effect_add(s.center,other,Effect::center);return;}
        if(frame==24) {r.effect_add(s.center,other,Effect::center);ellen_angles[0]=64;return;}
        if(frame<28)return;
        t.angle=ellen_angles[0];t.group=34;t.center=s.center;t.speed=parameters[0];t.type=2;t.pid=std::uint8_t(other);t.sprite=std::uint16_t(8+pid*640);
        if(frame<36) {
            if(!(frame%2)) {r.sounds.push_back(3);add();ellen_angles[0]=std::uint8_t(ellen_angles[0]+8);}
        } else if(frame==36) {
            r.sounds.push_back(3);
            for(unsigned i=0;i<8;++i) {add();ellen_angles[0]=std::uint8_t(ellen_angles[0]+8);t.angle=ellen_angles[0];}
        } else if(frame<=44&&!(frame%2)) {r.sounds.push_back(3);add();ellen_angles[0]=std::uint8_t(ellen_angles[0]+8);}
        if(frame>=44) {s.render_mode=0;s.mode=1;frame=0;}
    } else if(s.mode>=6&&s.mode<=10) {
        s.render_frame=std::uint8_t(s.render_frame+3);if(frame<32)return;
        if(frame==32||frame==36||frame==40) {r.effect_add(s.center,other,Effect::center);return;}
        if(frame==48||frame==96) {
            auto angle=std::uint8_t(r.random.ring());
            for(unsigned i=0;i<parameters[1];++i) {r.extra_attacks.special(r,s.center,pid,angle,frame==48 ? 2 : 254);angle=std::uint8_t(angle+256/parameters[1]);}
            if(frame==96) {s.mode=1;frame=0;}
        }
    } else if(s.mode>=11&&s.mode<=17) {
        move_sine();
        if(frame%parameters[3]==1) {
            r.sounds.push_back(10);t.group=14;t.center=s.center;t.angle=ellen_angles[1];t.speed=parameters[2];t.type=1;t.pid=std::uint8_t(other);add();
            t.angle=std::uint8_t(ellen_angles[1]+128);add();t.speed=std::uint8_t(parameters[2]/2);add();t.angle=ellen_angles[1];add();ellen_angles[1]=std::uint8_t(ellen_angles[1]+16);
        }
        if(frame>=96) {s.mode=1;frame=0;}
    }
}
void Bosses::update_ellen(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;parameters[0]=std::uint8_t(level*2+50);parameters[1]=std::uint8_t(level/10+4);
        parameters[2]=std::uint8_t(level+48);parameters[3]=std::uint8_t(10-level/3);
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++state.render_frame;++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:ellen_pattern(r,pid);break;
    }
    hit(r,pid,collision,charge,20,24,384);
}

void Bosses::kotohime_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;s.effect_radius=0;
    s.hp=110;s.sprite=std::uint16_t(0x288+pid*40);
}
void Bosses::kotohime_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    if(s.mode>=12&&s.mode<=14) {
        move_sine();
        if(frame%parameters[5]==1) {
            r.sounds.push_back(3);t.type=1;t.angle=std::uint8_t(frame);t.speed=parameters[4];t.group=38;t.count=4;
            constexpr int x[5]={-768,-384,0,384,768},y[5]={0,192,384,192,0};
            for(unsigned i=0;i<5;++i) {t.center={motion::wrap(int(s.center.x)+x[i]),motion::wrap(int(s.center.y)+y[i])};add();}
        }
        if(frame>=96) {s.mode=1;frame=0;}return;
    }
    const bool random=s.mode>=2&&s.mode<=6,aimed=s.mode>=7&&s.mode<=9;
    const bool radial=s.mode==10||s.mode==11||(s.mode>=15&&s.mode<=17);
    if(!random&&!aimed&&!radial)return;
    if(frame==1) {s.render_mode=1;s.effect_radius=0;s.render_frame=0;if(aimed)s.move_phase=0;}
    s.move_phase=std::uint8_t(s.move_phase+(random ? 4 : aimed ? -2 : -4));
    if(motion::wrap(s.effect_radius)<=1024) {move_sine();s.effect_radius=std::uint16_t(s.effect_radius+32);return;}
    s.render_mode=2;
    if(!random)s.effect_radius=std::uint16_t(s.effect_radius+8);
    s.move_phase=std::uint8_t(s.move_phase+(random||aimed ? 2 : -2));++s.render_frame;
    if(s.render_frame<=64)return;
    const auto emit=[&](bool randomize) {
        t.type=2;
        for(unsigned i=0;i<parameters[1];++i) {
            if(randomize)t.angle=std::uint8_t(r.random.ring());
            t.center=orbit(s.center,std::uint8_t(i*256/parameters[1]+s.move_phase),motion::wrap(s.effect_radius));add();
        }
    };
    if(random) {t.group=36;t.speed=parameters[0];emit(true);}
    else if(aimed) {t.group=5;t.angle=0;t.speed=parameters[3];emit(false);t.group=24;t.angle=0;t.speed=parameters[2];emit(false);}
    else {
        t.group=0;t.type=2;
        for(unsigned i=0;i<parameters[1];++i) {
            const auto angle=std::uint8_t(s.move_phase+i*256/parameters[1]);t.center=orbit(s.center,angle,motion::wrap(s.effect_radius));
            for(unsigned j=0;j<parameters[6];++j) {t.angle=std::uint8_t(64+angle+j*128/parameters[6]);t.speed=std::uint8_t(16+j*48/parameters[6]);add();}
        }
    }
    r.sounds.push_back(3);s.render_mode=0;s.mode=1;frame=0;
}
void Bosses::update_kotohime(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto half=r.boss_level/2;
        parameters={{std::uint8_t(16+half),std::uint8_t(6+r.boss_level/3),std::uint8_t(16+half),std::uint8_t(32+half),
            std::uint8_t(24+half),std::uint8_t(32-half),std::uint8_t(8+half)}};
    }
    if(r.boss_launched_by!=pid)return;
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    r.bullets.model.pid=std::uint8_t(pid^1);++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:kotohime_pattern(r,pid);break;
    }
    hit(r,pid,collision,charge,32,24,512);
}

void Bosses::kana_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;s.effect_radius=0;
    s.hp=100;s.sprite=std::uint16_t(0x288+pid*40);
}
void Bosses::kana_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.render_mode=0;frame=0;s.mode=1;};
    const auto explosion=[&] {r.effect_add(s.center,other,Effect::explosion);};
    const auto ring=[&](unsigned speed,unsigned count) {t.speed=std::uint8_t(speed);t.count=std::uint8_t(count);add();r.sounds.push_back(10);};
    if(s.mode>=13&&s.mode<=15) {
        move_sine();
        if(!(frame%parameters[4])) {
            auto angle=std::uint8_t((r.random.ring()&31)-16);if(r.random.ring()&1)angle=std::uint8_t(128-angle);
            r.extra_attacks.special(r,s.center,pid,angle);t.type=4;t.group=38;t.count=parameters[5];t.center=s.center;t.speed=48;add();r.sounds.push_back(10);
        }
        if(frame>100)finish();
        return;
    }
    if(frame==1) {s.render_mode=1;return;}
    const bool rotating=s.mode==5||s.mode==6||s.mode==16||s.mode==17;
    if(frame==16) {
        s.render_frame=0;s.render_mode=2;r.effect_add(s.center,other,Effect::center);
        if(rotating) {kana_angles[0]=192;constexpr std::uint8_t deltas[4]={253,255,1,3};kana_angles[1]=deltas[r.random.ring()&3];}
        return;
    }
    if(s.mode>=2&&s.mode<=4) {
        if(frame==40) {
            explosion();for(auto angle:{224,8,120,160})r.extra_attacks.special(r,s.center,pid,std::uint8_t(angle));
            t.type=7;t.group=38;t.count=parameters[0];t.acceleration=128;t.center=s.center;t.speed=48;add();r.sounds.push_back(10);return;
        }
        if(frame>80)finish();
    } else if(s.mode>=7&&s.mode<=12) {
        if(frame>=40&&frame<80) {
            t.type=2;t.group=38;t.center=s.center;
            if(frame==40) {explosion();ring(16,parameters[1]);return;}
            if(frame==64) {
                explosion();ring(40,parameters[2]);t.type=1;t.angle=32;t.speed=16;t.group=34;
                for(unsigned i=0;i<16;++i) {add();t.angle=std::uint8_t(t.angle+6);t.speed=std::uint8_t(t.speed+3);}return;
            }
            if(frame==72) {explosion();ring(56,parameters[3]);return;}
            return;
        }
        if(frame>96)finish();
    } else if(rotating) {
        if(frame>=32&&frame<108) {
            if(!(frame%4)) {t.type=2;t.group=38;t.count=5;t.center=s.center;t.speed=parameters[6];t.angle=kana_angles[0];add();r.sounds.push_back(10);}
            if(frame>64)kana_angles[0]=std::uint8_t(kana_angles[0]+kana_angles[1]);
            return;
        }
        if(frame>112)finish();
    }
}
void Bosses::update_kana(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;const auto half=level/2;
        parameters={{std::uint8_t(half+16),std::uint8_t(half+24),std::uint8_t(half+16),std::uint8_t(half+20),
            std::uint8_t(32-level),std::uint8_t(half+24),std::uint8_t(level+64)}};
    }
    if(r.boss_launched_by!=pid)return;
    r.bullets.model.pid=std::uint8_t(pid^1);
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:kana_pattern(r,pid);break;
    }
    ++state.render_frame;hit(r,pid,collision,charge,32,24,512);
}

void Bosses::rikako_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=0;s.effect_radius=0;s.spin=4;
    s.hp=110;s.sprite=std::uint16_t(0x286+pid*40);
}
void Bosses::rikako_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {frame=0;s.mode=1;};
    if(s.mode>=2&&s.mode<=5) {
        if(s.spin<=8&&!(frame%8))++s.spin;
        if(frame==16)r.effect_add(s.center,other,Effect::center);
        else if(frame==40) {
            r.effect_add(s.center,other,Effect::explosion);t.type=2;t.group=22;t.speed=28;
            const int delta=(r.random.ring()&1) ? 48 : -48;
            for(unsigned i=0;i<parameters[0];++i) {const auto angle=std::uint8_t(i*256/parameters[0]);t.center=orbit(s.center,angle,768);t.angle=std::uint8_t(angle+delta);add();}
            r.sounds.push_back(5);
        } else if(frame>80)finish();
    } else if(s.mode>=7&&s.mode<=12) {
        if(s.spin>=-8&&!(frame%8))--s.spin;
        if(frame==16)r.effect_add(s.center,other,Effect::axis);
        else if(frame==40) {
            r.effect_add(s.center,other,Effect::explosion);r.random.ring();
            for(unsigned i=0;i<parameters[1];++i)r.extra_attacks.special(r,s.center,pid,std::uint8_t(i*256/parameters[1]));
            r.sounds.push_back(5);
        } else if(frame==64) {
            t.type=1;t.group=38;t.count=parameters[2];t.center=s.center;t.speed=32;
            for(unsigned i=0;i<4;++i) {t.angle=std::uint8_t(r.random.ring());t.speed=std::uint8_t(t.speed+8);add();}
            r.sounds.push_back(10);
        } else if(frame>80)finish();
    } else if(s.mode==6||(s.mode>=13&&s.mode<=17)) {
        move_sine();if(s.spin!=2&&!(frame%8))s.spin=std::int8_t(s.spin+(s.spin>2 ? -1 : 1));
        const auto remainder=std::uint8_t(frame%parameters[3]);
        if(remainder==1) {rikako_angles[0]=std::uint8_t(r.random.ring());rikako_angles[1]=std::uint8_t((r.random.ring()&1)+1);}
        t.type=rikako_angles[1];t.group=14;t.center=s.center;t.angle=rikako_angles[0];t.speed=parameters[4];
        if(remainder==1||remainder==5||remainder==9||remainder==13) {r.sounds.push_back(10);add();t.angle=std::uint8_t(rikako_angles[0]+128);add();}
        if(frame>=128)finish();
    }
}
void Bosses::update_rikako(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;parameters[0]=std::uint8_t(level/2+16);parameters[1]=std::uint8_t(level/4+8);
        parameters[2]=std::uint8_t(level/2+28);parameters[3]=std::uint8_t(32-level);parameters[4]=std::uint8_t(level+64);
    }
    if(r.boss_launched_by!=pid)return;
    r.bullets.model.pid=std::uint8_t(pid^1);
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;
    switch(state.mode) {
    case 0:if(frame!=100)return;frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:rikako_pattern(r,pid);break;
    }
    state.render_frame=std::uint8_t(state.render_frame+state.spin);hit(r,pid,collision,charge,32,24,512);
}

void Bosses::chiyuri_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=s.move_phase=0;s.effect_radius=0;
    s.hp=140;s.sprite=std::uint16_t(0x288+pid*40);
}
void Bosses::chiyuri_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.mode=1;frame=0;s.render_mode=32;};
    const auto axis=[&](int x,int y) {r.effect_add({motion::wrap(x),motion::wrap(y)},other,Effect::axis);};
    if(s.mode>=2&&s.mode<=5) {
        if(frame%parameters[1]!=1)return;
        if(frame==1) {
            chiyuri_angles={{224,0}};axis(s.center.x-896,s.center.y);axis(s.center.x+896,s.center.y);axis(s.center.x,s.center.y-896);axis(s.center.x,s.center.y+896);
        } else if(frame>=128)finish();
        t.type=1;t.group=0;t.speed=parameters[0];
        if(!chiyuri_angles[1]) {chiyuri_angles[0]=std::uint8_t(chiyuri_angles[0]+8);if(chiyuri_angles[0]==32)chiyuri_angles={{36,1}};}
        else {chiyuri_angles[0]=std::uint8_t(chiyuri_angles[0]-8);if(chiyuri_angles[0]==228)chiyuri_angles={{224,0}};}
        constexpr int x[4]={896,0,-896,0},y[4]={0,896,0,-896};t.angle=chiyuri_angles[0];
        for(unsigned i=0;i<4;++i) {t.center={motion::wrap(s.center.x+x[i]),motion::wrap(s.center.y+y[i])};if(i)t.angle=std::uint8_t(t.angle+64);add();}
    } else if(s.mode>=6&&s.mode<=9) {
        if(frame%parameters[3]!=1)return;
        axis(s.center.x,s.center.y);if(frame>=128)finish();
        t.center=s.center;t.angle=std::uint8_t(r.random.ring());t.type=2;t.group=37;t.speed=parameters[2];add();
        if(r.boss_level>=8) {
            t.type=1;t.group=35;t.speed=std::uint8_t(parameters[2]/4);
            t.center.x=motion::wrap(s.center.x+896);add();t.center.x=motion::wrap(s.center.x-896);add();
            t.center.x=s.center.x;t.center.y=motion::wrap(s.center.y+896);add();t.center.y=motion::wrap(s.center.y-896);add();
        }
    } else if(s.mode>=10&&s.mode<=13) {
        if(!(frame%8))axis(s.center.x,s.center.y);
        if(frame==48) {t.center=s.center;t.angle=std::uint8_t(r.random.ring());t.type=2;t.group=38;t.count=48;t.speed=parameters[4];t.has_trail=true;add();t.has_trail=false;finish();}
    } else if(s.mode>=14&&s.mode<=17) {
        const auto count=parameters[6];
        if(frame==32) {
            axis(s.center.x-896,s.center.y);axis(s.center.x+896,s.center.y);t.center.y=s.center.y;t.group=0;t.type=1;t.speed=parameters[5];
            for(unsigned pass=0;pass<2;++pass)for(unsigned i=0;i<count;++i) {
                t.center.x=motion::wrap(s.center.x-896+(i*112/count)*16);t.angle=std::uint8_t(96-i*64/count);add();t.angle=std::uint8_t(-t.angle);add();t.speed=std::uint8_t(t.speed+(pass ? -2 : 2));
            }
        } else if(frame==64) {
            axis(s.center.x,s.center.y-896);axis(s.center.x,s.center.y+896);t.center.x=s.center.x;t.type=1;t.group=34;t.speed=parameters[5];
            for(unsigned pass=0;pass<2;++pass)for(unsigned i=0;i<count;++i) {
                t.center.y=motion::wrap(s.center.y-896+(i*112/count)*16);t.angle=std::uint8_t(i*64/count-32);add();t.speed=std::uint8_t(t.speed+(pass ? -2 : 2));
            }
            finish();
        }
    }
}
void Bosses::update_chiyuri(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;parameters={{std::uint8_t(48+level),std::uint8_t(6-level/4),std::uint8_t(52+level),std::uint8_t(32-level),
            std::uint8_t(56+level*2),std::uint8_t(16+level),std::uint8_t(12+level/2)}};
    }
    if(r.boss_launched_by!=pid)return;
    const unsigned other=pid^1;
    const auto gray=[&](unsigned level) {std::fill_n(r.palette.begin()+other*3,3,std::uint8_t(level));};
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    r.bullets.model.animated=false;r.bullets.model.pid=std::uint8_t(other);++frame;
    switch(state.mode) {
    case 0:
        if(frame==96) {frame=0;state.mode=1;gray(255);state.move_phase=state.render_mode=16;break;}
        if(frame==80) {
            constexpr int x[4]={-896,896,0,0},y[4]={0,0,-896,896};
            for(unsigned i=0;i<4;++i)r.effect_add({motion::wrap(state.center.x+x[i]),motion::wrap(state.center.y+y[i])},other,Effect::center);
            break;
        }
        r.bullets.model.animated=true;return;
    case 1:
        if(state.render_mode==16) {constexpr Point positions[5]={{768,1792},{1536,1536},{2304,1280},{3072,1536},{3840,1792}};state.center=positions[r.random.ring()%5];state.move_phase=16;}
        if(frame>=48) {frame=0;state.mode=std::uint8_t(2+(r.random.ring()&15));++state.pattern;if(state.pattern>state.count)state.mode=128;}
        break;
    case 128:fall(r,pid);restore(r,other);break;
    case 255:r.bullets.model.animated=true;return;
    default:chiyuri_pattern(r,pid);break;
    }
    r.bullets.model.animated=true;state.render_frame=std::uint8_t((state.render_frame+(!(r.result_frame%4)))&3);
    if(state.move_phase) {--state.move_phase;if(state.move_phase)gray(16*state.move_phase);}
    if(state.render_mode)--state.render_mode;
    hit(r,pid,collision,charge,32,24,512);
}

void Bosses::yumemi_template(unsigned pid) {
    auto& s=templates[pid];s.center={2304,1280};s.velocity={-32,0};s.angle=s.hit=s.mode=s.pattern=s.render_mode=s.render_frame=s.move_phase=0;s.effect_radius=0;
    s.hp=130;s.sprite=std::uint16_t(0x288+pid*40);
}
void Bosses::yumemi_pattern(Round& r,unsigned pid) {
    auto& s=state;auto& t=r.bullets.model;const unsigned other=pid^1;
    const auto add=[&] {r.bullets.add(r,pid*40);};
    const auto finish=[&] {s.mode=1;frame=0;};
    const auto effect=[&](Point p,Effect kind=Effect::axis) {r.effect_add(p,other,kind);};
    if(s.mode>=2&&s.mode<=4) {
        if(frame==1) {s.render_mode=1;yumemi_state[2]=std::uint8_t(r.random.ring());yumemi_state[0]=0;s.effect_radius=256;yumemi_state[1]=(r.random.ring()&1) ? 253 : 3;}
        if(frame<4) {effect(yumemi_origin);return;}if(frame<32)return;
        if(frame==32) {effect(yumemi_origin,Effect::explosion);s.render_mode=2;r.sounds.push_back(5);}
        if(!(frame%4)) {t.type=2;t.angle=yumemi_state[2];t.group=38;t.center=yumemi_origin;t.speed=std::uint8_t(parameters[0]+yumemi_state[0]);t.count=parameters[1];add();yumemi_state[2]=std::uint8_t(yumemi_state[2]+yumemi_state[1]);yumemi_state[0]=std::uint8_t(yumemi_state[0]+8);}
        if(frame>60) {s.render_mode=0;finish();}
    } else if(s.mode>=7&&s.mode<=9) {
        if(frame==1) {
            s.render_mode=1;s.scratch=r.players[other].center;yumemi_state[2]=motion::angle_to({yumemi_origin.x,yumemi_origin.y},{s.scratch.x,s.scratch.y});s.effect_radius=256;s.render_frame=32;
        }
        if(frame<16) {if(frame%4==1)effect(s.scratch);return;}if(frame<32)return;
        if(frame==32) {effect(yumemi_origin,Effect::explosion);s.render_mode=2;}
        if(!(frame%2)) {
            r.sounds.push_back(3);t.center=yumemi_origin;t.angle=yumemi_state[2];t.speed=std::uint8_t(parameters[2]+(r.random.ring()&31));t.type=std::uint8_t(1+(r.random.ring()&1));
            constexpr std::uint8_t groups[5]={8,14,2,20,0};t.group=groups[r.random.ring()%5];add();
        }
        if(frame>96) {s.render_mode=0;finish();}
    } else if(s.mode>=11&&s.mode<=14) {
        move_sine();
        if(!(frame%parameters[3])) {
            t.group=32;t.speed=32;t.type=std::uint8_t(1+(r.random.ring()&1));
            constexpr int x[4]={0,0,-512,512},y[4]={-512,512,0,0};
            for(unsigned i=0;i<4;++i) {t.angle=std::uint8_t(r.random.ring());t.center={motion::wrap(s.center.x+x[i]),motion::wrap(s.center.y+y[i])};add();}
        }
        if(frame>=96)finish();
    } else if(s.mode>=15&&s.mode<=17) {
        if(!s.move_phase) {if(s.center.x>896&&s.center.x<3712) {move_sine();return;}s.move_phase=1;frame=0;return;}
        s.render_frame=2;s.scratch=r.players[other].center;if(frame<32)return;
        move_sine();move_sine();
        if(frame%16==15) {s.render_mode=1;effect(s.scratch);r.extra_attacks.special(r,s.scratch,pid);}
        else if(frame>parameters[4]) {s.render_mode=0;finish();s.move_phase=0;}
    } else if(s.mode==5||s.mode==6||s.mode==10) {
        move_sine();
        if(!(frame%parameters[5])) {
            t.type=2;
            if(frame<64) {t.center=yumemi_origin;t.angle=192;t.speed=96;t.group=22;add();t.group=16;add();}
            if(frame>=32) {
                t.group=0;t.speed=36;t.center.y=0;
                for(unsigned i=0;i<12;++i) {t.center.x=std::int16_t(r.random.ring()%4608);t.angle=std::uint8_t(32+(r.random.ring()&63));add();}
            }
        }
        if(frame>=96)finish();
    }
}
void Bosses::update_yumemi(Round& r,unsigned pid,CollisionMap& collision,const ChargeQuery& charge) {
    if(start(r,pid)) {
        const auto level=r.boss_level;parameters[0]=parameters[1]=std::uint8_t(16+level/2);parameters[2]=std::uint8_t(64+level);
        parameters[3]=std::uint8_t(18-level);parameters[4]=std::uint8_t(80+level*4);parameters[5]=std::uint8_t(16-level/2);
    }
    if(r.boss_launched_by!=pid)return;
    r.bullets.model.pid=std::uint8_t(pid^1);
    if(state.mode!=128)r.boss_target={state.center.x,motion::wrap(int(state.center.y)+2048)};
    ++frame;yumemi_origin={motion::wrap(state.center.x+144),motion::wrap(state.center.y-384)};
    switch(state.mode) {
    case 0:
        if(frame==24||frame==72) {r.sounds.push_back(255);r.sounds.push_back(5);}
        if(frame!=96)return;
        frame=0;state.mode=1;break;
    case 1:next_pattern(r);break;
    case 128:fall(r,pid);break;
    case 255:return;
    default:yumemi_pattern(r,pid);break;
    }
    if(state.effect_radius)state.effect_radius=std::uint16_t(state.effect_radius-8);
    if(state.render_frame)--state.render_frame;
    hit(r,pid,collision,charge);
}

}
