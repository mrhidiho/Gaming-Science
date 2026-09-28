// C++17 one-shot publication. A passing run is not proof of all executions.
#include <atomic>
#include <charconv>
#include <cstddef>
#include <iostream>
#include <stdexcept>
#include <string_view>
#include <thread>

struct Payload { int value = 0; int checksum = 0; };

int main(int argc, char** argv) {
    int rounds = 200;
    if (argc > 2) { std::cerr << "Usage: publication [rounds:1..100000]\n"; return 2; }
    if (argc == 2) {
        const std::string_view text{argv[1]};
        const auto result = std::from_chars(text.data(), text.data() + text.size(), rounds);
        if (result.ec != std::errc{} || result.ptr != text.data() + text.size() ||
            rounds < 1 || rounds > 100000) {
            std::cerr << "Invalid round count\n"; return 2;
        }
    }
    for (int i = 0; i < rounds; ++i) {
        Payload payload;
        std::atomic<bool> ready{false};
        bool valid = false; // Only consumer writes; main reads after join.
        std::thread consumer([&] {
            while (!ready.load(std::memory_order_acquire)) { std::this_thread::yield(); }
            valid = payload.value == 42 && payload.checksum == 42 * 17;
        });
        // Main is the producer. No further payload writes after publication.
        payload.value = 42;
        payload.checksum = 42 * 17;
        ready.store(true, std::memory_order_release);
        consumer.join();
        if (!valid) { std::cerr << "Publication failed at round " << i << '\n'; return 1; }
    }
    std::cout << "PASS: " << rounds << " independent one-shot publications\n";
    return 0;
}
