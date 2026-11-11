#pragma once
#include "graphics.hpp"
#include <string_view>

namespace th03 {
// Anex86-format bitmap supplied by the user, also accepted by DOSBox-X.
// Adapted from TH04 port64/dialog.cpp at 1ba7107; TH03 uses its C++ renderer.
class Font {
public:
    explicit Font(Bytes bitmap);
    bool present() const {return !bytes_.empty();}
    std::uint16_t jis_row(unsigned jis,unsigned y) const;
    void text(Canvas& dest,int left,int top,std::string_view cp932,unsigned color,unsigned weight=0) const;
private:
    Bytes bytes_;
    unsigned offset_=0;
};
}
