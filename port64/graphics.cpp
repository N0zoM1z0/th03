#include "graphics.hpp"
#include <algorithm>
#include <stdexcept>

namespace th03 {
namespace {
unsigned word(const Bytes& bytes,unsigned at) {return bytes.at(at)|(unsigned(bytes.at(at+1))<<8);}
void need(bool ok,const char* message) {if(!ok)throw std::runtime_error(message);}
}
void Canvas::put(int x,int y,std::uint8_t color) {
    if(x>=0&&x<640&&y>=0&&y<400)pixels[unsigned(y)*640+unsigned(x)]=color&15;
}
void Canvas::fill(int left,int top,int right,int bottom,std::uint8_t color) {
    for(int y=std::max(top,0);y<=std::min(bottom,399);++y)
        for(int x=std::max(left,0);x<=std::min(right,639);++x)put(x,y,color);
}
Frame Canvas::frame(const Palette& palette,int tone) const {
    tone=std::max(0,std::min(tone,200));
    std::array<std::uint32_t,16> colors{};
    for(unsigned i=0;i<16;++i) {
        std::uint32_t rgb=0xff000000;
        for(unsigned channel=0;channel<3;++channel) {
            unsigned nibble=palette[i*3+channel]>>4;
            nibble=tone<=100 ? nibble*unsigned(tone)/100 : 15-(15-nibble)*unsigned(200-tone)/100;
            unsigned six=(nibble<<2)|(nibble>>2);
            rgb|=((six<<2)|(six>>4))<<(16-channel*8);
        }
        colors[i]=rgb;
    }
    Frame out(pixels.size());
    for(std::size_t i=0;i<out.size();++i)out[i]=colors[pixels[i]&15];
    return out;
}
Palette read_palette(const Bytes& bytes) {
    need(bytes.size()==48,"RGB palette must have 48 components");
    Palette out{};
    // palette_entry_rgb duplicates each four-bit file component into both nibbles.
    for(unsigned i=0;i<48;++i)out[i]=std::uint8_t(bytes[i]|(bytes[i]<<4));
    return out;
}
Cdg::Cdg(Bytes bytes):bytes_(std::move(bytes)) {
    need(bytes_.size()>=16,"short CDG header");
    plane_size=word(bytes_,0);width=word(bytes_,2);height=word(bytes_,4);count=bytes_[10];
    if(!count)count=1; // TH03 single-image files use zero here.
    need(width&&width%32==0&&height&&plane_size==width/8*height&&
         bytes_[11]==0&&word(bytes_,12)==0&&word(bytes_,14)==0,"unsupported TH03 CDG geometry");
    need(bytes_.size()==16+std::size_t(plane_size)*5*count,"CDG plane extent differs");
}
void Cdg::put(Canvas& dest,unsigned image,int left,int top,bool alpha,bool flip) const {
    need(image<count,"CDG image index outside file");
    left=(left/8)*8;
    const auto base=16+std::size_t(image)*plane_size*5;
    for(unsigned y=0;y<height;++y)for(unsigned x=0;x<width;++x) {
        const auto at=(height-1-y)*(width/8)+x/8;
        const auto mask=std::uint8_t(0x80u>>(x&7));
        unsigned color=0;
        for(unsigned plane=0;plane<4;++plane)
            if(bytes_[base+(plane+1)*plane_size+at]&mask)color|=1u<<plane;
        const int dx=left+int(flip ? width-1-x : x),dy=top+int(y);
        if(dx<0||dx>=640||dy<0||dy>=400)continue;
        const auto destination=unsigned(dy)*640+unsigned(dx);
        if(alpha) {
            if(bytes_[base+at]&mask)dest.pixels[destination]=0;
            dest.pixels[destination]|=std::uint8_t(color);
        } else dest.pixels[destination]=std::uint8_t(color);
    }
}
Bfnt::Bfnt(Bytes bytes):bytes_(std::move(bytes)) {
    need(bytes_.size()>=32&&std::equal(bytes_.begin(),bytes_.begin()+5,"BFNT\x1a")&&
         (bytes_[5]&127)==3,"unsupported BFNT sprite header");
    width=word(bytes_,8);height=word(bytes_,10);
    const auto first=word(bytes_,12),last=word(bytes_,14);
    need(width&&width%8==0&&height&&last>=first,"unsupported BFNT sprite geometry");
    count=last-first+1;
    data_offset=32+word(bytes_,28)+((bytes_[5]&128) ? 48 : 0);
    need(data_offset<=bytes_.size()&&std::size_t(width)*height/2*count<=bytes_.size()-data_offset,
         "BFNT sprite pixels truncated");
}
void Bfnt::put(Canvas& dest,unsigned image,int left,int top) const {
    need(image<count,"BFNT image index outside file");
    for(unsigned y=0;y<height;++y)for(unsigned x=0;x<width;++x) {
        const auto packed=bytes_[data_offset+(std::size_t(image)*height+y)*(width/2)+x/2];
        const auto color=std::uint8_t((x&1) ? packed&15 : packed>>4);
        if(color)dest.put(left+int(x),top+int(y),color);
    }
}
void gaiji(Canvas& dest,const Bytes& font,unsigned code,int left,int top,std::uint8_t color) {
    const auto base=32+word(font,28)+code*32;
    need(base+32<=font.size(),"gaiji outside font");
    for(unsigned y=0;y<16;++y)for(unsigned x=0;x<16;++x)
        if(font[base+y*2+x/8]&(0x80u>>(x&7)))dest.put(left+int(x),top+int(y),color);
}
}
