#include "lab_16_3.hpp"
#include <iostream>
int main(){course::DirectCache c(2,16); for(std::uint64_t a:{0,4,32,0,16,20})std::cout<<a<<':'<<(c.access(a)?"hit":"miss")<<'\n';}
