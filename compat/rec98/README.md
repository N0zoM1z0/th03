# ReC98 compatibility boundary

Temporary C/C++ forwarders contain only `#include "<upstream-relative-path>"`.
TASM `.inc` forwarders contain only `include <upstream-relative-path>`.
Every forwarder must be declared in the build graph.
Localize and attest declarations under their TH03 owner before removing it.
The reference checkout is not maintained product source.
