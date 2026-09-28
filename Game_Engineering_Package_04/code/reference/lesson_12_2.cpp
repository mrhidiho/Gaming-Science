// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "resources.hpp"
#include <type_traits>
#include <utility>
#include <stdexcept>


int main() {
    return p4test::run("12.2", [] {

        static_assert(!std::is_copy_constructible_v<ge::MockOwner>);
        static_assert(!std::is_copy_assignable_v<ge::MockOwner>);
        static_assert(std::is_nothrow_move_constructible_v<ge::MockOwner>);
        ge::Counts counts;
        {
            ge::MockOwner current(counts);const int old_id=current.id();
            CHECK(p4test::throws<std::runtime_error>([&]{ge::replace_mock(current,counts,true);}));
            CHECK(current.id()==old_id);CHECK(counts.live==1);
            ge::replace_mock(current,counts,false);CHECK(current.id()!=old_id);CHECK(counts.live==1);
            const int selected=current.id();ge::MockOwner moved(std::move(current));
            CHECK(current.id()==0);CHECK(moved.id()==selected);CHECK(counts.live==1);
            ge::MockOwner destination(counts);CHECK(counts.live==2);
            destination=std::move(moved);CHECK(counts.live==1);CHECK(moved.id()==0);
            CHECK(destination.id()==selected);
            auto& alias=destination;destination=std::move(alias);
            CHECK(destination.id()==selected);CHECK(counts.live==1);
        }
        CHECK(counts.live==0);CHECK(counts.acquired==counts.released);

    });
}
