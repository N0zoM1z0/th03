#include "font.hpp"
#include <stdexcept>

namespace th03 {
Font::Font(Bytes bitmap):bytes_(std::move(bitmap)) {
    if(bytes_.empty())return;
    const auto word=[&](unsigned at) {return unsigned(bytes_.at(at))|(unsigned(bytes_.at(at+1))<<8);};
    const auto dword=[&](unsigned at) {return word(at)|(word(at+2)<<16);};
    if(bytes_.size()<62||word(0)!=0x4d42||dword(14)!=40||dword(18)!=2048||dword(22)!=2048||
       word(26)!=1||word(28)!=1||dword(30)!=0)
        throw std::runtime_error("PC-98 font requires a 2048x2048 uncompressed monochrome BMP");
    offset_=dword(10);
    if(offset_>bytes_.size()||bytes_.size()-offset_<524288)throw std::runtime_error("truncated PC-98 font bitmap");
}
std::uint16_t Font::jis_row(unsigned jis,unsigned y) const {
    const unsigned row=jis>>8,cell=jis&255;
    if(bytes_.empty()||y>=16||row<0x20||row>=0xa0||cell>=128)return 0;
    const auto at=offset_+(2047-(cell*16+y))*256+(row-0x20)*2;
    return std::uint16_t(~((unsigned(bytes_[at])<<8)|bytes_[at+1]));
}
void Font::text(Canvas& dest,int left,int top,std::string_view cp932,unsigned color,unsigned weight) const {
    // TH03 graph_putsa_fx (TH02 C++ implementation). Unlike TH04 ASM, it
    // restarts the address for each glyph and stores halfwidth rows in AH.
    std::size_t at=0;
    while(at<cp932.size()&&cp932[at]) {
        unsigned c=std::uint8_t(cp932[at++]),jis=0x2b21;
        if((c>=0x81&&c<=0x9f)||(c>=0xe0&&c<=0xfc)) {
            if(at>=cp932.size())throw std::runtime_error("truncated CP932 glyph");
            const unsigned trail=std::uint8_t(cp932[at++]);
            unsigned row=(c-(c<0xa0 ? 0x81 : 0xc1))*2+0x21;
            const unsigned cell=trail>=0x9f ? (++row,trail-0x7e) : trail-(trail>0x7e ? 0x20 : 0x1f);
            jis=(row<<8)|cell;
        } else if(c>=0xa1&&c<=0xdf)jis=c+0x2980;
        else if(c>=0x21&&c<=0x7e)jis=c+0x2900;
        const bool half=jis>=0x2921&&jis<=0x2b7e;
        if(left>(half ? 632 : 624))break;
        for(unsigned y=0;y<16;++y) {
            std::uint16_t row=jis_row(jis,y);
            if(half)row&=0xff00;
            if(weight==1||weight==3)row=std::uint16_t(row|(row<<1));
            if(weight==2||weight==3) {
                const auto expanded=std::uint16_t(row|(row<<1));
                row=std::uint16_t(expanded&~std::uint16_t((row^expanded)<<1));
            }
            // The original truncates leftward weight dots to WORD width.
            for(unsigned x=0;x<16;++x)if(row&(0x8000u>>x))dest.put(left+int(x),top+int(y),std::uint8_t(color));
        }
        left+=half ? 8 : 16;
    }
}
}
