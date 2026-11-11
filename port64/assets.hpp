#pragma once
#include "pi_image.hpp"
#include <string>
#include <vector>

Bytes read_file(const std::string& path);
void write_file(const std::string& path, const Bytes& bytes);
// Original CP932 FAT 8.3 name: 夢時空1.DAT (OP and MAINL).
inline const std::string op_archive_name("\x96\xb2\x8e\x9e\x8b\xf3" "1 DAT", 11);
Bytes hdi_file(const Bytes& image, const std::string& short_name);
struct ArchiveEntry {
    std::string name;
    std::uint16_t type{}, packed_size{}, size{};
    std::uint8_t key{};
    std::uint32_t offset{};
};
class PfArchive {
public:
    explicit PfArchive(Bytes bytes);
    const std::vector<ArchiveEntry>& entries() const { return entries_; }
    Bytes read(std::string name) const;
private:
    Bytes bytes_;
    std::vector<ArchiveEntry> entries_;
};
