#pragma once
#include <algorithm>
#include <optional>
#include <span>
#include <stdexcept>
#include <vector>
namespace ge {
struct Position {
    int x = 0, y = 0;
    bool operator==(const Position&) const = default;
};
struct Unit {
    int id = 0;
    Position position;
    int hit_points = 0;
    bool operator==(const Unit&) const = default;
};
inline std::optional<Position> position_of(std::span<const Unit> units, int id) {
    for (const Unit& unit : units)
        if (unit.id == id) return unit.position;
    return std::nullopt;
}
inline std::optional<int> hp_of(const Unit* target) {
    if (target == nullptr) return std::nullopt;
    return target->hit_points;
}
class UnitStore {
    std::vector<Unit> units_;
public:
    bool insert(Unit u) {
        if (find(u.id)) return false;
        units_.push_back(u);
        return true;
    }
    std::optional<Unit> find(int id) const {
        for (const auto& u : units_) if (u.id == id) return u;
        return std::nullopt;
    }
    bool erase(int id) {
        const auto it = std::find_if(units_.begin(), units_.end(),
            [id](const Unit& u) { return u.id == id; });
        if (it == units_.end()) return false;
        units_.erase(it);
        return true;
    }
    std::size_t size() const noexcept { return units_.size(); }
};
// Teaching grid: one orthogonal step or a no-op; blocked boundary => false.
// Bad model/command => exception, and no mutation. No collisions or terrain.
inline bool move_unit(Unit& u, int dx, int dy, int width, int height) {
    if (width < 1 || height < 1 || width > 10000 || height > 10000)
        throw std::invalid_argument("grid dimensions");
    if (u.position.x < 0 || u.position.x >= width ||
        u.position.y < 0 || u.position.y >= height)
        throw std::invalid_argument("unit outside grid");
    if (dx < -1 || dx > 1 || dy < -1 || dy > 1 ||
        (dx != 0 && dy != 0))
        throw std::invalid_argument("not one orthogonal step");
    const int nx = u.position.x + dx, ny = u.position.y + dy;
    if (nx < 0 || nx >= width || ny < 0 || ny >= height) return false;
    u.position = {nx, ny};
    return true;
}
}
