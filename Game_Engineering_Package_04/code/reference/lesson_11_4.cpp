// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "model.hpp"
#include <vector>


int main() {
    return p4test::run("11.4", [] {

        ge::UnitStore store;CHECK(!store.find(7));CHECK(!store.erase(7));
        CHECK(store.insert({7,{2,3},10}));CHECK(!store.insert({7,{9,9},0}));
        CHECK(store.size()==1);const auto copy=store.find(7);
        for(int id=100;id<300;++id) CHECK(store.insert({id,{0,0},1}));
        CHECK(store.find(7)==copy);CHECK(store.erase(7));CHECK(!store.find(7));
        CHECK(!store.erase(7));CHECK(store.size()==200);
        std::vector<ge::Unit> units;units.reserve(100);CHECK(units.size()==0);
        CHECK(units.capacity()>=100);
        units={{1,{0,0},0},{2,{0,0},5},{3,{0,0},0}};
        for(auto it=units.begin();it!=units.end();) {
            if(it->hit_points==0) it=units.erase(it);else ++it;
        }
        CHECK(units.size()==1);CHECK(units[0].id==2);

    });
}
