// Music polygon raster adapted from TH04 port/modern-64 1ba7107 (MIT).
// TH03 owns the 19-track menu, comment blits, input order and playback requests.
#include "music.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
constexpr const char* songs[]={"op.m","select.m","00mm.m","01mm.m","02mm.m","03mm.m","04mm.m","05mm.m","06mm.m","dec.m","07mm.m","08mm.m","demo1.m","demo2.m","demo3.m","demo4.m","demo5.m","ed.m","score.m"};
constexpr const char* choices[]={
    "\x4e\x4f\x2e\x31\x20\x20\x20\x20\x20\x81\x40\x96\xb2\x82\xcd\x8e\x9e\x8b\xf3\x82\xf0\x89\x7a\x82\xa6\x82\xc4\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x32\x20\x20\x20\x20\x81\x40\x20\x81\x40\x20\x53\x65\x6c\x65\x63\x74\x69\x6f\x6e\x20\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x33\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x93\x8c\x95\xfb\x97\x64\x97\xf6\x92\x6b\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x34\x20\x20\x20\x20\x20\x20\x20\x20\x52\x65\x69\x6e\x63\x61\x72\x6e\x61\x74\x69\x6f\x6e\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x35\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x44\x69\x6d\x2e\x20\x44\x72\x65\x61\x6d\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x36\x20\x20\x20\x54\x61\x62\x75\x6c\x61\x20\x72\x61\x73\x61\x81\x40\x81\x60\x8b\xf3\x94\x92\x8f\xad\x8f\x97\x20\x20",
    "\x4e\x4f\x2e\x37\x20\x20\x20\x81\x40\x20\x20\x4d\x61\x6e\x69\x61\x63\x61\x6c\x20\x50\x72\x69\x6e\x63\x65\x73\x73\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x38\x20\x20\x20\x20\x20\x20\x96\xb2\x8f\xc1\x8e\xb8\x20\x20\x81\x60\x4c\x6f\x73\x74\x20\x44\x72\x65\x61\x6d\x20\x20",
    "\x4e\x4f\x2e\x39\x20\x20\x20\x20\x20\x96\xb2\x8c\xb6\x97\x56\x8b\x59\x20\x20\x81\x60\x44\x72\x65\x61\x6d\x20\x57\x61\x72\x20\x20",
    "\x4e\x4f\x2e\x31\x30\x20\x20\x96\x82\x96\x40\x8c\x88\x90\xed\x81\x49\x81\x60\x46\x69\x67\x68\x74\x20\x69\x74\x20\x6f\x75\x74\x21",
    "\x4e\x4f\x2e\x31\x31\x20\x20\x20\x20\x81\x40\x20\x53\x61\x69\x6c\x6f\x72\x20\x6f\x66\x20\x54\x69\x6d\x65\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x32\x20\x20\x20\x20\x20\x53\x74\x72\x61\x77\x62\x65\x72\x72\x79\x20\x43\x72\x69\x73\x69\x73\x21\x21\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x33\x20\x20\x20\x20\x20\x20\x94\xf1\x93\x9d\x88\xea\x96\x82\x96\x40\x90\xa2\x8a\x45\x98\x5f\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x34\x20\x20\x20\x20\x20\x20\x20\x20\x81\x40\x96\x82\x96\x40\x8f\xe0\x88\xa4\x20\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x35\x20\x20\x20\x20\x20\x20\x20\x20\x81\x40\x8b\x76\x89\x93\x82\xcc\x96\xb2\x20\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x36\x20\x20\x20\x20\x20\x20\x20\x20\x93\x8c\x95\xfb\x82\xcc\x90\xc2\x82\xa2\x8b\xf3\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x37\x20\x20\x20\x20\x20\x20\x20\x20\x20\x89\x69\x89\x93\x82\xcc\x96\x9e\x8c\x8e\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x38\x20\x20\x20\x20\x20\x20\x20\x4d\x61\x70\x6c\x65\x20\x44\x72\x65\x61\x6d\x2e\x2e\x2e\x20\x20\x20\x20\x20\x20",
    "\x4e\x4f\x2e\x31\x39\x20\x20\x20\x20\x20\x20\x20\x20\x20\x97\xec\x90\x6c\x82\xcc\x8b\x78\x93\xfa\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x81\x40\x81\x40\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20",
    "\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x20\x81\x40\x81\x40\x82\x70\x82\x95\x82\x89\x82\x94\x20\x20\x20\x20\x20\x20\x20\x20\x20",
};
int floor16(std::int64_t x) {return int(x>=0 ? x/65536 : -((-x+65535)/65536));}
}
void music_polygon(Canvas& dest,const std::vector<Point>& input) {
    auto& page=dest.pixels;
    if(page.size()!=256000 || input.size()<4)throw std::invalid_argument("Music polygon geometry");
    const unsigned n=unsigned(input.size()-1);
    if(input.back().x!=input.front().x || input.back().y!=input.front().y)throw std::invalid_argument("Music polygon closure");
    int ymin=input[0].y,ymax=ymin,xmin=input[0].x,xmax=xmin;unsigned left=0,right=0;
    for(unsigned i=1;i<n;++i) {
        if(input[i].y<ymin) {ymin=input[i].y;left=right=i;}
        else if(input[i].y==ymin)right=i;
        ymax=std::max(ymax,int(input[i].y));xmin=std::min(xmin,int(input[i].x));xmax=std::max(xmax,int(input[i].x));
    }
    if(ymin>399 || ymax<0 || xmin>639 || xmax<0)return;
    if(left==0 && right==n-1)std::swap(left,right);
    struct Edge {unsigned end;int direction;std::int64_t x,step;};
    const auto next=[&](unsigned i,int direction){return unsigned((int(i)+direction+int(n))%int(n));};
    const auto setup=[&](Edge& e,unsigned start,bool clip) {
        unsigned end=next(start,e.direction);unsigned guard=0;
        if(clip)while(input[end].y<0) {start=end;end=next(end,e.direction);if(++guard>n)throw std::logic_error("Music polygon edge");}
        const Point a=input[start],b=input[end];int x=a.x,y=a.y;
        if(clip && y<0) {x+=int(std::int64_t(int(b.x)-a.x)*(-y)/(int(b.y)-y));y=0;}
        const int height=int(b.y)-y;
        e.end=end;e.x=std::int64_t(x)*65536+32768;
        // make_linework truncates the signed fixed-point quotient towards zero.
        e.step=std::int64_t(motion::wrap(int(b.x)-x))*65536/(height ? height : 1);
    };
    Edge a{left,-1,0,0},b{right,1,0,0};setup(a,left,true);setup(b,right,true);
    int y=std::max(ymin,0),bottom=std::min(ymax,399);unsigned guard=0;
    while(y<=bottom) {
        if(++guard>n*2+1)throw std::invalid_argument("Music polygon is not convex");
        const int end=std::min(int(input[a.end].y),int(input[b.end].y));
        const bool final=bottom<=end;const int last=final ? bottom : end-1;
        // draw_trapezoid writes once even with length -1 at a zero-height edge.
        for(int row=y;row<=std::max(y,last);++row) {
            const int xa=floor16(a.x),xb=floor16(b.x),lo=std::max(0,std::min(xa,xb)),hi=std::min(639,std::max(xa,xb));
            if(row>=0 && row<400)for(int x=lo;x<=hi;++x)page[unsigned(row)*640+unsigned(x)]|=1;
            a.x+=a.step;b.x+=b.step;
        }
        if(final)break;
        y=end;
        if(input[a.end].y==end)setup(a,a.end,false);
        if(input[b.end].y==end)setup(b,b.end,false);
    }
}void MusicState::update(const std::function<void(const std::vector<Point>&)>& draw) {
    const auto angles=[&](MusicPolygon& p,int vx) {
        p.velocity.x=std::int16_t(vx ? vx : 1);
        p.velocity.y=std::int16_t(32+((random_next(seed)&3)<<4));
        p.angle=std::uint8_t(random_next(seed));p.angle_speed=std::uint8_t(4-(random_next(seed)&7));
        if(!p.angle_speed)p.angle_speed=4;
    };
    if(!initialized) {
        for(auto& p:polygons) {
            p.center.x=std::int16_t(random_next(seed)%640);p.center.y=std::int16_t(random_next(seed)%6400);
            angles(p,4-(random_next(seed)&7));
        }
        initialized=true;
    }
    for(unsigned i=0;i<16;++i) {
        auto& p=polygons[i];const unsigned count=i/4+3;std::vector<Point> points;
        for(unsigned v=0;v<count;++v) {
            const auto delta=motion::polar(std::uint8_t(v*256/count+p.angle),std::int16_t((i&3)*16+64));
            points.push_back({motion::wrap(p.center.x+delta.x),motion::wrap((p.center.y>>4)+delta.y)});
        }
        points.push_back(points.front());
        p.center.x=motion::wrap(p.center.x+p.velocity.x);p.center.y=motion::wrap(p.center.y+p.velocity.y);
        p.angle=std::uint8_t(p.angle+p.angle_speed);
        if(p.center.x<=0||p.center.x>=639)p.velocity.x=motion::wrap(-int(p.velocity.x));
        if(p.center.y>=8000) {
            p.center.x=std::int16_t(random_next(seed)%640);p.center.y=-1600;
            angles(p,8-(random_next(seed)&15));
        }
        draw(points);
    }
}
MusicRoom::MusicRoom(const PfArchive& assets,const Font& font,MusicState& state,std::uint16_t input):font_(font),state_(state),comments_(assets.read("MUSIC.TXT")),blue_(640*400) {
    if(!font.present())throw std::runtime_error("Music Room requires --font-bmp FILE");
    const auto image=decode_pi(assets.read("OP3.PI"));palette_=image.palette;picture(pages[1],image);
    selected=state.playing;
    // Track drawing switches to the other page and back, then OP copies page1.
    for(unsigned i=0;i<21;++i)track(i,i==selected ? 15 : 3);
    pages[0]=pages[1];accessed=1;comment_background_=pages[1];
    for(unsigned i=0;i<blue_.size();++i)blue_[i]=pages[1].pixels[i]&1;
    comment();accessed=0;comment();
    // music_page_accessed remains1 although the last comment was put on page0.
    pump(input);
}
void MusicRoom::track(unsigned index,unsigned color) {
    accessed=1-back;font_.text(pages[accessed],16,40+int(index)*16,choices[index],color,2);
    accessed=back;font_.text(pages[accessed],16,40+int(index)*16,choices[index],color,2);
}
void MusicRoom::restore_blue() {for(unsigned i=0;i<blue_.size();++i)pages[accessed].pixels[i]=std::uint8_t((pages[accessed].pixels[i]&14)|blue_[i]);}
void MusicRoom::comment() {
    restore_blue();
    for(unsigned y=64;y<384;++y)for(unsigned x=304;x<624;++x)pages[accessed].pixels[y*640+x]=comment_background_.pixels[y*640+x];
    for(unsigned line=0;line<20;++line) {
        const auto at=std::size_t(state_.playing)*840+line*42;
        std::string text;for(unsigned i=0;i<40&&comments_.at(at+i);++i)text+=char(comments_[at+i]);
        font_.text(pages[accessed],304,64+int(line)*16,text,line ? 13 : 15,1);
    }
    for(unsigned i=0;i<blue_.size();++i)blue_[i]=pages[accessed].pixels[i]&1;
}
void MusicRoom::animate() {
    restore_blue();state_.update([&](const std::vector<Point>& points) {music_polygon(pages[accessed],points);});
    shown=back;back=1-back;accessed=back;++frames;
}
void MusicRoom::pump(std::uint16_t input) {
    for(;;) {
        if(phase==Phase::done)return;
        if(phase==Phase::exit_release) {
            if(input) {animate();return;}
            shown=0;accessed=0;pages[0].fill(0,0,639,399,0);phase=Phase::done;return;
        }
        if(phase==Phase::release) {
            if(input) {animate();return;}
            phase=Phase::controls;
        }
        if(input&up) {track(selected,3);selected=selected ? selected-1 : 20;if(selected==19)--selected;track(selected,15);}
        if(input&down) {track(selected,3);selected=selected<20 ? selected+1 : 0;if(selected==19)++selected;track(selected,15);}
        if(input&(shot|ok)) {
            if(selected==20) {phase=Phase::exit_release;continue;}
            sounds.push_back({SceneSound::Kind::control,{},0x100});sounds.push_back({SceneSound::Kind::load,songs[selected],0});sounds.push_back({SceneSound::Kind::control,{},0});
            state_.playing=std::uint8_t(selected);sampled_=input;comment();phase=Phase::after_play;animate();return;
        }
        if(input&cancel) {phase=Phase::exit_release;continue;}
        if(!input) {phase=Phase::controls;animate();return;}
        phase=Phase::release;
    }
}
void MusicRoom::tick(std::uint16_t input) {
    if(done())return;
    if(phase==Phase::after_play) {comment();phase=sampled_&cancel ? Phase::exit_release : Phase::release;}
    pump(input);
}
}
