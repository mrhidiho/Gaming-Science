// Package 04 reference demonstration. Student work is in ../starter/.
#include "check.hpp"
#include "ge_c_api.h"
#include <algorithm>
#include <optional>
#include <stdexcept>


enum class Type {Number,Boolean};enum class Operator {Add,And};
std::optional<Type> type_of(Operator op,Type a,Type b) {
    if(op==Operator::Add && a==Type::Number && b==Type::Number)return Type::Number;
    if(op==Operator::And && a==Type::Boolean && b==Type::Boolean)return Type::Boolean;
    return std::nullopt;
}
void validate_damage(int hp,int damage,int armor) {
    if(hp<0 || damage<0 || armor<0 || hp>1000000 || damage>1000000 || armor>1000000)
        throw std::invalid_argument("damage domain");
}
int pure_damage(int hp,int damage,int armor) {
    validate_damage(hp,damage,armor);return std::max(0,hp-std::max(0,damage-armor));
}
void imperative_damage(int& hp,int damage,int armor) {
    validate_damage(hp,damage,armor);int effective=damage-armor;
    if (effective < 0) { effective = 0; }
    hp -= effective;
    if (hp < 0) { hp = 0; }
}

int main() {
    return p4test::run("15.1", [] {

        for(int hp=0;hp<=20;++hp)for(int damage=0;damage<=20;++damage)for(int armor=0;armor<=5;++armor) {
            int state=hp;imperative_damage(state,damage,armor);CHECK(state==pure_damage(hp,damage,armor));
        }
        CHECK(pure_damage(20,12,5)==13);CHECK(pure_damage(3,100,0)==0);
        CHECK(type_of(Operator::Add,Type::Number,Type::Number)==Type::Number);
        CHECK(!type_of(Operator::Add,Type::Number,Type::Boolean));
        CHECK(type_of(Operator::And,Type::Boolean,Type::Boolean)==Type::Boolean);
        CHECK(!type_of(Operator::And,Type::Number,Type::Boolean));
        int out=99;CHECK(ge_apply_damage(20,7,&out)==GE_OK);CHECK(out==13);
        CHECK(ge_apply_damage(20,-1,&out)==GE_INVALID);CHECK(out==13);
        CHECK(ge_apply_damage(20,7,nullptr)==GE_INVALID);

    });
}
