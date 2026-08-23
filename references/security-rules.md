# Security and Non-Destructive Operation

## Hard rule

The skill is an analysis/documentation workflow, not a maintenance workflow.

Never change application source or repository state.

## Forbidden operations

Do not:
- edit source/config outside the generated blueprint directory;
- run formatters with write mode;
- run fix-mode linters;
- run migrations against real databases;
- deploy;
- upload artifacts;
- rotate credentials;
- stage or commit;
- checkout/switch/reset/clean/rebase/merge;
- modify Git refs;
- update dependencies;
- rewrite lockfiles;
- run package installs that alter project files;
- delete caches if they may contain user data.

## Potentially mutating commands

Before running a build/test tool, reason about side effects.

Avoid or isolate commands that may:
- generate tracked files;
- update snapshots;
- rewrite lockfiles;
- create migrations;
- mutate a database;
- launch persistent background services;
- write to cloud services.

If uncertain, skip execution and document the intended command and blocker.

## Secret detection

Treat these as potentially sensitive:
- `.env*`;
- credential files;
- cloud profiles;
- private keys/certificates;
- auth config;
- CI secret references;
- database URLs;
- access tokens.

Record names and requirements, not values.

Safe:

```md
Required environment variables:
- `DATABASE_URL`
- `AUTH_SECRET`
```

Unsafe:

```md
AUTH_SECRET=actual-secret-value
```

## Generated output

By default, the only writes allowed are inside:

```text
project-blueprint/
```

If the directory exists, preserve unrelated user-authored files unless they are clearly part of the generated blueprint contract.
