---
name: project-blueprint
description: Reverse-engineer an existing software repository into a human-readable and machine-readable Project Blueprint, explain architecture and evidence-backed design rationale, generate Mermaid diagrams, and produce reconstruction documentation sufficient to rebuild a behaviorally equivalent, runnable, testable project from an empty directory. Supports full analysis and incremental update modes. Never modifies application source code.
---

# Project Blueprint

## Purpose

Use this skill when a developer needs to understand an unfamiliar repository, document its real architecture, explain how and why it is built the way it is, or generate documentation that another developer or coding agent can use to reconstruct the project from an empty directory.

The skill produces:
- a high-level `BLUEPRINT.md`;
- a machine-readable `blueprint.yaml`;
- architecture and dependency diagrams;
- directory, module, data, API, runtime, build, test, and deployment documentation;
- evidence-backed design rationale;
- project evolution notes when Git history is available;
- a phased reconstruction guide;
- a validation plan;
- an evidence index and known-unknowns report.

The skill must explain the project, not merely enumerate files.

## Core guarantees

1. **Read deeply.** Inspect all relevant repository files needed to understand the system. Do not stop after reading manifests or the directory tree.
2. **Do not modify source.** Never edit, reformat, delete, rename, stage, commit, reset, install into, or otherwise modify application source files, tracked configuration, Git state, or user data.
3. **Generated docs are the only allowed project writes.** Write only under `project-blueprint/` unless the user explicitly chooses another output directory.
4. **Commands may execute but must be non-destructive.** Static analysis, build, test, lint, typecheck, dependency inspection, Git history inspection, and other read-only/ephemeral validation commands are allowed.
5. **Never expose secrets.** Detect secret-bearing files and environment variables, but never copy values into generated artifacts.
6. **Evidence before assertion.** Separate confirmed facts, strongly inferred conclusions, possible interpretations, and unknowns.
7. **Reconstruction means behavioral and architectural equivalence.** Do not attempt byte-for-byte source reproduction. Produce enough specification to rebuild the same essential architecture, contracts, data model, runtime behavior, build/run path, and tests.
8. **Machine-readable first.** Keep identifiers, paths, module names, flows, commands, dependencies, unknowns, and reconstruction phases structured consistently.
9. **No hallucinated rationale.** A plausible reason is not a fact. Label rationale confidence.
10. **Keep going.** In full mode, continue until the repository has been analyzed, outputs generated, and validation completed or concrete blockers are documented.

## Invocation modes

Infer the mode from the request.

### Full analysis mode

Use when:
- no existing blueprint exists;
- the user asks to understand, map, document, reverse engineer, hand off, or reconstruct a project;
- the user explicitly requests a full blueprint.

Perform the complete workflow in this skill.

### Update mode

Use when:
- `project-blueprint/` already exists and the user asks to refresh/update it;
- the user says `blueprint update`, `update blueprint`, or equivalent.

In update mode:
1. inspect the existing blueprint;
2. inspect Git status/history and source changes when available;
3. identify impacted modules, flows, contracts, diagrams, rationale, tests, and reconstruction steps;
4. re-read enough surrounding source to avoid local-only misunderstandings;
5. update affected generated files;
6. mark stale or unverified sections explicitly;
7. rerun relevant validation;
8. update timestamps, evidence, unknowns, and the machine-readable index.

Do not blindly regenerate unchanged documents.

## Output location

Default:

```text
project-blueprint/
├── BLUEPRINT.md
├── blueprint.yaml
├── architecture/
├── implementation/
├── operations/
├── rationale/
├── reconstruction/
└── audit/
```

Follow `references/blueprint-spec.md` for the complete output contract.

## Analysis workflow

### Phase 0 — Establish boundaries

Determine:
- repository root;
- working tree state;
- repository size;
- language/toolchain;
- whether Git history is available;
- whether an existing blueprint exists;
- excluded/generated/vendor directories;
- likely secret-bearing files.

Read repository-specific instructions such as `AGENTS.md`, `README*`, contribution docs, architecture docs, ADRs, and tool configuration before running broad analysis.

Never change application files while preparing the blueprint.

### Phase 1 — Repository inventory

Use the bundled inventory script when possible:

```bash
python3 <skill-dir>/scripts/repository_inventory.py .
```

Also use appropriate read-only tools available in the environment, such as:
- `git ls-files`
- `git status --short`
- `git log`
- `find`
- `rg`
- language/package-manager inspection commands
- framework-specific introspection commands

Ignore bulky generated/vendor content unless it is itself architecturally relevant.

### Phase 2 — Find project anchors

Identify and inspect:
- manifests and lockfiles;
- executable/application entrypoints;
- startup/bootstrap code;
- package/workspace boundaries;
- route definitions;
- public APIs;
- service/domain boundaries;
- storage/database adapters and schema/migrations;
- job/queue/event consumers;
- frontend roots and navigation;
- build scripts;
- tests and fixtures;
- deployment/infrastructure files;
- environment configuration;
- third-party integrations.

Do not assume directory names reflect real runtime responsibilities.

### Phase 3 — Reconstruct architecture

Build a mental model before writing documentation.

Answer:
- What processes/applications exist?
- Where does execution begin?
- What are the architectural layers?
- What are the module boundaries?
- Which dependencies point inward/outward?
- Which modules own business rules?
- Which code is infrastructure glue?
- Where is state persisted?
- Which external systems are required?
- Which runtime paths are critical?
- Which interfaces are stable contracts?
- Where are cross-cutting concerns implemented?

