#pragma once
#include "graphics.hpp"
#include "game_types.hpp"

namespace th03 {
struct Clip {int left=0,top=0,right=639,bottom=199;};
void grcg_circle(Canvas& canvas,Point center,unsigned radius,std::uint8_t color,Clip clip);
void grcg_line(Canvas& canvas,Point from,Point to,std::uint8_t color,Clip clip);
void grcg_triangle(Canvas& canvas,std::array<Point,3> points,std::uint8_t color,Clip clip);
void grcg_trapezoid(Canvas& canvas,int y1,int left1,int right1,int y2,int left2,int right2,std::uint8_t color,Clip clip);
}
