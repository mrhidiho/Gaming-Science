#include <array>
#include <charconv>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string_view>
#include <system_error>
#include <vector>
struct Cell {std::int64_t x=0,vx=1,y=0,vy=1;std::array<std::int64_t,4> unused{};};
std::size_t parse_size(const char* text,std::size_t max) {
    const std::string_view s(text);std::size_t n=0;
    const auto r=std::from_chars(s.data(),s.data()+s.size(),n);
    if(r.ec!=std::errc{} || r.ptr!=s.data()+s.size() || n==0 || n>max)
        throw std::invalid_argument("positive bounded integer expected");
    return n;
}
int main(int argc,char** argv) {
    try {
        if(argc>3)throw std::invalid_argument("usage: layout_benchmark [entities<=1000000] [rounds<=1000]");
        const std::size_t n=argc>1?parse_size(argv[1],1000000):100000;
        const std::size_t rounds=argc>2?parse_size(argv[2],1000):100;
        std::cout<<"sample,layout,entities,rounds,nanoseconds,checksum\n";
        for(int sample=0;sample<8;++sample)for(int order=0;order<2;++order) {
            const bool aos=(sample+order)%2==0;
            // Allocate and initialize outside the timed region for both layouts.
            std::vector<Cell> cells(aos?n:0);
            std::vector<std::int64_t> x(aos?0:n,0),vx(aos?0:n,1);
            const auto start=std::chrono::steady_clock::now();
            if(aos) {
                for(std::size_t r=0;r<rounds;++r)for(auto& cell:cells)cell.x+=cell.vx;
            } else {
                for(std::size_t r=0;r<rounds;++r)for(std::size_t i=0;i<n;++i)x[i]+=vx[i];
            }
            const auto end=std::chrono::steady_clock::now();
            std::int64_t checksum=0;
            if(aos)for(const auto& cell:cells)checksum+=cell.x;
            else for(auto value:x)checksum+=value;
            if(checksum!=static_cast<std::int64_t>(n)*static_cast<std::int64_t>(rounds))
                throw std::runtime_error("checksum mismatch");
            const auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(end-start).count();
            std::cout<<sample<<','<<(aos?"AoS":"SoA")<<','<<n<<','<<rounds<<','<<ns<<','<<checksum<<'\n';
        }
        return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
