#pragma option -zCSHARED

#include "src/main/math/polar.hpp"

// Signed 16-bit coordinates; Q8 sine/cosine entries multiply a signed
// 16-bit radius in 32-bit intermediate precision before arithmetic shift.
enum { POLAR_FRACTION_BITS = 8 };

// The original ABI takes three signed 16-bit integers; the multiplication
// widens to signed 32-bit *before* a Q8 arithmetic shift. In pinned TC4,
// negative products shift toward negative infinity, unlike signed /256.
// The signed 16-bit return type truncates the widened result in the
// original calling convention, with no separate source-level cast required.
int far __cdecl polar(int center, int radius, int ratio)
{
    // The center is added after the signed 32-bit product's arithmetic
    // Q8 shift, before truncation to the far-cdecl 16-bit result.
    return center + ((static_cast<long>(radius) * ratio) >> POLAR_FRACTION_BITS);
}
