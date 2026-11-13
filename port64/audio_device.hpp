// Adapted from TH04 port/modern-64 1ba7107 (MIT).
#pragma once
#include "audio_output.hpp"

namespace th03::audio {
// Calling this factory opts into the platform device. Merely creating a
// muted Output does not initialize an audio subsystem or open a device.
std::unique_ptr<Device> platform_device();
} // namespace th03::audio
