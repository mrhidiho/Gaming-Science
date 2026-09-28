#include "lab_18_2.hpp"
#include <iostream>
#include <thread>
#include <vector>
int main() {
    course::BoundedQueue queue(2);
    std::vector<int> seen;
    std::jthread consumer([&]{
        while(auto value=queue.pop()) seen.push_back(*value);
    });
    for(int value=1;value<=5;++value) queue.push(value);
    queue.close();
    consumer.join();
    for(auto value:seen) std::cout<<value<<' ';
    std::cout<<'\n';
}
