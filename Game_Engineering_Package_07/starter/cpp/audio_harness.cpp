// Offline teaching harness. No device is opened. It cannot prove underrun safety.
// Exactly one producer and one consumer may access each SPSC queue.
#include <array>
#include <atomic>
#include <cmath>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>

constexpr double pi = 3.14159265358979323846;
struct Command { std::size_t voice; float gain; double frequency; };
template<std::size_t N> class Spsc {
    static_assert(N > 1, "Queue requires a sentinel slot");
    static_assert(std::atomic<std::size_t>::is_always_lock_free,
                  "Use a verified lock-free index type on this target");
    std::array<Command,N> data_{};
    alignas(64) std::atomic<std::size_t> write_{0};
    alignas(64) std::atomic<std::size_t> read_{0};
public:
    // Producer owns write_, consumer owns read_. Full => explicit rejection.
    bool push(Command value) noexcept {
        const auto w=write_.load(std::memory_order_relaxed);
        const auto next=(w+1)%N;
        if(next==read_.load(std::memory_order_acquire)) return false;
        data_[w]=value;
        write_.store(next,std::memory_order_release);
        return true;
    }
    bool pop(Command& value) noexcept {
        const auto r=read_.load(std::memory_order_relaxed);
        if(r==write_.load(std::memory_order_acquire)) return false;
        value=data_[r];
        read_.store((r+1)%N,std::memory_order_release);
        return true;
    }
};
class Mixer {
    struct Voice { double phase=0; double frequency=0; float gain=0; };
    std::array<Voice,8> voices_{};
    // Prepared before callback use. No lazy allocation or file I/O in render.
    std::array<float,2048> sine_{};
    Spsc<65> commands_;
public:
    std::size_t rejected_commands=0; // Consumer-owned diagnostic; inspect after stop.
    Mixer() { for(std::size_t i=0;i<sine_.size();++i)
        sine_[i]=static_cast<float>(std::sin(2*pi*i/sine_.size())); }
    bool enqueue(Command c) noexcept { return commands_.push(c); }
    void render(std::array<float,256>& output) noexcept {
        Command c{};
        // Bound command work even when producer continuously replenishes queue.
        for(int n=0;n<16 && commands_.pop(c);++n) {
            if(c.voice>=voices_.size() || !std::isfinite(c.gain) ||
               !std::isfinite(c.frequency) || std::abs(c.gain)>.125f ||
               c.frequency<0 || c.frequency>=24000) { ++rejected_commands; continue; }
            auto& v=voices_[c.voice]; v.gain=c.gain; v.frequency=c.frequency;
        }
        for(auto& sample:output) {
            float sum=0;
            for(auto& v:voices_) {
                const auto index=static_cast<std::size_t>(v.phase*sine_.size());
                sum+=v.gain*sine_[index];
                v.phase+=v.frequency/48000.0;
                if(v.phase>=1.0) v.phase-=1.0;
            }
            sample=sum;
        }
    }
};
static void require(bool condition,const char* message) {
    if(!condition) throw std::runtime_error(message);
}
int main() {
    try {
        Spsc<4> q; Command c{};
        require(!q.pop(c),"empty queue");
        for(std::size_t i=0;i<3;++i) require(q.push({i,0,0}),"fill queue");
        require(!q.push({9,0,0}),"full queue rejected");
        require(q.pop(c)&&c.voice==0,"FIFO head");
        require(q.push({3,0,0}),"wrap write");
        for(std::size_t i=1;i<4;++i) require(q.pop(c)&&c.voice==i,"wrap FIFO");
        require(!q.pop(c),"drained queue");
        Mixer a,b;
        require(a.enqueue({0,.125f,440})&&b.enqueue({0,.125f,440}),"voice command");
        std::array<float,256> x{},y{};
        double energy=0;
        for(int block=0;block<100;++block) {
            a.render(x);b.render(y);
            for(std::size_t i=0;i<x.size();++i) {
                require(std::isfinite(x[i])&&std::abs(x[i])<=1.0f,"sample range");
                require(x[i]==y[i],"same-run deterministic samples");
                energy+=x[i]*x[i];
            }
        }
        require(energy>1,"nonzero audio");
        require(a.enqueue({99,.1f,440}),"enqueue invalid command for consumer validation");
        a.render(x);require(a.rejected_commands==1,"invalid command rejected");
        std::cout << "PASS: ring empty/full/FIFO/wrap; 100 paired blocks; sample bounds; invalid command\n";
        std::cout << "Format: 48000 frames/s, mono, 256 frames/block, max 8 voices, max 16 commands/block\n";
        std::cout << "Scope: offline, single-thread queue exercise; no device, thread stress or deadline proof\n";
        return EXIT_SUCCESS;
    } catch(const std::exception& e) {
        std::cerr<<"FAIL: "<<e.what()<<'\n';return EXIT_FAILURE;
    }
}
