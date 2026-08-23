# Blueprint Output Specification

## Required tree

```text
project-blueprint/
├── BLUEPRINT.md
├── blueprint.yaml
├── architecture/
│   ├── system.md
│   ├── modules.md
│   ├── dependencies.md
│   └── diagrams.md
├── implementation/
│   ├── directory-map.md
│   ├── modules.md
│   ├── runtime-flows.md
│   ├── data-model.md
│   └── api-contracts.md
├── operations/
│   ├── environment.md
│   ├── build.md
│   ├── testing.md
│   └── deployment.md
├── rationale/
│   ├── design-decisions.md
│   └── project-evolution.md
├── reconstruction/
│   ├── README.md
│   ├── phase-01-bootstrap.md
│   ├── phase-02-foundation.md
│   ├── phase-03-core.md
│   ├── phase-04-integrations.md
│   ├── phase-05-client.md
│   ├── phase-06-tests.md
│   └── validation.md
└── audit/
    ├── evidence-index.md
    ├── known-unknowns.md
    └── analysis-report.md
```

Omit files that are truly not applicable, but do not silently omit major concerns. State `Not applicable` with evidence when useful.

## BLUEPRINT.md

This is the primary navigation and mental model.

Required sections:
1. project identity and purpose;
2. system at a glance;
3. technology stack;
4. deployable/runtime units;
5. architecture summary;
6. module map;
7. critical runtime flows;
8. data/storage summary;
9. external integrations;
10. build/run/test quickstart;
11. design rationale summary;
12. reconstruction readiness;
13. known unknowns;
14. links to detailed documents.

## blueprint.yaml

Required top-level shape:

```yaml
schema_version: "1.0"
generated:
  mode: full
  repository_root: "."
  revision: null
project:
  name: null
  summary: null
  repository_type: null
  languages: []
  frameworks: []
  package_managers: []
runtime_units: []
entrypoints: []
modules: []
runtime_flows: []
data:
  stores: []
  entities: []
contracts:
  apis: []
  events: []
  public_interfaces: []
external_services: []
environment:
  required_variables: []
build:
  commands: []
test:
  commands: []
deploy:
  targets: []
rationale: []
reconstruction:
  phases: []
unknowns: []
validation: []
```

Use stable IDs for modules/flows whenever practical.

### Module shape

```yaml
- id: auth_service
  name: Auth Service
  path: src/auth
  responsibility: Session and identity lifecycle
  kind: application_service
  depends_on:
    - user_repository
  evidence:
    - src/auth/session.ts
  status: confirmed
```

### Runtime flow shape

```yaml
- id: login
  trigger: POST /login
  steps:
    - module: http_auth
      action: parse request
    - module: auth_service
      action: validate credentials
    - module: session_repository
      action: persist session
  evidence: []
```

### Rationale shape

```yaml
- id: service_layer
  decision: Keep application logic outside HTTP handlers
  status: strongly_inferred
  confidence: 0.87
  evidence: []
```

## Mermaid

Put Mermaid source directly in Markdown so it remains portable.

Prefer:
- `flowchart` for architecture/dependencies;
- `sequenceDiagram` for runtime interactions;
- `erDiagram` for relational data;
- `stateDiagram-v2` for stateful domain behavior.

## Evidence index

Map important findings to the paths that support them. The index should make auditing fast rather than duplicate every sentence in the blueprint.

## Analysis report

Include:
- scope inspected;
- files/directories intentionally excluded;
- commands executed;
- commands skipped and why;
- build/test results;
- Git revision;
- unresolved blockers;
- overall reconstruction confidence.
