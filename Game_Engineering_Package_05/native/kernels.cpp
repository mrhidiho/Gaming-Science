#include <cstddef>
#include <cstdint>
extern "C" std::uint64_t sum_serial(const std::uint64_t* a,std::size_t n) {
    std::uint64_t s=0; for(std::size_t i=0;i<n;++i)s+=a[i]; return s;
}
extern "C" std::uint64_t sum_four(const std::uint64_t* a,std::size_t n) {
    std::uint64_t s[4]={0,0,0,0}; std::size_t i=0;
    for(; n-i>=4;i+=4)for(std::size_t j=0;j<4;++j)s[j]+=a[i+j];
    for(;i<n;++i)s[0]+=a[i];
    return s[0]+s[1]+s[2]+s[3];
}
