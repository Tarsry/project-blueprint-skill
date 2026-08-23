#!/usr/bin/env python3
"""
Read-only repository inventory helper for the project-blueprint skill.

Prints a compact JSON inventory to stdout. It does not write into the target
repository and intentionally avoids reading secret values.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from collections import Counter
from pathlib import Path

DEFAULT_EXCLUDE = {
    ".git", ".hg", ".svn",
    "node_modules", ".venv", "venv", "env",
    "dist", "build", "target", ".next", ".nuxt",
    "__pycache__", ".pytest_cache", ".mypy_cache",
    ".ruff_cache", ".tox", "coverage", ".coverage",
}

SECRET_NAMES = {
    ".env", ".env.local", ".env.production", ".env.development",
    "id_rsa", "id_ed25519", "credentials", "credentials.json",
}

MANIFEST_NAMES = {
    "package.json", "pnpm-workspace.yaml", "yarn.lock", "pnpm-lock.yaml",
    "package-lock.json", "pyproject.toml", "requirements.txt", "poetry.lock",
    "uv.lock", "Cargo.toml", "Cargo.lock", "go.mod", "go.sum",
    "pom.xml", "build.gradle", "build.gradle.kts",
    "Gemfile", "Gemfile.lock", "composer.json", "composer.lock",
    "mix.exs", "deno.json", "deno.jsonc",
    "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
}

DOC_NAMES = {
    "README.md", "README", "AGENTS.md", "CONTRIBUTING.md",
    "ARCHITECTURE.md", "SECURITY.md",
}

EXT_LANG = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
    ".kts": "Kotlin", ".rb": "Ruby", ".php": "PHP",
    ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C",
    ".h": "C/C++ Header", ".swift": "Swift", ".scala": "Scala",
    ".ex": "Elixir", ".exs": "Elixir", ".dart": "Dart",
    ".vue": "Vue", ".svelte": "Svelte",
    ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell",
}

def git(root: Path, *args: str):
    try:
        cp = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True, text=True, timeout=15, check=False
        )
        if cp.returncode == 0:
            return cp.stdout.strip()
    except Exception:
        pass
    return None

def should_exclude(parts):
    return any(p in DEFAULT_EXCLUDE for p in parts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--max-files", type=int, default=200000)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    files = []
    manifests = []
    docs = []
    potential_secrets = []
    languages = Counter()
    top_dirs = Counter()

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = Path(dirpath).relative_to(root)
        dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDE]
        if should_exclude(rel_dir.parts):
            continue
        if rel_dir.parts:
            top_dirs[rel_dir.parts[0]] += len(filenames)
        for name in filenames:
            p = Path(dirpath) / name
            rel = p.relative_to(root)
            if len(files) >= args.max_files:
                break
            files.append(rel.as_posix())

            if name in MANIFEST_NAMES:
                manifests.append(rel.as_posix())
            if name in DOC_NAMES or name.lower().startswith(("readme", "adr-")):
                docs.append(rel.as_posix())

            lower = name.lower()
            if (
                name in SECRET_NAMES
                or lower.startswith(".env")
                or lower.endswith((".pem", ".key", ".p12", ".pfx"))
                or "secret" in lower
                or "credential" in lower
            ):
                potential_secrets.append(rel.as_posix())

            lang = EXT_LANG.get(p.suffix.lower())
            if lang:
                languages[lang] += 1

    revision = git(root, "rev-parse", "HEAD")
    branch = git(root, "branch", "--show-current")
    status = git(root, "status", "--short")
    tracked_count = git(root, "ls-files")
    if tracked_count is not None:
        tracked_count = len(tracked_count.splitlines())

    result = {
        "root": str(root),
        "git": {
            "revision": revision,
            "branch": branch,
            "dirty": bool(status),
            "status_summary": status.splitlines()[:100] if status else [],
            "tracked_file_count": tracked_count,
        },
        "inventory": {
            "file_count_seen": len(files),
            "truncated": len(files) >= args.max_files,
            "top_level_entries": sorted(
                [p.name for p in root.iterdir() if p.name not in DEFAULT_EXCLUDE]
            )[:500],
            "top_directories_by_file_count": top_dirs.most_common(50),
        },
        "languages_by_file_count": languages.most_common(),
        "manifests": sorted(set(manifests)),
        "documentation": sorted(set(docs)),
        "potential_secret_files": sorted(set(potential_secrets)),
        "notes": [
            "Potential secret files are reported by path only; contents are not read.",
            "Generated/vendor/cache directories are excluded by default.",
        ],
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
