#pragma once
#include "round.hpp"
#include <optional>

namespace th03 {
// Two original column-major 144x184 bitmaps, one bit per 2x2 display tile.
class CollisionMap {
public:
    std::array<std::uint8_t,2*18*184> bytes{};
    std::function<std::uint8_t(std::uint16_t)> adjacent_read;
    void clear() {bytes.fill(0);}
    void rectangle(unsigned pid,Point center,int width,int height);
    void vertical(unsigned pid,Point top,int height);
    void slope(unsigned pid,int left,int right,unsigned width);
    std::optional<Point> hit(unsigned pid,const Player& player,int size) const;
private:
    void merge(unsigned address,unsigned mask);
};
}
