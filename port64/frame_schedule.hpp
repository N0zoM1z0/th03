#pragma once
#include <cstdint>

namespace th03 {
// Host deadlines only. Resync discards overdue host waits without advancing
// game/PMD counters for discarded wall time. Preserve the existing 16,667 us
// cadence until raster attestation.
class FrameSchedule {
public:
    static constexpr std::int64_t period=16667000;
    static constexpr unsigned catchup_limit=4;
    explicit FrameSchedule(std::int64_t now):next_(now){}
    void wake(){steps_=0;}
    bool due(std::int64_t now)const{return steps_<catchup_limit&&now>=next_;}
    void completed(){next_+=period;++steps_;}
    void resync(std::int64_t now) {
        if(steps_==catchup_limit&&now>=next_)next_=now+period;
    }
    std::int64_t next()const{return next_;}
private:
    std::int64_t next_;
    unsigned steps_=0;
};
}
