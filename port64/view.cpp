#include "view.hpp"
#include <chrono>
#include <stdexcept>
#include <thread>

#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
namespace {
struct Window { const std::function<th03::Frame()>* draw; };
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
            auto pixels=(*state->draw)();
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

void run_view(th03::Menu& menu, const std::function<th03::Frame()>& frame, unsigned frame_limit) {
#ifdef _WIN32
    SetProcessDPIAware();
    WNDCLASSA wc{}; wc.lpfnWndProc=procedure; wc.lpszClassName="TH03Port64";
    wc.hInstance=GetModuleHandle(nullptr); wc.hCursor=LoadCursor(nullptr,IDC_ARROW);
    if (!RegisterClassA(&wc)) throw std::runtime_error("cannot register native window");
    Window state{&frame};
    HWND window=CreateWindowA(wc.lpszClassName,"TH03 port64 - title/menu bring-up",WS_OVERLAPPEDWINDOW,
                              CW_USEDEFAULT,CW_USEDEFAULT,1296,840,nullptr,nullptr,wc.hInstance,&state);
    if (!window) throw std::runtime_error("cannot create native window");
    ShowWindow(window,SW_SHOW);
#else
    if (SDL_Init(SDL_INIT_VIDEO|SDL_INIT_EVENTS)!=0) throw std::runtime_error(SDL_GetError());
    SDL_Window* window=SDL_CreateWindow("TH03 port64 - title/menu bring-up",SDL_WINDOWPOS_CENTERED,
                                        SDL_WINDOWPOS_CENTERED,1280,800,SDL_WINDOW_RESIZABLE);
    SDL_Renderer* renderer=window ? SDL_CreateRenderer(window,-1,SDL_RENDERER_SOFTWARE) : nullptr;
    SDL_Texture* texture=renderer ? SDL_CreateTexture(renderer,SDL_PIXELFORMAT_ARGB8888,SDL_TEXTUREACCESS_STREAMING,640,400) : nullptr;
    if (!texture) { SDL_Quit(); throw std::runtime_error("cannot create SDL video output"); }
    SDL_RenderSetLogicalSize(renderer,640,400);
#endif
    unsigned frames=0;
    bool quit=false;
    auto deadline=std::chrono::steady_clock::now();
    while (!quit && menu.screen!=th03::Screen::quit && menu.screen!=th03::Screen::handoff &&
           (!frame_limit || frames<frame_limit)) {
        std::uint16_t input=0;
#ifdef _WIN32
        MSG message;
        while (PeekMessage(&message,nullptr,0,0,PM_REMOVE)) {
            if (message.message==WM_QUIT) quit=true;
            TranslateMessage(&message); DispatchMessage(&message);
        }
        const auto held=[&](int key){return GetForegroundWindow()==window && (GetAsyncKeyState(key)&0x8000);};
        if (held(VK_UP)) input|=th03::up;
        if (held(VK_DOWN)) input|=th03::down;
        if (held(VK_LEFT)) input|=th03::left;
        if (held(VK_RIGHT)) input|=th03::right;
        if (held('Z') || held(VK_SPACE)) input|=th03::shot;
        if (held('X')) input|=th03::bomb;
        if (held(VK_ESCAPE)) input|=th03::cancel;
        if (held(VK_RETURN)) input|=th03::ok;
        menu.tick(input);
        InvalidateRect(window,nullptr,FALSE); UpdateWindow(window);
#else
        SDL_Event event;
        while (SDL_PollEvent(&event)) if (event.type==SDL_QUIT) quit=true;
        const auto* keys=SDL_GetKeyboardState(nullptr);
        if (SDL_GetWindowFlags(window)&SDL_WINDOW_INPUT_FOCUS) {
            if (keys[SDL_SCANCODE_UP]) input|=th03::up;
            if (keys[SDL_SCANCODE_DOWN]) input|=th03::down;
            if (keys[SDL_SCANCODE_LEFT]) input|=th03::left;
            if (keys[SDL_SCANCODE_RIGHT]) input|=th03::right;
            if (keys[SDL_SCANCODE_Z] || keys[SDL_SCANCODE_SPACE]) input|=th03::shot;
            if (keys[SDL_SCANCODE_X]) input|=th03::bomb;
            if (keys[SDL_SCANCODE_ESCAPE]) input|=th03::cancel;
            if (keys[SDL_SCANCODE_RETURN]) input|=th03::ok;
        }
        menu.tick(input);
        auto pixels=frame();
        SDL_UpdateTexture(texture,nullptr,pixels.data(),640*sizeof(std::uint32_t));
        SDL_SetRenderDrawColor(renderer,0,0,0,255); SDL_RenderClear(renderer);
        SDL_RenderCopy(renderer,texture,nullptr,nullptr); SDL_RenderPresent(renderer);
#endif
        ++frames;
        deadline+=std::chrono::microseconds(16667);
        std::this_thread::sleep_until(deadline);
    }
#ifdef _WIN32
    if (IsWindow(window)) DestroyWindow(window);
    UnregisterClassA(wc.lpszClassName,wc.hInstance);
#else
    SDL_DestroyTexture(texture); SDL_DestroyRenderer(renderer); SDL_DestroyWindow(window); SDL_Quit();
#endif
}
