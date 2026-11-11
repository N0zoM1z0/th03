// FAT/PF reader adapted from TH04 port/modern-64 1ba7107 (MIT).
#include "assets.hpp"
#include <algorithm>
#include <fstream>
#include <iterator>
#include <stdexcept>
#include <cctype>

static void require(bool ok, const char* reason) {
    if (!ok) throw std::runtime_error(reason);
}

static uint16_t le16(const Bytes& b, size_t p) {
    require(p <= b.size() && b.size() - p >= 2, "short LE16 field");
    return uint16_t(b[p] | (uint16_t(b[p + 1]) << 8));
}

static uint32_t le32(const Bytes& b, size_t p) {
    return uint32_t(le16(b, p)) | (uint32_t(le16(b, p + 2)) << 16);
}

Bytes read_file(const std::string& name) {
    std::ifstream in(name, std::ios::binary);
    require(bool(in), "cannot open input file");
    Bytes b((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    require(!b.empty(), "empty input file");
    return b;
}

void write_file(const std::string& name, const Bytes& b) {
    std::ofstream out(name, std::ios::binary);
    require(bool(out), "cannot open output file");
    out.write(reinterpret_cast<const char*>(b.data()), std::streamsize(b.size()));
    require(bool(out), "cannot write output file");
}

namespace {
class Fat12 {
public:
    explicit Fat12(const Bytes& image) : b(image) {
        constexpr size_t p = 38912;
        require(b.size() >= p + 512, "short PC-98 HDI");
        sector = le16(b, p + 11);
        cluster_sectors = b[p + 13];
        const auto reserved = le16(b, p + 14);
        const auto fats = b[p + 16];
        const auto entries = le16(b, p + 17);
        const auto sectors = le16(b, p + 19);
        const auto fat_sectors = le16(b, p + 22);
        require(sector == 1024 && cluster_sectors == 8 && reserved == 1 &&
                fats == 2 && entries == 1536 && sectors == 20706 &&
                fat_sectors == 4, "unexpected TH03 FAT12 geometry");
        require(p + size_t(sectors) * sector <= b.size(), "FAT12 volume truncated");
        fat_start = p + size_t(reserved) * sector;
        const size_t fat_bytes = size_t(fat_sectors) * sector;
        require(std::equal(b.begin() + fat_start, b.begin() + fat_start + fat_bytes,
                           b.begin() + fat_start + fat_bytes), "FAT mirrors disagree");
        root = fat_start + size_t(fats) * fat_bytes;
        const size_t root_sectors = (size_t(entries) * 32 + sector - 1) / sector;
        data = root + root_sectors * sector;
        max_cluster = 1 + (sectors - reserved - fats * fat_sectors - root_sectors) / cluster_sectors;
    }

    Bytes game_file(const std::string& name) const {
        const size_t dir = find({root}, "YUMEZIKU   ");
        const auto dirs = chain(le16(b, dir + 26));
        std::vector<size_t> offsets;
        for (auto c : dirs) offsets.push_back(cluster_offset(c));
        // CP932 short name of the original OP/ending resource archive.
        const size_t file = find(offsets, name);
        return file_bytes(le16(b, file + 26), le32(b, file + 28));
    }

private:
    const Bytes& b;
    size_t sector{}, cluster_sectors{}, fat_start{}, root{}, data{}, max_cluster{};

    uint16_t next(uint16_t cluster) const {
        require(cluster >= 2 && cluster <= max_cluster, "FAT cluster out of range");
        uint16_t word = le16(b, fat_start + cluster + cluster / 2);
        return cluster & 1 ? (word >> 4) & 0xfff : word & 0xfff;
    }

    std::vector<uint16_t> chain(uint16_t first) const {
        std::vector<uint16_t> result;
        std::vector<bool> seen(max_cluster + 1);
        for (uint16_t c = first; c < 0xff8; c = next(c)) {
            require(c >= 2 && c <= max_cluster && !seen[c], "invalid FAT chain");
            seen[c] = true;
            result.push_back(c);
        }
        require(!result.empty(), "empty FAT chain");
        return result;
    }

    size_t cluster_offset(uint16_t c) const {
        require(c >= 2 && c <= max_cluster, "cluster out of range");
        const size_t at = data + (size_t(c) - 2) * sector * cluster_sectors;
        require(at <= b.size() && b.size() - at >= sector * cluster_sectors,
                "cluster outside image");
        return at;
    }

    size_t find(const std::vector<size_t>& dirs, const std::string& name) const {
        require(name.size() == 11, "FAT name must be 11 bytes");
        for (size_t start : dirs) {
            const size_t end = start + (start == root ? 1536 * 32 : sector * cluster_sectors);
            require(end <= b.size(), "directory outside image");
            for (size_t at = start; at < end; at += 32) {
                if (b[at] == 0) break;
                if (b[at] != 0xe5 && b[at + 11] != 0x0f &&
                    std::equal(name.begin(), name.end(), b.begin() + at,
                               [](char a, uint8_t c) { return uint8_t(a) == c; })) return at;
            }
        }
        throw std::runtime_error("YUMEZIKU or game file missing from HDI");
    }

    Bytes file_bytes(uint16_t first, size_t size) const {
        const auto clusters = chain(first);
        const size_t cluster_bytes = sector * cluster_sectors;
        require(size <= clusters.size() * cluster_bytes, "file exceeds FAT chain");
        Bytes out;
        out.reserve(size);
        for (uint16_t c : clusters) {
            const auto at = cluster_offset(c);
            const auto n = std::min(size - out.size(), cluster_bytes);
            out.insert(out.end(), b.begin() + at, b.begin() + at + n);
            if (out.size() == size) break;
        }
        return out;
    }
};
}

Bytes hdi_file(const Bytes& image, const std::string& name) { return Fat12(image).game_file(name); }

PfArchive::PfArchive(Bytes bytes) : bytes_(std::move(bytes)) {
    require(bytes_.size() >= 16, "short PF archive");
    const auto count = le16(bytes_, 4);
    const auto size = le16(bytes_, 0);
    require(count && size == (std::size_t(count) + 1) * 32 &&
            16 + std::size_t(size) <= bytes_.size() && le16(bytes_, 6) <= 255,
            "invalid PF directory");
    Bytes directory(bytes_.begin() + 16, bytes_.begin() + 16 + size);
    auto key = std::uint8_t(le16(bytes_, 6));
    // The key subtracts the decoded byte, with byte wrap, after each XOR.
    for (auto& value : directory) {
        value ^= key;
        key = std::uint8_t(key - value);
    }
    require(std::all_of(directory.end() - 32, directory.end(),
                        [](auto value) { return value == 0; }), "PF terminal record changed");
    for (std::size_t i = 0; i < count; ++i) {
        const auto at = i * 32;
        const auto first = directory.begin() + at + 3;
        const auto last = std::find(first, first + 13, 0);
        ArchiveEntry entry{std::string(first, last), le16(directory, at),
                           le16(directory, at + 16), le16(directory, at + 18),
                           directory[at + 2], le32(directory, at + 20)};
        require(entry.offset >= 16 + std::size_t(size) && entry.offset <= bytes_.size() &&
                entry.packed_size <= bytes_.size() - entry.offset, "PF member outside archive");
        require(entry.type == 0xf388 || entry.type == 0x9595, "unknown PF compression");
        entries_.push_back(std::move(entry));
    }
}

Bytes PfArchive::read(std::string wanted) const {
    std::transform(wanted.begin(), wanted.end(), wanted.begin(),
                   [](unsigned char c) { return char(std::toupper(c)); });
    for (const auto& entry : entries_) {
        if (entry.name != wanted) continue;
        Bytes out;
        int previous = -1;
        for (std::size_t at = entry.offset; at < entry.offset + entry.packed_size; ++at) {
            const auto value = std::uint8_t(bytes_[at] ^ entry.key);
            out.push_back(value);
            // PF RLE: equal consecutive bytes introduce a further repeat count.
            if (entry.type == 0x9595 && value == previous) {
                require(++at < entry.offset + entry.packed_size, "PF repeat count missing");
                out.insert(out.end(), bytes_[at] ^ entry.key, value);
            }
            previous = value;
            require(out.size() <= std::size_t(entry.size) + 1, "PF expansion exceeds length");
        }
        // pfread() exposes logical_size bytes even when the final run is longer.
        require(out.size() == entry.size || out.size() == std::size_t(entry.size) + 1,
                "PF expanded length differs");
        out.resize(entry.size);
        return out;
    }
    throw std::runtime_error("PF member missing: " + wanted);
}
