#pragma once
#include <stdexcept>
#include <utility>
namespace course {
class Inventory {
public:
 Inventory(int,int) {throw std::logic_error("TODO 18.1");}
 bool buy(int) {throw std::logic_error("TODO 18.1");}
 std::pair<int,int> snapshot() const {throw std::logic_error("TODO 18.1");}
};
}