Use import/reference evidence, route wiring, dependency injection, registrations, build definitions, schema definitions, tests, and runtime configuration.

### Phase 4 — Trace runtime flows

Trace representative end-to-end flows from entrypoint to side effects.

Examples:
- HTTP request → middleware → handler → service → repository → database;
- UI action → state → API client → backend → persistence → UI refresh;
- message → consumer → domain service → outgoing event;
- CLI invocation → parser → command → service → filesystem;
- scheduled job → orchestration → integration → state update.

For each important flow record:
- trigger;
- ordered steps;
- participating modules;
- data exchanged;
- persistence;
- external calls;
- error/retry behavior;
- evidence paths.

### Phase 5 — Understand data and contracts

Document:
- entities;
- schemas;
- migrations;
- relationships;
- serialization formats;
- API routes/endpoints;
- RPC/events/messages;
- public library interfaces;
- configuration contracts;
- important invariants.

Prefer exact names and paths from source.

### Phase 6 — Explain design rationale

Follow `references/architecture-reasoning.md`.

Use four statuses:

- `confirmed`
- `strongly_inferred`
- `possible`
- `unknown`

Never state inferred rationale as confirmed history.

When Git is available, inspect history for architecturally significant areas. Use read-only commands such as:

```bash
git log --oneline --decorate --all
git log -- <path>
git blame <path>
git show <commit>
git diff <old>..<new> -- <path>
```

Do not checkout, reset, clean, rebase, merge, cherry-pick, stage, commit, or modify refs.

### Phase 7 — Validate reality

When feasible, run existing project checks without changing source:
- build;
- tests;
- typecheck;
- lint;
- compile;
- framework validation;
- schema validation.

Prefer commands already defined by the repository.

If a command would install dependencies, alter a lockfile, generate tracked files, start persistent services, mutate a database, deploy infrastructure, or otherwise cause lasting changes, do not run it unless it can be isolated safely. Document the blocker instead.

Record:
- command;
- result;
- exit status if available;
- important failure reason;
- what the result proves or does not prove.

### Phase 8 — Generate diagrams

Generate Mermaid diagrams whenever the evidence supports them.

At minimum attempt:
1. system context/component diagram;
2. module dependency diagram;
3. one or more critical runtime sequence/flow diagrams;
4. data/entity diagram when persistent structured data exists;
5. build/deployment flow when applicable.

Diagrams must use real module/process names. Avoid speculative edges.

### Phase 9 — Generate reconstruction plan

Follow `references/reconstruction-spec.md`.

The reconstruction plan must start from an empty directory and specify an implementation order that respects dependencies.

Each phase must contain:
- goal;
- prerequisites;
- files/modules to create;
- contracts to implement;
- dependencies;
- behavior requirements;
- tests/verification;
- evidence references;
- completion criteria.

Never use vague instructions such as “implement the backend” without defining boundaries and acceptance criteria.

### Phase 10 — Cross-check documentation

Before finishing:
- verify every major runtime component appears in `BLUEPRINT.md`;
- ensure all important modules map to evidence;
- ensure every diagram agrees with prose;
- ensure commands match repository manifests/config;
- ensure reconstruction order is topologically plausible;
- ensure `blueprint.yaml` agrees with Markdown;
- ensure secrets are redacted;
- list unresolved uncertainty;
- distinguish untested claims from validated behavior.

## Evidence standard

Follow `references/evidence-standard.md`.

Every significant architectural or behavioral claim should cite source evidence using repository-relative paths.

Preferred form:

```md
**Status:** strongly_inferred  
**Confidence:** 0.86  
**Evidence:** `src/http/auth.ts`, `src/domain/session.ts`, `tests/session.test.ts`
```

Use line ranges only when reliable and stable. Paths are required; line numbers are optional.

## Secret handling

Follow `references/security-rules.md`.

Never copy:
- passwords;
- tokens;
- API keys;
- private keys;
- session secrets;
- connection-string credentials;
- `.env` values;
- cloud credentials.

It is acceptable to document required variable names:

```text
DATABASE_URL=<required>
STRIPE_SECRET_KEY=<required>
```

Do not quote the real values.

## Quality bar

A good blueprint enables a new developer or coding agent to answer, without rereading the entire repository:
- What does this system do?
- How do I run it?
- What are the major components?
- How do those components communicate?
- Where do the important behaviors live?
- What are the stable contracts?
- What state exists?
- What external dependencies exist?
- How do I test it?
- How is it built/deployed?
- Why is it structured this way, and how certain are we?
- What remains unknown?
- In what order could I rebuild it from scratch?
- How would I know the rebuilt system is equivalent enough?

## Anti-patterns

Do not produce low-value descriptions such as:

> `src/services` contains services.

Instead explain responsibility and relationships:

> `src/services/session.ts` owns session lifecycle behavior between HTTP adapters and persistence. HTTP handlers call the service rather than querying session storage directly, keeping transport concerns outside the core session behavior.

Do not:
- dump the full source tree without interpretation;
- paraphrase filenames as architecture;
- copy large amounts of source into docs;
- invent missing business requirements;
- treat tests as the only truth when production code contradicts them;
- treat comments as unquestionably current;
- hide failed validation;
- omit uncertainty.

## Supporting references

Read these when executing the skill:
- `references/analysis-protocol.md`
- `references/blueprint-spec.md`
- `references/evidence-standard.md`
- `references/architecture-reasoning.md`
- `references/reconstruction-spec.md`
- `references/security-rules.md`

Use templates as structural guidance, not as placeholders that must be filled mechanically.
