#pragma once
#include "application.hpp"
#include <functional>
void run_view(th03::Application& app, const std::function<th03::Frame()>& frame, unsigned frame_limit);
