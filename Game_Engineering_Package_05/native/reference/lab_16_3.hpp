#pragma once
#include <cstdint>
#include <cstddef>
#include <optional>
#include <stdexcept>
#include <vector>
namespace course {
class DirectCache {
    std::uint64_t line_bytes_;
    std::vector<std::optional<std::uint64_t>> tags_;
public:
    DirectCache(std::size_t lines, std::uint64_t line_bytes) : line_bytes_(line_bytes) {
        if (lines==0 || lines>65536 || line_bytes==0 || line_bytes>1048576)
            throw std::invalid_argument("invalid educational cache dimensions");
        tags_.resize(lines);
    }
    // Byte addresses; one access fits in one line. True means model hit.
    bool access(std::uint64_t address) {
        const auto block=address/line_bytes_;
        const auto index=static_cast<std::size_t>(block%tags_.size());
        const auto tag=block/tags_.size();
        const bool hit=tags_[index].has_value() && tags_[index].value()==tag;
        tags_[index]=tag;
        return hit;
    }
    void reset() { for (auto& t:tags_) t.reset(); }
};
}
