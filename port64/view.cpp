#include "view.hpp"
#include "frame_schedule.hpp"
#include "win32_frame_timer.hpp"
#include <chrono>
#include <stdexcept>
#include <thread>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
namespace {
struct Window { const ViewFrames* frames; };
LRESULT CALLBACK procedure(HWND window, UINT message, WPARAM w, LPARAM l) {
    if (message==WM_CREATE) {
        SetWindowLongPtr(window,GWLP_USERDATA,reinterpret_cast<LONG_PTR>(reinterpret_cast<CREATESTRUCT*>(l)->lpCreateParams));
        return 0;
    }
    if (message==WM_DESTROY) { PostQuitMessage(0); return 0; }
    if (message==WM_ERASEBKGND) return 1;
    if (message==WM_PAINT) {
        PAINTSTRUCT paint;
        HDC dc=BeginPaint(window,&paint);
        auto* state=reinterpret_cast<Window*>(GetWindowLongPtr(window,GWLP_USERDATA));
        if (state) {
            const auto& pixels=state->frames->pixels();
            RECT rect; GetClientRect(window,&rect);
            FillRect(dc,&rect,reinterpret_cast<HBRUSH>(GetStockObject(BLACK_BRUSH)));
            const int scale_width=rect.right*400 <= rect.bottom*640 ? rect.right : rect.bottom*640/400;
            const int scale_height=scale_width*400/640;
            BITMAPINFO info{};
            info.bmiHeader.biSize=sizeof(BITMAPINFOHEADER);
            info.bmiHeader.biWidth=640; info.bmiHeader.biHeight=-400;
            info.bmiHeader.biPlanes=1; info.bmiHeader.biBitCount=32; info.bmiHeader.biCompression=BI_RGB;
            SetStretchBltMode(dc,COLORONCOLOR);
            StretchDIBits(dc,(rect.right-scale_width)/2,(rect.bottom-scale_height)/2,scale_width,scale_height,
                          0,0,640,400,pixels.data(),&info,DIB_RGB_COLORS,SRCCOPY);
        }
        EndPaint(window,&paint);
        return 0;
    }
    return DefWindowProc(window,message,w,l);
}
}
#else
#include <SDL.h>
#endif

namespace {
template<class Held> th03::InputFrame keyboard_input(const Held& held,const int* keys) {
    th03::InputFrame out;
    const auto bit=[&](unsigned key,unsigned mask,std::uint16_t& target){if(held(keys[key]))target|=std::uint16_t(mask);};
    bit(0,th03::up,out.single);bit(1,th03::down,out.single);
    bit(2,th03::left,out.single);bit(3,th03::right,out.single);
    bit(4,th03::shot,out.players[0]);bit(5,th03::bomb,out.players[0]);
    bit(6,th03::shot,out.single);bit(7,th03::cancel,out.single);bit(8,th03::ok,out.single);
    constexpr unsigned p1[]={th03::left,th03::right,th03::up,th03::down,th03::up_left,th03::up_right,th03::down_left,th03::down_right};
    for(unsigned i=0;i<8;++i)bit(9+i,p1[i],out.players[0]);
    bit(2,th03::shot,out.players[1]);bit(3,th03::bomb,out.players[1]);
    constexpr unsigned p2[]={th03::up_left,th03::up,th03::up_right,th03::left,th03::right,th03::down_left,th03::down,th03::down_right};
    for(unsigned i=0;i<8;++i) {bit(17+i,p2[i],out.players[1]);bit(17+i,p2[i],out.single);}
    bit(25,th03::q,out.single);
    out.single|=out.players[0];
    return out;
}
}

