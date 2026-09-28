# Optional CUDA reduction: validation pending

`reduction.cu` is an unsigned 32-bit, multi-dispatch reduction teaching reference. Every lane reaches the shared-memory barriers; out-of-range lanes contribute the identity. Host-side dispatches create the global staging boundary. The sum wraps modulo 2^32. Empty input returns zero without a launch. The implementation intentionally limits the number of first-stage groups to 65,535 and allocates two full-size device buffers; it is not a memory-optimal library implementation.

**Not compiled or executed for this package.** No CUDA compiler/device validation was available. CPU scan/reduction tests cannot establish GPU correctness or performance. Source inspection alone does not establish portability.

On a machine with a compatible CUDA toolkit, supported NVIDIA GPU and driver, record the actual versions and device capabilities first. Use the installed toolkit's documentation for valid architecture flags and sanitizer availability.

```sh
nvcc -std=c++17 -O2 reduction.cu -o reduction
./reduction
compute-sanitizer --tool memcheck ./reduction
compute-sanitizer --tool racecheck ./reduction
compute-sanitizer --tool synccheck ./reduction
```

Commands are intended validation steps, not successful results from this package. Treat unsupported tools as a documented gap, not a silent pass. Check device limits and add overflow-safe allocation arithmetic before generalizing input sizes.

For Module 42, implement a GPU scan or compaction in addition to reduction, benchmark against a competent vendor/library primitive when available, and integrate into an engine workload. Test 0, 1, partial groups, non-powers of two, capacity limits and repeated execution. Include allocation, upload/download and dispatch costs where the application pays them. A GPU kernel timed in isolation and a CPU analytical model answer different questions.

CUDA is one optional API route. Metal, Vulkan compute or another supported GPU interface can satisfy the project with equivalent correctness, synchronization and performance evidence. Selecting a non-GPU Gate I topic does not fabricate completion of this module's pending device work.

Primary documentation: https://docs.nvidia.com/cuda/cuda-programming-guide/
