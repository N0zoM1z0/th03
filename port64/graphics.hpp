#pragma once
#include "menu.hpp"
#include <array>

namespace th03 {
using Palette=std::array<std::uint8_t,48>;
// Visible PC-98 graphics plane state. Operations act on four-bit indices,
// so masked clear/OR has the same meaning even with a non-linear palette.
struct Canvas {
    Bytes pixels=Bytes(640*400);
    void put(int x,int y,std::uint8_t color);
    void fill(int left,int top,int right,int bottom,std::uint8_t color);
    Frame frame(const Palette& palette,int tone=100) const;
};
Palette read_palette(const Bytes& bytes);
class Cdg {
public:
    explicit Cdg(Bytes bytes);
    void put(Canvas& dest,unsigned image,int left,int top,bool alpha=true,bool flip=false) const;
    unsigned width{},height{},count{};
private:
    Bytes bytes_;
    unsigned plane_size{};
};
class Bfnt {
public:
    std::uint8_t pixel(unsigned image,unsigned x,unsigned y) const;
    explicit Bfnt(Bytes bytes);
    void put(Canvas& dest,unsigned image,int left,int top) const;
    unsigned width{},height{},count{};
private:
    Bytes bytes_;
    unsigned data_offset{};
};
void pellet(Canvas& dest,int left,int top,unsigned cel);
void picture(Canvas& dest,const PiImage& image,int left=0,int top=0);
void gaiji(Canvas& dest,const Bytes& font,unsigned code,int left,int top,std::uint8_t color);
}
