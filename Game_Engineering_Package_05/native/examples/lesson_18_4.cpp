#include "task_graph.hpp"
#include <array>
#include <iostream>
int main(){std::array<int,3> output{0,0,0};
std::vector<course::Task> graph{{{},[&]{output[0]=6;}},{{},[&]{output[1]=9;}},{{0,1},[&]{output[2]=output[0]+output[1];}}};
auto report=course::execute_graph(graph,2);
for(auto s:report.state)if(s!=course::TaskState::done)return 1;
std::cout<<"result="<<output[2]<<" modeled_span="<<course::critical_path({2,5,1},{{},{},{0,1}})<<'\n';}
