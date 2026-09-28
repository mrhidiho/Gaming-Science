#include <charconv>
#include <cstdint>
#include <iostream>
#include <string_view>
int main(int argc,char** argv) {
    if(argc<2 || argc>257) {std::cerr<<"expected 1..256 integers in 0..1000\n"; return 2;}
    std::uint64_t sum=0;
    for(int i=1;i<argc;++i) {
        std::string_view s(argv[i]); unsigned value=0;
        const auto [end,ec]=std::from_chars(s.data(),s.data()+s.size(),value);
        if(ec!=std::errc{} || end!=s.data()+s.size() || value>1000 || s.empty()) {
            std::cerr<<"invalid bounded integer\n"; return 2;
        }
        sum+=static_cast<std::uint64_t>(value)*value;
    }
    std::cout<<sum<<'\n';
}
