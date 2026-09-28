#include "lab_18_1.hpp"
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>
int main() {
    course::Inventory inventory(100,20);
    std::atomic<int> sold{0};
    std::vector<std::jthread> workers;
    for (int i=0;i<4;++i) {
        workers.emplace_back([&]{
            for(int j=0;j<20;++j) {
                if(inventory.buy(10)) sold.fetch_add(1);
            }
        });
    }
    for(auto& thread:workers) thread.join();
    const auto [gold,stock]=inventory.snapshot();
    std::cout<<"sold="<<sold.load()<<" gold="<<gold<<" stock="<<stock<<'\n';
}
