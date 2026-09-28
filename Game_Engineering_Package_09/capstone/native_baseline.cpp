// Optional measured host baseline. C++17, no third-party libraries.
// Model hardware frequency and transfer estimates are NOT measured by this file.
#include <algorithm>
#include <cfenv>
#include <charconv>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string_view>
#include <vector>

static std::size_t parse(const char* text, std::size_t lo, std::size_t hi) {
    std::string_view s(text); std::size_t result=0;
    auto [p, ec]=std::from_chars(s.data(),s.data()+s.size(),result);
    if (ec!=std::errc{} || p!=s.data()+s.size() || result<lo || result>hi)
        throw std::invalid_argument("numeric argument outside supported range");
    return result;
}
static std::int16_t transform(std::int16_t x) {
    const std::int64_t product=static_cast<std::int64_t>(x)*384;
    const bool negative=product<0;
    const std::int64_t mag=negative ? -product : product;
    std::int64_t q=mag/256, rem=mag%256;
    if (rem>128 || (rem==128 && (q&1))) ++q;
    const std::int64_t rounded=negative ? -q : q;
    return static_cast<std::int16_t>(std::clamp<std::int64_t>(rounded+64,-32768,32767));
}
static void contiguous(const std::vector<std::int16_t>& in,std::vector<std::int16_t>& out) {
    for (std::size_t i=0;i<in.size();++i) out[i]=transform(in[i]);
}
static void blocked(const std::vector<std::int16_t>& in,std::vector<std::int16_t>& out) {
    constexpr std::size_t block=256;
    for (std::size_t begin=0;begin<in.size();begin+=block)
        for (std::size_t i=begin;i<std::min(begin+block,in.size());++i) out[i]=transform(in[i]);
}
int main(int argc,char** argv) {
    try {
        if (argc>3) throw std::invalid_argument("usage: baseline [N 0..10000000] [repetitions 1..2000]");
        const std::size_t n=argc>1 ? parse(argv[1],0,10000000) : 65536;
        const std::size_t reps=argc>2 ? parse(argv[2],1,2000) : 30;
        if (std::fesetround(FE_TONEAREST)!=0) throw std::runtime_error("rounding mode unavailable");
        std::vector<std::int16_t> in(n),out(n),gold(n);
        for (std::size_t i=0;i<n;++i) {
            in[i]=static_cast<std::int16_t>(static_cast<std::int64_t>((i*37)%20001)-10000);
            // Independent exact-double oracle: these small binary values are exact.
            auto rounded=static_cast<std::int64_t>(std::nearbyint(static_cast<double>(in[i])*1.5));
            gold[i]=static_cast<std::int16_t>(std::clamp<std::int64_t>(rounded+64,-32768,32767));
        }
        std::cout << "n,phase,run,variant,elapsed_ns,checksum,correct\n";
        for (std::size_t r=0;r<reps+5;++r) {
            for (int j=0;j<2;++j) {
                const int which=(j+static_cast<int>(r%2))%2; // alternate paired order
                const auto start=std::chrono::steady_clock::now();
                if (which==0) contiguous(in,out); else blocked(in,out);
                const auto end=std::chrono::steady_clock::now();
                if (out!=gold) throw std::runtime_error("wrong result; reject timing");
                std::int64_t checksum=0; for (auto value:out) checksum+=value;
                const auto ns=std::chrono::duration_cast<std::chrono::nanoseconds>(end-start).count();
                std::cout << n << ',' << (r<5?"warmup":"sample") << ',' << r << ','
                          << (which==0?"contiguous":"blocked") << ',' << ns << ',' << checksum << ",true\n";
            }
        }
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n'; return EXIT_FAILURE;
    }
}
