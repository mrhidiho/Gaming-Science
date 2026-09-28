#pragma once
#include <cstdint>
#include <cstddef>
#include <stdexcept>
namespace course {
class DirectCache {
public:
 DirectCache(std::size_t, std::uint64_t) {throw std::logic_error("TODO 16.3");}
 bool access(std::uint64_t) {throw std::logic_error("TODO 16.3");}
 void reset() {throw std::logic_error("TODO 16.3");}
};
}
