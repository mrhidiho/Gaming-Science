#include "task_graph.hpp"
#include <chrono>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <thread>
#include <vector>
int main() {
    std::cout << "workers,trial,nanoseconds,checksum\n";
    std::vector<std::uint64_t> data(1048576,3);
    for(std::size_t workers:{1U,2U,4U}) {
        for(int trial=0;trial<5;++trial) {
            std::vector<std::uint64_t> partial(64,0);
            std::vector<course::Task> tasks;
            for(std::size_t i=0;i<partial.size();++i) {
                tasks.push_back({{},[&,i]{
                    std::uint64_t result=0;
                    for(std::size_t j=i*16384;j<(i+1)*16384;++j) result+=data[j]*data[j];
                    partial[i]=result;
                }});
            }
            const auto begin=std::chrono::steady_clock::now();
            auto report=course::execute_graph(tasks,workers);
            const auto sum=std::accumulate(partial.begin(),partial.end(),std::uint64_t{0});
            const auto end=std::chrono::steady_clock::now();
            for(auto state:report.state)if(state!=course::TaskState::done)return 1;
            if(sum!=9437184)return 2;
            std::cout<<workers<<','<<trial<<','<<std::chrono::duration_cast<std::chrono::nanoseconds>(end-begin).count()<<','<<sum<<'\n';
        }
    }
}
