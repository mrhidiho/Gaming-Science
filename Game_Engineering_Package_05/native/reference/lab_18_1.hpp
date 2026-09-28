#pragma once
#include <mutex>
#include <stdexcept>
#include <utility>
namespace course {
class Inventory {
    mutable std::mutex mutex_;
    int gold_, stock_;
public:
    Inventory(int gold, int stock) : gold_(gold),stock_(stock) {
        if(gold<0 || stock<0) throw std::invalid_argument("negative initial state");
    }
    bool buy(int price) {
        if(price<=0) throw std::invalid_argument("price must be positive");
        std::lock_guard guard(mutex_);
        if(stock_==0 || gold_<price) return false;
        gold_-=price; --stock_;
        return true;
    }
    std::pair<int,int> snapshot() const {
        std::lock_guard guard(mutex_);
        return {gold_,stock_};
    }
};
}
