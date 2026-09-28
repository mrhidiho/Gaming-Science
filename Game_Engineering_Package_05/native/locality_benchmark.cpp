#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
int main() {
    std::mt19937 random(2026);
    std::cout << "elements,trial,pattern,nanoseconds,checksum\n";
    for (std::size_t n : {4096U, 65536U, 1048576U}) {
        std::vector<std::uint32_t> data(n);
        for (auto& x : data) x = static_cast<std::uint32_t>(random() % 1024);
        const auto expected = std::accumulate(data.begin(), data.end(), std::uint64_t{0});
        std::vector<std::vector<std::size_t>> index(3);
        index[0].resize(n);
        std::iota(index[0].begin(), index[0].end(), std::size_t{0});
        // Cover EVERY element exactly once; this is not one sparse 1/16 sample.
        for (std::size_t r = 0; r < 16; ++r)
            for (std::size_t i = r; i < n; i += 16) index[1].push_back(i);
        index[2] = index[0];
        std::shuffle(index[2].begin(), index[2].end(), random);
        const char* names[] = {"sequential", "stride16_residues", "random"};
        for (int trial = -2; trial < 7; ++trial) {
            std::vector<int> order{0, 1, 2};
            std::shuffle(order.begin(), order.end(), random);
            for (int pattern : order) {
                std::uint64_t checksum = 0;
                const auto begin = std::chrono::steady_clock::now();
                for (const auto i : index[static_cast<std::size_t>(pattern)]) checksum += data[i];
                const auto end = std::chrono::steady_clock::now();
                if (checksum != expected) return 1;
                if (trial >= 0) {
                    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count();
                    std::cout << n << ',' << trial << ',' << names[pattern] << ',' << ns << ',' << checksum << '\n';
                }
            }
        }
    }
}
