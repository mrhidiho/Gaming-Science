#pragma once
#include "lab_18_4.hpp"
#include <condition_variable>
#include <exception>
#include <functional>
#include <mutex>
#include <thread>
#include <string>
namespace course {
enum class TaskState { pending, running, done, failed, blocked };
struct Task { std::vector<std::size_t> deps; std::function<void()> run; };
struct TaskReport { std::vector<TaskState> state; std::vector<std::exception_ptr> errors; };
// Finite graph scheduler with a global ready scan, NOT a work-stealing scheduler.
// Data captured by tasks must have disjoint writes or follow dependency/locking rules.
inline TaskReport execute_graph(const std::vector<Task>& tasks,std::size_t workers) {
    if(workers==0 || workers>32) throw std::invalid_argument("worker count must be 1..32");
    std::vector<std::vector<std::size_t>> deps;
    for(const auto& t:tasks) {if(!t.run) throw std::invalid_argument("empty task"); deps.push_back(t.deps);}
    (void)critical_path(std::vector<std::uint64_t>(tasks.size(),1),deps);
    TaskReport report{std::vector<TaskState>(tasks.size(),TaskState::pending),
                      std::vector<std::exception_ptr>(tasks.size())};
    if(tasks.empty()) return report;
    std::mutex m; std::condition_variable cv;
    std::size_t remaining=tasks.size(); bool abort_start=false;
    auto available=[&]() {
        for(std::size_t i=0;i<tasks.size();++i) {
            if(report.state[i]!=TaskState::pending) continue;
            bool all=true;
            for(auto d:tasks[i].deps) {
                auto s=report.state[d];
                if(s==TaskState::pending || s==TaskState::running) {all=false; break;}
            }
            if(all) return i;
        }
        return tasks.size();
    };
    auto work=[&]() {
        for(;;) {
            std::unique_lock lock(m);
            cv.wait(lock,[&]{return abort_start || remaining==0 || available()!=tasks.size();});
            if(abort_start || remaining==0) return;
            const auto i=available(); bool blocked=false;
            for(auto d:tasks[i].deps) if(report.state[d]!=TaskState::done) blocked=true;
            if(blocked) {
                report.state[i]=TaskState::blocked; --remaining;
                lock.unlock(); cv.notify_all(); continue;
            }
            report.state[i]=TaskState::running;
            lock.unlock();
            std::exception_ptr error;
            try {tasks[i].run();} catch(...) {error=std::current_exception();}
            lock.lock();
            report.errors[i]=error;
            report.state[i]=error?TaskState::failed:TaskState::done;
            --remaining;
            lock.unlock(); cv.notify_all();
        }
    };
    std::vector<std::jthread> pool;
    pool.reserve(workers);
    try {for(std::size_t i=0;i<workers;++i) pool.emplace_back(work);}
    catch(...) {
        {std::lock_guard g(m); abort_start=true;}
        cv.notify_all();
        for(auto& t:pool) t.join();
        throw;
    }
    for(auto& t:pool) t.join();
    return report;
}
}
