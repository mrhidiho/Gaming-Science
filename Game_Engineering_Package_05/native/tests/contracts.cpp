
#include "lab_16_1.hpp"
#include "lab_16_2.hpp"
#include "lab_16_3.hpp"
#include "lab_16_4.hpp"
#include "lab_18_1.hpp"
#include "lab_18_2.hpp"
#include "lab_18_3.hpp"
#include "lab_18_4.hpp"
#include <algorithm>
#include <array>
#include <atomic>
#include <functional>
#include <future>
#include <iostream>
#include <limits>
#include <numeric>
#include <random>
#include <string>
#include <thread>
#include <vector>
struct Case { std::string id,name; std::function<void()> run; };
void require(bool b){if(!b)throw std::runtime_error("contract assertion failed");}
template<class E,class F> void rejects(F f){bool hit=false;try{f();}catch(const E&){hit=true;}require(hit);}
int main(int argc,char** argv){
 std::vector<Case> cases;
 auto add=[&](std::string id,std::string name,std::function<void()> f){cases.push_back({id,name,f});};
 add("16.1","empty",[]{require(course::sum_u32({})==0);});
 add("16.1","known",[]{std::array<std::uint32_t,4>a{7,11,0,5};require(course::sum_u32(a)==23);});
 add("16.1","wrap",[]{std::array<std::uint32_t,2>a{UINT32_MAX,2};require(course::sum_u32(a)==1);});
 add("16.1","one",[]{std::array<std::uint32_t,1>a{UINT32_MAX};require(course::sum_u32(a)==UINT32_MAX);});
 add("16.1","zeros",[]{std::vector<std::uint32_t>a(100,0);require(course::sum_u32(a)==0);});
 add("16.1","slice",[]{std::array<std::uint32_t,5>a{99,1,2,3,88};require(course::sum_u32(std::span(a).subspan(1,3))==6);});
 add("16.1","property",[]{std::mt19937 r(77);for(int n=0;n<129;++n){std::vector<std::uint32_t>a(static_cast<std::size_t>(n));std::uint64_t wide=0;for(auto& v:a){v=static_cast<std::uint32_t>(r());wide+=v;}require(course::sum_u32(a)==static_cast<std::uint32_t>(wide));}});
 add("16.1","input_unchanged",[]{std::vector<std::uint32_t>a{2,3,4};auto before=a;(void)course::sum_u32(a);require(a==before);});
 add("16.2","empty",[]{require(course::sum_split({})==0);});
 add("16.2","tails",[]{for(std::size_t n=0;n<65;++n){std::vector<std::uint64_t>a(n);std::iota(a.begin(),a.end(),std::uint64_t{1});require(course::sum_split(a)==n*(n+1)/2);}});
 add("16.2","wrap",[]{std::array<std::uint64_t,5>a{UINT64_MAX,1,0,0,7};require(course::sum_split(a)==7);});
 add("16.2","property",[]{std::mt19937_64 r(44);for(int trial=0;trial<50;++trial){std::vector<std::uint64_t>a(257);for(auto&x:a)x=r();require(course::sum_split(a)==std::accumulate(a.begin(),a.end(),std::uint64_t{0}));}});
 add("16.2","input_unchanged",[]{std::vector<std::uint64_t>a{8,9};auto before=a;(void)course::sum_split(a);require(a==before);});
 add("16.2","slice",[]{std::array<std::uint64_t,6>a{99,2,4,6,8,99};require(course::sum_split(std::span(a).subspan(1,4))==20);});
 add("16.3","cold",[]{course::DirectCache c(2,16);require(!c.access(0));});
 add("16.3","same_line",[]{course::DirectCache c(2,16);c.access(0);require(c.access(15));});
 add("16.3","conflict",[]{course::DirectCache c(2,16);c.access(0);require(!c.access(32));require(!c.access(0));});
 add("16.3","distinct_index",[]{course::DirectCache c(2,16);c.access(0);c.access(16);require(c.access(0));require(c.access(16));});
 add("16.3","reset",[]{course::DirectCache c(2,16);c.access(0);c.reset();require(!c.access(0));});
 add("16.3","zero_lines",[]{rejects<std::invalid_argument>([]{course::DirectCache c(0,16);});});
 add("16.3","zero_bytes",[]{rejects<std::invalid_argument>([]{course::DirectCache c(2,0);});});
 add("16.3","capacity_bound",[]{rejects<std::invalid_argument>([]{course::DirectCache c(65537,16);});});
 add("16.3","max_address",[]{course::DirectCache c(3,7);require(!c.access(UINT64_MAX));require(c.access(UINT64_MAX));});
 add("16.3","non_power_two",[]{course::DirectCache c(3,10);c.access(0);c.access(10);c.access(20);require(c.access(9));require(!c.access(30));require(!c.access(0));});
 add("16.4","tails",[]{for(std::size_t n=0;n<65;++n){std::vector<std::uint32_t>a(n,3),b(n,5),out(n,99);course::add_blocks(a,b,out);require(std::all_of(out.begin(),out.end(),[](auto x){return x==8;}));}});
 add("16.4","mismatch",[]{std::vector<std::uint32_t>a(1),b(2),o(1,9);rejects<std::invalid_argument>([&]{course::add_blocks(a,b,o);});require(o[0]==9);});
 add("16.4","output_mismatch",[]{std::vector<std::uint32_t>a(1),b(1),o;rejects<std::invalid_argument>([&]{course::add_blocks(a,b,o);});});
 add("16.4","wrap",[]{std::array<std::uint32_t,1>a{UINT32_MAX},b{2},o{};course::add_blocks(a,b,o);require(o[0]==1);});
 add("16.4","exact_alias",[]{std::vector<std::uint32_t>a{1,2,3,4,5},b(5,10);course::add_blocks(a,b,a);require(a==std::vector<std::uint32_t>({11,12,13,14,15}));});
 add("16.4","offset_guard",[]{std::vector<std::uint32_t>a(9,1),b(9,2),o(9,99);course::add_blocks(std::span(a).subspan(1,7),std::span(b).subspan(1,7),std::span(o).subspan(1,7));require(o.front()==99 && o.back()==99);for(int i=1;i<=7;++i)require(o[static_cast<std::size_t>(i)]==3);});
 add("18.1","exact_funds",[]{course::Inventory i(10,1);require(i.buy(10));require(i.snapshot()==std::pair(0,0));});
 add("18.1","no_stock",[]{course::Inventory i(10,0);require(!i.buy(10));require(i.snapshot()==std::pair(10,0));});
 add("18.1","insufficient",[]{course::Inventory i(9,1);require(!i.buy(10));require(i.snapshot()==std::pair(9,1));});
 add("18.1","invalid_state",[]{rejects<std::invalid_argument>([]{course::Inventory i(-1,1);});});
 add("18.1","invalid_price",[]{course::Inventory i(10,1);rejects<std::invalid_argument>([&]{i.buy(0);});rejects<std::invalid_argument>([&]{i.buy(-1);});});
 add("18.1","contention",[]{course::Inventory i(1000,1000);std::atomic<int> sold{0};std::vector<std::jthread>pool;for(int k=0;k<8;++k)pool.emplace_back([&]{for(int j=0;j<300;++j)if(i.buy(3))++sold;});for(auto&t:pool)t.join();require(sold==333);require(i.snapshot()==std::pair(1,667));});
 add("18.1","stock_limit",[]{course::Inventory i(1000,7);std::vector<std::jthread>pool;for(int k=0;k<4;++k)pool.emplace_back([&]{for(int j=0;j<20;++j)i.buy(1);});for(auto&t:pool)t.join();require(i.snapshot()==std::pair(993,0));});
 add("18.2","invalid",[]{rejects<std::invalid_argument>([]{course::BoundedQueue q(0);});});
 add("18.2","fifo",[]{course::BoundedQueue q(3);require(q.push(5));require(q.push(2));require(q.pop()==5);require(q.pop()==2);q.close();require(!q.pop());});
 add("18.2","drain",[]{course::BoundedQueue q(2);q.push(7);q.push(8);q.close();require(q.pop()==7);require(q.pop()==8);require(!q.pop());require(!q.push(9));});
 add("18.2","discard",[]{course::BoundedQueue q(2);q.push(7);q.close(false);require(!q.pop());require(!q.push(9));});
 add("18.2","repeat_close",[]{course::BoundedQueue q(1);q.close();q.close();require(!q.pop());});
 add("18.2","wake_consumer",[]{course::BoundedQueue q(1);std::promise<void>started;std::optional<int>result=1;std::jthread t([&]{started.set_value();result=q.pop();});started.get_future().wait();q.close();t.join();require(!result);});
 add("18.2","wake_producer",[]{course::BoundedQueue q(1);q.push(1);std::promise<void>started;bool ok=true;std::jthread t([&]{started.set_value();ok=q.push(2);});started.get_future().wait();q.close();t.join();require(!ok);require(q.pop()==1);});
 add("18.2","wrap_stress",[]{course::BoundedQueue q(3);std::vector<int>seen;std::jthread t([&]{while(auto v=q.pop())seen.push_back(*v);});for(int i=0;i<4000;++i)q.push(i);q.close();t.join();require(seen.size()==4000);for(std::size_t i=0;i<seen.size();++i)require(seen[i]==static_cast<int>(i));});
 add("18.2","multiple_consumers",[]{course::BoundedQueue q(7);std::atomic<int>sum{0},count{0};std::vector<std::jthread>pool;for(int i=0;i<4;++i)pool.emplace_back([&]{while(auto v=q.pop()){sum.fetch_add(*v);++count;}});for(int i=1;i<=1000;++i)q.push(i);q.close();for(auto&t:pool)t.join();require(sum==500500 && count==1000);});
 add("18.3","zero",[]{require(course::publish_once(0)==0);});
 add("18.3","known",[]{require(course::publish_once(42)==42);});
 add("18.3","max",[]{require(course::publish_once(UINT64_MAX)==UINT64_MAX);});
 add("18.3","repeat_independent",[]{for(std::uint64_t i=0;i<100;++i)require(course::publish_once(i)==i);});
 add("18.4","empty",[]{require(course::critical_path({},{})==0);});
 add("18.4","one",[]{require(course::critical_path({7},{{}})==7);});
 add("18.4","fork_join",[]{require(course::critical_path({2,5,1},{{},{},{0,1}})==6);});
 add("18.4","chain",[]{require(course::critical_path({2,5,1},{{},{0},{1}})==8);});
 add("18.4","cycle",[]{rejects<std::invalid_argument>([]{course::critical_path({1,1},{{1},{0}});});});
 add("18.4","self",[]{rejects<std::invalid_argument>([]{course::critical_path({1},{{0}});});});
 add("18.4","bad_index",[]{rejects<std::invalid_argument>([]{course::critical_path({1},{{1}});});});
 add("18.4","duplicates",[]{rejects<std::invalid_argument>([]{course::critical_path({1,1},{{},{0,0}});});});
 add("18.4","mismatch",[]{rejects<std::invalid_argument>([]{course::critical_path({1},{});});});
 add("18.4","overflow",[]{rejects<std::overflow_error>([]{course::critical_path({UINT64_MAX,1},{{},{0}});});});
 add("18.4","unordered_ids",[]{require(course::critical_path({3,4,2},{{2},{0},{}})==9);});
 add("18.4","zero_times",[]{require(course::critical_path({0,0},{{},{0}})==0);});

 int passed=0,failed=0;
 for(const auto& c:cases){
  if(argc==2 && c.id!=argv[1])continue;
  try{c.run();++passed;std::cout<<"PASS "<<c.id<<'/'<<c.name<<'\n';}
  catch(const std::exception& e){++failed;std::cerr<<"FAIL "<<c.id<<'/'<<c.name<<": "<<e.what()<<'\n';}
 }
 std::cout<<"cases="<<(passed+failed)<<" passed="<<passed<<" failed="<<failed<<'\n';
 return passed+failed==0?2:(failed?1:0);
}
