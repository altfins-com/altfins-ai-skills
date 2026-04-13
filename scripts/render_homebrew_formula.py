#!/usr/bin/env python3
"""Render the Homebrew formula for altfins-skills."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

FORMULA_TEMPLATE = """class AltfinsSkills < Formula
  desc \"Install and package reusable altFINS AI skills\"
  homepage \"https://github.com/altfins-com/altfins-ai-skills\"
  url \"{url}\"
  sha256 \"{sha256}\"
  version \"{version}\"
  license \"Apache-2.0\"

  depends_on \"python@3.12\"

  def install
    (libexec/\"repo\").install Dir[\"*\"]

    (bin/\"altfins-skills\").write <<~SH
      #!/bin/bash
      export ALTFINS_SKILLS_ROOT=\"#{{libexec}}/repo\"
      export ALTFINS_SKILLS_PYTHON=\"#{{Formula[\"python@3.12\"].opt_bin}}/python3.12\"
      exec \"$ALTFINS_SKILLS_PYTHON\" \"$ALTFINS_SKILLS_ROOT/scripts/skills.py\" \"$@\"
    SH
  end

  test do
    output = shell_output(\"#{{bin}}/altfins-skills list --json\")
    assert_match \"altfins-market-analyst\", output
  end
end
"""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render altfins-skills.rb for the Homebrew tap.")
    parser.add_argument("--version", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--output", help="Optional output file. Defaults to stdout.")
    args = parser.parse_args(argv)
    formula = FORMULA_TEMPLATE.format(version=args.version, url=args.url, sha256=args.sha256)
    if args.output:
        Path(args.output).expanduser().resolve().write_text(formula, encoding="utf-8")
    else:
        sys.stdout.write(formula)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
