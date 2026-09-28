#include <cstdint>
#include "check.hpp"
#include "ge_c_api.h"
#include <array>
int main() {return p4test::run("C04",[]{
    int out=17;
    CHECK(ge_apply_damage(-1,2,&out)==GE_INVALID);CHECK(out==17);
    CHECK(ge_apply_damage(1000001,2,&out)==GE_RANGE);CHECK(out==17);
    CHECK(ge_apply_damage(10,2,nullptr)==GE_INVALID);
    ge_device* raw=nullptr;ge_fail_next_allocation();
    CHECK(ge_device_create(1,&raw)==GE_NOMEM);CHECK(raw==nullptr);
    CHECK(ge_device_create(1,nullptr)==GE_INVALID);
    unsigned id=99;CHECK(ge_device_id(nullptr,&id)==GE_INVALID);CHECK(id==99);
    ge_packet packet{1,1,2,3};std::array<std::uint8_t,8> bytes{};bytes.fill(0xAA);
    const auto before=bytes;
    CHECK(ge_packet_encode(&packet,bytes.data(),7)==GE_RANGE);CHECK(bytes==before);
    packet.version=2;CHECK(ge_packet_encode(&packet,bytes.data(),8)==GE_INVALID);CHECK(bytes==before);
    ge_packet decoded{1,99,33,4};
    CHECK(ge_packet_decode(bytes.data(),8,&decoded)==GE_INVALID);CHECK(decoded.id==99);
    CHECK(ge_packet_decode(nullptr,8,&decoded)==GE_INVALID);
});}
