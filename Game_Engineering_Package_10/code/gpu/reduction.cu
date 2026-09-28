// Optional CUDA exercise reference. NOT compiled or executed for this package.
// CPU tests do not validate CUDA barriers, device memory safety or performance.
#include <cuda_runtime.h>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>
#include <utility>
using U=std::uint32_t;
void cuda_check(cudaError_t err) {
    if(err!=cudaSuccess)throw std::runtime_error(cudaGetErrorString(err));
}
constexpr unsigned BLOCK=256;
__global__ void reduce_stage(const U* input,U* output,std::size_t n) {
    __shared__ U partial[BLOCK];
    const unsigned lane=threadIdx.x;
    const std::size_t i=static_cast<std::size_t>(blockIdx.x)*BLOCK+lane;
    // All lanes reach every barrier, including out-of-range lanes.
    partial[lane]=i<n?input[i]:0U;
    __syncthreads();
    for(unsigned stride=BLOCK/2;stride;stride/=2) {
        if(lane<stride)partial[lane]+=partial[lane+stride];
        __syncthreads();
    }
    if(lane==0)output[blockIdx.x]=partial[0];
}
struct DeviceBuffer {
    U* ptr=nullptr;
    explicit DeviceBuffer(std::size_t n){cuda_check(cudaMalloc(reinterpret_cast<void**>(&ptr),n*sizeof(U)));}
    ~DeviceBuffer(){if(ptr)cudaFree(ptr);}
    DeviceBuffer(const DeviceBuffer&)=delete;
    DeviceBuffer&operator=(const DeviceBuffer&)=delete;
};
U reduce_gpu(const std::vector<U>& host) {
    if(host.empty())return 0U;
    DeviceBuffer first(host.size()),second(host.size());
    cuda_check(cudaMemcpy(first.ptr,host.data(),host.size()*sizeof(U),cudaMemcpyHostToDevice));
    U* in=first.ptr;U* out=second.ptr;std::size_t n=host.size();
    while(n>1) {
        const std::size_t groups=(n+BLOCK-1)/BLOCK;
        if(groups>65535)throw std::runtime_error("teaching launch bound exceeded");
        reduce_stage<<<static_cast<unsigned>(groups),BLOCK>>>(in,out,n);
        cuda_check(cudaGetLastError());
        std::swap(in,out);n=groups;
    }
    U result=0;
    cuda_check(cudaMemcpy(&result,in,sizeof(U),cudaMemcpyDeviceToHost));
    return result;
}
int main() {
    try {
        int devices=0;cuda_check(cudaGetDeviceCount(&devices));
        if(!devices)throw std::runtime_error("no CUDA device");
        for(std::size_t n:std::vector<std::size_t>{0,1,3,255,256,257,1025,1000003}) {
            std::vector<U> v(n);U expected=0;
            for(std::size_t i=0;i<n;++i){v[i]=static_cast<U>(i*17U+3U);expected+=v[i];}
            if(reduce_gpu(v)!=expected)throw std::runtime_error("reduction mismatch");
            std::cout<<"PASS n="<<n<<'\n';
        }
        cuda_check(cudaDeviceSynchronize());return 0;
    }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
