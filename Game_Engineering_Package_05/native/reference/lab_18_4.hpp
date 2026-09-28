#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <stdexcept>
#include <vector>
namespace course {
// deps[i] lists prerequisites of node i. Durations are chosen model units.
inline std::uint64_t critical_path(const std::vector<std::uint64_t>& durations,
                         const std::vector<std::vector<std::size_t>>& deps) {
    const auto n=durations.size();
    if(n!=deps.size() || n>1024) throw std::invalid_argument("invalid graph size");
    std::vector<std::size_t> indegree(n,0);
    std::vector<std::vector<std::size_t>> next(n);
    for(std::size_t i=0;i<n;++i) {
        auto copy=deps[i]; std::sort(copy.begin(),copy.end());
        if(std::adjacent_find(copy.begin(),copy.end())!=copy.end())
            throw std::invalid_argument("duplicate dependency");
        for(const auto d:copy) {
            if(d>=n || d==i) throw std::invalid_argument("invalid dependency");
            next[d].push_back(i); ++indegree[i];
        }
    }
    std::vector<std::size_t> ready;
    for(std::size_t i=0;i<n;++i) if(indegree[i]==0) ready.push_back(i);
    std::vector<std::uint64_t> finish(n,0),start(n,0);
    std::size_t done=0;
    while(done<ready.size()) {
        auto i=ready[done++];
        if(durations[i]>std::numeric_limits<std::uint64_t>::max()-start[i])
            throw std::overflow_error("modeled time overflow");
        finish[i]=start[i]+durations[i];
        for(auto j:next[i]) {
            start[j]=std::max(start[j],finish[i]);
            if(--indegree[j]==0) ready.push_back(j);
        }
    }
    if(done!=n) throw std::invalid_argument("dependency cycle");
    return n==0?0:*std::max_element(finish.begin(),finish.end());
}
}
