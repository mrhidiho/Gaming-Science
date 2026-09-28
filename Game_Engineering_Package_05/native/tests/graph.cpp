
#include "task_graph.hpp"
#include <atomic>
#include <iostream>
#include <stdexcept>
void check(bool b){if(!b)throw std::runtime_error("graph check failed");}
int main(){
 int cases=0;
 for(std::size_t workers:{1U,2U,4U}){
  std::vector<int>output(101,0);std::vector<course::Task>g;
  for(std::size_t i=0;i<100;++i)g.push_back({{},[&,i]{output[i]=static_cast<int>(i);}});
  std::vector<std::size_t>deps(100);for(std::size_t i=0;i<100;++i)deps[i]=i;
  g.push_back({deps,[&]{for(std::size_t i=0;i<100;++i)output[100]+=output[i];}});
  auto r=course::execute_graph(g,workers);
  check(output[100]==4950);for(auto st:r.state)check(st==course::TaskState::done);++cases;
 }
 {std::atomic<int>count{0};std::vector<course::Task>g{
  {{},[]{throw std::runtime_error("injected");}},
  {{0},[&]{++count;}},{{1},[&]{++count;}},{{},[&]{++count;}}};
  auto r=course::execute_graph(g,3);check(count==1);check(r.state[0]==course::TaskState::failed);
  check(r.state[1]==course::TaskState::blocked && r.state[2]==course::TaskState::blocked);
  check(r.state[3]==course::TaskState::done);check(bool(r.errors[0]));++cases;}
 {check(course::execute_graph({},1).state.empty());++cases;}
 {bool rejected=false;try{course::execute_graph({},0);}catch(const std::invalid_argument&){rejected=true;}check(rejected);++cases;}
 {bool rejected=false;try{course::execute_graph({{{1},[]{}},{{0},[]{}}},2);}catch(const std::invalid_argument&){rejected=true;}check(rejected);++cases;}
 {bool rejected=false;try{course::execute_graph({{{}, {}}},2);}catch(const std::invalid_argument&){rejected=true;}check(rejected);++cases;}
 std::cout<<"graph_cases="<<cases<<" passed="<<cases<<'\n';
}
