# ReC98 compatibility boundary

Temporary C/C++ forwarders contain only `#include "<upstream-relative-path>"`.
Only `th03/main/chars/speed.hpp` and `th03/hardware/input.h` may wrap that
same path-correct include in their reviewed guards,
`TH03_COMPAT_REC98_MAIN_CHARS_SPEED_HPP` and
`TH03_COMPAT_REC98_HARDWARE_INPUT_H`, respectively. The guarded form contains
exactly `#ifndef GUARD`, `#define GUARD`, the include, and `#endif`, allowing
only blank lines and leading/trailing spaces or tabs. It permits no comments,
continuations, other directives, definitions, declarations, or alternate includes.
These guards suppress repeated declarations; they do not establish ABI, layout,
compiler or link equivalence.
TASM `.inc` forwarders contain only `include <upstream-relative-path>`.
Every forwarder must be declared in the build graph.
Localize and attest declarations under their TH03 owner before removing it.
The reference checkout is not maintained product source.
