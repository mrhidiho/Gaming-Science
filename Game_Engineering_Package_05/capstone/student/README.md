# Gate D student workspace
Implement your own bounded task-processing application from CAPSTONE_SPEC.pdf.
The reference service is a worked design, not a student submission. Keep an attribution
record for any support code you reuse. Native concurrency work from Module 18 remains
required even when your service uses Python as its local orchestration layer.

Begin with requirements and an ownership map. Then implement validation, one job,
bounded admission, persistence, retry behavior, cancellation and a failure test matrix.
Do not expose the service publicly. A loopback gateway is an integration option;
an offline file-driven interface can satisfy Gate D with the same failure evidence.

A copied reference with renamed variables is not completion. Add a new bounded
operation or protocol-version migration, defend its invariants, and write your own
acceptance tests including failure cases not present in the reference suite.
