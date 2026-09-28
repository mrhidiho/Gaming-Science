#pragma once
#include <cstdint>
#include <span>
#include <stdexcept>
namespace course {
inline std::uint32_t sum_u32(std::span<const std::uint32_t>) {
 throw std::logic_error("TODO 16.1: implement low-32-bit sum");
}
}
