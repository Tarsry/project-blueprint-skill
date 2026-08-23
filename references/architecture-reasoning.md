# Architecture Reasoning Standard

## Goal

Explain not only what exists, but the likely forces behind major structural decisions without inventing historical intent.

## Rationale record

For each significant decision, use:

```md
## <decision>

**Status:** confirmed | strongly_inferred | possible | unknown  
**Confidence:** <optional 0-1>

### Decision
What architectural choice is visible?

### Why it appears to exist
What problem, constraint, or trade-off does the structure address?

### Evidence
- `<path>` — reason this path matters
- `<path>`

### Trade-offs
Benefits and costs observable from the repository.

### Alternatives not evidenced
Mention only when useful, and make clear they are not known rejected alternatives.
```

## Strong rationale signals

Prefer:
- ADRs;
- architecture docs;
- comments near complex boundaries;
- commit messages;
- issue references found in repository history;
- explicit framework configuration;
- tests preserving boundary behavior;
- repeated dependency direction;
- interfaces/adapters separating external systems;
- migrations showing a before/after architecture.

## Examples of safe inference

If HTTP handlers delegate to framework-independent services and tests exercise services directly:

> Status: strongly_inferred. The service layer appears intended to isolate application behavior from HTTP transport concerns.

If a repository uses an interface plus two storage adapters:

> Status: strongly_inferred. Persistence is intentionally abstracted so application logic does not depend on a single storage implementation.

## Examples of unsafe claims

Do not say:
- “The team chose X because they had scalability problems” without evidence.
- “This abstraction exists for future microservices” without evidence.
- “Performance was the reason for this cache” unless configuration/history/docs support it.

Use `unknown` instead.
