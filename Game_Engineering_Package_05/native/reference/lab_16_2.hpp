#pragma once
#include <cstdint>
#include <span>
namespace course {
// Unsigned modular addition allows regrouping, unlike arbitrary float sums.
inline std::uint64_t sum_split(std::span<const std::uint64_t> a) {
    std::uint64_t x=0, y=0, z=0, w=0;
    std::size_t i=0;
    for (; a.size()-i >= 4; i+=4) {
        x+=a[i]; y+=a[i+1]; z+=a[i+2]; w+=a[i+3];
    }
    for (; i<a.size(); ++i) x+=a[i];
    return x+y+z+w;
}
}
