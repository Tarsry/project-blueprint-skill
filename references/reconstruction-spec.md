# Reconstruction Specification

## Definition of success

A reconstruction is successful when a competent developer or coding agent can begin from an empty directory and, using the generated documentation, build a system that is sufficiently equivalent in:
- architecture;
- externally visible contracts;
- major runtime flows;
- persistence model;
- essential domain behavior;
- configuration requirements;
- build/run process;
- testable acceptance behavior.

The target is not byte-for-byte reproduction.

## Required reconstruction phases

Adapt phase names to the repository, but preserve dependency order.

Typical sequence:
1. bootstrap/toolchain;
2. workspace/package skeleton;
3. shared primitives and configuration;
4. data/storage layer;
5. core domain/application logic;
6. transport/API layer;
7. integrations/background processing;
8. frontend/client layer;
9. observability/security/cross-cutting behavior;
10. tests and fixtures;
11. build/deployment;
12. equivalence validation.

## Per-phase contract

Every phase document must include:

### Goal
What capability exists at the end?

### Prerequisites
Which earlier phases/contracts are required?

### Create
Concrete modules/files/components to create. Paths may be adapted for a clean reconstruction but should map to original responsibilities.

### Contracts
Exact APIs, events, schemas, command interfaces, configuration keys, or behavioral boundaries required.

### Behavior
Important rules, edge cases, error behavior, sequencing, state transitions, retry/idempotency rules.

### Dependencies
Runtime/build packages or external services required.

### Tests
Tests to implement or behavior to verify.

### Evidence
Original repository paths that justify the specification.

### Completion criteria
Observable conditions that prove the phase is done.

## Acceptance matrix

`reconstruction/validation.md` must provide a matrix covering:
- application starts;
- key interfaces respond;
- primary happy paths work;
- important errors are preserved;
- persistence schema behaves correctly;
- critical integrations can be substituted/mocked or exercised;
- tests pass;
- build succeeds;
- important runtime flows match documented behavior.

## Missing information

If reconstruction is blocked by unavailable information, state:
- what is missing;
- why source inspection could not recover it;
- what assumption a reconstructor would need to make;
- how to validate that assumption.
