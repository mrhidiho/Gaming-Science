#include "ge_c_api.h"
#include <stddef.h>
#include <stdio.h>
#include <string.h>
static size_t checks=0;
#define CHECK_C(condition) do { ++checks; if(!(condition)) { \
    fprintf(stderr,"FAIL C03 line %d\n",__LINE__);return 1; } } while(0)
int main(void) {
    struct ge_packet p={1,0x12345678u,0x1234u,5},decoded={0,0,0,0};
    uint8_t bytes[8];const uint8_t expected[8]={1,0x78,0x56,0x34,0x12,0x34,0x12,5};
    printf("packet size=%zu alignment=%zu offsets version=%zu id=%zu hp=%zu flags=%zu\n",
        sizeof p,_Alignof(struct ge_packet),offsetof(struct ge_packet,version),
        offsetof(struct ge_packet,id),offsetof(struct ge_packet,hp),offsetof(struct ge_packet,flags));
    CHECK_C(ge_packet_encode(&p,bytes,8)==GE_OK);CHECK_C(memcmp(bytes,expected,8)==0);
    CHECK_C(ge_packet_decode(bytes,8,&decoded)==GE_OK);
    CHECK_C(decoded.id==p.id);CHECK_C(decoded.hp==p.hp);CHECK_C(decoded.flags==p.flags);
    CHECK_C(decoded.version==p.version);
    printf("PASS C03 checks=%zu\n",checks);return 0;
}
