// Volume 9 native semantic probe. uint32 arithmetic is modulo 2^32.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <random>
#include <span>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint32_t;
std::vector<U> scan_reference(std::span<const U> a) {
    std::vector<U> out(a.size());
    std::exclusive_scan(a.begin(),a.end(),out.begin(),U{0});
    return out;
}
std::vector<U> scan_tree(std::span<const U> values) {
    if(values.empty()) return {};
    std::size_t size=1;
    while(size<values.size()) {
        if(size > std::vector<U>().max_size()/2) throw std::length_error("scan too large");
        size*=2;
    }
    std::vector<U> work(size,0);
    std::copy(values.begin(),values.end(),work.begin());
    for(std::size_t step=2; step<=size; step*=2) {
        for(std::size_t j=step-1; j<size; j+=step) work[j]+=work[j-step/2];
        if(step==size) break; // No overflow after the final level.
    }
    work.back()=0;
    for(std::size_t step=size;step>=2;step/=2)
        for(std::size_t j=step-1;j<size;j+=step) {
            const auto t=work[j-step/2];work[j-step/2]=work[j];work[j]+=t;
        }
    work.resize(values.size());return work;
}
U expression(U x) { return (x+U{0})*(U{2}+U{3}); }
U optimized_expression(U x) { return x*U{5}; }
void check(bool truth,const std::string& name) {
    if(!truth) throw std::runtime_error("FAILED: "+name);
}
void tests() {
    std::mt19937 rng(45);
    const std::vector<std::size_t> sizes{0,1,2,3,7,31,32,33,1023,1024,1025,65537};
    for(auto n:sizes) {
        std::vector<U> a(n);for(auto& v:a)v=rng();
        check(scan_reference(a)==scan_tree(a),"scan size "+std::to_string(n));
    }
    for(int i=0;i<100000;++i) {const auto x=rng();check(expression(x)==optimized_expression(x),"u32 folding");}
    std::vector<U> recurrence{7,0,0,0};
    for(std::size_t i=1;i<recurrence.size();++i)recurrence[i]=recurrence[i-1]+1;
    check(recurrence==std::vector<U>({7,8,9,10}),"loop-carried dependency");
    std::cout<<"PASS: 12 scan sizes; 100000 u32 cases; recurrence contract\n";
}
void benchmark() {
    std::mt19937 rng(42);std::vector<U>a(1<<18);for(auto&v:a)v=rng();
    U checksum=0;
    // Warm both functions; randomize order within each pair.
    auto x=scan_reference(a);auto y=scan_tree(a);check(x==y,"benchmark equality");
    std::cout<<"pair,method,elapsed_ns,checksum\n";
    for(int pair=0;pair<12;++pair) {
        const bool tree_first=(rng()&1U)!=0;
        for(int order=0;order<2;++order) {
            const bool tree=(order==0)==tree_first;
            const auto start=std::chrono::steady_clock::now();
            const auto out=tree?scan_tree(a):scan_reference(a);
            const auto end=std::chrono::steady_clock::now();
            checksum^=out.back();
            std::cout<<pair<<','<<(tree?"cpu_tree":"std_exclusive_scan")<<','
              <<std::chrono::duration_cast<std::chrono::nanoseconds>(end-start).count()<<','<<out.back()<<'\n';
        }
    }
    std::cerr<<"consumed checksum="<<checksum<<"; within-process diagnostic pairs only\n";
}
int main(int argc,char**argv) {
    try {if(argc==2&&std::string(argv[1])=="--bench")benchmark();else tests();return 0;}
    catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
