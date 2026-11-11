// master.lib integer DDA and circle algorithms, translated from the local
// ReC98 supplier sources. Pixel clipping remains in the physical VRAM domain.
#include "raster.hpp"
#include <algorithm>
#include <cstdlib>

namespace th03 {
namespace {
void dot(Canvas& canvas,int x,int y,std::uint8_t color,Clip clip) {
    if(x>=clip.left&&x<=clip.right&&y>=clip.top&&y<=clip.bottom)canvas.put(x,y,color);
}
unsigned outcode(Point p,Clip clip) {
    return (p.x<clip.left ? 1u : p.x>clip.right ? 2u : 0u)|(p.y<clip.top ? 4u : p.y>clip.bottom ? 8u : 0u);
}
// Original cutline clips horizontally first, then vertically. It does not
// repeatedly restart a general polygon clipping algorithm.
void cut(Point& p,Point other,Clip clip) {
    const unsigned code=outcode(p,clip);if(!code)return;
    if(code&3) {
        const int x=(code&1) ? clip.left : clip.right,dx=p.x-other.x;
        if(!dx)return;
        const int y=other.y+(x-other.x)*(p.y-other.y)/dx;p={std::int16_t(x),std::int16_t(y)};
        if(y>=clip.top&&y<=clip.bottom)return;
    }
    const int y=p.y<clip.top ? clip.top : clip.bottom,dy=p.y-other.y;if(!dy)return;
    const int x=other.x+(y-other.y)*(p.x-other.x)/dy;p={std::int16_t(x),std::int16_t(y)};
}
struct Edge {
    int x,step;unsigned fraction,phase=32768;
    Edge(Point from,Point to):x(from.x) {
        const int dy=std::max(1,int(to.y)-from.y),dx=to.x-from.x;
        step=dx/dy;if(dx%dy<0)--step;
        const unsigned remainder=unsigned(dx-step*dy);
        fraction=dx<0 ? (65536u-unsigned((-dx%dy)*65536u/unsigned(dy)))&65535u : remainder*65536u/unsigned(dy);
    }
    void next() {phase+=fraction;x+=step+int(phase>>16);phase&=65535;}
};
}
void grcg_line(Canvas& canvas,Point from,Point to,std::uint8_t color,Clip clip) {
    if(outcode(from,clip)&outcode(to,clip))return;
    cut(from,to,clip);
    if(outcode(from,clip)||outcode(to,clip)) {
        std::swap(from,to);cut(from,to,clip);if(outcode(from,clip)||outcode(to,clip))return;
    }
    if(from.x>to.x)std::swap(from,to);
    const int dx=to.x-from.x,dy=std::abs(int(to.y)-from.y),direction=to.y<from.y ? -1 : 1;
    const unsigned denominator=unsigned(std::max(dx,dy));
    if(!denominator) {dot(canvas,from.x,from.y,color,clip);return;}
    const unsigned delta=unsigned(std::min(dx,dy))*65536u/denominator;
    unsigned phase=32768;int x=from.x,y=from.y;
    for(unsigned i=0;i<=denominator;++i) {
        dot(canvas,x,y,color,clip);phase+=delta;const int carry=int(phase>>16);phase&=65535;
        if(dx>dy) {++x;y+=direction*carry;}else if(dx<dy) {x+=carry;y+=direction;}else {++x;y+=direction;}
    }
}
void grcg_circle(Canvas& canvas,Point center,unsigned radius,std::uint8_t color,Clip clip) {
    if(!radius)return;
    const bool inside=center.x-int(radius)>=clip.left&&center.x+int(radius)<=clip.right&&
        center.y-int(radius)>=clip.top&&center.y+int(radius)<=clip.bottom;
    const auto four=[&](int x,int y) {
        if(inside||y) {dot(canvas,center.x-x,center.y-y,color,clip);dot(canvas,center.x+x,center.y-y,color,clip);}
        // The clipped routine's lower-half test excludes ClipYH itself.
        const auto lower=inside ? clip : Clip{clip.left,clip.top,clip.right,clip.bottom-1};
        dot(canvas,center.x-x,center.y+y,color,lower);dot(canvas,center.x+x,center.y+y,color,lower);
    };
    int x=int(radius),y=0,error=x;
    do {
        four(x,y);if(x!=y)four(y,x);
        error-=y*2+1;if(error<0) {--x;error+=x*2;}++y;
    }while(x>=y);
}
void grcg_triangle(Canvas& canvas,std::array<Point,3> p,std::uint8_t color,Clip clip) {
    if(p[0].y>=p[1].y)std::swap(p[0],p[1]);
    if(p[0].y>=p[2].y)std::swap(p[0],p[2]);
    if(p[1].y>=p[2].y)std::swap(p[1],p[2]);
    if(p[0].y>clip.bottom||p[2].y<clip.top)return;
    Edge long_edge(p[0],p[2]),edge(p[0],p[1]);
    if(p[0].y==p[1].y)edge=Edge(p[1],p[2]);
    for(int y=p[0].y;y<=p[2].y;++y) {
        if(y==p[1].y&&p[0].y!=p[1].y&&p[1].y!=p[2].y)edge=Edge(p[1],p[2]);
        if(y>=clip.top&&y<=clip.bottom)canvas.fill(std::max(clip.left,std::min(edge.x,long_edge.x)),y,
            std::min(clip.right,std::max(edge.x,long_edge.x)),y,color);
        edge.next();long_edge.next();
    }
}
}
