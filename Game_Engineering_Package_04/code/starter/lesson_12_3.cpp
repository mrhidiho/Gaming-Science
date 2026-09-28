// Student work: this file intentionally compiles but fails until implemented.
// The tests here are a starting contract, NOT the complete lesson acceptance suite.
// Read LAB_WORKBOOK.pdf; add its boundary cases and your independent transfer test.
#include "check.hpp"
#include <algorithm>
#include <array>
#include <cstdint>
#include <limits>
#include <memory>
#include <optional>
#include <queue>
#include <span>
#include <stdexcept>
#include <string>
#include <string_view>
#include <utility>
#include <vector>

struct DrawCommand { int entity; int x; int y; };
struct Renderer { virtual ~Renderer()=default; virtual void draw(DrawCommand)=0; };
struct RecordingRenderer final : Renderer {
    std::vector<DrawCommand> commands;
    void draw(DrawCommand /*command*/) override { throw std::logic_error("TODO: capture command by value"); }
};
void render_one(Renderer& renderer, const DrawCommand& command) { renderer.draw(command); }

int main() { return p4test::run("student_12_3", [] {
    RecordingRenderer recording;
    DrawCommand command{4,10,20};
    render_one(recording,command);
    command.x=99;
    CHECK(recording.commands.size()==1);
    CHECK(recording.commands[0].x==10);
    std::unique_ptr<Renderer> owner=std::make_unique<RecordingRenderer>();
    owner->draw({1,0,0});
}); }
