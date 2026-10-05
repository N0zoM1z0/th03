#pragma option -zCSHARED

#include "src/main/math/polar.hpp"

// Signed 16-bit coordinates, with an 8-bit fractional sine/cosine ratio.
int far __cdecl polar(int center, int radius, int ratio)
{
    return ((static_cast<long>(radius) * ratio) >> 8) + center;
}
