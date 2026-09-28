#pragma once
#include <cstdint>
#include <span>
namespace course {
// Semantics of the teaching RV32 sum: low 32 bits; no ISA emulation.
inline std::uint32_t sum_u32(std::span<const std::uint32_t> values) {
    std::uint32_t acc = 0;
    for (const auto value : values) acc += value;
    return acc;
}
}
