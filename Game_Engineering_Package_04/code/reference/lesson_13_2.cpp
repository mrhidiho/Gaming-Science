// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "structures.hpp"
#include <deque>
#include <random>


int main() {
    return p4test::run("13.2", [] {

        ge::Ring<3> q;CHECK(!q.pop());
        CHECK(q.push(10));CHECK(q.push(20));CHECK(q.push(30));CHECK(!q.push(99));
        CHECK(q.pop()==10);CHECK(q.push(40));CHECK(q.pop()==20);CHECK(q.pop()==30);CHECK(q.pop()==40);CHECK(!q.pop());
        ge::Ring<1> one;
        for(int i=0;i<20;++i) {CHECK(one.push(i));CHECK(!one.push(99));CHECK(one.pop()==i);CHECK(!one.pop());}
        ge::Ring<7> ring;std::deque<int> oracle;std::mt19937 rng(1302);
        for(int i=0;i<5000;++i) {
            if(rng()%2==0) {
                const bool expected=oracle.size()<7;CHECK(ring.push(i)==expected);
                if(expected) oracle.push_back(i);
            } else {
                const auto result=ring.pop();CHECK(result.has_value()==!oracle.empty());
                if(result) {CHECK(*result==oracle.front());oracle.pop_front();}
            }
            CHECK(ring.size()==oracle.size());
        }

    });
}
