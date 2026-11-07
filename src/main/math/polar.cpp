#pragma option -zCSHARED

#include "src/main/math/polar.hpp"

// Signed 16-bit coordinates; Q8 sine/cosine entries multiply a signed
// 16-bit radius in 32-bit intermediate precision before arithmetic shift.
enum { POLAR_FRACTION_BITS = 8 };

int far __cdecl polar(int center, int radius, int ratio)
{
    return center + ((static_cast<long>(radius) * ratio) >> POLAR_FRACTION_BITS);
}
