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

struct Unit { int id; int hp; };
class UnitStore {
    std::vector<Unit> units_;
public:
    bool insert(Unit /*unit*/) { throw std::logic_error("TODO: reject duplicate IDs"); }
    std::optional<Unit> find(int /*id*/) const { throw std::logic_error("TODO: value lookup"); }
    bool erase(int /*id*/) { throw std::logic_error("TODO: erase by stable ID"); }
};

int main() { return p4test::run("student_11_4", [] {
    UnitStore store;
    CHECK(store.insert({7,100}));
    CHECK(!store.insert({7,10}));
    CHECK(store.find(7)->hp==100);
    CHECK(store.erase(7));
    CHECK(!store.erase(7));
    CHECK(!store.find(7));
}); }
