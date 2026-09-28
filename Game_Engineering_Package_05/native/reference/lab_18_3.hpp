#pragma once
#include <atomic>
#include <cstdint>
#include <thread>
#include <stdexcept>
namespace course {
inline std::uint64_t publish_once(std::uint64_t input) {
    std::uint64_t payload=0;
    std::atomic<bool> ready{false};
    std::jthread producer([&]{
        payload=input;
        ready.store(true,std::memory_order_release);
    });
    // One publication, immutable payload afterward. No flag reset/reuse.
    while(!ready.load(std::memory_order_acquire)) std::this_thread::yield();
    const auto result=payload;
    producer.join();
    return result;
}
}
