// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "graphs.hpp"
#include <algorithm>
#include <stdexcept>
#include <vector>


bool valid_order(const ge::Graph& g,const std::vector<std::size_t>& order) {
    if(order.size()!=g.size())return false;
    std::vector<std::size_t> pos(g.size(),g.size());
    for(std::size_t i=0;i<order.size();++i) {
        if(order[i]>=g.size() || pos[order[i]]!=g.size())return false;
        pos[order[i]]=i;
    }
    for(std::size_t u=0;u<g.size();++u)for(auto v:g[u])if(pos[u]>=pos[v])return false;
    return true;
}

int main() {
    return p4test::run("14.2", [] {

        ge::Graph diamond{{1,2},{3},{3},{},{}};
        const auto path=ge::bfs(diamond,0,3);CHECK(path==std::vector<std::size_t>{0,1,3});
        CHECK(!ge::bfs(diamond,0,4));CHECK(ge::bfs(diamond,2,2)==std::vector<std::size_t>{2});
        const auto order=ge::topological(diamond);CHECK(order.has_value());
        CHECK(valid_order(diamond,*order));
        diamond[3].push_back(0);CHECK(!ge::topological(diamond));CHECK(ge::bfs(diamond,0,3).has_value());
        CHECK(!ge::topological(ge::Graph{{0}}));
        CHECK(ge::topological(ge::Graph{})->empty());
        CHECK(p4test::throws<std::invalid_argument>([]{ge::bfs(ge::Graph{{9}},0,0);}));
        CHECK(p4test::throws<std::invalid_argument>([]{ge::bfs(ge::Graph{},0,0);}));
        ge::Graph duplicates{{1,1},{},{}};CHECK(valid_order(duplicates,*ge::topological(duplicates)));

    });
}
