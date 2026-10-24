// Standalone Reimu producers for scoped replay and the live update/render TU.
// The live prefix shares a native CODE record with flight functions.
#pragma codeseg MAIN_06_TEXT

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

#include "src/main/player/exatt_shared.hpp"
void near reimu_exatt_render_one(void);

#ifndef TH03_EXATT_REIMU_UPDATE_ONLY
#include "src/main/player/exatt_reimu_prefix.inl"
#endif
#ifndef TH03_EXATT_REIMU_PREFIX_ONLY
#include "src/main/player/exatt_reimu_update.inl"
#endif
