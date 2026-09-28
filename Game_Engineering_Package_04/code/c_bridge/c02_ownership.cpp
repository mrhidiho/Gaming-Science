#include "check.hpp"
#include "ge_c_api.h"
#include <memory>
#include <stdexcept>
#include <utility>
using Device=std::unique_ptr<ge_device,decltype(&ge_device_destroy)>;
Device open_device(unsigned id) {
    ge_device* raw=nullptr;
    const int status=ge_device_create(id,&raw);
    if(status!=GE_OK) throw std::runtime_error("C device creation failed");
    return Device(raw,&ge_device_destroy);
}
int main() {return p4test::run("C02",[]{
    const auto baseline=ge_live_devices();
    {
        auto a=open_device(42);CHECK(ge_live_devices()==baseline+1);
        auto b=std::move(a);CHECK(!a);unsigned id=0;
        CHECK(ge_device_id(b.get(),&id)==GE_OK);CHECK(id==42);
    }
    CHECK(ge_live_devices()==baseline);
    ge_fail_next_allocation();CHECK(p4test::throws<std::runtime_error>([]{auto d=open_device(7);(void)d;}));
    CHECK(ge_live_devices()==baseline);ge_device_destroy(nullptr);
});}
