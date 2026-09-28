#pragma once
#include <cstdint>
#include <span>
#include <stdexcept>
namespace course {
// Blocked scalar code: never claim intrinsic SIMD merely from this loop.
inline void add_blocks(std::span<const std::uint32_t> a,
                       std::span<const std::uint32_t> b,
                       std::span<std::uint32_t> out) {
    if (a.size()!=b.size() || a.size()!=out.size())
        throw std::invalid_argument("length mismatch");
    // Caller contract: output is disjoint or exactly aliases an entire input.
    // Partially overlapping spans are not supported.
    std::size_t i=0;
    for (; a.size()-i>=4; i+=4)
        for (std::size_t lane=0; lane<4; ++lane) out[i+lane]=a[i+lane]+b[i+lane];
    for (; i<a.size(); ++i) out[i]=a[i]+b[i];
}
}