void run_view(th03::Application& app, const std::function<th03::Frame()>& frame, unsigned frame_limit) {
#ifdef _WIN32
    SetProcessDPIAware();
    ViewFrames images;images.update(app,frame);
    WNDCLASSA wc{}; wc.lpfnWndProc=procedure; wc.lpszClassName="TH03Port64";
    wc.hInstance=GetModuleHandle(nullptr); wc.hCursor=LoadCursor(nullptr,IDC_ARROW);
    if (!RegisterClassA(&wc)) throw std::runtime_error("cannot register native window");
    Window state{&images};
    HWND window=CreateWindowA(wc.lpszClassName,"TH03 port64",WS_OVERLAPPEDWINDOW,
                              CW_USEDEFAULT,CW_USEDEFAULT,1296,840,nullptr,nullptr,wc.hInstance,&state);
    if (!window) throw std::runtime_error("cannot create native window");
    ShowWindow(window,SW_SHOW);UpdateWindow(window);
    th03::FrameTimer timer;
#else
    if (SDL_Init(SDL_INIT_VIDEO|SDL_INIT_EVENTS)!=0) throw std::runtime_error(SDL_GetError());
    SDL_Window* window=SDL_CreateWindow("TH03 port64",SDL_WINDOWPOS_CENTERED,
                                        SDL_WINDOWPOS_CENTERED,1280,800,SDL_WINDOW_RESIZABLE);
    SDL_Renderer* renderer=window ? SDL_CreateRenderer(window,-1,SDL_RENDERER_SOFTWARE) : nullptr;
    SDL_Texture* texture=renderer ? SDL_CreateTexture(renderer,SDL_PIXELFORMAT_ARGB8888,SDL_TEXTUREACCESS_STREAMING,640,400) : nullptr;
    if (!texture) { SDL_QuitSubSystem(SDL_INIT_VIDEO); throw std::runtime_error("cannot create SDL video output"); }
    SDL_RenderSetLogicalSize(renderer,640,400);
    ViewFrames images;images.update(app,frame);
    SDL_UpdateTexture(texture,nullptr,images.pixels().data(),640*sizeof(std::uint32_t));
    bool exposed=true;
#endif
    const auto now=[] {return std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count();};
    th03::FrameSchedule schedule(now());
    unsigned frames=0;
    bool quit=false;
    while(!quit&&!app.finished()&&(!frame_limit||frames<frame_limit)) {
#ifdef _WIN32
        MSG message;
        for(unsigned count=0;count<64&&PeekMessage(&message,nullptr,0,0,PM_REMOVE);++count) {
            if(message.message==WM_QUIT) {quit=true;break;}
            TranslateMessage(&message);DispatchMessage(&message);
        }
#else
        SDL_Event event;
        for(unsigned count=0;count<64&&SDL_PollEvent(&event);++count) {
            if(event.type==SDL_QUIT)quit=true;
            if(event.type==SDL_WINDOWEVENT&&(event.window.event==SDL_WINDOWEVENT_EXPOSED||
                event.window.event==SDL_WINDOWEVENT_SIZE_CHANGED))exposed=true;
        }
#endif
        if(quit)break;
        schedule.wake();bool stepped=false;
        while(!app.finished()&&(!frame_limit||frames<frame_limit)&&schedule.due(now())) {
            th03::InputFrame input;
#ifdef _WIN32
            const auto held=[&](int key){return GetForegroundWindow()==window && (GetAsyncKeyState(key)&0x8000);};
            constexpr int codes[]={VK_UP,VK_DOWN,VK_LEFT,VK_RIGHT,'Z','X',VK_SPACE,VK_ESCAPE,VK_RETURN,
                               'F','H','T','B','R','Y','V','N',VK_NUMPAD7,VK_NUMPAD8,VK_NUMPAD9,
                               VK_NUMPAD4,VK_NUMPAD6,VK_NUMPAD1,VK_NUMPAD2,VK_NUMPAD3,'Q'};
            input=keyboard_input(held,codes);
#else
            const auto* keys=SDL_GetKeyboardState(nullptr);
            const auto held=[&](int key){return (SDL_GetWindowFlags(window)&SDL_WINDOW_INPUT_FOCUS)&&keys[key];};
            constexpr int codes[]={SDL_SCANCODE_UP,SDL_SCANCODE_DOWN,SDL_SCANCODE_LEFT,SDL_SCANCODE_RIGHT,
                SDL_SCANCODE_Z,SDL_SCANCODE_X,SDL_SCANCODE_SPACE,SDL_SCANCODE_ESCAPE,SDL_SCANCODE_RETURN,
                SDL_SCANCODE_F,SDL_SCANCODE_H,SDL_SCANCODE_T,SDL_SCANCODE_B,SDL_SCANCODE_R,SDL_SCANCODE_Y,
                SDL_SCANCODE_V,SDL_SCANCODE_N,SDL_SCANCODE_KP_7,SDL_SCANCODE_KP_8,SDL_SCANCODE_KP_9,
                SDL_SCANCODE_KP_4,SDL_SCANCODE_KP_6,SDL_SCANCODE_KP_1,SDL_SCANCODE_KP_2,SDL_SCANCODE_KP_3,SDL_SCANCODE_Q};
            input=keyboard_input(held,codes);
#endif
            app.tick(input);++frames;stepped=true;schedule.completed();
        }
        schedule.resync(now());
        if(stepped) {
            const bool changed=images.update(app,frame);
#ifdef _WIN32
            if(changed) {InvalidateRect(window,nullptr,FALSE);UpdateWindow(window);}
#else
            if(changed) {SDL_UpdateTexture(texture,nullptr,images.pixels().data(),640*sizeof(std::uint32_t));exposed=true;}
#endif
        }
#ifndef _WIN32
        if(exposed) {
            SDL_SetRenderDrawColor(renderer,0,0,0,255);SDL_RenderClear(renderer);
            SDL_RenderCopy(renderer,texture,nullptr,nullptr);SDL_RenderPresent(renderer);exposed=false;
        }
#endif
        if(app.finished()||(frame_limit&&frames>=frame_limit))break;
#ifdef _WIN32
        timer.wait(schedule.next()-now());
#else
        std::this_thread::sleep_until(std::chrono::steady_clock::time_point(std::chrono::nanoseconds(schedule.next())));
#endif
    }

#ifdef _WIN32
    if (IsWindow(window)) DestroyWindow(window);
    UnregisterClassA(wc.lpszClassName,wc.hInstance);
#else
    SDL_DestroyTexture(texture); SDL_DestroyRenderer(renderer); SDL_DestroyWindow(window); SDL_QuitSubSystem(SDL_INIT_VIDEO);
#endif
}
