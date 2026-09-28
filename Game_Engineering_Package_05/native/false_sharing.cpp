#include <atomic>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <thread>
struct Compact { std::atomic<std::uint64_t> value{0}; };
// 64 is an experimental alignment, NOT measured cache-line information.
struct alignas(64) Padded { std::atomic<std::uint64_t> value{0}; };
template<class Cell> bool run(const char* name, int trial) {
    Cell cells[2];
    const auto begin = std::chrono::steady_clock::now();
    std::jthread first([&]{ for(int i=0;i<100000;++i) cells[0].value.fetch_add(1,std::memory_order_relaxed); });
    std::jthread second([&]{ for(int i=0;i<100000;++i) cells[1].value.fetch_add(1,std::memory_order_relaxed); });
    first.join(); second.join();
    const auto end = std::chrono::steady_clock::now();
    const bool correct = cells[0].value==100000 && cells[1].value==100000;
    auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count();
    std::cout << trial << ',' << name << ',' << sizeof(Cell) << ',' << alignof(Cell) << ',' << ns << ',' << correct << '\n';
    return correct;
}
int main() {
    std::cout << "trial,layout,cell_bytes,alignment,nanoseconds,correct\n";
    for(int trial=0;trial<6;++trial) {
        // Alternate order to reduce a simple fixed-order bias.
        if(trial%2==0) { if(!run<Compact>("compact",trial)||!run<Padded>("padded64",trial)) return 1; }
        else { if(!run<Padded>("padded64",trial)||!run<Compact>("compact",trial)) return 1; }
    }
}
