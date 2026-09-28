#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <vector>
extern "C" std::uint64_t sum_serial(const std::uint64_t*,std::size_t);
extern "C" std::uint64_t sum_four(const std::uint64_t*,std::size_t);
int main() {
    std::mt19937_64 random(42);
    std::cout<<"elements,trial,variant,nanoseconds,checksum\n";
    for(std::size_t n:{4096U,65536U,1048576U}) {
        std::vector<std::uint64_t> a(n);
        for(auto& x:a) x=random()%1024;
        const auto expected=std::accumulate(a.begin(),a.end(),std::uint64_t{0});
        using Fn=std::uint64_t(*)(const std::uint64_t*,std::size_t);
        Fn functions[2]={sum_serial,sum_four};
        for(int warm=0;warm<3;++warm)for(auto f:functions)if(f(a.data(),n)!=expected)return 1;
        for(int trial=0;trial<9;++trial) {
            std::vector<int> order={0,1}; std::shuffle(order.begin(),order.end(),random);
            for(int variant:order) {
                auto begin=std::chrono::steady_clock::now();
                auto checksum=functions[variant](a.data(),n);
                auto end=std::chrono::steady_clock::now();
                if(checksum!=expected) return 2;
                auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count();
                std::cout<<n<<','<<trial<<','<<(variant==0?"serial":"four")<<','<<ns<<','<<checksum<<'\n';
            }
        }
    }
}
