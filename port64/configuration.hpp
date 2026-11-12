#pragma once
#include "menu.hpp"
#include <filesystem>

namespace th03 {
class Configuration {
public:
    Configuration(Options fallback,std::filesystem::path directory={},Bytes original={});
    Options options() const {return {bytes_[0],bytes_[1],bytes_[2]};}
    const Bytes& bytes() const {return bytes_;}
    void save(Options options,bool exiting);
private:
    Bytes bytes_;
    std::filesystem::path path_;
};
}
