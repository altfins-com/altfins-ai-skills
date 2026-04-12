#!/usr/bin/env python3
"""Thin entrypoint for the altfins-ai-skills installer."""

from __future__ import annotations

import sys

from skills_core import main


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
