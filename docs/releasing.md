# Releasing

This document describes the tagged release flow for `altfins-ai-skills`.

## Release Goal

A tagged release should produce:
- `altfins-ai-skills-src.tar.gz` for Homebrew
- `altfins-skills-windows.zip` for Windows users
- `altfins-skills.rb` for the manual tap update

## Versioning

Use tags in the form:

```text
v0.1.0
```

The Homebrew formula should use the plain version without the `v` prefix.

## Pre-Release Checks

Run:

```bash
python3 scripts/validate_skills.py
python3 scripts/lint_markdown_contracts.py
python3 scripts/test_skills.py
```

## Release Workflow

1. Create and push a tag such as `v0.1.0`.
2. GitHub Actions runs `.github/workflows/release.yml`.
3. The release workflow creates a GitHub Release and uploads:
   - `altfins-ai-skills-src.tar.gz`
   - `altfins-skills-windows.zip`
   - `altfins-skills.rb`
4. Update `altfins-com/homebrew-tap` manually by copying the rendered `altfins-skills.rb` into `Formula/altfins-skills.rb`.
5. Commit and push the tap update.

## Homebrew Formula Update

The formula is rendered from:

- [scripts/render_homebrew_formula.py](../scripts/render_homebrew_formula.py)
- [packaging/homebrew/altfins-skills.rb.template](../packaging/homebrew/altfins-skills.rb.template)

The public contract for the formula is:
- formula name: `altfins-skills`
- tap repo: `altfins-com/homebrew-tap`
- install command: `brew install altfins-com/tap/altfins-skills`

## Windows Bundle Build

The release workflow builds the Windows ZIP on `windows-latest` using `PyInstaller`.

ZIP layout:

```text
altfins-skills.exe
altfins-skills.cmd
repo/
```

`altfins-skills.exe` is the primary beginner-facing entrypoint.
`altfins-skills.cmd` is the fallback for users who already have Python.

## Notes

- This release flow does not add Winget or Chocolatey.
- Brew is the primary end-user install story for macOS and Linux.
- Windows remains ZIP-first in this pass.
