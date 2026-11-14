#pragma once
#include "application.hpp"
#include <functional>
#include <array>
#include <optional>
void run_view(th03::Application& app, const std::function<th03::Frame()>& frame, unsigned frame_limit);

// One owned image serves ordinary refreshes and OS expose/resize paints.
// Only OP's visible menu fields can suppress a render; other scenes animate.
class ViewFrames {
public:
    bool update(const th03::Application& app,const std::function<th03::Frame()>& draw) {
        std::optional<std::array<int,7>> menu;
        if(app.phase==th03::Phase::op||app.phase==th03::Phase::versus)
            menu=std::array<int,7>{{int(app.phase),int(app.menu.screen),int(app.menu.request),app.menu.selected,
                app.menu.options.rank,app.menu.options.music,app.menu.options.keys}};
        if(!pixels_.empty()&&menu&&menu==menu_)return false;
        pixels_=draw();menu_=menu;return true;
    }
    const th03::Frame& pixels()const{return pixels_;}
private:
    th03::Frame pixels_;
    std::optional<std::array<int,7>> menu_;
};
