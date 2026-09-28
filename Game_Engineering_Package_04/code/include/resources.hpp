#pragma once
#include <stdexcept>
#include <utility>
namespace ge {
// Counts must outlive every MockOwner borrowing them. Single-threaded only.
struct Counts { int acquired = 0, released = 0, live = 0; };
class MockOwner {
    Counts* counts_ = nullptr;
    int id_ = 0;
    void release() noexcept {
        if (counts_) { ++counts_->released; --counts_->live; }
        counts_ = nullptr; id_ = 0;
    }
public:
    MockOwner() noexcept = default;
    explicit MockOwner(Counts& c) noexcept : counts_(&c), id_(++c.acquired) {
        ++c.live;
    }
    ~MockOwner() { release(); }
    MockOwner(const MockOwner&) = delete;
    MockOwner& operator=(const MockOwner&) = delete;
    MockOwner(MockOwner&& other) noexcept
        : counts_(std::exchange(other.counts_, nullptr)),
          id_(std::exchange(other.id_, 0)) {}
    MockOwner& operator=(MockOwner&& other) noexcept {
        if (this != &other) {
            release();
            counts_ = std::exchange(other.counts_, nullptr);
            id_ = std::exchange(other.id_, 0);
        }
        return *this;
    }
    void swap(MockOwner& other) noexcept {
        std::swap(counts_, other.counts_); std::swap(id_, other.id_);
    }
    int id() const noexcept { return id_; }
};
inline MockOwner load_mock(Counts& counts, bool fail) {
    MockOwner candidate(counts);
    if (fail) throw std::runtime_error("injected validation failure");
    return candidate;
}
inline void replace_mock(MockOwner& current, Counts& counts, bool fail) {
    auto candidate = load_mock(counts, fail);
    current.swap(candidate);
}
}
