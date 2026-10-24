// One native 825-byte TC4 CODE record: shared flight precedes the Reimu
// prefix physically; descending FIXUPP order puts Reimu relocations first.
#pragma codeseg MAIN_06_TEXT
#include "src/main/player/exatt_shared.hpp"
#include "src/main/math/vector_far.hpp"
#include "src/main/player/exatt_reimu.hpp"
#include "compat/rec98/th03/main/player/cur.hpp"
#include "compat/rec98/th03/main/collmap.hpp"
#include "compat/rec98/th03/main/hitbox.hpp"
#include "compat/rec98/th03/main/sprite16.hpp"
#include "compat/rec98/th03/main/playfld.hpp"
#include "compat/rec98/th03/main/difficul.hpp"
#include "compat/rec98/th03/math/randring.hpp"
#include "compat/rec98/th03/math/vector.hpp"
#include "compat/rec98/libs/master.lib/master.hpp"

#pragma option -a2
#include "src/main/player/exatt_entity.hpp"

extern exatt_entity_t exatt_entities[PLAYER_COUNT][16];
extern exatt_entity_t near *exatt_entity_p;
void near reimu_exatt_render_one(void);

#include "src/main/player/exatt_flight.inl"
#include "src/main/player/exatt_reimu_prefix.inl"
