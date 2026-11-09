# MAIN initializer: native DOS paragraph allocation and ordered startup

The complete far-Pascal `initmain` owner now expresses the original 288,000-
byte DOS allocation as a natural 16-byte paragraph division instead of a
hardcoded right shift. The allocation error test explicitly checks the
helper's nonzero result, before any PC-98 video, VSync, EGC, joystick or
packed-resource initialization call. All six startup calls and the signed
16-bit success/failure return codes retain their original order.

Original TC4/TLINK `af1180b` matched the full 62 CODE bytes, seven ordered
native fields, the PUBLIC and the complete Japanese MAIN image/relocations
in two independent rounds. Inverting the top-level error branch to wrap
all startup calls in the success path (`af1180c`) changed CODE, and was
rejected; the natural error-first return remains.
