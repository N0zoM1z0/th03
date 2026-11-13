// Adapted from TH04 port/modern-64 1ba7107 (MIT); checked with TH03 resources.
#pragma once
#include "pmd_fm_effects.hpp"
namespace th03::pmd {
struct MusicalLfo : FmLfo {
    std::int8_t depth_step=0;
    std::uint8_t depth_speed=0,initial_depth_speed=0;
    std::uint8_t depth_count=255,initial_depth_count=255,mask=0;
};
}
