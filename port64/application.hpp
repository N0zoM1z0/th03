#pragma once
#include "selection.hpp"
#include <optional>

namespace th03 {
enum class Phase {op,versus,selection,mainl_handoff,quit};
class Application {
public:
    Application(const PfArchive& assets,Options options,const Bytes& nem,const std::string& picture="TL02.PI");
    void tick(const InputFrame& input);
    Frame render() const;
    bool finished() const {return phase==Phase::quit||phase==Phase::mainl_handoff;}
    void start_selection(SelectKind kind);
    void return_to_title();
    Phase phase=Phase::op;
    Menu menu;
    Resident resident;
    Selection selection;
private:
    const PfArchive& assets_;
    PiImage background_;
    Bytes font_,window_;
    std::optional<SelectionAssets> selection_assets_;
    unsigned available_=7,transition_wait_=0;
    std::int8_t return_selection_=0;
};
}
