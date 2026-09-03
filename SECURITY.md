# Security Policy

## Scope

`maths-for-ai` is an **educational curriculum** — a collection of Jupyter notebooks, supporting
documentation, and repository tooling. It is not a deployed service, library, or application, and
it ships **no secrets, credentials, or network endpoints**. The realistic security surface is
therefore small, but we still take a few things seriously:

- **Accidentally committed secrets.** The repository must never contain API keys, tokens,
  passwords, or private keys. Notebooks use placeholders and environment variables for any
  credential-shaped example, and `.gitignore` excludes `.env`, `*.pem`, `*.key`, and similar
  files.
- **Unsafe code in notebooks.** Notebook code should be safe to run in a fresh kernel or a Google
  Colab session — no destructive filesystem operations, no fetching and executing untrusted
  remote code.
- **Dependency supply chain.** Dependencies are pinned/bounded (`requirements.txt`,
  `requirements-lock.txt`) and reviewed before changes; see [`docs/CI.md`](docs/CI.md).

## Reporting a vulnerability

If you find a security issue — most likely an **accidentally committed secret** or unsafe code in
a notebook — please report it privately rather than opening a public issue:

1. Use GitHub's **[Private vulnerability reporting](https://github.com/NiravRVaghasiya/maths-for-ai/security/advisories/new)**
   ("Report a vulnerability" under the repo's *Security* tab), or
2. Contact the maintainer directly through their GitHub profile.

Please include the file path and a description. **Do not paste the secret value** into the report.

We aim to acknowledge reports within a few days. Because this is a volunteer-maintained
educational project, there is no formal SLA, but credential exposure and unsafe-code reports are
prioritized.

## If a secret is ever exposed

Removing a secret from the current files is **not sufficient** — it remains in Git history. If a
real credential is committed:

1. **Rotate/revoke the credential immediately** at its provider (the exposed value must be
   treated as compromised).
2. Remove it from the working tree and replace it with a placeholder or environment variable.
3. Purge it from history (e.g. `git filter-repo` or the BFG Repo-Cleaner) and force-push, if the
   repository is already public.

Rotation is the important step: once a secret has been pushed to a public repository, assume it
is public permanently.

## Supported versions

Only the current `main` branch is maintained. There are no released/versioned artifacts to
back-port fixes to.
