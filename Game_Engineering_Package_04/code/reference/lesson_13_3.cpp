// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "structures.hpp"
#include <type_traits>
static_assert(!std::is_move_constructible_v<ge::IntMap>);
static_assert(!std::is_copy_constructible_v<ge::IntMap>);
#include <random>
#include <unordered_map>


int main() {
    return p4test::run("13.3", [] {

        for(bool force:{false,true}) {
            ge::IntMap table(force);std::unordered_map<int,int> oracle;std::mt19937 rng(1303);
            CHECK(!table.find(1));CHECK(!table.erase(1));
            for(int i=0;i<1000;++i) {
                const int key=static_cast<int>(rng()%101)-50;
                if(rng()%3==0) CHECK(table.erase(key)==(oracle.erase(key)!=0));
                else {table.insert(key,i);oracle[key]=i;}
                CHECK(table.invariant());CHECK(table.size()==oracle.size());
                for(const auto& [k,v]:oracle) CHECK(table.find(k)==v);
            }
            table.insert(999,1);const auto n=table.size();table.insert(999,2);
            CHECK(table.size()==n);CHECK(table.find(999)==2);CHECK(table.invariant());
        }

    });
}
