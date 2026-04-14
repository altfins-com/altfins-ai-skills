# Releasing

This document describes the tagged release flow for `altfins-ai-skills`.

## Release Goal

A tagged release publishes:
- `altfins-ai-skills-src.tar.gz` for Homebrew
- `altfins-skills-windows.zip` for Windows users
- `altfins-skills.rb` as the rendered formula artifact
- an updated `Formula/altfins-skills.rb` in `altfins-com/homebrew-tap`

## Versioning

Use tags in the form:

```text
v0.1.0
```

The Homebrew formula uses the plain version without the `v` prefix.

## Pre-Release Checks

Run:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
python3 scripts/test_skills.py
python3 scripts/test_release_assets.py
```

## Release Workflow

1. Create and push a tag such as `v0.1.0`.
2. GitHub Actions runs [.github/workflows/release.yml](../.github/workflows/release.yml).
3. The release workflow creates or updates the GitHub Release and uploads:
   - `altfins-ai-skills-src.tar.gz`
   - `altfins-skills-windows.zip`
   - `altfins-skills.rb`
4. The same workflow updates `altfins-com/homebrew-tap` by pushing `Formula/altfins-skills.rb`.

## Required Secret

The tap update step requires this repository secret:

```text
HOMEBREW_TAP_GITHUB_TOKEN
```

The token must be able to push to `altfins-com/homebrew-tap`.

## Homebrew Formula Contract

The formula is rendered from:

- [scripts/render_homebrew_formula.py](../scripts/render_homebrew_formula.py)
- [packaging/homebrew/altfins-skills.rb.template](../packaging/homebrew/altfins-skills.rb.template)

Public contract:
- formula name: `altfins-skills`
- tap repo: `altfins-com/homebrew-tap`
- install command: `brew install altfins-com/tap/altfins-skills`

## Windows Bundle Contract

The release workflow builds the Windows ZIP on `windows-latest` using `PyInstaller`.

ZIP layout:

```text
altfins-skills.exe
altfins-skills.cmd
repo/
```

`altfins-skills.exe` is the primary beginner-facing entrypoint.
`altfins-skills.cmd` is the fallback for users who already have Python.

## Post-Release Verification

Verify the live release with:

```bash
gh release view vX.Y.Z --repo altfins-com/altfins-ai-skills
brew install altfins-com/tap/altfins-skills
altfins-skills list
```

On Windows, verify the latest bundle after extraction with:

```powershell
.\altfins-skills.exe list
```

## Notes

- This release flow does not add Winget or Chocolatey.
- Brew is the primary end-user install story for macOS and Linux.
- Windows remains ZIP-first.
