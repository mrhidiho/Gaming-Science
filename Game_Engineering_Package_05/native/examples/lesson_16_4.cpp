#include "lab_16_4.hpp"
#include <array>
#include <iostream>
int main(){std::array<std::uint32_t,5>a{1,2,3,4,5},b{10,20,30,40,50},o{};course::add_blocks(a,b,o);for(auto v:o)std::cout<<v<<' ';std::cout<<'\n';}
