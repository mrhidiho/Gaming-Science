#pragma once
#include <cstdint>
#include <span>
#include <stdexcept>
namespace course {
inline void add_blocks(std::span<const std::uint32_t>, std::span<const std::uint32_t>, std::span<std::uint32_t>) {
 throw std::logic_error("TODO 16.4: check lengths; process all tails safely");
}
}
