// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "model.hpp"
#include <memory>
#include <ostream>
#include <sstream>
#include <span>
#include <vector>


struct Renderer {
    virtual ~Renderer()=default;
    virtual void draw(std::span<const ge::Unit> units)=0;
};
class ConsoleRenderer final:public Renderer {
    std::ostream& output_;
public:
    explicit ConsoleRenderer(std::ostream& output):output_(output) {}
    void draw(std::span<const ge::Unit> units) override {
        for(const auto& u:units) output_<<u.id<<':'<<u.position.x<<','<<u.position.y<<'\n';
    }
};
class RecordingRenderer final:public Renderer {
    bool* destroyed_;
public:
    std::vector<ge::Unit> commands;
    explicit RecordingRenderer(bool* destroyed):destroyed_(destroyed) {}
    ~RecordingRenderer() override { if(destroyed_) *destroyed_=true; }
    void draw(std::span<const ge::Unit> units) override {
        commands.assign(units.begin(),units.end());
    }
};
void frame(Renderer& renderer,std::span<const ge::Unit> units) { renderer.draw(units); }

int main() {
    return p4test::run("12.3", [] {

        std::vector<ge::Unit> units{{7,{2,3},10},{2,{4,5},8}};
        std::ostringstream output;ConsoleRenderer console(output);frame(console,units);
        CHECK(output.str()=="7:2,3\n2:4,5\n");
        bool destroyed=false;
        {
            auto recording=std::make_unique<RecordingRenderer>(&destroyed);
            RecordingRenderer* observer=recording.get();
            std::unique_ptr<Renderer> backend=std::move(recording);
            frame(*backend,units);CHECK(observer->commands==units);
            units[0].position.x=99;CHECK(observer->commands[0].position.x==2);
            frame(*backend,{});CHECK(observer->commands.empty());
        }
        CHECK(destroyed);

    });
}
