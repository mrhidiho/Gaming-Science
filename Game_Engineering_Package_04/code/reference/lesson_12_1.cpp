// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "resources.hpp"
#include <stdexcept>


int fail_initialization() { throw std::runtime_error("second member fails"); }
struct Partial {
    ge::MockOwner first;
    int second;
    explicit Partial(ge::Counts& counts):first(counts),second(fail_initialization()) {}
};

int main() {
    return p4test::run("12.1", [] {

        ge::Counts counts;
        { ge::MockOwner empty;CHECK(empty.id()==0); }
        CHECK(counts.acquired==0);
        { ge::MockOwner owner(counts);CHECK(counts.live==1); }
        CHECK(counts.live==0);CHECK(counts.acquired==counts.released);
        CHECK(p4test::throws<std::runtime_error>([&]{auto owner=ge::load_mock(counts,true);(void)owner;}));
        CHECK(counts.live==0);CHECK(counts.acquired==counts.released);
        CHECK(p4test::throws<std::runtime_error>([&]{Partial object(counts);(void)object;}));
        CHECK(counts.live==0);CHECK(counts.acquired==counts.released);
        { ge::MockOwner a(counts);{ge::MockOwner b(counts);CHECK(counts.live==2);}CHECK(counts.live==1); }
        CHECK(counts.live==0);CHECK(counts.acquired==counts.released);

    });
}
