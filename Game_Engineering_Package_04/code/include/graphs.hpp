#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <optional>
#include <queue>
#include <stdexcept>
#include <tuple>
#include <vector>
namespace ge {
using Graph=std::vector<std::vector<std::size_t>>;
inline void validate_graph(const Graph& g) {
    if(g.size()>10000) throw std::length_error("graph vertex budget");
    std::size_t edges=0;
    for(const auto& adjacency:g) {
        if(adjacency.size()>1000000-edges) throw std::length_error("edge budget");
        edges+=adjacency.size();
        for(auto v:adjacency) if(v>=g.size()) throw std::invalid_argument("bad vertex");
    }
}
inline std::vector<std::size_t> reconstruct(
        const std::vector<std::size_t>& parent,std::size_t source,std::size_t goal) {
    std::vector<std::size_t> path;
    for(std::size_t v=goal;;v=parent[v]) {
        if(v>=parent.size() || path.size()>=parent.size())
            throw std::logic_error("invalid predecessor chain");
        path.push_back(v); if(v==source) break;
    }
    std::reverse(path.begin(),path.end()); return path;
}
inline std::optional<std::vector<std::size_t>> bfs(
        const Graph& g,std::size_t source,std::size_t goal) {
    validate_graph(g);
    if(source>=g.size() || goal>=g.size()) throw std::invalid_argument("bad endpoint");
    std::vector<bool> seen(g.size(),false);
    std::vector<std::size_t> parent(g.size(),g.size());
    std::queue<std::size_t> q; q.push(source); seen[source]=true;
    while(!q.empty()) {
        const auto u=q.front();q.pop();
        if(u==goal) return reconstruct(parent,source,goal);
        for(auto v:g[u]) if(!seen[v]) {
            seen[v]=true; parent[v]=u; q.push(v);
        }
    }
    return std::nullopt;
}
// FIFO frontier: O(V+E). Input vertex order and adjacency order determine ties.
inline std::optional<std::vector<std::size_t>> topological(const Graph& g) {
    validate_graph(g); std::vector<std::size_t> indegree(g.size(),0),order;
    for(const auto& neighbors:g) for(auto v:neighbors) ++indegree[v];
    std::queue<std::size_t> q;
    for(std::size_t v=0;v<g.size();++v) if(indegree[v]==0) q.push(v);
    while(!q.empty()) {
        const auto u=q.front();q.pop();order.push_back(u);
        for(auto v:g[u]) if(--indegree[v]==0) q.push(v);
    }
    if(order.size()!=g.size()) return std::nullopt;
    return order;
}
struct Edge { std::size_t to; std::int64_t cost; };
using WeightedGraph=std::vector<std::vector<Edge>>;
inline constexpr std::int64_t distance_limit=1000000000000LL;
struct Route {
    std::int64_t cost=0;
    std::vector<std::size_t> path;
    std::size_t expansions=0,pushes=0;
};
inline std::optional<Route> shortest_path(const WeightedGraph& g,
    std::size_t source,std::size_t goal,
    const std::function<std::int64_t(std::size_t)>& heuristic) {
    if(g.size()>10000) throw std::length_error("graph vertex budget");
    if(source>=g.size() || goal>=g.size()) throw std::invalid_argument("bad endpoint");
    std::size_t edges=0;
    for(const auto& neighbors:g) {
        if(neighbors.size()>1000000-edges) throw std::length_error("edge budget");
        edges+=neighbors.size();
        for(auto e:neighbors)
            if(e.to>=g.size() || e.cost<0 || e.cost>1000000000)
                throw std::invalid_argument("edge domain");
    }
    auto h=[&](std::size_t v) {
        const auto value=heuristic(v);
        if(value<0 || value>distance_limit) throw std::invalid_argument("heuristic domain");
        return value;
    };
    if(h(goal)!=0) throw std::invalid_argument("goal heuristic must be zero");
    using Entry=std::tuple<std::int64_t,std::int64_t,std::size_t>; // f,g,id
    std::priority_queue<Entry,std::vector<Entry>,std::greater<Entry>> q;
    std::vector<std::int64_t> dist(g.size(),distance_limit+1);
    std::vector<std::size_t> parent(g.size(),g.size());
    dist[source]=0;q.push({h(source),0,source});
    std::size_t expansions=0,pushes=1;
    while(!q.empty()) {
        const auto [f,old_g,u]=q.top();q.pop(); (void)f;
        if(old_g!=dist[u]) continue;
        ++expansions;
        if(u==goal) return Route{dist[u],reconstruct(parent,source,goal),expansions,pushes};
        for(auto edge:g[u]) {
            if(dist[u]>distance_limit-edge.cost)
                throw std::overflow_error("candidate distance budget");
            const auto candidate=dist[u]+edge.cost;
            if(candidate<dist[edge.to]) {
                dist[edge.to]=candidate;parent[edge.to]=u;
                q.push({candidate+h(edge.to),candidate,edge.to});++pushes;
            }
        }
    }
    return std::nullopt;
}
inline std::optional<Route> dijkstra(const WeightedGraph& g,std::size_t s,std::size_t t) {
    return shortest_path(g,s,t,[](std::size_t){return std::int64_t{0};});
}
}
