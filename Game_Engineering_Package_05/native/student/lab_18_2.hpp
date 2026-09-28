#pragma once
#include <cstddef>
#include <optional>
#include <stdexcept>
namespace course {
class BoundedQueue {
public:
 explicit BoundedQueue(std::size_t) {throw std::logic_error("TODO 18.2");}
 bool push(int) {throw std::logic_error("TODO 18.2");}
 std::optional<int> pop() {throw std::logic_error("TODO 18.2");}
 void close(bool=true) {throw std::logic_error("TODO 18.2");}
};
}
