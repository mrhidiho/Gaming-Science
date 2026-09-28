#include "ge_c_api.h"
#include <stdlib.h>
#include <string.h>
#ifdef __cplusplus
#error This file must be compiled as C, not C++.
#endif
#if !defined(__STDC_VERSION__) || __STDC_VERSION__ < 201710L
#error This teaching bridge selects C17.
#endif
struct ge_device { unsigned id; };
static size_t live=0;
static int fail_next=0;
int ge_apply_damage(int hp,int damage,int *out_hp) {
    if(out_hp==NULL || hp<0 || damage<0) return GE_INVALID;
    if(hp>1000000 || damage>1000000) return GE_RANGE;
    *out_hp=damage>=hp?0:hp-damage;
    return GE_OK;
}
void ge_fail_next_allocation(void) { fail_next=1; }
size_t ge_live_devices(void) { return live; }
int ge_device_create(unsigned id,struct ge_device **out_device) {
    struct ge_device *candidate;
    if(out_device==NULL) return GE_INVALID;
    *out_device=NULL;
    if(fail_next) { fail_next=0;return GE_NOMEM; }
    candidate=(struct ge_device*)malloc(sizeof *candidate);
    if(candidate==NULL) return GE_NOMEM;
    candidate->id=id;*out_device=candidate;++live;
    return GE_OK;
}
void ge_device_destroy(struct ge_device *device) {
    if(device!=NULL) { free(device);--live; }
}
int ge_device_id(const struct ge_device *device,unsigned *out_id) {
    if(device==NULL || out_id==NULL) return GE_INVALID;
    *out_id=device->id;return GE_OK;
}
int ge_packet_encode(const struct ge_packet *p,uint8_t *out,size_t length) {
    uint8_t bytes[8];
    if(p==NULL || out==NULL) return GE_INVALID;
    if(length!=8) return GE_RANGE;
    if(p->version!=1) return GE_INVALID;
    bytes[0]=p->version;
    bytes[1]=(uint8_t)(p->id&255u);bytes[2]=(uint8_t)((p->id>>8)&255u);
    bytes[3]=(uint8_t)((p->id>>16)&255u);bytes[4]=(uint8_t)((p->id>>24)&255u);
    bytes[5]=(uint8_t)(p->hp&255u);bytes[6]=(uint8_t)((p->hp>>8)&255u);
    bytes[7]=p->flags;
    memcpy(out,bytes,8);return GE_OK;
}
int ge_packet_decode(const uint8_t *bytes,size_t length,struct ge_packet *out) {
    struct ge_packet p;
    if(bytes==NULL || out==NULL) return GE_INVALID;
    if(length!=8) return GE_RANGE;
    if(bytes[0]!=1) return GE_INVALID;
    p.version=bytes[0];
    p.id=(uint32_t)bytes[1]|((uint32_t)bytes[2]<<8)|
         ((uint32_t)bytes[3]<<16)|((uint32_t)bytes[4]<<24);
    p.hp=(uint16_t)((uint16_t)bytes[5]|((uint16_t)bytes[6]<<8));
    p.flags=bytes[7];*out=p;return GE_OK;
}
