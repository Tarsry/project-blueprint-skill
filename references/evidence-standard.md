# Evidence Standard

## Evidence classes

### Confirmed

Use when the claim is directly supported by executable code, configuration, schema, tests plus implementation, explicit architecture documentation, or clear Git history.

### Strongly inferred

Use when multiple independent repository signals support the conclusion, but the repository does not explicitly state the intent.

### Possible

Use for a plausible interpretation supported by limited evidence. It must not be presented as the project's confirmed intent.

### Unknown

Use when evidence is insufficient or contradictory.

## Confidence

Optional numeric confidence may accompany non-confirmed findings:

```yaml
confidence: 0.85
```

Suggested interpretation:
- `0.90–0.99`: very strong inference;
- `0.75–0.89`: strong inference;
- `0.55–0.74`: plausible;
- below `0.55`: prefer `unknown` unless useful as a hypothesis.

Do not fake precision. Confidence is a communication aid, not a statistical probability.

## Evidence citation

Use repository-relative paths.

Good:

```md
Evidence:
- `src/server.ts`
- `src/routes/users.ts`
- `src/services/user-service.ts`
- `tests/users.test.ts`
```

Better when needed:

```md
Evidence:
- `src/server.ts` — route registration
- `src/services/user-service.ts` — business orchestration
- `db/schema.sql` — persistence contract
```

## Contradictions

When evidence conflicts:
1. record both sources;
2. prefer executable/runtime wiring over stale prose;
3. prefer current code over old Git history;
4. mark the conflict;
5. place unresolved contradictions in `audit/known-unknowns.md`.

## No-source claims

Generic ecosystem knowledge may be used to explain technology, but project-specific claims must be traceable to repository evidence.
