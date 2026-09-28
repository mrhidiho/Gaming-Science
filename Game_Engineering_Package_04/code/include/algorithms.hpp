#pragma once
#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <optional>
#include <span>
#include <stdexcept>
#include <utility>
#include <vector>
namespace ge {
inline std::size_t lower_bound_index(std::span<const int> a, int x) {
    std::size_t lo=0,hi=a.size();
    while(lo<hi) {
        const auto mid=lo+(hi-lo)/2;
        if(a[mid]<x) lo=mid+1; else hi=mid;
    }
    return lo;
}
template<class T, class Less>
void insertion_sort(std::vector<T>& a, Less less) {
    for(std::size_t i=1;i<a.size();++i) {
        T value=a[i]; std::size_t j=i;
        while(j>0 && less(value,a[j-1])) { a[j]=a[j-1]; --j; }
        a[j]=value;
    }
}
template<class T, class Less>
void merge_sort(std::vector<T>& a, Less less) {
    if(a.size()<2) return;
    const auto mid=a.size()/2;
    using Diff=typename std::vector<T>::difference_type;
    std::vector<T> left(a.begin(),a.begin()+static_cast<Diff>(mid));
    std::vector<T> right(a.begin()+static_cast<Diff>(mid),a.end());
    merge_sort(left,less); merge_sort(right,less);
    std::size_t i=0,j=0,k=0;
    while(i<left.size() && j<right.size()) {
        // Take left on equivalence: preserves stability.
        if(less(right[j],left[i])) a[k++]=right[j++];
        else a[k++]=left[i++];
    }
    while(i<left.size()) a[k++]=left[i++];
    while(j<right.size()) a[k++]=right[j++];
}
struct Item { std::size_t weight; std::int64_t value; };
inline void validate_items(std::span<const Item> items,std::size_t capacity) {
    if(capacity>10000 || items.size()>100)
        throw std::length_error("knapsack teaching budget");
    for(const auto& item:items)
        if(item.weight==0 || item.value<0 || item.value>1000000)
            throw std::invalid_argument("item domain");
}
inline std::int64_t knapsack(std::span<const Item> items,std::size_t capacity) {
    validate_items(items,capacity);
    std::vector<std::int64_t> best(capacity+1,0);
    for(const auto& item:items) {
        if(item.weight>capacity) continue;
        for(std::size_t b=capacity;b>=item.weight;--b) {
            best[b]=std::max(best[b],item.value+best[b-item.weight]);
            if(b==item.weight) break;
        }
    }
    return best[capacity];
}
inline std::int64_t knapsack_brute(std::span<const Item> items,std::size_t capacity) {
    validate_items(items,capacity);
    if(items.size()>20) throw std::length_error("exhaustive item budget");
    std::int64_t best=0;
    const auto subsets=std::uint64_t{1}<<items.size();
    for(std::uint64_t mask=0;mask<subsets;++mask) {
        std::size_t weight=0; std::int64_t value=0; bool fits=true;
        for(std::size_t i=0;i<items.size();++i) {
            if((mask&(std::uint64_t{1}<<i))==0) continue;
            if(items[i].weight>capacity-weight) { fits=false; break; }
            weight+=items[i].weight; value+=items[i].value;
        }
        if(fits) best=std::max(best,value);
    }
    return best;
}
}
