#ifndef GE_C_API_H
#define GE_C_API_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Same-toolchain teaching ABI. No thread-safety guarantee. */
enum ge_status { GE_OK=0, GE_INVALID=1, GE_RANGE=2, GE_NOMEM=3 };
/* Nonnegative inputs <= 1,000,000. On failure, *out_hp is unchanged. */
int ge_apply_damage(int hp,int damage,int *out_hp);
/* Opaque unique owner. Only ge_device_destroy releases a successful create.
   out_device must be nonnull. *out_device becomes NULL on failed creation. */
struct ge_device;
int ge_device_create(unsigned id,struct ge_device **out_device);
void ge_device_destroy(struct ge_device *device); /* NULL is allowed. */
int ge_device_id(const struct ge_device *device,unsigned *out_id);
/* Deterministic, single-threaded test hooks; not a production device API. */
void ge_fail_next_allocation(void);
size_t ge_live_devices(void);
struct ge_packet { uint8_t version;uint32_t id;uint16_t hp;uint8_t flags; };
/* Wire bytes: version, id little-endian (4), hp little-endian (2), flags.
   Exactly 8 bytes are required; native struct padding is never serialized.
   Encode/decode failures leave destination unchanged. Version must be 1. */
int ge_packet_encode(const struct ge_packet *packet,uint8_t *out,size_t length);
int ge_packet_decode(const uint8_t *bytes,size_t length,struct ge_packet *out);
#ifdef __cplusplus
}
#endif
#endif
