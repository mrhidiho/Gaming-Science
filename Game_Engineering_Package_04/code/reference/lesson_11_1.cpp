// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "tick.hpp"
#include "model.hpp"
#include <limits>
#include <array>
#include <iostream>
#include <stdexcept>


int main() {
    return p4test::run("11.1", [] {

        CHECK(next_tick(0)==1);CHECK(next_tick(41)==42);
        CHECK(next_tick(-2)==-1);
        CHECK(p4test::throws<std::overflow_error>([]{next_tick(std::numeric_limits<int>::max());}));
        ge::Unit unit{7,{0,0},10};
        CHECK(!ge::move_unit(unit,-1,0,3,3));CHECK(unit.position==ge::Position{0,0});
        CHECK(ge::move_unit(unit,1,0,3,3));CHECK(unit.position==ge::Position{1,0});
        CHECK(p4test::throws<std::invalid_argument>([&]{ge::move_unit(unit,1,1,3,3);}));
        CHECK(unit.position==ge::Position{1,0});

        struct Step { int dx; int dy; int x; int y; bool accepted; };
        const std::array<Step,6> trace{{
            {-1,0,0,0,false}, {1,0,1,0,true}, {0,1,1,1,true},
            {0,0,1,1,true}, {1,0,2,1,true}, {1,0,2,1,false}}};
        ge::Unit replay{1,{0,0},100};
        std::cout << "command,dx,dy,x,y,accepted\n";
        int command = 0;
        for (const auto& step : trace) {
            command = next_tick(command);
            const bool accepted = ge::move_unit(replay,step.dx,step.dy,3,3);
            CHECK(accepted == step.accepted);
            CHECK(replay.position == ge::Position{step.x,step.y});
            std::cout << command << ',' << step.dx << ',' << step.dy << ','
                      << replay.position.x << ',' << replay.position.y << ','
                      << (accepted ? 1 : 0) << '\n';
        }

    });
}
