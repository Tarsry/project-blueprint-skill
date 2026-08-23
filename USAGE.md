# Usage Recipes

## Full blueprint

```text
Use the project-blueprint skill in full analysis mode on this repository.

Requirements:
- read all relevant source needed to understand the actual system;
- do not modify application source or Git state;
- run safe existing build/test/typecheck commands where feasible;
- analyze Git history for architectural evolution;
- explain design rationale with evidence/confidence labels;
- generate Mermaid diagrams;
- write the complete output under project-blueprint/;
- ensure the reconstruction guide can start from an empty directory.
```

## Update an existing blueprint

```text
Use the project-blueprint skill in update mode.

Compare the current repository with the existing project-blueprint/.
Update only affected documentation after re-reading the necessary surrounding
context. Refresh diagrams, evidence, unknowns, validation results, and
blueprint.yaml. Do not modify application source or Git state.
```

## Handoff-focused analysis

```text
Use project-blueprint to prepare this repository for handoff to a developer who
has never seen it. Prioritize architecture, runtime flows, design rationale,
build/test instructions, operational dependencies, and reconstruction accuracy.
```

## Reconstruction check

```text
Audit the existing project-blueprint as if you had only the documentation and
needed to rebuild the system from an empty directory. Identify missing
contracts, missing behavior, ambiguous steps, and unverifiable assumptions,
then improve only the blueprint documents.
```
