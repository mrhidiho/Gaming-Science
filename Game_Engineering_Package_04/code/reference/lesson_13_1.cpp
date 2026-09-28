// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "structures.hpp"
#include <stdexcept>


int main() {
    return p4test::run("13.1", [] {

        ge::IntBuffer exact(false),doubling(true);
        CHECK(p4test::throws<std::out_of_range>([&]{exact.at(0);}));
        for(int i=0;i<8;++i) {exact.push(i);doubling.push(i);}
        CHECK(exact.moved()==28);CHECK(doubling.moved()==7);
        doubling.push(8);CHECK(doubling.moved()==15);
        for(std::size_t i=0;i<8;++i) {CHECK(exact.at(i)==static_cast<int>(i));CHECK(doubling.at(i)==static_cast<int>(i));}
        CHECK(p4test::throws<std::out_of_range>([&]{exact.at(exact.size());}));
        ge::IntBuffer many(true);
        for(int i=0;i<1000;++i) many.push(i);
        CHECK(many.moved()<2*many.size());CHECK(many.capacity()>=many.size());
        for(std::size_t i=0;i<many.size();++i) CHECK(many.at(i)==static_cast<int>(i));
        ge::IntBuffer bounded(true);
        for(std::size_t i=0;i<ge::IntBuffer::limit;++i) bounded.push(0);
        CHECK(p4test::throws<std::length_error>([&]{bounded.push(1);}));
        CHECK(bounded.size()==ge::IntBuffer::limit);

    });
}
