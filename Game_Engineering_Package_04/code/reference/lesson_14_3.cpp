// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "graphs.hpp"
#include <algorithm>
#include <array>
#include <cstdlib>
#include <random>
#include <stdexcept>
#include <vector>


constexpr std::int64_t infinity=1000000000;
std::vector<std::vector<std::int64_t>> floyd(const ge::WeightedGraph& graph) {
    const auto n=graph.size();std::vector<std::vector<std::int64_t>> d(n,std::vector<std::int64_t>(n,infinity));
    for(std::size_t i=0;i<n;++i){d[i][i]=0;for(auto e:graph[i])d[i][e.to]=std::min(d[i][e.to],e.cost);}
    for(std::size_t k=0;k<n;++k)for(std::size_t i=0;i<n;++i)for(std::size_t j=0;j<n;++j)
        if(d[i][k]!=infinity && d[k][j]!=infinity)d[i][j]=std::min(d[i][j],d[i][k]+d[k][j]);
    return d;
}
bool valid_route(const ge::WeightedGraph& graph,const ge::Route& route) {
    if(route.path.empty())return false;
    std::int64_t total=0;
    for(std::size_t i=1;i<route.path.size();++i) {
        std::int64_t cost=infinity;
        for(auto e:graph[route.path[i-1]])if(e.to==route.path[i])cost=std::min(cost,e.cost);
        if (cost == infinity) { return false; }
        total += cost;
    }
    return total==route.cost;
}

int main() {
    return p4test::run("14.3", [] {

        ge::WeightedGraph counter{{{2,10},{1,1}},{{2,1}}, {}};
        CHECK(ge::dijkstra(counter,0,2)->cost==2);
        CHECK(ge::shortest_path(counter,0,2,[](std::size_t v){return v==1?100LL:0LL;})->cost==10);
        CHECK(ge::dijkstra(counter,0,0)->cost==0);CHECK(!ge::dijkstra(counter,2,0));
        CHECK(p4test::throws<std::invalid_argument>([]{ge::dijkstra(ge::WeightedGraph{{{1,-1}},{}},0,1);}));
        CHECK(ge::dijkstra(ge::WeightedGraph{{{1,0}},{}},0,1)->cost==0);
        std::mt19937 rng(1403);
        for(int trial=0;trial<30;++trial) {
            constexpr int side=5;constexpr std::size_t n=25;
            std::array<bool,n> blocked{};for(std::size_t i=1;i<n-1;++i)blocked[i]=rng()%5==0;
            ge::WeightedGraph graph(n);
            for(int y=0;y<side;++y)for(int x=0;x<side;++x) {
                const auto u=static_cast<std::size_t>(y*side+x);if(blocked[u])continue;
                for(const auto& delta:std::array<std::pair<int,int>,4>{{{1,0},{-1,0},{0,1},{0,-1}}}) {
                    const int nx=x+delta.first,ny=y+delta.second;
                    if(nx<0 || nx>=side || ny<0 || ny>=side)continue;
                    const auto v=static_cast<std::size_t>(ny*side+nx);if(blocked[v])continue;
                    graph[u].push_back({v,1+static_cast<std::int64_t>(rng()%4)});
                }
            }
            const auto baseline=floyd(graph);
            const auto d=ge::dijkstra(graph,0,24);
            const auto a=ge::shortest_path(graph,0,24,[](std::size_t v){
                return static_cast<std::int64_t>((4-v%5)+(4-v/5));
            });
            CHECK(a.has_value()==d.has_value());CHECK(d.has_value()==(baseline[0][24]<infinity));
            if(d) {CHECK(d->cost==baseline[0][24]);CHECK(a->cost==d->cost);CHECK(valid_route(graph,*d));CHECK(valid_route(graph,*a));}
        }

    });
}
