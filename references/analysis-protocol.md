# Analysis Protocol

## Objective

Produce a repository model that is deep enough to support architecture explanation and project reconstruction, while remaining evidence-driven and non-destructive.

## Progressive inspection

Use a funnel:

1. repository instructions and top-level metadata;
2. inventory and manifests;
3. entrypoints and wiring;
4. architectural boundaries;
5. runtime paths;
6. data/contracts;
7. tests;
8. operations/deployment;
9. Git evolution;
10. cross-checks.

Do not read files in arbitrary alphabetical order if dependency relationships provide a better path.

## Repository classification

Identify whether the repository is:
- single application;
- monorepo;
- library;
- CLI;
- service/backend;
- frontend;
- mobile/desktop;
- infrastructure;
- data/ML;
- mixed.

For monorepos, document each deployable/package boundary and the dependency graph between them.

## Exclusion strategy

Normally exclude generated bulk from deep reading:
- `.git/`
- dependency vendors (`node_modules/`, `.venv/`, `vendor/`, etc.);
- build outputs (`dist/`, `build/`, `target/`, etc.);
- caches;
- coverage output;
- minified bundles;
- binary assets.

Do not exclude schema migrations, generated API specifications, generated clients, lockfiles, or infrastructure state definitions when they reveal contracts.

## Anchor-first reading

Prioritize:
- `AGENTS.md`;
- README and docs;
- manifests;
- workspace files;
- lockfiles;
- entrypoints;
- dependency-injection/wiring files;
- routes/controllers;
- core domain/business services;
- persistence/schema;
- tests;
- deployment files.

## Dependency reasoning

Use imports, references, registrations, and calls to distinguish:
- ownership;
- orchestration;
- adapter boundaries;
- cross-cutting utilities;
- external integration boundaries.

Avoid interpreting folder nesting as dependency direction without corroboration.

## Runtime verification

Prefer repository-defined commands from manifests/CI:
- build;
- test;
- lint;
- typecheck;
- compile.

If tests require external infrastructure or secrets, document that accurately instead of fabricating success.

## Git reasoning

Git may reveal:
- migrations between frameworks;
- why abstractions were introduced;
- module extraction;
- breaking contract changes;
- architectural reversals.

Commit messages are evidence but are not necessarily complete explanations.

## Completion checklist

Analysis is complete enough when:
- entrypoints are known;
- deployable units are known;
- primary module boundaries are known;
- major dependencies are known;
- important flows are traced;
- persistence/contracts are documented;
- build/run/test path is known or blocker documented;
- external systems are known;
- key rationale has confidence labels;
- reconstruction order is possible;
- unknowns are explicit.
