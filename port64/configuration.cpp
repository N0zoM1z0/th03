#include "configuration.hpp"
#include <algorithm>
#include <fstream>
#include <iterator>
#include <stdexcept>
#ifdef _WIN32
#ifndef NOMINMAX
#define NOMINMAX
#endif
#include <windows.h>
#endif

namespace th03 {
Configuration::Configuration(Options fallback,std::filesystem::path directory,Bytes original):bytes_(std::move(original)) {
    if(bytes_.empty())bytes_={fallback.music,fallback.keys,fallback.rank,0,0,0,0,0};
    if(!directory.empty()) {
        path_=std::move(directory)/"YUME.CFG";
        if(std::filesystem::exists(path_)) {
            std::ifstream input(path_,std::ios::binary);if(!input)throw std::runtime_error("cannot read native YUME.CFG");
            bytes_=Bytes(std::istreambuf_iterator<char>(input),{});
            if(input.bad())throw std::runtime_error("native YUME.CFG read failed");
        }
    }
    if(bytes_.size()!=8||bytes_[0]>2||bytes_[1]>2||bytes_[2]>3)throw std::runtime_error("unsupported native YUME.CFG");
}
void Configuration::save(Options options,bool exiting) {
    bytes_[0]=options.music;bytes_[1]=options.keys;bytes_[2]=options.rank;
    // DOS cfg_save writes an indeterminate stack byte at offset3. The native
    // file retains its opaque byte there; no real-mode segment becomes a pointer.
    if(exiting)std::fill(bytes_.begin()+3,bytes_.end(),0);
    if(path_.empty())return;
    std::filesystem::create_directories(path_.parent_path());auto temporary=path_;temporary+=".tmp";
    std::ofstream output(temporary,std::ios::binary|std::ios::trunc);
    if(!output)throw std::runtime_error("cannot create native configuration temporary file");
    output.write(reinterpret_cast<const char*>(bytes_.data()),std::streamsize(bytes_.size()));output.flush();
    if(!output)throw std::runtime_error("cannot write native configuration");
    output.close();if(!output)throw std::runtime_error("cannot close native configuration temporary file");
#ifdef _WIN32
    if(!MoveFileExW(temporary.c_str(),path_.c_str(),MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("cannot replace native YUME.CFG");
#else
    std::filesystem::rename(temporary,path_);
#endif
}
}
