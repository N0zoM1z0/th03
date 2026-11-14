#pragma once
#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#include <cstdint>
#include <cstdlib>
#include <stdexcept>

namespace th03 {
// Process-local one-shot timer; message wakeups do not admit extra game ticks.
class FrameTimer {
public:
    FrameTimer() {
        const auto legacy=std::getenv("TH03_LEGACY_WINDOW_TIMER");
        if(!legacy||legacy[0]!='1'||legacy[1])
            timer_=CreateWaitableTimerExW(nullptr,nullptr,2,TIMER_MODIFY_STATE|SYNCHRONIZE);
    }
    ~FrameTimer(){if(timer_){CancelWaitableTimer(timer_);CloseHandle(timer_);}}
    FrameTimer(const FrameTimer&)=delete;
    FrameTimer& operator=(const FrameTimer&)=delete;
    void wait(std::int64_t remaining_ns) {
        if(remaining_ns<=0)return;
        if(timer_) {
            LARGE_INTEGER due{};due.QuadPart=-(remaining_ns+99)/100;
            if(SetWaitableTimer(timer_,&due,0,nullptr,nullptr,FALSE)) {
                if(MsgWaitForMultipleObjectsEx(1,&timer_,INFINITE,QS_ALLINPUT,MWMO_INPUTAVAILABLE)==WAIT_FAILED)
                    throw std::runtime_error("frame timer wait failed");
                return;
            }
            CloseHandle(timer_);timer_=nullptr;
        }
        // Older Windows / timer-arm failure: retain message-aware coarse waits.
        const auto timeout=DWORD((remaining_ns+999999)/1000000);
        if(MsgWaitForMultipleObjectsEx(0,nullptr,timeout,QS_ALLINPUT,MWMO_INPUTAVAILABLE)==WAIT_FAILED)
            throw std::runtime_error("frame message wait failed");
    }
private:
    HANDLE timer_=nullptr;
};
}
#endif
