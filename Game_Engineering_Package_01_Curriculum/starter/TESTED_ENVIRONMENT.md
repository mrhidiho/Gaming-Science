# Supplied starter: executed validation

Edition: September 28, 2026.

Executed in a Linux container with Python 3.13.5, GCC/g++ 14.2.0 and CMake 3.31.6.
The Python unittest discovery run passed all 23 test methods (including parameterized
subtests). The C++ project configured and built successfully; its single CTest
`motion_contract` passed all internal checks. The five-tick motion output and
winning grid replay were also executed and matched their expected results.

This is validation of the supplied examples in this environment, not a claim that
every curriculum lab has been implemented, that the learner has passed a gate,
or that Windows/macOS execution was tested. The package supplies source only,
not the container's compiled binaries or third-party font files.
