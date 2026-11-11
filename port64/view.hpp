#pragma once
#include "menu.hpp"
#include <functional>
void run_view(th03::Menu& menu, const std::function<th03::Frame()>& frame, unsigned frame_limit);
