#pragma once
#include <condition_variable>
#include <cstddef>
#include <mutex>
#include <optional>
#include <stdexcept>
#include <vector>
namespace course {
// Fixed storage after construction. One owner closes and joins users before destruction.
class BoundedQueue {
    std::mutex mutex_;
    std::condition_variable readable_, writable_;
    std::vector<int> slots_;
    std::size_t head_=0, tail_=0, size_=0;
    bool closed_=false;
public:
    explicit BoundedQueue(std::size_t capacity) {
        if(capacity==0 || capacity>65536) throw std::invalid_argument("invalid capacity");
        slots_.resize(capacity);
    }
    bool push(int value) {
        std::unique_lock lock(mutex_);
        writable_.wait(lock,[&]{return closed_ || size_<slots_.size();});
        if(closed_) return false;
        slots_[tail_]=value;
        tail_=(tail_+1)%slots_.size(); ++size_;
        lock.unlock(); readable_.notify_one();
        return true;
    }
    std::optional<int> pop() {
        std::unique_lock lock(mutex_);
        readable_.wait(lock,[&]{return closed_ || size_>0;});
        if(size_==0) return std::nullopt;
        const int value=slots_[head_];
        head_=(head_+1)%slots_.size(); --size_;
        lock.unlock(); writable_.notify_one();
        return value;
    }
    // drain=true keeps accepted entries; false discards pending entries.
    // A value already popped belongs to its consumer and is not revoked.
    void close(bool drain=true) {
        {
            std::lock_guard guard(mutex_);
            closed_=true;
            if(!drain) {size_=0; head_=tail_;}
        }
        readable_.notify_all(); writable_.notify_all();
    }
};
}
