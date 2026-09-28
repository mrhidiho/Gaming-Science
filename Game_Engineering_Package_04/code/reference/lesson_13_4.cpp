// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "structures.hpp"
#include <random>
#include <set>
#include <tuple>
#include <queue>
#include <functional>


int main() {
    return p4test::run("13.4", [] {

        ge::MinHeap heap;std::multiset<int> oracle;std::mt19937 rng(1304);CHECK(!heap.pop());
        for(int i=0;i<4000;++i) {
            if(oracle.empty() || rng()%2==0) {
                const int value=static_cast<int>(rng()%101)-50;heap.push(value);oracle.insert(value);
            } else {
                CHECK(heap.pop()==*oracle.begin());oracle.erase(oracle.begin());
            }
            CHECK(heap.invariant());CHECK(heap.size()==oracle.size());
        }
        while(!oracle.empty()) {CHECK(heap.pop()==*oracle.begin());oracle.erase(oracle.begin());CHECK(heap.invariant());}
        CHECK(!heap.pop());
        using Event=std::pair<int,int>;std::priority_queue<Event,std::vector<Event>,std::greater<Event>> events;
        events.push({5,2});events.push({5,1});events.push({3,9});
        CHECK(events.top()==Event{3,9});events.pop();CHECK(events.top()==Event{5,1});

    });
}
