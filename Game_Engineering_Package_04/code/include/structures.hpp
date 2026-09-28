#pragma once
#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <memory>
#include <optional>
#include <stdexcept>
#include <utility>
#include <vector>
namespace ge {
class IntBuffer {
    std::unique_ptr<int[]> data_;
    std::size_t size_ = 0, capacity_ = 0;
    std::uint64_t moved_ = 0;
    bool doubling_;
public:
    static constexpr std::size_t limit = 1000000;
    explicit IntBuffer(bool doubling = true) : doubling_(doubling) {}
    // The educational buffer deliberately forbids moving too: default moving
    // a pointer but copying size/capacity would break the source invariant.
    IntBuffer(const IntBuffer&) = delete;
    IntBuffer& operator=(const IntBuffer&) = delete;
    IntBuffer(IntBuffer&&) = delete;
    IntBuffer& operator=(IntBuffer&&) = delete;
    void push(int value) {
        if (size_ == limit) throw std::length_error("buffer budget");
        if (size_ == capacity_) {
            const std::size_t next = !doubling_ ? capacity_ + 1 :
                (capacity_ == 0 ? 1 : std::min(limit, capacity_ * 2));
            auto candidate = std::make_unique<int[]>(next);
            for (std::size_t i = 0; i < size_; ++i) candidate[i] = data_[i];
            moved_ += size_;
            data_.swap(candidate); capacity_ = next;
        }
        data_[size_++] = value;
    }
    int at(std::size_t i) const {
        if (i >= size_) throw std::out_of_range("buffer index");
        return data_[i];
    }
    std::size_t size() const noexcept { return size_; }
    std::size_t capacity() const noexcept { return capacity_; }
    std::uint64_t moved() const noexcept { return moved_; }
};
template<std::size_t Capacity>
class Ring {
    static_assert(Capacity > 0 && Capacity <= 1000000);
    std::array<int, Capacity> data_{};
    std::size_t head_ = 0, count_ = 0;
public:
    bool push(int value) noexcept {
        if (count_ == Capacity) return false;
        data_[(head_ + count_) % Capacity] = value;
        ++count_; return true;
    }
    std::optional<int> pop() noexcept {
        if (count_ == 0) return std::nullopt;
        const int result = data_[head_];
        head_ = (head_ + 1) % Capacity;
        --count_; return result;
    }
    std::size_t size() const noexcept { return count_; }
};
// Restricted int->int separate-chaining table. No stable iterator promise.
class IntMap {
    using Bucket = std::vector<std::pair<int,int>>;
    std::vector<Bucket> buckets_{4};
    std::size_t size_ = 0;
    bool collide_;
    std::size_t bucket_for(int key, std::size_t n) const {
        return collide_ ? 0 : std::hash<int>{}(key) % n;
    }
    void rehash(std::size_t n) {
        std::vector<Bucket> candidate(n);
        for (const auto& bucket : buckets_)
            for (const auto& kv : bucket)
                candidate[bucket_for(kv.first,n)].push_back(kv);
        buckets_.swap(candidate);
    }
public:
    explicit IntMap(bool force_collisions=false) : collide_(force_collisions) {}
    // Moving only buckets_ while copying size_ would invalidate the source.
    // This narrow teaching map deliberately provides neither copy nor move.
    IntMap(const IntMap&) = delete;
    IntMap& operator=(const IntMap&) = delete;
    IntMap(IntMap&&) = delete;
    IntMap& operator=(IntMap&&) = delete;
    void insert(int key, int value) {
        for (auto& kv : buckets_[bucket_for(key,buckets_.size())])
            if (kv.first == key) { kv.second = value; return; }
        if (size_ >= 65536) throw std::length_error("map budget");
        if (size_ + 1 > buckets_.size()) rehash(buckets_.size()*2);
        buckets_[bucket_for(key,buckets_.size())].push_back({key,value});
        ++size_;
    }
    std::optional<int> find(int key) const {
        for (const auto& kv : buckets_[bucket_for(key,buckets_.size())])
            if (kv.first == key) return kv.second;
        return std::nullopt;
    }
    bool erase(int key) {
        auto& bucket = buckets_[bucket_for(key,buckets_.size())];
        const auto it = std::find_if(bucket.begin(),bucket.end(),
            [key](const auto& kv){ return kv.first == key; });
        if (it == bucket.end()) return false;
        bucket.erase(it); --size_; return true;
    }
    std::size_t size() const noexcept { return size_; }
    bool invariant() const {
        std::size_t count=0;
        for (std::size_t b=0;b<buckets_.size();++b) {
            const auto& bucket=buckets_[b]; count+=bucket.size();
            for (std::size_t i=0;i<bucket.size();++i) {
                if (bucket_for(bucket[i].first,buckets_.size())!=b) return false;
                for (std::size_t j=0;j<i;++j)
                    if (bucket[i].first==bucket[j].first) return false;
            }
        }
        return count==size_;
    }
};
class MinHeap {
    std::vector<int> data_;
public:
    void push(int value) {
        if(data_.size()>=1000000) throw std::length_error("heap budget");
        data_.push_back(value);
        std::size_t i=data_.size()-1;
        while(i>0) {
            const auto parent=(i-1)/2;
            if (!(data_[i]<data_[parent])) break;
            std::swap(data_[i],data_[parent]); i=parent;
        }
    }
    std::optional<int> pop() {
        if(data_.empty()) return std::nullopt;
        const int result=data_.front();
        data_.front()=data_.back(); data_.pop_back();
        std::size_t i=0;
        while(i<data_.size()/2) {
            std::size_t child=2*i+1;
            if(child+1<data_.size() && data_[child+1]<data_[child]) ++child;
            if(!(data_[child]<data_[i])) break;
            std::swap(data_[child],data_[i]); i=child;
        }
        return result;
    }
    bool invariant() const {
        for(std::size_t i=1;i<data_.size();++i)
            if(data_[i]<data_[(i-1)/2]) return false;
        return true;
    }
    std::size_t size() const noexcept { return data_.size(); }
};
}
