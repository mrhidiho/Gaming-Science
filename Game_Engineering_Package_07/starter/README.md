# Runnable teaching material

Run from the extracted package root, or supply the absolute script path. All Python examples use the standard library; Python 3.11+ is the syntax baseline. Actual testing is recorded under evidence.

`python starter/run_all.py` checks all references, invariant tests, twenty demos and five integration companions. Add `--native` to build/test the offline C++17 harness with CMake. The combined runner fails on a missing required selected tool, a timeout or any nonzero test result.

## Exercises and tests

Each of the twenty files in python/exercises defines solve(payload) and deliberately raises NotImplementedError. Replace that body independently, then run:

```text
python starter/python/run_tests.py --target exercises --lesson 26.1
```

Use the matching demonstration and reference after an attempt. Cases in python/cases.json specify inputs, expected outputs or ValueError for selected invalid input. Floating outputs are compared with relative/absolute tolerance 1e-9; exact state replay uses canonical representations in its own kernel. The contract bank is not exhaustive hostile-input testing. Add tests for the full engine boundary, native integer arithmetic and supported physical scale.

The seventeen invariant/oracle test methods in python/test_properties.py target the provided references. They include 700 seeded randomized cases across six test methods, plus directed properties. They do not certify a rewritten native implementation: port and rerun appropriate tests there.

## Five integration companions

physics_lab.py: free-fall convergence, positional constraint residuals and an off-center contact. Not a maintained-library adapter.

learning_lab.py: a synthetic episode-split logistic experiment, validation selection and held-out errors against a training-derived majority baseline. Not evidence of real-game performance or target-device latency.

network_lab.py: two in-process client simulations, scalar authoritative motion, deterministic delay/loss/duplication/reorder and a labeled reliable drain. Not a socket server or production authentication.

service_lab.py: SQLite result/reward transaction, pre-/post-commit failure, idempotency and fresh-process persistence. Not the full match registry, real identity provider or distributed system.

release_lab.py: save replacement and staged activation using temporary folders and exception injection. Not power-loss durability or signed-update authentication.

## Native code

cpp/audio_harness.cpp is an offline bounded mixer/queue demonstration. The queue is single-producer/single-consumer; the bundled tests exercise it sequentially, not under concurrent stress. No device is opened and no hard-real-time deadline is proven. Read NATIVE_INTEGRATION_GUIDE and complete the actual platform/audio lab.

## Student evidence

The reference results are supplied teaching aids. Full lab procedures, engine transfer, external-library comparison, actual audio/device testing, local process/socket networking and independent review remain learner work. Keep these evidence tiers separate.
