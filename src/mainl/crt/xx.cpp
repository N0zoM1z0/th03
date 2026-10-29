// Recovered DOS exception/RTTI translation unit. Whole native equality remains
// open; keep the original source order,near/far interfaces and compiler data.
#include "xx_abi.h"

static int near dtorCleanup(XXDtorTable far *,long,xx_registration_ptr,unsigned);

#include "xx_front.inl"
#include "xx_type_equal.inl"
#include "xx_type_match.inl"
#include "xx_calls.inl"
#include "xx_throw.inl"
#include "xx_catch.inl"
#include "xx_dispatch.inl"
#include "xx_destroy.inl"
#include "xx_rtti.inl"
