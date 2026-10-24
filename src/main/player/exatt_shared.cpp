// Standalone shared-flight producer for scoped replay. The live MAIN build
// joins these functions with the Reimu prefix in exatt_flight_reimu.cpp.
#pragma codeseg MAIN_06_TEXT

#include "src/main/player/exatt_shared.hpp"
#include "src/main/math/vector_far.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/difficul.hpp"

#pragma option -a2

#include "src/main/player/exatt_entity.hpp"

extern exatt_entity_t near *exatt_entity_p;

#include "src/main/player/exatt_flight.inl"
