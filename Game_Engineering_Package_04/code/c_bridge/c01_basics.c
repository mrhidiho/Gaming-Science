#include "ge_c_api.h"
#include <stdio.h>
static size_t checks=0;
#define CHECK_C(condition) do { ++checks; if(!(condition)) { \
    fprintf(stderr,"FAIL C01 line %d\n",__LINE__);return 1; } } while(0)
int main(void) {
    int out=99;
    CHECK_C(ge_apply_damage(20,7,&out)==GE_OK);CHECK_C(out==13);
    CHECK_C(ge_apply_damage(3,10,&out)==GE_OK);CHECK_C(out==0);
    CHECK_C(ge_apply_damage(-1,2,&out)==GE_INVALID);CHECK_C(out==0);
    CHECK_C(ge_apply_damage(3,2,NULL)==GE_INVALID);
    printf("C standard macro=%ld\n",(long)__STDC_VERSION__);
    printf("PASS C01 checks=%zu\n",checks);return 0;
}
