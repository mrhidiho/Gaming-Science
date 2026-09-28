// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include <array>
#include <charconv>
#include <climits>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <optional>
#include <stdexcept>
#include <string_view>
#include <system_error>


std::optional<std::size_t> parse_length(std::string_view text,std::size_t limit) {
    if(text.empty() || text.front()=='-') return std::nullopt;
    std::uint64_t value=0;
    const auto result=std::from_chars(text.data(),text.data()+text.size(),value);
    if(result.ec!=std::errc{} || result.ptr!=text.data()+text.size() || value>limit)
        return std::nullopt;
    return static_cast<std::size_t>(value);
}
bool fits_budget(std::size_t count,std::size_t item,std::size_t limit) {
    return item!=0 && count<=limit/item;
}
int checked_add(int a,int b) {
    if((b>0 && a>std::numeric_limits<int>::max()-b) ||
       (b<0 && a<std::numeric_limits<int>::min()-b))
        throw std::overflow_error("signed sum");
    return a+b;
}
std::array<std::uint8_t,4> encode(std::uint32_t x) {
    return {static_cast<std::uint8_t>(x&255u),static_cast<std::uint8_t>((x>>8)&255u),
            static_cast<std::uint8_t>((x>>16)&255u),static_cast<std::uint8_t>((x>>24)&255u)};
}
std::uint32_t decode(const std::array<std::uint8_t,4>& b) {
    return std::uint32_t{b[0]} | (std::uint32_t{b[1]}<<8) |
           (std::uint32_t{b[2]}<<16) | (std::uint32_t{b[3]}<<24);
}

int main() {
    return p4test::run("11.2", [] {

        std::cout<<"CHAR_BIT="<<CHAR_BIT<<" int_bytes="<<sizeof(int)
                 <<" pointer_bytes="<<sizeof(void*)<<" size_t_bytes="<<sizeof(std::size_t)<<'\n';
        CHECK(parse_length("0",1024)==0);CHECK(parse_length("1024",1024)==1024);
        for(auto bad:{"","-1","1025","12junk","9999999999999999999999999"})
            CHECK(!parse_length(bad,1024));
        CHECK(fits_budget(42,24,1024));CHECK(!fits_budget(43,24,1024));
        CHECK(!fits_budget(1,0,1024));
        CHECK(!fits_budget(std::numeric_limits<std::size_t>::max(),2,1024));
        CHECK(checked_add(20,22)==42);CHECK(checked_add(-5,2)==-3);
        CHECK(p4test::throws<std::overflow_error>([]{checked_add(std::numeric_limits<int>::max(),1);}));
        CHECK(p4test::throws<std::overflow_error>([]{checked_add(std::numeric_limits<int>::min(),-1);}));
        const auto bytes=encode(0x12345678u);
        CHECK(bytes==std::array<std::uint8_t,4>{0x78,0x56,0x34,0x12});
        CHECK(decode(bytes)==0x12345678u);
        for(auto x:{0u,1u,255u,65535u,0xffffffffu}) CHECK(decode(encode(x))==x);

    });
}
