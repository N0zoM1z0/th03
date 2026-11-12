#include "collision.hpp"
#include "motion.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
int shift(int value,unsigned bits) {
    const int scale=1<<bits;return value>=0 ? value/scale : -((-value+scale-1)/scale);
}
}
void CollisionMap::merge(unsigned address,unsigned mask) {
    if(address>=bytes.size())throw std::runtime_error("collision write needs its adjacent DGROUP owner");
    bytes[address]|=std::uint8_t(mask);
}
void CollisionMap::rectangle(unsigned pid,Point center,int width,int height) {
    if(center.y<0||center.y>=368*16)return;
    int top=shift(center.y,5)-int(unsigned(height)>>1),bottom=top+height;
    top=std::max(top,0);bottom=std::min(bottom,183);
    int left=shift(center.x,5)-int(unsigned(width)>>1);
    if(left<0) {width+=left;if(width<=0)return;left=0;}
    const int first=left&7;
    int column=left>>3,remaining=width+first;
    unsigned pattern=0xffu>>first;
    if(remaining<8)pattern^=0xffu>>remaining;
    do {
        if(column>=18)return;
        // The assembly's row loop writes once even when its height is zero.
        int y=top;
        do {merge(pid*3312+unsigned(column)*184+unsigned(y),pattern);y+=4;}while(y<bottom);
        remaining-=8;if(remaining<=0)return;
        ++column;pattern=remaining<8 ? ~(0xffu>>remaining)&255 : 255;
    }while(true);
}
void CollisionMap::vertical(unsigned pid,Point top,int height) {
    if(top.x<0||top.x>=288*16||top.y<0||top.y>=368*16)return;
    const auto x=unsigned(top.x)>>5,y=unsigned(top.y)>>5;
    const auto count=std::min(height ? unsigned(std::uint16_t(height)) : 65536u,184-y);
    for(unsigned i=0;i<count;++i)merge(pid*3312+(x/8)*184+y+i,0x80u>>(x&7));
}
void CollisionMap::slope(unsigned pid,int left,int right,unsigned width) {
    const int delta=motion::wrap(right-left);
    const auto pattern=std::uint16_t(~(0xffu>>(width&31))&255);
    for(int j=91;j>0;--j) {
        const auto x=std::uint16_t(j==91 ? right : motion::wrap(left+delta*j/92));
        const auto tile=unsigned(x)>>5,bit=tile&7;
        const auto mask=bit ? std::uint16_t((pattern>>bit)|(pattern<<(16-bit))) : pattern;
        const auto at=pid*3312+(tile/8)*184+unsigned(j*2+1);
        merge(at,mask&255);if(mask>>8)merge(at+184,mask>>8);
    }
}
std::optional<Point> CollisionMap::hit(unsigned pid,const Player& player,int size) const {
    if(player.invincibility||player.hyper_active)return {};
    const int left=shift(player.center.x,5)-size/2;
    int top=shift(player.center.y,5)-size/2,bottom=top+size;
    if(top<0)top=0;else if(bottom>=184)bottom=183;
    const auto first=unsigned(left)&7;
    int column=shift(left,3),remaining=size+int(first);
    unsigned pattern=0xffu>>first,stride=first;
    if(remaining<=8)pattern^=0xffu>>remaining;
    // MUL takes the unsigned low column byte, then the DGROUP pointer wraps.
    auto address=std::uint16_t(0x4ba0+pid*3312+unsigned(std::uint8_t(column))*184+top);
    do {
        if(column>=18)break;
        if(column>=0) {
            unsigned y=std::uint8_t(top);stride=184;
            do {
                const bool in_map=address>=0x4ba0&&unsigned(address)-0x4ba0<bytes.size();
                if(!in_map&&!adjacent_read)
                    throw std::runtime_error("CPU edge scan needs DGROUP read owner at "+std::to_string(address));
                // The target returns the scan rectangle's top, not the
                // occupied tile's row; X is the containing eight-tile column.
                if((in_map ? bytes[unsigned(address)-0x4ba0] : adjacent_read(address))&pattern)return Point{std::int16_t(column*256),std::int16_t(top*32)};
                ++address;--stride;++y;
            }while(y<unsigned(std::uint8_t(bottom)));
        }
        ++column;address=std::uint16_t(address+stride);remaining-=8;
        pattern=unsigned(std::uint16_t(remaining))<8 ? ~(0xffu>>(unsigned(remaining)&31))&255 : 255;
    }while(remaining>0);
    return {};
}
}
